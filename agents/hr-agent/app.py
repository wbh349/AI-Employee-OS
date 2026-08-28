"""
AI HR Agent - Resume Screener
OpenAI-powered candidate evaluation agent.

Two ways to run it:
  1) CLI  : python app.py --resume cv.pdf --jd job.txt [--context ctx.txt]
  2) API  : python app.py --serve            # exposes POST /analyze on :8000
            (used by the n8n workflow under workflows/n8n/)
"""

import os
import sys
import json
import io
import argparse
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import base64

from openai import OpenAI
from pypdf import PdfReader


# ============ Configuration ============

MODEL_NAME = "gpt-4o-mini"
MAX_RESUME_CHARS = 12000  # safety cap sent to the model


@dataclass
class CandidateScore:
    """Structured candidate evaluation result."""

    name: str
    overall_score: int  # 0-100
    strengths: List[str]
    risks: List[str]
    recommendation: str  # "Advance to interview" / "Reject" / "On hold"
    match_breakdown: Dict[str, int]  # skills_match, experience_match, culture_fit, growth_potential

    def to_markdown(self) -> str:
        """Render the evaluation as a human-readable markdown report."""
        lines = [
            f"# Candidate Report: {self.name}",
            "",
            f"**Overall Score:** {self.overall_score}/100",
            "",
            "## Strengths",
        ]
        lines += [f"- {s}" for s in self.strengths] or ["- (none listed)"]
        lines += ["", "## Risks"]
        lines += [f"- {r}" for r in self.risks] or ["- (none listed)"]
        lines += ["", f"## Recommendation: **{self.recommendation}**", "", "## Match Breakdown"]
        lines += [f"- {k}: {v}/100" for k, v in self.match_breakdown.items()]
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        """JSON-serialisable view (consumed by the n8n Notion node)."""
        return asdict(self)


# ============ Resume parsing ============

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text content from PDF bytes."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    chunks: List[str] = []
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
    return "\n".join(chunks).strip()


def parse_resume_with_openai(client: OpenAI, pdf_text: str) -> Dict:
    """Use OpenAI to structure a resume into JSON."""
    prompt = f"""
    Extract structured information from the following resume:

    ---
    {pdf_text[:MAX_RESUME_CHARS]}
    ---

    Return JSON with:
    - name: str
    - skills: list[str]
    - experience_years: int
    - education: str
    - key_achievements: list[str]
    - previous_roles: list[str]
    - industry: str
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a resume parsing assistant. Return ONLY valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


# ============ Main Agent ============

class HRAgent:
    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in, "
                "or export the variable in your shell."
            )
        self.client = OpenAI(api_key=key)

    def analyze(
        self,
        resume_bytes: bytes,
        job_description: str,
        company_context: Optional[str] = None,
    ) -> CandidateScore:
        """Evaluate a candidate end-to-end and return a CandidateScore."""
        resume_text = extract_text_from_pdf(resume_bytes)
        if not resume_text:
            raise ValueError("Could not extract any text from the resume PDF.")
        parsed = parse_resume_with_openai(self.client, resume_text)
        score_data = self._score_candidate(parsed, job_description, company_context)
        return CandidateScore(
            name=parsed.get("name", "Unknown"),
            overall_score=int(score_data["overall_score"]),
            strengths=score_data["strengths"],
            risks=score_data["risks"],
            recommendation=score_data["recommendation"],
            match_breakdown=score_data["match_breakdown"],
        )

    def _score_candidate(self, parsed: Dict, jd: str, context: Optional[str]) -> Dict:
        """Score the parsed resume against the job description."""
        prompt = f"""
        You are an HR recruiting expert. Score this candidate against the job description.

        ## Candidate Profile
        {json.dumps(parsed, indent=2, ensure_ascii=False)}

        ## Job Description
        {jd}

        ## Company Context
        {context or "Standard tech company"}

        Return JSON with:
        - overall_score: int (0-100)
        - strengths: list[str] (top 3-5)
        - risks: list[str] (top 2-4)
        - recommendation: "Advance to interview" | "Reject" | "On hold"
        - match_breakdown: dict with keys:
            skills_match, experience_match, culture_fit, growth_potential (each 0-100)
        """

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a recruiting expert. Return ONLY valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    def batch_analyze(self, resumes: List[bytes], jd: str) -> List[CandidateScore]:
        """Analyze multiple candidates sequentially."""
        return [self.analyze(r, jd) for r in resumes]


# ============ HTTP server (for n8n) ============

def _read_body(handler) -> Dict:
    length = int(handler.headers.get("Content-Length", 0))
    raw = handler.rfile.read(length) if length else b"{}"
    return json.loads(raw or b"{}")


def make_server(host: str = "0.0.0.0", port: int = 8000):
    """Build a stdlib HTTP server exposing POST /analyze (no extra dependency)."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, payload: Dict):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):  # noqa: N802
            if self.path.rstrip("/") not in ("/analyze", ""):
                self._send(404, {"error": "not found"})
                return
            try:
                data = _read_body(self)
                resume_b64 = data.get("resume_base64") or ""
                resume_bytes = base64.b64decode(resume_b64)
                if not resume_bytes:
                    raise ValueError("resume_base64 is required")
                agent = HRAgent()
                result = agent.analyze(
                    resume_bytes,
                    data.get("job_description", ""),
                    data.get("company_context"),
                )
                self._send(200, result.to_dict())
            except Exception as exc:  # surface errors as JSON, not 500 HTML
                self._send(400, {"error": str(exc)})

        def log_message(self, *args):  # quieter logs
            pass

    return ThreadingHTTPServer((host, port), Handler)


# ============ CLI ============

def _load_resume(path: str) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


def _load_text(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="AI HR Agent - resume screener")
    parser.add_argument("--resume", help="Path to the candidate resume PDF")
    parser.add_argument("--jd", help="Path to the job description file (.txt/.md)")
    parser.add_argument("--context", help="Optional company context file")
    parser.add_argument("--serve", action="store_true", help="Run the /analyze HTTP server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    if args.serve:
        server = make_server(args.host, args.port)
        print(f"HR Agent API listening on http://{args.host}:{args.port}/analyze  (Ctrl+C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
        return 0

    if not args.resume or not args.jd:
        parser.error("--resume and --jd are required unless --serve is given")

    try:
        agent = HRAgent()
        score = agent.analyze(_load_resume(args.resume), _load_text(args.jd), _load_text(args.context))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(score.to_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
AI HR Agent - Resume Screener
OpenAI-powered candidate evaluation agent
"""

import os
import json
import io
from typing import Dict, List, Optional
from dataclasses import dataclass
import base64

from openai import OpenAI
from pypdf import PdfReader


# ============ Configuration ============

@dataclass
class CandidateScore:
    """Candidate evaluation result"""
    name: str
    overall_score: int  # 0-100
    strengths: List[str]
    risks: List[str]
    recommendation: str  # "Advance to interview" / "Reject" / "On hold"
    match_breakdown: Dict[str, int]  # skills, experience, culture, etc.

    def to_markdown(self) -> str:
        lines = [
            f"# Candidate Report: {self.name}",
            "",
            f"**Overall Score:** {self.overall_score}/100",
            "",
            "## Strengths",
        ]
        for s in self.strengths:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("## Risks")
        for r in self.risks:
            lines.append(f"- {r}")
        lines.append("")
        lines.append(f"## Recommendation: **{self.recommendation}**")
        lines.append("")
        lines.append("## Match Breakdown")
        for k, v in self.match_breakdown.items():
            lines.append(f"- {k}: {v}/100")
        return "\n".join(lines)


# ============ Resume Parser ============

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes"""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def parse_resume_with_openai(client: OpenAI, pdf_text: str) -> Dict:
    """Use OpenAI to structure resume data"""
    prompt = f"""
    Extract structured information from the following resume:

    ---
    {pdf_text[:8000]}
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
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a resume parsing assistant. Return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


# ============ Main Agent ============

class HRAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def analyze(
        self,
        resume_bytes: bytes,
        job_description: str,
        company_context: Optional[str] = None
    ) -> CandidateScore:
        """Main entry point - evaluate a candidate"""

        # Step 1: Extract text from PDF
        resume_text = extract_text_from_pdf(resume_bytes)

        # Step 2: Parse resume with OpenAI
        parsed = parse_resume_with_openai(self.client, resume_text)

        # Step 3: Score against JD
        score_data = self._score_candidate(parsed, job_description, company_context)

        return CandidateScore(
            name=parsed.get("name", "Unknown"),
            overall_score=score_data["overall_score"],
            strengths=score_data["strengths"],
            risks=score_data["risks"],
            recommendation=score_data["recommendation"],
            match_breakdown=score_data["match_breakdown"],
        )

    def _score_candidate(self, parsed: Dict, jd: str, context: Optional[str]) -> Dict:
        """Score candidate against job description"""
        prompt = f"""
        You are an HR recruiting expert. Score this candidate against the job description.

        ## Candidate Profile
        {json.dumps(parsed, indent=2)}

        ## Job Description
        {jd}

        ## Company Context
        {context or "Standard tech company"}

        Return JSON with:
        - overall_score: int (0-100)
        - strengths: list[str] (top 3-5)
        - risks: list[str] (top 2-4)
        - recommendation: "Advance to interview" | "Reject" | "On hold"
        - match_breakdown: dict with keys: skills_match, experience_match, culture_fit, growth_potential
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a recruiting expert. Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def batch_analyze(self, resumes: List[bytes], jd: str) -> List[CandidateScore]:
        """Analyze multiple candidates in batch"""
        results = []
        for r in resumes:
            results.append(self.analyze(r, jd))
        return results


# ============ Quick CLI Test ============

if __name__ == "__main__":
    print("AI HR Agent - Quick Test")
    print("=" * 40)

    sample_jd = """
    Senior AI Engineer at TechCorp

    Responsibilities:
    - Build LLM-powered applications
    - Design agentic workflows
    - Lead technical projects

    Requirements:
    - 5+ years in AI/ML
    - Experience with OpenAI API
    - Strong Python skills
    - Familiar with RAG, LangChain, or similar
    """

    print(f"JD loaded: {sample_jd[:50]}...")
    print("\nTo use: agent = HRAgent()")
    print("result = agent.analyze(resume_bytes, jd_string)")

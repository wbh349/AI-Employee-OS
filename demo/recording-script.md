# AI Employee OS - Demo Recording Script

## Video Title: AI Employee OS - HR Agent in Action

**Duration:** ~3 minutes
**Target:** OphenAI Developer Award Application

> Paths below match the actual repo. Note: the resume screening API runs locally
> (`python agents/hr-agent/app.py --serve`) — start it before the n8n scene.

---

## 0:00 - 0:30 | Introduction

### Visual: Project README on GitHub

**Script:**

"Hi, I'm [Your Name]. Today I'm demoing AI Employee OS, an open-source framework for building practical AI agents for business workflows.

This is the HR Agent Edition — an AI-powered recruitment assistant that automates resume screening and candidate evaluation.

AI Employee OS helps developers build business automation agents using LLMs and workflows. It's fully open-source and ready to fork."

### Screenshot to include:
- GitHub repository landing page
- Project structure tree (from README)

---

## 0:30 - 1:30 | Core Agent Demo

### Visual: Streamlit UI (`streamlit run agents/hr-agent/ui.py`) OR terminal CLI

**Script:**

"The core of the system is the HR Agent. Let me show you how it works.

I have a resume PDF for a Senior AI Engineer candidate and a job description.

When I run the agent, it:
1. Extracts text from the PDF
2. Uses OpenAI to parse the resume into structured data
3. Scores the candidate against the job requirements
4. Generates a comprehensive report with strengths, risks, and interview recommendations

Watch as the agent processes this candidate..."

### Action (pick one):
- **UI:** `streamlit run agents/hr-agent/ui.py` → upload `examples/sample_resume.pdf`, paste `examples/sample_jd.txt`, click **Analyze**
- **CLI:** `python agents/hr-agent/app.py --resume examples/sample_resume.pdf --jd examples/sample_jd.txt`

### Screenshot to include:
- Input: resume file + job description
- Output: score report (87/100, strengths, risks, recommendation)

---

## 1:30 - 2:00 | Report Output

### Visual: The generated markdown report

**Script:**

"Here's the output. The candidate scored 87 out of 100.

We can see:
- **Strengths**: 5 years AI experience, strong automation background
- **Risks**: Limited LLM deployment experience
- **Recommendation**: Advance to interview
- **Interview focus areas**: Specific questions to probe further

This gives HR teams actionable insights in seconds, not hours."

### Screenshot to include:
- Full report in markdown format
- Highlight key sections (score, strengths, risks, recommendation)

---

## 2:00 - 2:45 | Automation with n8n

### Visual: n8n workflow diagram or the JSON (`workflows/n8n/hr-agent-workflow.json`)

**Script:**

"What makes this an 'AI Employee' is the automation layer.

I've configured an n8n workflow that:
1. Listens for incoming resumes on a webhook (`POST /resume-screening`)
2. Calls the HR Agent API at `http://localhost:8000/analyze`
3. Saves the analysis report to Notion

This creates a fully automated recruitment pipeline — no manual intervention needed.

The workflow is defined as code in the repository, so you can customize it for your own tools."

### Setup before recording:
```bash
# terminal 1 — start the agent API
python agents/hr-agent/app.py --serve
# terminal 2 — import workflows/n8n/hr-agent-workflow.json into n8n and activate
```

### Screenshot to include:
- n8n workflow visualization
- Notion database with stored reports

---

## 2:45 - 3:00 | Closing & Call to Action

### Visual: GitHub repository and roadmap

**Script:**

"AI Employee OS is designed to be extensible. The roadmap includes:
- Sales Agent
- Content Agent
- Data Agent

The full code is available on GitHub. You can fork it, customize it, and build your own AI employees.

This project was built for the OphenAI Developer Award. Thank you for watching!"

### Screenshot to include:
- Repository link: https://github.com/wbh349/AI-Employee-OS
- Roadmap section from README

---

## Tech Setup Checklist

Before recording:

- [ ] Clone the repo locally
- [ ] `pip install -r agents/hr-agent/requirements.txt`
- [ ] Set up `.env` with your OpenAI API key
- [ ] Have a sample resume PDF ready (or use `examples/sample_resume.pdf`)
- [ ] Have a sample job description ready (`examples/sample_jd.txt`)
- [ ] (Optional) `python agents/hr-agent/app.py --serve` running for the n8n scene
- [ ] (Optional) n8n running locally with the workflow imported

## Sample Resume (for demo)

Create or use a sample resume with:
- 5+ years experience in AI/ML
- Python and OpenAI experience
- Strong project leadership
- Educational background in CS or related

## Post-Production

1. Record screen with OBS or QuickTime
2. Add voiceover (optional)
3. Keep under 3 minutes
4. Upload to YouTube or Vimeo
5. Paste the link into `docs/submission.md` (### Video Walkthrough)

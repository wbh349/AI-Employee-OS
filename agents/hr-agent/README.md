# HR Agent

AI-powered recruitment assistant — the first agent shipped in **AI Employee OS**.

## Features

- Resume analysis (PDF → structured JSON via OpenAI)
- Job description matching
- Candidate scoring (skills / experience / culture / growth)
- Interview recommendation
- Optional Streamlit UI for live demos
- `POST /analyze` HTTP endpoint for n8n automation

## Install

```bash
pip install -r requirements.txt
cp .env.example .env   # then set OPENAI_API_KEY
```

> Run the commands from the repo root, e.g. `pip install -r agents/hr-agent/requirements.txt`.

## Usage

### 1. CLI

```bash
python app.py --resume path/to/cv.pdf --jd path/to/job.txt
# optional company context:
python app.py --resume cv.pdf --jd job.txt --context company.txt
```

### 2. Streamlit demo UI

```bash
streamlit run ui.py
```

### 3. HTTP server (for n8n)

```bash
python app.py --serve          # POST http://localhost:8000/analyze
```

Request body:

```json
{ "resume_base64": "<base64 PDF>", "job_description": "<JD text>", "company_context": "<optional>" }
```

## Future

- Multi-round interview assistant
- Candidate database
- Automated HR workflow (see `workflows/n8n/hr-agent-workflow.json`)

# Codex for Open Source — Maintainer Application

> OpenAI 开源维护者计划申请稿（原 `submission.md` 已按 Codex for Open Source 口径重写）。
> 申请入口：https://openai.com/form/codex-for-oss/
> 官方说明：https://developers.openai.com/codex/community/codex-for-oss

---

## 1. Applicant & Repository

| Field | Value |
|-------|-------|
| **Program** | OpenAI Codex for Open Source (开源维护者计划) |
| **GitHub username** | wbh349 |
| **Public repository** | https://github.com/wbh349/AI-Employee-OS |
| **Maintainer role** | Author & primary maintainer |
| **License** | MIT (public, open source) |

---

## 2. What this repository is

**AI Employee OS** is a public, open-source framework for building practical AI agents for business workflows. The shipped first agent — the **HR Agent Edition** — automates the first round of recruitment:

- Parses resumes (PDF) and structures them with the OpenAI API
- Scores candidates against a job description across skills / experience / culture / growth
- Produces a markdown scoring report with strengths, risks, and a clear recommendation
- Ships a Streamlit demo UI and a built-in `POST /analyze` HTTP endpoint
- Includes an n8n workflow for end-to-end resume → API → Notion automation

The project is written in Python with type hints, minimal dependencies, and full documentation, so other developers can fork it and build their own "AI employees" (Sales / Content / Data agents are on the roadmap).

---

## 3. Why I qualify as a maintainer

I am the author and primary maintainer of this public repository. I own the project, set its direction, and handle day-to-day maintenance:

- **Active development**: I recently completed a structural refactor — fixed broken repository paths, made the core agent genuinely runnable (CLI + HTTP server), added a Streamlit UI, and aligned all documentation with the actual code.
- **Documentation & onboarding**: I maintain the README, per-agent docs, the award/demo scripts, and a sample job description so newcomers can run the project in minutes.
- **Ecosystem value**: The repo is a reusable starting point for anyone building OpenAI-powered business agents, not a one-off demo. It lowers the barrier for developers to integrate the OpenAI API into real workflows.

> The program has no hard Star/download requirement. This repository qualifies on the basis of being a public, actively maintained open-source project with clear ecosystem value.

---

## 4. How I will use Codex & API credits in my maintainer workflow

I will apply the ChatGPT Pro / Codex benefits directly to maintaining this repository:

- **Pull request review**: use Codex to review incoming PRs, catch regressions, and suggest improvements before merge.
- **Issue triage**: classify and respond to Issues, and draft reproducible minimal examples for bug reports.
- **Release notes & changelogs**: generate accurate release notes from commit history.
- **Documentation**: keep README / per-agent docs / examples in sync with code as the project evolves.
- **Feature work**: extend the agent (e.g. `.docx`/`.txt` resume support, multi-agent orchestration on the roadmap) with Codex assistance.
- **API credits**: used for the project's own OpenAI integration (the HR Agent already calls `gpt-4o-mini` for resume parsing and scoring), and for maintainer automation such as PR-review bots.

---

## 5. Genuine OpenAI API usage (evidence)

This is not a placeholder project — the agent already integrates the OpenAI API in production-style code:

- Model: `gpt-4o-mini` via the OpenAI Python SDK
- Structured JSON output (`response_format: json_object`) for resume parsing and scoring
- Real end-to-end flow: PDF → parse → score → report → (optional) n8n automation

This demonstrates the repository is a live consumer of OpenAI developer infrastructure, which the program is designed to support.

---

## 6. Notes for submission

- Replace any bracketed fields in the official form with your ChatGPT account email and exact role.
- Keep the narrative focused on **maintenance workflow**, not project novelty — reviewers weigh active, ongoing open-source maintenance over flashiness.
- Apply promptly: the program is reviewed on a rolling basis and slots are limited.

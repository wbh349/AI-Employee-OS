"""
HR Agent - Streamlit demo UI
Gives non-technical users a clickable interface for the resume screener.

Run:
    streamlit run agents/hr-agent/ui.py
"""

import io
import streamlit as st

from app import HRAgent, extract_text_from_pdf


st.set_page_config(page_title="AI HR Agent", page_icon="🤖", layout="centered")
st.title("🤖 AI HR Agent — Resume Screener")

st.markdown(
    "Upload a candidate resume (PDF) and paste the job description. "
    "The agent parses the resume, scores the candidate, and produces a report."
)

resume_file = st.file_uploader("Candidate resume (PDF)", type=["pdf"])
job_description = st.text_area("Job description", height=200, placeholder="Paste the JD here…")
company_context = st.text_input("Company context (optional)", placeholder="e.g. early-stage AI startup")

if st.button("Analyze candidate", type="primary"):
    if not resume_file:
        st.error("Please upload a resume PDF first.")
        st.stop()
    if not job_description.strip():
        st.error("Please provide a job description.")
        st.stop()

    with st.spinner("Evaluating candidate…"):
        try:
            agent = HRAgent()
            resume_bytes = resume_file.getvalue()
            # quick sanity check that text is extractable
            if not extract_text_from_pdf(resume_bytes):
                st.error("Could not extract text from this PDF (it may be scanned/image-only).")
                st.stop()
            score = agent.analyze(resume_bytes, job_description, company_context or None)
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
            st.stop()

    st.markdown(f"## Overall score: {score.overall_score}/100")
    st.markdown(score.to_markdown())

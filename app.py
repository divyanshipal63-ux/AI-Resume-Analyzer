import streamlit as st
import tempfile
import os
from home_page import show_home
from utils import extract_text_from_pdf
from matcher import calculate_match
from suggestions import generate_suggestions
from ats_score import calculate_ats_score
from gemini_helper import analyze_resume

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "React",
    "Node.js",
    "HTML",
    "CSS",
    "SQL",
    "MongoDB",
    "FastAPI",
    "Git",
    "GitHub",
    "C",
    "C++",
    "Machine Learning",
    "Artificial Intelligence"
]


# Page Navigation
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    show_home()
    st.stop()
if st.button("← Back to Home"):
    st.session_state["page"] = "home"
    st.rerun()
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with a job description.")

st.divider()

# Resume Upload
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

# Job Description
job_description = st.text_area(
    "Paste Job Description",
    height=200,
    placeholder="Paste the job description here..."
)

# Analyze Button
if st.button("🔍 Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please enter the job description.")

    else:

        with st.spinner("Analyzing your resume..."):

            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(uploaded_file.getbuffer())
                file_path = temp_file.name

            try:
                # Extract resume text
                text = extract_text_from_pdf(file_path)

                # Calculate match score
                match_score = calculate_match(
                    text,
                    job_description
                )

                # Find skills in resume
                found_skills = []

                for skill in SKILLS:
                    if skill.lower() in text.lower():
                        found_skills.append(skill)

                # Find skills in job description
                jd_skills = []

                for skill in SKILLS:
                    if skill.lower() in job_description.lower():
                        jd_skills.append(skill)

                # Find missing skills
                missing_skills = []

                for skill in jd_skills:
                    if skill not in found_skills:
                        missing_skills.append(skill)

                # Generate suggestions
                suggestions = generate_suggestions(
                    missing_skills
                )

                # Calculate ATS score
                ats_score = calculate_ats_score(
                    match_score,
                    found_skills,
                    missing_skills
                )

                # Gemini AI analysis
                ai_analysis = analyze_resume(
                    text,
                    job_description
                )

                # -------------------------
                # RESULTS
                # -------------------------

                st.success("Resume analyzed successfully! 🎉")

                st.subheader("📊 Resume Score")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "ATS Score",
                        f"{ats_score}%"
                    )

                with col2:
                    st.metric(
                        "Match Score",
                        f"{match_score}%"
                    )

                st.divider()

                # Skills Found
                st.subheader("✅ Skills Found")

                if found_skills:
                    st.write(", ".join(found_skills))
                else:
                    st.write("No matching skills found.")

                # Missing Skills
                st.subheader("❌ Missing Skills")

                if missing_skills:
                    st.write(", ".join(missing_skills))
                else:
                    st.write("No missing skills found! 🎉")

                # Suggestions
                st.subheader("💡 Suggestions")

                if isinstance(suggestions, list):
                    for suggestion in suggestions:
                        st.write("•", suggestion)
                else:
                    st.write(suggestions)

                # AI Analysis
                st.subheader("🤖 AI Analysis")

                if isinstance(ai_analysis, dict):

                    if "summary" in ai_analysis:
                        st.write("### Summary")
                        st.write(ai_analysis["summary"])

                    if "strengths" in ai_analysis:
                        st.write("### Strengths")
                        st.write(ai_analysis["strengths"])

                    if "weaknesses" in ai_analysis:
                        st.write("### Weaknesses")
                        st.write(ai_analysis["weaknesses"])

                    if "missing_skills" in ai_analysis:
                        st.write("### AI Suggested Missing Skills")
                        st.write(ai_analysis["missing_skills"])

                    if "improvement_tips" in ai_analysis:
                        st.write("### Improvement Tips")
                        st.write(ai_analysis["improvement_tips"])

                    if "interview_tips" in ai_analysis:
                        st.write("### Interview Tips")
                        st.write(ai_analysis["interview_tips"])

                else:
                    st.write(ai_analysis)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

            finally:
                # Delete temporary file
                if os.path.exists(file_path):
                    os.remove(file_path)

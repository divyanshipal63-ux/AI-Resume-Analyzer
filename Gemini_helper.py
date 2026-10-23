import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("Gemini_api_key"))


model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an ATS Resume Analyzer.

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY valid JSON in the following format.

{{
  "summary": "...",
  "strengths": [
    "...",
    "..."
  ],
  "weaknesses": [
    "...",
    "..."
  ],
  "missing_skills": [
    "...",
    "..."
  ],
  "improvement_tips": [
    "...",
    "..."
  ],
  "interview_tips": [
    "...",
    "..."
  ]
}}

Do not write markdown.
Do not use ```json.
Return only JSON.
"""

    response = model.generate_content(prompt)
    try:
     return json.loads(response.text)
    except:
     return {
        "summary": response.text,
        "strengths": [],
        "weaknesses": [],
        "missing_skills": [],
        "improvement_tips": [],
        "interview_tips": []
    }

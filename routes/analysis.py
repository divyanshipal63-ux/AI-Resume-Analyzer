
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from pathlib import Path

from services.pdf_extractor import extract_text_from_pdf
from services.docx_extractor import extract_text_from_docx
from services.skill_extractor import extract_skills
from services.matcher import calculate_match
from services.scorer import calculate_score
from services.suggestion_engine import generate_suggestions

analysis_bp = Blueprint("analysis", __name__)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"


def extract_resume_text(file_path):
    """Extract text according to the resume file extension."""
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(str(file_path))

    if extension == ".docx":
        return extract_text_from_docx(str(file_path))

    raise ValueError("Unsupported resume file format.")


@analysis_bp.route("/analysis", methods=["GET", "POST"])
def analyze_resume():
    """Analyze an uploaded resume against a job description."""

    if "user_id" not in session:
        flash("Please log in to analyze your resume.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        job_description = request.form.get(
            "job_description", ""
        ).strip()

        if not job_description:
            flash("Please enter a job description.", "error")
            return render_template("analysis.html")

        saved_name = session.get("uploaded_resume")

        if not saved_name:
            flash("Please upload your resume first.", "error")
            return redirect(url_for("resume.upload_resume"))

        # Prevent directory traversal by accepting only a saved filename.
        if Path(saved_name).name != saved_name:
            flash("Invalid resume reference.", "error")
            return redirect(url_for("resume.upload_resume"))

        file_path = UPLOAD_FOLDER / saved_name

        if not file_path.is_file():
            session.pop("uploaded_resume", None)
            flash("Resume file not found. Please upload it again.", "error")
            return redirect(url_for("resume.upload_resume"))

        try:
            resume_text = extract_resume_text(file_path)

            if not resume_text.strip():
                raise ValueError("No readable text found in the resume.")

            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_description)

            match_result = calculate_match(
                resume_skills, job_skills
            )

            score = calculate_score(
                resume_skills, job_skills
            )

            suggestions = generate_suggestions(
                resume_skills, job_skills
            )

            return render_template(
                "analysis.html",
                resume_skills=resume_skills,
                job_skills=job_skills,
                match_result=match_result,
                score=score,
                suggestions=suggestions,
            )

        except Exception:
            flash(
                "Analysis could not be completed. "
                "Check your service functions and resume file.",
                "error",
            )
            return render_template("analysis.html")

    return render_template("analysis.html")


from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    send_file,
)
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

report_bp = Blueprint("report", __name__)


@report_bp.route("/reports")
def reports():
    """Display the reports page."""
    if "user_id" not in session:
        flash("Please log in to view reports.", "error")
        return redirect(url_for("auth.login"))

    # Analysis history/database integration can be added later.
    return render_template("reports.html")


@report_bp.route("/download")
def download_report():
    """Generate and download a PDF report for the current session."""

    if "user_id" not in session:
        flash("Please log in to download reports.", "error")
        return redirect(url_for("auth.login"))

    # The analysis route should save these results in the session
    # or retrieve them from a database before a report is generated.
    analysis = session.get("analysis_result")

    if not analysis:
        flash("Please analyze a resume before downloading a report.", "error")
        return redirect(url_for("analysis.analyze_resume"))

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Resume Analyzer Report", styles["Title"]))
    story.append(Spacer(1, 16))

    user_name = session.get("user_name", "User")
    story.append(
        Paragraph(f"Prepared for: {user_name}", styles["Normal"])
    )
    story.append(Spacer(1, 12))

    score = analysis.get("score", "N/A")
    story.append(Paragraph(f"Resume Match Score: {score}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    resume_skills = analysis.get("resume_skills", [])
    job_skills = analysis.get("job_skills", [])
    suggestions = analysis.get("suggestions", [])

    story.append(Paragraph("Skills Found in Resume", styles["Heading2"]))
    story.append(
        Paragraph(", ".join(map(str, resume_skills)) or "None identified",
                  styles["BodyText"])
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("Skills Required for the Job", styles["Heading2"]))
    story.append(
        Paragraph(", ".join(map(str, job_skills)) or "None identified",
                  styles["BodyText"])
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("Suggestions for Improvement", styles["Heading2"]))

    if suggestions:
        for suggestion in suggestions:
            story.append(
                Paragraph(
                    f"- {suggestion}",
                    styles["BodyText"],
                )
            )
            story.append(Spacer(1, 5))
    else:
        story.append(Paragraph("No suggestions available.", styles["BodyText"]))

    document.build(story)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="resume_analysis_report.pdf",
    )

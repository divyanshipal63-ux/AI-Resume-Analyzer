
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from werkzeug.utils import secure_filename
from pathlib import Path
from uuid import uuid4

resume_bp = Blueprint("resume", __name__)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"

ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def allowed_file(filename):
    """Check whether the file has an allowed extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@resume_bp.route("/upload", methods=["GET", "POST"])
def upload_resume():
    """Upload a PDF or DOCX resume for the logged-in user."""

    if "user_id" not in session:
        flash("Please log in before uploading a resume.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        if "resume" not in request.files:
            flash("Please select a resume file.", "error")
            return redirect(url_for("resume.upload_resume"))

        file = request.files["resume"]

        if not file.filename:
            flash("No file selected.", "error")
            return redirect(url_for("resume.upload_resume"))

        if not allowed_file(file.filename):
            flash("Only PDF and DOCX files are allowed.", "error")
            return redirect(url_for("resume.upload_resume"))

        # Read at most 5 MB plus one byte to enforce the limit.
        file_bytes = file.stream.read(MAX_FILE_SIZE + 1)

        if len(file_bytes) > MAX_FILE_SIZE:
            flash("File size must not exceed 5 MB.", "error")
            return redirect(url_for("resume.upload_resume"))

        if not file_bytes:
            flash("The uploaded file is empty.", "error")
            return redirect(url_for("resume.upload_resume"))

        UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

        original_name = secure_filename(file.filename)
        extension = original_name.rsplit(".", 1)[1].lower()
        saved_name = f"{uuid4().hex}.{extension}"
        save_path = UPLOAD_FOLDER / saved_name

        try:
            with save_path.open("xb") as output:
                output.write(file_bytes)
        except OSError:
            flash("Could not save the uploaded file.", "error")
            return redirect(url_for("resume.upload_resume"))

        # Store only the saved filename in the session.
        session["uploaded_resume"] = saved_name

        flash("Resume uploaded successfully.", "success")
        return redirect(url_for("analysis.analyze_resume"))

    return render_template("upload.html")


from datetime import datetime
from . import db


class Analysis(db.Model):
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    resume_id = db.Column(
        db.Integer,
        db.ForeignKey("resumes.id"),
        nullable=False
    )

    job_description = db.Column(db.Text, nullable=False)

    ats_score = db.Column(db.Float, nullable=False, default=0.0)
    match_score = db.Column(db.Float, nullable=False, default=0.0)

    extracted_skills = db.Column(db.JSON, nullable=False, default=list)
    missing_skills = db.Column(db.JSON, nullable=False, default=list)
    suggestions = db.Column(db.JSON, nullable=False, default=list)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref("analyses", lazy=True)
    )

    resume = db.relationship(
        "Resume",
        backref=db.backref("analyses", lazy=True)
    )

    def __repr__(self):
        return f"<Analysis {self.id}: ATS {self.ats_score}>"

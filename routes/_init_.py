

"""
Routes package for the AI Resume Analyzer application.
"""

from .auth import auth_bp
from .dashboard import dashboard_bp
from .resume import resume_bp
from .analysis import analysis_bp
from .report import report_bp

__all__ = [
    "auth_bp",
    "dashboard_bp",
    "resume_bp",
    "analysis_bp",
    "report_bp",
]


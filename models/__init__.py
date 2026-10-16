
"""
Database models package for AI Resume Analyzer.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .resume import Resume
from .analysis import Analysis

__all__ = ["db", "User", "Resume", "Analysis"]

def generate_report(resume_name, score, matched_skills, missing_skills, suggestions):
    """
    Generate a resume analysis report.

    Args:
        resume_name: Name of the resume.
        score: Resume match score.
        matched_skills: Skills matched with the job.
        missing_skills: Skills missing from the resume.
        suggestions: Improvement suggestions.

    Returns:
        Dictionary containing the complete analysis report.
    """

    report = {
        "resume_name": resume_name,
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
    }

    return report

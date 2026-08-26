def match_skills(resume_skills, required_skills):
    """
    Compare resume skills with job-required skills.

    Args:
        resume_skills: Skills found in the resume.
        required_skills: Skills required by the job.

    Returns:
        Dictionary containing matched and missing skills.
    """

    resume_skills = {skill.lower() for skill in resume_skills}
    required_skills = {skill.lower() for skill in required_skills}

    matched_skills = resume_skills.intersection(required_skills)
    missing_skills = required_skills - resume_skills

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
    }

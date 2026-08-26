def calculate_score(matched_skills, required_skills):
    """
    Calculate resume score based on matched skills.

    Args:
        matched_skills: Skills that match the job requirements.
        required_skills: Skills required by the job.

    Returns:
        Resume match score as a percentage.
    """

    if not required_skills:
        return 0

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score, 2)

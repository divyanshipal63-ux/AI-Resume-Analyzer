COMMON_SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "react",
    "node.js",
    "flask",
    "django",
    "fastapi",
    "streamlit",
    "machine learning",
    "deep learning",
    "data analysis",
    "excel",
    "power bi",
]


def extract_skills(text):
    """
    Extract skills from resume text.

    Args:
        text: Resume text.

    Returns:
        List of skills found in the resume.
    """

    text = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills

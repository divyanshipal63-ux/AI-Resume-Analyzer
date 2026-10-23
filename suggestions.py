def generate_suggestions(missing_skills):
    suggestions=[]
    for skill in missing_skills:
        suggestions.append(f"Add {skill} to your resume if you have experience with it.")
    return suggestions

def calculate_ats_score(match_score,found_skills,missing_skills):
    score=match_score
    score+=len(found_skills)*2
    score-=len(missing_skills)*3
    score=max(0,min(score,100))
    return round(score,2)

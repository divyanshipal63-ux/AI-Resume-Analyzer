from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match(resume_text,job_description):
    documents=[resume_text,job_description]
    cv=CountVectorizer()
    matrix=cv.fit_transform(documents)
    similarity=cosine_similarity(matrix)[0][1]
    return round(similarity*100,2)

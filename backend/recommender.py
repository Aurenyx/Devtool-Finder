"""Explainable hybrid content based recommendation using TF-IDF and cosine similarity."""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

WEIGHTS = {"text":.40,"domain":.20,"language":.15,"features":.15,"compatibility":.10}

def _field(row, name):
    value = row.get(name, []) if isinstance(row, dict) else getattr(row,name,None)
    return value if value is not None else []

def preprocess_text(value):
    """Normalize whitespace/case before vectorization while preserving identifiers."""
    return " ".join(str(value or "").casefold().split())

def _tool_text(tool):
    parts=[_field(tool,"name"),_field(tool,"description"),_field(tool,"category")]
    for key in ("languages","domains","features","project_types","databases"):
        parts.extend(_field(tool,key) or [])
    return preprocess_text(" ".join(str(x) for x in parts if x))

def vectorize_tools(tools):
    """Build the catalog TF-IDF matrix from tool text and structured metadata."""
    frame = pd.DataFrame({"text": [_tool_text(tool) for tool in tools]})
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    return vectorizer, vectorizer.fit_transform(frame.text)

def similarity_scores(vectorizer, matrix, query, size):
    """Return cosine similarities between one requirement query and all tools."""
    query_vector = vectorizer.transform([preprocess_text(query)])
    return cosine_similarity(query_vector, matrix).ravel() if query_vector.nnz else np.zeros(size)

def recommend(tools, profile):
    if not tools: return []
    vectorizer,matrix=vectorize_tools(tools)
    query_parts=[profile.get(k) for k in ("language","domain","experience_level","project_type","database_preference")]
    query_parts += profile.get("required_features",[])
    query_parts += [profile.get("custom_requirements","")]
    query=" ".join(str(x) for x in query_parts if x)
    if query.strip() and matrix.shape[1]:
        text_scores=similarity_scores(vectorizer,matrix,query,len(tools))
    else:
        text_scores=np.zeros(len(tools))
    results=[]
    for i,tool in enumerate(tools):
        domains=_field(tool,"domains"); languages=_field(tool,"languages"); features=_field(tool,"features")
        matches=lambda wanted,available: bool(wanted and any(str(wanted).casefold() in str(x).casefold() or str(x).casefold() in str(wanted).casefold() for x in available))
        domain_score=float(matches(profile.get("domain"),domains))
        language_score=float(matches(profile.get("language"),languages))
        req=profile.get("required_features",[])
        feature_score=(sum(any(f.casefold() in x.casefold() or x.casefold() in f.casefold() for x in features) for f in req)/len(req)) if req else 0
        compat=[]
        for key, attr in (("project_type","project_types"),("experience_level","experience_level"),("database_preference","databases")):
            if profile.get(key): compat.append(float(matches(profile[key],_field(tool,attr))))
        compatibility=float(np.mean(compat)) if compat else 0
        # Weights are normalized over dimensions the user actually supplied.
        active={"text":bool(query.strip()),"domain":bool(profile.get("domain")),"language":bool(profile.get("language")),"features":bool(req),"compatibility":bool(compat)}
        denominator=sum(WEIGHTS[k] for k,v in active.items() if v)
        score=sum(WEIGHTS[k]*v for k,v in (("text",float(text_scores[i])),("domain",domain_score),("language",language_score),("features",feature_score),("compatibility",compatibility)) if active[k])/denominator if denominator else 0
        explanations=[]
        if domain_score: explanations.append(f"Supports your {profile['domain']} domain")
        if language_score: explanations.append(f"Works with {profile['language']}")
        hit=[f for f in req if any(f.casefold() in x.casefold() or x.casefold() in f.casefold() for x in features)]
        if hit: explanations.append("Includes requested features: " + ", ".join(hit))
        if profile.get("project_type") and matches(profile["project_type"],_field(tool,"project_types")): explanations.append(f"Fits {profile['project_type']} projects")
        if profile.get("experience_level") and matches(profile["experience_level"],_field(tool,"experience_level")): explanations.append(f"Suitable for {profile['experience_level']} experience")
        if profile.get("database_preference") and matches(profile["database_preference"],_field(tool,"databases")): explanations.append(f"Compatible with {profile['database_preference']}")
        if not explanations: explanations.append("Ranked by TF-IDF similarity to your requirements")
        results.append({"tool":tool,"relevance_score":round(float(score)*100,1),"explanations":explanations})
    results.sort(key=lambda r:(r["relevance_score"],r["tool"].name),reverse=True)
    return results

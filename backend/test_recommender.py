import pytest
from .seed import seed_tools
from .recommender import recommend, preprocess_text, vectorize_tools, similarity_scores, _tool_text
from .database import Tool

def records(): return [Tool(id=i+1,**row) for i,row in enumerate(seed_tools())]

def test_dataset_and_metadata_are_populated():
    data=seed_tools(); assert len(data)>=100
    assert all(all(row.get(k) for k in ("name","description","category","languages","domains","features","pricing_type","license_type","website")) for row in data)

def test_preprocessing_tfidf_and_cosine_similarity():
    tools=records()[:2]
    assert preprocess_text("  DevTool\tFINDER  ")=="devtool finder"
    vectorizer,matrix=vectorize_tools(tools)
    assert matrix.shape[0]==2 and matrix.shape[1]>0 and matrix.nnz>0
    scores=similarity_scores(vectorizer,matrix,_tool_text(tools[0]),len(tools))
    assert scores.shape==(2,) and scores[0]>scores[1] and scores[0]>0

def test_recommendation_returns_ranked_explanations():
    result=recommend(records(),{"language":"Python","domain":"AI/ML","required_features":["Model training"]})
    assert result and result[0]["relevance_score"]>=result[-1]["relevance_score"]
    assert all(0<=r["relevance_score"]<=100 and r["explanations"] for r in result)
    assert result[0]["tool"].name in {"TensorFlow","PyTorch","scikit-learn","Hugging Face Transformers","Keras","MLflow","Ollama"}

def test_profile_changes_top_recommendations():
    data=records()
    py=recommend(data,{"language":"Python","domain":"AI/ML"})[:5]
    design=recommend(data,{"domain":"Design","project_type":"Prototyping"})[:5]
    assert [x["tool"].id for x in py] != [x["tool"].id for x in design]

def test_empty_profiles_and_catalog_are_safe():
    data=records(); assert recommend([],{})==[]
    result=recommend(data,{})
    assert len(result)==len(data) and all(r["relevance_score"]==0 for r in result)

def test_empty_or_unsupported_preferences_do_not_crash():
    result=recommend(records(),{"language":"Klingon","domain":"Underwater robotics","required_features":["telepathy"],"custom_requirements":""})
    assert len(result)>=100

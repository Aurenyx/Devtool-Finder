"""Endpoint handler tests. Live HTTP routing is smoke-checked against Uvicorn separately."""
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import select
from .database import init_db, SessionLocal, Tool
from .main import health, list_tools, get_tool, categories, recommendations, compare
from .schemas import RecommendRequest, CompareRequest

def test_api_handlers_and_validation():
    init_db()
    with SessionLocal() as db:
        assert health(db)["tools"] >= 100
        tools=list_tools(db=db); assert len(tools)>=100
        assert list_tools(search="PostgreSQL",db=db)[0].name=="PostgreSQL"
        assert categories(db)[0]["count"] > 0
        assert get_tool(1,db).name
        with pytest.raises(HTTPException) as missing: get_tool(99999,db)
        assert missing.value.status_code==404
        picks=recommendations(RecommendRequest(language="Python",domain="AI/ML",limit=5),db)
        assert len(picks)==5 and picks[0]["explanations"]
        with pytest.raises(ValidationError): RecommendRequest(limit=11)
        compared=compare(CompareRequest(tool_ids=[1,2]),db)
        assert len(compared)==2
        with pytest.raises(ValidationError): CompareRequest(tool_ids=[1])
        with pytest.raises(HTTPException) as missing_compare: compare(CompareRequest(tool_ids=[1,99999]),db)
        assert missing_compare.value.status_code==404


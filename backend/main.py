from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from .database import init_db, get_db, Tool
from .schemas import ToolOut, RecommendRequest, Recommendation, CompareRequest
from .recommender import recommend

@asynccontextmanager
async def lifespan(_app):
    init_db()
    yield
app=FastAPI(title="DevTool Finder API",version="1.0.0",description="Explainable, content-based developer tool recommendations.",lifespan=lifespan)
dev_origins={"http://localhost:5173","http://127.0.0.1:5173"}
configured_origins={origin.strip().rstrip("/") for origin in os.getenv("FRONTEND_ORIGINS","").split(",") if origin.strip()}
app.add_middleware(CORSMiddleware,allow_origins=sorted(dev_origins|configured_origins),allow_methods=["*"],allow_headers=["*"])

@app.get("/api/health")
def health(db:Session=Depends(get_db)): return {"status":"ok","tools":len(db.scalars(select(Tool)).all())}

@app.get("/api/tools",response_model=list[ToolOut])
def list_tools(search:str|None=None,category:str|None=None,language:str|None=None,license_type:str|None=None,sort:str=Query("popular",pattern="^(popular|name|category)$"),db:Session=Depends(get_db)):
    q=select(Tool)
    if search: q=q.where(or_(Tool.name.ilike(f"%{search}%"),Tool.description.ilike(f"%{search}%")))
    if category: q=q.where(Tool.category==category)
    rows=db.scalars(q).all()
    if language: rows=[t for t in rows if any(language.casefold() in x.casefold() for x in t.languages)]
    if license_type: rows=[t for t in rows if license_type.casefold() in t.license_type.casefold()]
    if sort=="name": rows.sort(key=lambda t:t.name.casefold())
    elif sort=="category": rows.sort(key=lambda t:(t.category,t.name.casefold()))
    else: rows.sort(key=lambda t:(t.popularity!="High",t.name.casefold()))
    return rows

@app.get("/api/tools/{tool_id}",response_model=ToolOut)
def get_tool(tool_id:int,db:Session=Depends(get_db)):
    tool=db.get(Tool,tool_id)
    if not tool: raise HTTPException(404,"Tool not found")
    return tool

@app.get("/api/categories")
def categories(db:Session=Depends(get_db)):
    rows=db.scalars(select(Tool)).all(); counts={}
    for t in rows: counts[t.category]=counts.get(t.category,0)+1
    return [{"name":k,"count":v} for k,v in sorted(counts.items())]

@app.post("/api/recommend",response_model=list[Recommendation])
def recommendations(profile:RecommendRequest,db:Session=Depends(get_db)):
    try: return recommend(db.scalars(select(Tool)).all(),profile.model_dump())[:profile.limit]
    except Exception as exc: raise HTTPException(500,"Recommendation engine could not process the profile") from exc

@app.post("/api/compare")
def compare(request:CompareRequest,db:Session=Depends(get_db)):
    if len(set(request.tool_ids))!=len(request.tool_ids): raise HTTPException(422,"Tool IDs must be unique")
    tools=db.scalars(select(Tool).where(Tool.id.in_(request.tool_ids))).all()
    found={t.id:t for t in tools}
    missing=[i for i in request.tool_ids if i not in found]
    if missing: raise HTTPException(404,detail={"message":"Some tools were not found","missing_ids":missing})
    return [found[i] for i in request.tool_ids]

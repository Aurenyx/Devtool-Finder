from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class ToolOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; name: str; description: str; category: str
    languages: list[str]; domains: list[str]; experience_level: list[str]
    features: list[str]; project_types: list[str]; databases: list[str]
    pricing_type: str; license_type: str; website: str
    strengths: list[str]; limitations: list[str]; popularity: str

class RecommendRequest(BaseModel):
    language: str | None = None
    domain: str | None = None
    experience_level: str | None = None
    project_type: str | None = None
    database_preference: str | None = None
    required_features: list[str] = Field(default_factory=list, max_length=20)
    custom_requirements: str = Field(default="", max_length=500)
    limit: int = Field(default=8, ge=5, le=10)

class Recommendation(BaseModel):
    tool: ToolOut
    relevance_score: float
    explanations: list[str]

class CompareRequest(BaseModel):
    tool_ids: list[int] = Field(min_length=2, max_length=4)


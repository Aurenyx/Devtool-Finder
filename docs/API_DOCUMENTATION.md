# API documentation

Interactive OpenAPI: `http://127.0.0.1:8000/docs`.

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Status and tool count |
| GET | `/api/tools` | Catalog with optional `search`, `category`, `language`, `license_type`, and `sort` (`popular`, `name`, `category`) |
| GET | `/api/tools/{tool_id}` | Tool detail; 404 if missing |
| GET | `/api/categories` | Category names and live counts |
| POST | `/api/recommend` | Ranked recommendations |
| POST | `/api/compare` | Ordered tool records for 2–4 IDs |

Recommendation request example:

```json
{
  "language": "Python",
  "domain": "AI/ML",
  "experience_level": "Intermediate",
  "project_type": "Research",
  "database_preference": "PostgreSQL",
  "required_features": ["Model training"],
  "custom_requirements": "works with notebooks",
  "limit": 8
}
```

The response is an array of `{tool, relevance_score, explanations}`. Scores are relevance percentages for ranking, not probabilities. Invalid field bounds return 422. Comparison requests with missing tools return 404; duplicate IDs or invalid array sizes return 422.

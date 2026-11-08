# DevTool Finder

A local-first, explainable developer-tool recommender. The application combines a curated SQLite catalog with TF-IDF text similarity, cosine similarity, and weighted structured profile matching. The React dashboard talks to a FastAPI backend; no account or cloud service is needed.

## Quick start — Windows 11

Requirements: Python 3.11 or newer, Node.js 20 or newer, and npm.

1. Open this folder in File Explorer and double-click `setup.bat` once. It creates `.venv`, installs the pinned Python packages, and installs npm packages.
2. Double-click `start.bat`.
3. Open [http://127.0.0.1:5173](http://127.0.0.1:5173). The API and interactive Swagger page are at [http://127.0.0.1:8000](http://127.0.0.1:8000/docs).

Or use PowerShell from this folder:

```powershell
New-Item -ItemType Directory -Force .tmp | Out-Null
$env:TEMP = (Resolve-Path .tmp).Path
$env:TMP = $env:TEMP
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
npm install
```

Then run `python -m backend` in one terminal and `npm run dev` in another. To build the frontend, use `npm run build`. Configure `VITE_API_BASE_URL` to the API base URL, including `/api`, when the backend is hosted elsewhere.

## What's included

- Dashboard metrics and recently added/popular sections populated from the API.
- Catalog search, category, language, license, and sort controls.
- Personalized recommendations with editable language, domain, experience, project, database, feature, and free-text requirements.
- Per-result relevance scores and preference-specific explanations.
- Tool detail pages and side-by-side comparison of two to four tools.
- Favorites persisted in browser local storage.
- SQLite auto-initialization and additive seeding of **172 tools** across 11 categories. New catalog entries are added on startup without replacing existing rows.
- API docs, backend pytest suite, frontend Vitest/Testing Library suite, and system documentation in `docs/`.

## Testing

```powershell
.\.venv\Scripts\python.exe -m pytest backend
npm test
npm run build
```

## Deployment

The repository includes `vercel.json` for the Vite SPA and `render.yaml` for the FastAPI service.

### Vercel

- Import the GitHub repository and set the Root Directory to `.` (repository root).
- Use the Vite framework preset, `npm run build` build command, and `dist` output directory. The repository's `vercel.json` already supplies these settings and the SPA deep-link rewrite.
- Set `VITE_API_BASE_URL` to `https://<your-render-service>.onrender.com/api` for Production and Preview deployments.

### Render

- Create a Blueprint from the repository and select `render.yaml`.
- The blueprint installs `backend/requirements-prod.txt`, launches Uvicorn on `0.0.0.0:$PORT`, and checks `/api/health`.
- Set `FRONTEND_ORIGINS` to the exact deployed Vercel origin (for example, `https://devtool-finder.vercel.app`; no trailing slash). Add comma-separated origins only when multiple Vercel domains are needed.

The application uses SQLite for its read-only tool catalog and seeds it on startup when the database is empty. Render's free service filesystem is ephemeral, so the database can be recreated on restart or deploy; the seed makes the catalog recover automatically. Favorites are kept in each visitor's browser. Free Render services may sleep while idle and take time to wake. Persistent storage or PostgreSQL is unnecessary unless server-side user data is added.

After linking GitHub to both hosts, push changes to `main` to trigger deployments. Keep `.env` files and credentials out of Git; use Vercel and Render environment settings for deployment values.

## Project layout

```text
backend/       FastAPI, SQLAlchemy models, seed catalog, recommender, API tests
src/           React pages, API client, styles, frontend tests
docs/          Overview, architecture, algorithm, dataset, API, test report
```

## Notes

Catalog attributes are a curated educational snapshot. Pricing, license, and product features change; check the official vendor links and terms before making adoption decisions. The relevance score is a normalized ranking score, **not** a probability or quality guarantee. Favorites stay in the current browser profile. The API has no authentication, rate limiting, or multi-user persistence.

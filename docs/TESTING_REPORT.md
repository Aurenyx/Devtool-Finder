# Testing report

Automated test suites are included in `backend/test_recommender.py`, `backend/test_api.py`, and `src/App.test.tsx`. They cover seed completeness, metadata preprocessing, TF-IDF, cosine similarity, ranking, explanations, profile sensitivity, empty and unsupported requests, API handlers/validation/comparison, frontend navigation and search, recommendation form validation/results, and browser-local saved tools.

Run from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest backend
npm test
npm run build
```

## Results

- Backend: 7 passed.
- Frontend: 4 passed.
- Production frontend build: passed.
- Initial local browser smoke check (before catalog expansion): dashboard loaded 127 catalog records and 11 categories; the recommendation form returned an 8-item Python + AI/ML shortlist with explanations; the comparison page loaded and compared PyTorch with ONNX.
- Live production check after expansion: dashboard and About page showed 171 tools; the API health endpoint returned `{"status":"ok","tools":171}`; the recommendation form returned a ranked Data Science shortlist.

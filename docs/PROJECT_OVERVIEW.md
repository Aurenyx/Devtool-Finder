# Project overview

## Purpose

DevTool Finder helps a developer narrow a broad catalog using the stack and project context they already know. The experience links catalog discovery to a personalized recommender, then lets users inspect, compare, and save candidates.

## Main user journeys

1. See live catalog counts and popular tools on the dashboard.
2. Search/filter the catalog or open a category.
3. Submit any subset of profile preferences and review a ranked, explained shortlist.
4. Open tool details, save candidates locally, and compare two to four tools.

## Application components

- React 18, TypeScript, Vite, Tailwind CSS configuration, Lucide React, React Router.
- FastAPI/Pydantic API and SQLAlchemy 2 SQLite persistence.
- Pandas/NumPy preparation and score calculations, scikit-learn TF-IDF/cosine similarity.
- 171 seeded tools from 11 categories, with the catalog count shown dynamically in the dashboard and About page.

## Limitations

The catalog is a hand-curated snapshot, not a live product feed. Catalog tags are broad suitability signals. The recommender ranks only tools present in the local dataset and explanations describe matched metadata; they are not endorsements. Pricing and license facts can change. The public app is hosted at https://devtool-finder-myp2.vercel.app with its API at https://devtool-finder-api.onrender.com. There is no account system or server-side profile storage.

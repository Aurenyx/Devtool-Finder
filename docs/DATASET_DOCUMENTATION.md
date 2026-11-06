# Dataset documentation

The seed catalog contains 171 established developer products in 11 categories. It is embedded in `backend/seed.py` and seeded automatically into SQLite. Startup adds any catalog entries missing from an existing database without deleting or replacing its current rows. Deleting the local database and restarting regenerates it from the full seed catalog.

## Categories

IDE & Editor, Frontend Framework, Backend Framework, Database, API & Collaboration, Version Control, DevOps & Cloud, AI & Machine Learning, Data Science & Analytics, Testing, and Design & Product.

## Fields

Each row contains integer ID (assigned by SQLite), name, description, category, supported languages, supported domains, experience levels, features, project types, database compatibility, pricing type, license type, official website, strengths, limitations, and popularity level. Array values are stored as SQLite JSON columns.

## Provenance and limits

Official links and commonly documented license labels are curated in the seed file, not retrieved live. Pricing and licensing labels intentionally use broad categories where products have multiple editions or licensing components. Category defaults provide general project/database compatibility tags when product-specific details are not encoded. These are discoverability hints rather than a compatibility certification. Recheck vendor documentation before adoption, especially for commercial use or current pricing.

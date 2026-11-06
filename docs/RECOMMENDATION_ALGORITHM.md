# Recommendation algorithm

## Features and text representation

Each tool is represented by its name, description, category, supported languages, domains, features, project types, and database compatibility. The service fits a scikit-learn `TfidfVectorizer` with English stop words and unigrams/bigrams to that corpus. The user query concatenates the supplied profile values and optional custom requirements. Cosine similarity produces one text score per catalog item.

## Structured matches and configured weights

The structured score dimensions are:

| Dimension | Weight | Match |
|---|---:|---|
| Text similarity | 40% | TF-IDF cosine similarity |
| Development domain | 20% | Case-insensitive metadata overlap |
| Programming language | 15% | Case-insensitive metadata overlap |
| Required features | 15% | Fraction of requested feature phrases matched |
| Project and experience compatibility | 10% | Mean of supplied project, experience, and database matches |

Only dimensions represented in the profile participate; their weights are renormalized to sum to 1. The displayed value is `100 × normalized weighted score`, rounded to one decimal. It is a relevance percentage for ordering, never a predicted probability.

## Explanations and edge cases

Explanations list matching domain, language, requested feature, project type, experience level, and database preference. When no structured field matches, the result reports that TF-IDF ranked it against the free-text request. Empty profiles return a stable zero-score catalog ordering; unsupported text is safe and naturally produces low similarity. Empty catalogs return no results. The endpoint bounds result count to 5–10 and de-duplicates comparison IDs.

## Interpretation

The recommender is content-based: it does not learn from click or purchase history. Similarity depends on catalog wording and tags, so catalog coverage, phrase overlap, and metadata quality affect rankings. The model rebuilds vectors for each request, suitable for this small local dataset; a larger service should cache/version the fitted corpus.

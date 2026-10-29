# Second Brain Assistant

An AI-assisted personal knowledge-management system for capturing notes,
connecting ideas, searching knowledge semantically, and generating summaries.

## Status

**Foundation stage — local-first notes and search are implemented.**

The repository includes a dependency-free SQLite note store with CRUD,
archiving, tags, deterministic full-text search, and Markdown/JSON export.
Embeddings, authentication, and hosted AI providers are intentionally not
implemented yet.

## First-release scope

- Create, edit, archive, and tag notes
- Store links and attach them to notes
- Full-text search with filters for tags and dates
- Related-note suggestions based on embeddings
- Knowledge-graph view of note relationships
- AI summaries with visible source-note references
- Export notes as Markdown and JSON

## Recommended architecture

```text
web/                 Web client and note editor
api/                 Authentication and note/search APIs
worker/              Embedding and summary jobs
db/                  Relational schema and migrations
docs/                Architecture and threat model
```

Use a provider abstraction for embeddings and language models so local or
hosted providers can be selected without changing application code. Store
source references with every generated summary and never present generated
content as an independently verified fact.

## Roadmap

1. Scaffold the web client and API with health checks.
2. Add note CRUD, tags, links, and database migrations.
3. Add deterministic full-text search before semantic search.
4. Add background embedding jobs and related-note suggestions.
5. Add source-linked summaries, export, tests, and deployment.

## Non-functional requirements

- Encrypt credentials and never commit API keys.
- Apply per-user authorization to every note and search operation.
- Make deletion and export user-accessible.
- Add automated tests for search, authorization, and summary provenance.

## Development

```sh
python -m venv .venv
.venv/bin/pip install pytest
PYTHONPATH=src .venv/bin/pytest
```

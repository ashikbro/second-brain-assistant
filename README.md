# Second Brain Assistant

**Personal knowledge management system** for capturing notes, linking ideas, searching, and exporting — local-first.

Foundation stage: notes, tags, links, deterministic search, and export are working.

## What it does now

- Create, edit, archive, and tag notes
- Note-to-note links and related-note traversal
- Deterministic full-text search (tags + dates)
- Markdown and JSON export
- Dependency-free SQLite store

Embeddings, authentication, and hosted AI are intentionally not implemented yet.

## Quick start

```sh
python -m venv .venv
.venv/bin/pip install pytest
PYTHONPATH=src .venv/bin/pytest
```

## Browser showcase

Local-only demo in `web/`:

```sh
python -m http.server 8000 --directory web
```

## Keywords

second brain · knowledge management · notes · local-first · python · search · personal knowledge

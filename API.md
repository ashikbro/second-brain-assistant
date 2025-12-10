# API Reference

Quick reference for Second Brain Assistant API endpoints.

Base URL: `http://localhost:8000`

## Notes Endpoints

### Create Note
```http
POST /notes/
Content-Type: application/json

{
  "title": "Note Title",
  "content": "Note content here...",
  "tags": ["tag1", "tag2"]
}

Response: 201 Created
{
  "id": "uuid",
  "title": "Note Title",
  "content": "Note content here...",
  "tags": ["tag1", "tag2"],
  "auto_tags": ["auto1", "auto2"],
  "summary": "AI-generated summary",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### List All Notes
```http
GET /notes/

Response: 200 OK
[
  {
    "id": "uuid",
    "title": "Note Title",
    ...
  }
]
```

### Get Single Note
```http
GET /notes/{note_id}

Response: 200 OK
{
  "id": "uuid",
  "title": "Note Title",
  ...
}
```

### Update Note
```http
PUT /notes/{note_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content",
  "tags": ["new", "tags"]
}

Response: 200 OK
{
  "id": "uuid",
  "title": "Updated Title",
  ...
}
```

### Delete Note
```http
DELETE /notes/{note_id}

Response: 204 No Content
```

### Search Notes
```http
POST /notes/search
Content-Type: application/json

{
  "query": "natural language search query",
  "limit": 10
}

Response: 200 OK
[
  {
    "note": {
      "id": "uuid",
      "title": "Relevant Note",
      ...
    },
    "similarity_score": 0.85
  }
]
```

## Knowledge Graph Endpoints

### Build Graph
```http
POST /graph/build

Response: 200 OK
{
  "message": "Knowledge graph built successfully"
}
```

### Get Complete Graph
```http
GET /graph/

Response: 200 OK
{
  "nodes": [
    {
      "id": "uuid",
      "title": "Note Title",
      "tags": ["tag1", "tag2"]
    }
  ],
  "relationships": [
    {
      "source": "uuid1",
      "target": "uuid2",
      "relationship_type": "RELATED_TO",
      "weight": 2.0
    }
  ]
}
```

### Get Related Notes
```http
GET /graph/related/{note_id}?limit=5

Response: 200 OK
{
  "note_id": "uuid",
  "related_notes": ["uuid1", "uuid2", "uuid3"]
}
```

## AI Services Endpoints

### Summarize Content
```http
POST /ai/summarize
Content-Type: application/json

{
  "content": "Long text content to summarize..."
}

Response: 200 OK
{
  "summary": "Concise summary in 2-3 sentences."
}
```

### Generate Ideas
```http
POST /ai/generate-ideas
Content-Type: application/json

{
  "topic": "Machine Learning",
  "context": "Focus on practical applications"
}

Response: 200 OK
{
  "ideas": "Generated ideas and insights..."
}
```

### Extract Tags
```http
POST /ai/extract-tags
Content-Type: application/json

{
  "content": "Text to extract tags from..."
}

Response: 200 OK
{
  "tags": ["tag1", "tag2", "tag3"]
}
```

## System Endpoints

### Health Check
```http
GET /health

Response: 200 OK
{
  "status": "healthy"
}
```

### Root
```http
GET /

Response: 200 OK
{
  "message": "Welcome to Second Brain Assistant API",
  "docs": "/docs",
  "version": "1.0.0"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Note not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Authentication

Currently, no authentication is required. For production use, implement JWT or API key authentication.

## Rate Limiting

No rate limiting currently implemented. Recommended for production:
- 100 requests per minute per IP
- Separate limits for AI endpoints (more costly)

## CORS

Allowed origins:
- `http://localhost:3000`
- `http://localhost:5173`

For production, configure specific domains.

## Example Usage with curl

### Create and search a note
```bash
# Create a note
NOTE_ID=$(curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Tips",
    "content": "Use list comprehensions, type hints, and virtual environments.",
    "tags": ["python", "programming"]
  }' | jq -r '.id')

# Search for it
curl -X POST "http://localhost:8000/notes/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best practices for Python development",
    "limit": 5
  }' | jq '.'
```

### Build and view graph
```bash
# Build the graph
curl -X POST "http://localhost:8000/graph/build"

# Get the graph
curl "http://localhost:8000/graph/" | jq '.'
```

## Example Usage with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a note
response = requests.post(
    f"{BASE_URL}/notes/",
    json={
        "title": "My Note",
        "content": "Content here...",
        "tags": ["example"]
    }
)
note = response.json()
print(f"Created: {note['id']}")

# Search notes
response = requests.post(
    f"{BASE_URL}/notes/search",
    json={"query": "example", "limit": 10}
)
results = response.json()
print(f"Found {len(results)} results")
```

## Example Usage with JavaScript

```javascript
const BASE_URL = 'http://localhost:8000';

// Create a note
const response = await fetch(`${BASE_URL}/notes/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'My Note',
    content: 'Content here...',
    tags: ['example']
  })
});
const note = await response.json();
console.log('Created:', note.id);

// Search notes
const searchResponse = await fetch(`${BASE_URL}/notes/search`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'example',
    limit: 10
  })
});
const results = await searchResponse.json();
console.log('Found:', results.length, 'results');
```

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can:
- Try all endpoints
- View request/response schemas
- See parameter descriptions
- Test with sample data

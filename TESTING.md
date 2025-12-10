# Testing Guide

This guide explains how to test the Second Brain Assistant application.

## Manual Testing

### 1. Start the Application

First, ensure all services are running:

```bash
# Terminal 1 - Start Neo4j
docker-compose up

# Terminal 2 - Start Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 3 - Start Frontend
cd frontend
npm run dev
```

### 2. Test Note Creation

1. Open http://localhost:3000 in your browser
2. Fill in the note form:
   - Title: "Introduction to Machine Learning"
   - Content: "Machine learning is a subset of artificial intelligence that focuses on algorithms that learn from data. Common types include supervised learning, unsupervised learning, and reinforcement learning."
   - Tags: "AI, machine-learning, technology"
3. Click "Create Note"
4. Verify:
   - Note appears in the grid below
   - Auto-generated summary is displayed
   - Auto-extracted tags appear (in purple)
   - Manual tags appear (in blue)

### 3. Test Semantic Search

1. In the search box, enter: "What is AI?"
2. Click "Search"
3. Verify:
   - Relevant notes are returned
   - Similarity scores are shown
   - Results are ranked by relevance

### 4. Test Knowledge Graph

1. Create several notes with overlapping tags:
   - "Python Programming" with tags: ["python", "programming"]
   - "Django Framework" with tags: ["python", "web", "django"]
   - "React Development" with tags: ["javascript", "web", "react"]
2. Click the "🕸️ Knowledge Graph" tab
3. Click "Refresh Graph"
4. Verify:
   - All notes appear as nodes
   - Lines connect notes with shared tags
   - You can drag nodes to rearrange
   - Line thickness indicates relationship strength

### 5. Test Note Editing

1. Click "Edit" on any note card
2. Modify the title or content
3. Click "Update Note"
4. Verify:
   - Note is updated
   - New summary and tags are generated
   - Search results update accordingly

### 6. Test Note Deletion

1. Click "Delete" on any note card
2. Confirm the deletion
3. Verify:
   - Note is removed from the list
   - Knowledge graph updates when refreshed

## API Testing

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# Create a note
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Note",
    "content": "This is test content about programming and software development.",
    "tags": ["test", "programming"]
  }'

# List all notes
curl http://localhost:8000/notes/

# Search notes
curl -X POST "http://localhost:8000/notes/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "software development",
    "limit": 5
  }'

# Build knowledge graph
curl -X POST "http://localhost:8000/graph/build"

# Get knowledge graph
curl http://localhost:8000/graph/

# Generate ideas
curl -X POST "http://localhost:8000/ai/generate-ideas" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Software Architecture",
    "context": "Focus on microservices"
  }'
```

### Test with Python

Run the example script:

```bash
cd examples
python api_usage.py
```

### Test with Swagger UI

1. Open http://localhost:8000/docs
2. Try each endpoint interactively
3. View request/response schemas
4. Test error handling

## Edge Cases to Test

### 1. Empty Content
- Try creating a note with empty title or content
- Verify validation errors are shown

### 2. Long Content
- Create a note with very long content (>10,000 characters)
- Verify summarization works correctly

### 3. Special Characters
- Create notes with special characters in title and content
- Verify proper encoding/decoding

### 4. No Tags
- Create a note without manual tags
- Verify auto-tagging still works

### 5. Network Errors
- Stop the backend server
- Try operations in the frontend
- Verify error messages are shown

### 6. Empty Database
- Delete all notes
- Visit knowledge graph
- Verify appropriate message is shown

## Performance Testing

### Test Semantic Search Performance

```python
import time
import requests

API_URL = "http://localhost:8000"

# Create 100 notes
start = time.time()
for i in range(100):
    requests.post(
        f"{API_URL}/notes/",
        json={
            "title": f"Note {i}",
            "content": f"Content for note {i} with various topics",
            "tags": [f"tag{i % 10}"]
        }
    )
print(f"Created 100 notes in {time.time() - start:.2f}s")

# Test search performance
start = time.time()
results = requests.post(
    f"{API_URL}/notes/search",
    json={"query": "various topics", "limit": 10}
)
print(f"Search completed in {time.time() - start:.2f}s")
```

## Troubleshooting

### Backend won't start
- Check if OpenAI API key is set in `.env`
- Verify Neo4j is running: `docker ps`
- Check Python dependencies: `pip list`

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check for port conflicts on 3000

### Search returns no results
- Verify notes were created successfully
- Check ChromaDB directory exists: `ls backend/chroma_db`
- Verify embeddings are being generated (check backend logs)

### Knowledge graph is empty
- Click "Refresh Graph" button
- Verify notes have tags
- Check Neo4j connection in backend logs

## Expected Behavior

### Note Creation
- Takes 2-5 seconds (due to GPT API calls)
- Generates summary and 3-5 auto-tags
- Creates vector embedding for search

### Semantic Search
- Returns results in <1 second
- Uses cosine similarity for ranking
- Returns up to specified limit

### Knowledge Graph
- Build time proportional to number of notes
- Visualizes up to 100 nodes efficiently
- Updates require manual refresh

## Security Testing

### API Key Protection
- Verify `.env` is not committed to git
- Check CORS settings allow only local origins
- Ensure API key is not exposed in frontend

### Input Validation
- Try SQL injection in note content
- Test XSS with `<script>` tags
- Verify long inputs are handled

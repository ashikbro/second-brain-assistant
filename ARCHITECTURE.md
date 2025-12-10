# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Note Editor  │  │ Search Box   │  │ Knowledge Graph Viz  │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
│                                                                 │
│                    React.js Frontend (Vite)                     │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 │ HTTP/REST
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Notes API    │  │ Graph API    │  │ AI Services API      │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Business Logic Layer                    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │  │
│  │  │ Note Service │  │ Graph Service│  │  AI Service   │  │  │
│  │  └──────────────┘  └──────────────┘  └───────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │                    │                      │
         ▼                    ▼                      ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐
│  ChromaDB    │    │    Neo4j     │    │   OpenAI API         │
│  (Vector DB) │    │  (Graph DB)  │    │   (GPT Models)       │
└──────────────┘    └──────────────┘    └──────────────────────┘
```

## Data Flow

### 1. Creating a Note

```
User Input → Note Form → POST /notes/
                             ↓
                    Note Service receives data
                             ↓
                    ┌────────┴────────┐
                    ↓                 ↓
              AI Service        ChromaDB
           (summarize + tag)   (store embedding)
                    ↓
              Neo4j Graph
           (add node + edges)
                    ↓
              Return Note
```

### 2. Searching Notes

```
Search Query → POST /notes/search
                    ↓
           Generate Embedding
              (OpenAI API)
                    ↓
         Query Vector Database
              (ChromaDB)
                    ↓
         Rank by Similarity
                    ↓
         Return Results
```

### 3. Knowledge Graph

```
Notes → POST /graph/build
            ↓
    Analyze all notes
            ↓
    Create nodes (notes)
            ↓
    Create edges (shared tags)
            ↓
    Store in Neo4j
            ↓
       GET /graph/
            ↓
    Fetch nodes & edges
            ↓
    Visualize with D3.js
```

## Technology Stack

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **D3.js**: Graph visualization
- **Axios**: HTTP client

### Backend
- **FastAPI**: Web framework
- **LangChain**: LLM orchestration
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Databases
- **ChromaDB**: Vector embeddings for semantic search
- **Neo4j**: Graph database for relationships
- **In-Memory**: Note storage (demo purposes)

### AI Services
- **OpenAI GPT-3.5**: Summarization, tagging, idea generation
- **OpenAI Embeddings**: Text vectorization for search

## Key Features Implementation

### Natural Language Search
1. User enters query
2. Query converted to embedding (OpenAI)
3. Similarity search in ChromaDB
4. Results ranked by cosine similarity

### Auto-Tagging
1. Note content sent to GPT-3.5
2. Prompt: "Extract 3-5 relevant tags"
3. Tags returned and stored with note

### Knowledge Graph
1. Notes analyzed for shared tags
2. Nodes created for each note
3. Edges created based on tag overlap
4. Edge weight = number of shared tags
5. Rendered with D3.js force-directed graph

### Summarization
1. Note content sent to GPT-3.5
2. Prompt: "Summarize in 2-3 sentences"
3. Summary stored with note

## Scalability Considerations

### Current Implementation (Demo)
- In-memory note storage
- Single instance
- Local ChromaDB
- Suitable for personal use

### Production Enhancements
- PostgreSQL for note persistence
- Redis for caching
- Load balancing
- ChromaDB with S3 backend
- Neo4j clustering
- Rate limiting
- Authentication/Authorization

## Security Features

### Implemented
- Environment variable configuration
- CORS protection
- Input validation (Pydantic)
- No hardcoded secrets
- Dependency security scanning

### Recommended for Production
- User authentication (JWT)
- API rate limiting
- HTTPS encryption
- Database encryption at rest
- API key rotation
- Audit logging

## Performance Optimization

### Backend
- Async/await for I/O operations
- Connection pooling (Neo4j, ChromaDB)
- Caching frequently accessed data
- Batch embedding generation

### Frontend
- Code splitting
- Lazy loading components
- Debounced search
- Optimized re-renders
- Virtual scrolling for large lists

## Deployment Options

### Local Development
```bash
./setup.sh
```

### Docker Deployment
- Containerize backend and frontend
- Use docker-compose for all services
- Persist data in volumes

### Cloud Deployment
- **Backend**: AWS ECS, Google Cloud Run, Azure Container Apps
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Neo4j**: Neo4j Aura
- **ChromaDB**: Self-hosted or cloud persistence

## Monitoring

### Recommended Metrics
- API response times
- OpenAI API usage and costs
- Database query performance
- Error rates
- User activity patterns

### Tools
- FastAPI built-in metrics
- Prometheus + Grafana
- Application logs
- Database monitoring tools

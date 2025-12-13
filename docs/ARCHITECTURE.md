# Architecture Overview

## System Design

The Second Brain Assistant is designed as a modular system with the following components:

### Core Components

1. **Knowledge Graph** (`core.py`)
   - Central data structure for managing notes and relationships
   - Built on NetworkX for graph operations
   - Supports bidirectional linking between notes

2. **Note System** (`core.py`)
   - Individual note representation with metadata
   - Support for tags, timestamps, and content
   - Automatic link tracking

3. **Semantic Search** (`search.py`)
   - Natural language query processing
   - Similarity-based ranking
   - Integration with embedding models (planned)

4. **CLI Interface** (`cli.py`)
   - Command-line access to all features
   - Interactive mode for note management

### Data Flow

```
User Input → CLI/API → Knowledge Graph → Storage
                ↓
         Semantic Search ← Embeddings
                ↓
           Results → User
```

### Technology Stack

- **Python 3.8+**: Core language
- **NetworkX**: Graph data structure
- **Transformers**: NLP and embeddings
- **OpenAI API**: GPT-powered features
- **ChromaDB**: Vector storage (planned)
- **FastAPI**: REST API (planned)

## Future Enhancements

1. Persistent storage layer
2. Real-time graph visualization
3. Advanced NLP processing
4. Multi-user support
5. Plugin system for extensibility

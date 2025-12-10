# 🧠 Second Brain Assistant

An AI-powered personal knowledge management system that organizes notes, links ideas, and visualizes a knowledge graph. It supports natural language search, semantic tagging, and GPT-driven summaries.

## ✨ Features

- **Natural Language Search**: Search your notes using semantic similarity with OpenAI embeddings
- **Auto-Tagging**: Automatic tag extraction and categorization using GPT
- **Knowledge Graph**: Visualize connections between your notes using Neo4j
- **AI Summarization**: Generate concise summaries of your notes
- **Idea Generation**: Get AI-powered ideas and insights based on your topics
- **Modern UI**: Clean, responsive React interface with real-time updates

## 🏗️ Architecture

### Backend (Python + LangChain)
- **FastAPI**: High-performance API framework
- **LangChain**: Integration with OpenAI for LLM operations
- **ChromaDB**: Vector database for semantic search
- **Neo4j**: Graph database for knowledge relationships
- **OpenAI API**: GPT models for summarization, tagging, and idea generation

### Frontend (React.js)
- **React 18**: Modern UI with hooks
- **D3.js**: Interactive knowledge graph visualization
- **Axios**: HTTP client for API communication
- **Vite**: Fast build tool and dev server

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Docker and Docker Compose (for Neo4j)
- OpenAI API Key

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ashikbro/second-brain-assistant.git
cd second-brain-assistant
```

### 2. Start Neo4j Database

```bash
docker-compose up -d
```

Neo4j will be available at:
- Browser interface: http://localhost:7474
- Bolt protocol: bolt://localhost:7687
- Default credentials: neo4j/password

### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Update `.env` with your settings:
```env
OPENAI_API_KEY=your_openai_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### 4. Start Backend Server

```bash
# From backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## 📖 Usage

### Creating Notes

1. Navigate to the **Notes** tab
2. Fill in the title and content
3. Optionally add manual tags
4. Click "Create Note"
5. The system will automatically:
   - Generate a summary
   - Extract relevant tags
   - Create embeddings for semantic search
   - Add the note to the knowledge graph

### Searching Notes

1. Use the search box to enter a natural language query
2. The system uses semantic similarity to find relevant notes
3. Results are ranked by relevance score

### Viewing Knowledge Graph

1. Navigate to the **Knowledge Graph** tab
2. Click "Refresh Graph" to build/update the graph
3. Notes are represented as nodes
4. Connections show relationships based on shared tags
5. Drag nodes to rearrange the visualization

### API Endpoints

#### Notes
- `POST /notes/` - Create a new note
- `GET /notes/` - List all notes
- `GET /notes/{id}` - Get a specific note
- `PUT /notes/{id}` - Update a note
- `DELETE /notes/{id}` - Delete a note
- `POST /notes/search` - Search notes with natural language

#### Knowledge Graph
- `POST /graph/build` - Build/rebuild the knowledge graph
- `GET /graph/` - Get the complete graph
- `GET /graph/related/{note_id}` - Get related notes

#### AI Services
- `POST /ai/summarize` - Summarize content
- `POST /ai/generate-ideas` - Generate ideas on a topic
- `POST /ai/extract-tags` - Extract tags from content

## 🧪 Example API Usage

### Create a Note
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Best Practices",
    "content": "Always use virtual environments, write tests, follow PEP 8...",
    "tags": ["python", "programming"]
  }'
```

### Search Notes
```bash
curl -X POST "http://localhost:8000/notes/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to write clean Python code?",
    "limit": 5
  }'
```

## 🛠️ Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

## 📁 Project Structure

```
second-brain-assistant/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration
│   │   ├── db/           # Database connections
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   ├── App.jsx       # Main app
│   │   └── main.jsx      # Entry point
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml    # Neo4j setup
└── README.md
```

## 🔒 Security Notes

- Never commit your `.env` file
- Keep your OpenAI API key secure
- Use environment-specific configurations
- Change default Neo4j password in production

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT APIs
- LangChain for LLM orchestration
- Neo4j for graph database
- ChromaDB for vector embeddings
- D3.js for graph visualization

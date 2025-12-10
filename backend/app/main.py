from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import notes, graph, ai
from app.db.neo4j_connection import neo4j_conn
from app.db.chroma_connection import chroma_conn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    neo4j_conn.connect()
    chroma_conn.connect()
    yield
    # Shutdown
    neo4j_conn.close()


app = FastAPI(
    title="Second Brain Assistant",
    description="AI-powered personal knowledge management system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(notes.router)
app.include_router(graph.router)
app.include_router(ai.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Second Brain Assistant API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

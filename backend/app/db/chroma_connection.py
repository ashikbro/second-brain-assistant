import chromadb
from chromadb.config import Settings
from app.core.config import settings as app_settings


class ChromaDBConnection:
    """ChromaDB connection handler for vector embeddings"""
    
    def __init__(self):
        self.client = None
        self.collection = None
    
    def connect(self):
        """Initialize ChromaDB client and collection"""
        self.client = chromadb.PersistentClient(
            path=app_settings.CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection for notes
        self.collection = self.client.get_or_create_collection(
            name="notes",
            metadata={"description": "Note embeddings for semantic search"}
        )
    
    def get_collection(self):
        """Get the notes collection"""
        return self.collection


chroma_conn = ChromaDBConnection()

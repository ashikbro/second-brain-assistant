from neo4j import GraphDatabase
from app.core.config import settings


class Neo4jConnection:
    """Neo4j database connection handler"""
    
    def __init__(self):
        self.driver = None
    
    def connect(self):
        """Establish connection to Neo4j"""
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
    
    def get_session(self):
        """Get a new session"""
        return self.driver.session()


neo4j_conn = Neo4jConnection()

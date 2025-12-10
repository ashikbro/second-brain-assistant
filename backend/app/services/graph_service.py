from typing import List
from app.models.schemas import KnowledgeGraph, GraphNode, GraphRelationship
from app.db.neo4j_connection import neo4j_conn
from app.services.note_service import note_service


class GraphService:
    """Service for managing knowledge graph"""
    
    async def build_graph(self):
        """Build knowledge graph from notes"""
        notes = await note_service.list_notes()
        
        with neo4j_conn.get_session() as session:
            # Clear existing graph
            session.run("MATCH (n:Note) DETACH DELETE n")
            
            # Create nodes for each note
            for note in notes:
                all_tags = list(set(note.tags + note.auto_tags))
                session.run(
                    """
                    CREATE (n:Note {
                        id: $id,
                        title: $title,
                        tags: $tags
                    })
                    """,
                    id=note.id,
                    title=note.title,
                    tags=all_tags
                )
            
            # Create relationships based on shared tags
            for note in notes:
                all_tags = list(set(note.tags + note.auto_tags))
                if all_tags:
                    # Find related notes with shared tags
                    session.run(
                        """
                        MATCH (n1:Note {id: $note_id})
                        MATCH (n2:Note)
                        WHERE n1.id <> n2.id
                        AND ANY(tag IN n1.tags WHERE tag IN n2.tags)
                        WITH n1, n2, 
                             SIZE([tag IN n1.tags WHERE tag IN n2.tags]) as shared_count
                        MERGE (n1)-[r:RELATED_TO]->(n2)
                        SET r.weight = shared_count
                        """,
                        note_id=note.id
                    )
    
    async def get_graph(self) -> KnowledgeGraph:
        """Get the complete knowledge graph"""
        nodes = []
        relationships = []
        
        with neo4j_conn.get_session() as session:
            # Get all nodes
            result = session.run("MATCH (n:Note) RETURN n")
            for record in result:
                node = record["n"]
                nodes.append(
                    GraphNode(
                        id=node["id"],
                        title=node["title"],
                        tags=node["tags"]
                    )
                )
            
            # Get all relationships
            result = session.run(
                """
                MATCH (n1:Note)-[r:RELATED_TO]->(n2:Note)
                RETURN n1.id as source, n2.id as target, 
                       type(r) as rel_type, r.weight as weight
                """
            )
            for record in result:
                relationships.append(
                    GraphRelationship(
                        source=record["source"],
                        target=record["target"],
                        relationship_type=record["rel_type"],
                        weight=float(record["weight"])
                    )
                )
        
        return KnowledgeGraph(nodes=nodes, relationships=relationships)
    
    async def get_related_notes(self, note_id: str, limit: int = 5) -> List[str]:
        """Get related notes for a given note"""
        with neo4j_conn.get_session() as session:
            result = session.run(
                """
                MATCH (n1:Note {id: $note_id})-[r:RELATED_TO]->(n2:Note)
                RETURN n2.id as related_id, r.weight as weight
                ORDER BY r.weight DESC
                LIMIT $limit
                """,
                note_id=note_id,
                limit=limit
            )
            return [record["related_id"] for record in result]


graph_service = GraphService()

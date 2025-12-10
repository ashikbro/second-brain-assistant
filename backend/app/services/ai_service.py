from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.core.config import settings
from typing import List


class EmbeddingService:
    """Service for generating embeddings using OpenAI"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text"""
        return self.embeddings.embed_query(text)
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        return self.embeddings.embed_documents(texts)


class GPTService:
    """Service for GPT operations: summarization, tagging, idea generation"""
    
    MAX_TAGS = 5
    
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
    
    async def summarize(self, content: str) -> str:
        """Generate a summary of content"""
        prompt = PromptTemplate(
            input_variables=["content"],
            template="""Summarize the following content in 2-3 sentences:

{content}

Summary:"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = await chain.arun(content=content)
        return result.strip()
    
    async def extract_tags(self, content: str) -> List[str]:
        """Extract relevant tags from content"""
        prompt = PromptTemplate(
            input_variables=["content"],
            template="""Extract 3-5 relevant tags/keywords from the following content. 
Return only the tags separated by commas, no other text.

Content: {content}

Tags:"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = await chain.arun(content=content)
        tags = [tag.strip() for tag in result.strip().split(',')]
        return tags[:self.MAX_TAGS]
    
    async def generate_ideas(self, topic: str, context: str = "") -> str:
        """Generate ideas based on a topic and optional context"""
        prompt = PromptTemplate(
            input_variables=["topic", "context"],
            template="""Generate creative ideas and insights about the following topic.
{context}

Topic: {topic}

Ideas:"""
        )
        
        context_text = f"Context: {context}\n" if context else ""
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = await chain.arun(topic=topic, context=context_text)
        return result.strip()


embedding_service = EmbeddingService()
gpt_service = GPTService()

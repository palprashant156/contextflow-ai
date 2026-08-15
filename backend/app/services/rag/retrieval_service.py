from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from app.models.chunk import DocumentChunk
from app.services.rag.embedding_service import generate_query_embedding
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def retrieve_similar_chunks(db: Session, query: str, user_id: str, top_k: int = 5) -> List[DocumentChunk]:
    """
    Embeds the user query and performs a vector similarity search using pgvector's L2 distance (<->).
    We filter by user_id by joining with the documents table to ensure data privacy.
    """
    query_embedding = generate_query_embedding(query)
    
    # We use SQLAlchemy's text() for the pgvector <-> operator
    # The ::vector cast might be needed depending on pgvector setup
    sql = text("""
        SELECT c.* 
        FROM document_chunks c
        JOIN documents d ON c.document_id = d.id
        WHERE d.user_id = :user_id
        ORDER BY c.embedding <-> :embedding
        LIMIT :top_k
    """)
    
    result = db.execute(sql, {
        "user_id": user_id, 
        "embedding": str(query_embedding), 
        "top_k": top_k
    }).fetchall()
    
    return result

def generate_rag_answer(query: str, chunks: List[Any]) -> Dict[str, Any]:
    """
    Takes retrieved chunks, constructs a context window, and asks the LLM to generate an answer.
    """
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
    
    context_text = "\n\n".join([f"Source ID: {chunk.document_id}\nContent: {chunk.content}" for chunk in chunks])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are CortexFlow AI, an intelligent business assistant.
Answer the user's question based ONLY on the provided context.
If you cannot answer based on the context, say so. Do not invent information.
Always cite the Source ID in your answer when referencing facts."""),
        ("user", "Context:\n{context}\n\nQuestion: {question}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"context": context_text, "question": query})
    
    sources = list(set([str(chunk.document_id) for chunk in chunks]))
    
    return {
        "answer": response.content,
        "sources": sources
    }

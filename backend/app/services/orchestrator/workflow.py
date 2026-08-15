from sqlalchemy.orm import Session
from app.services.orchestrator.router import classify_intent, QueryIntent

# Import tools
from app.services.rag.retrieval_service import retrieve_similar_chunks, generate_rag_answer
from app.services.sql_agent.sql_generator import generate_sql_from_nl, synthesize_sql_answer
from app.services.sql_agent.sql_validator import validate_sql_query
from app.services.sql_agent.sql_execution import execute_safe_sql
from app.services.ml.classification_service import predict_document_category

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

def run_complex_workflow(db: Session, query: str, user_id: str) -> dict:
    """
    DAG Workflow for COMPLEX_ANALYSIS.
    1. Run SQL query to get data.
    2. Run RAG to get policy context.
    3. Synthesize everything.
    """
    analysis_steps = []
    
    # Step 1: SQL Data
    analysis_steps.append("1. Extracting structured metrics from PostgreSQL.")
    try:
        sql_query = generate_sql_from_nl(query)
        validate_sql_query(sql_query)
        sql_results = execute_safe_sql(db, sql_query)
    except Exception as e:
        sql_results = f"Failed to get SQL data: {e}"
        
    # Step 2: RAG Context
    analysis_steps.append("2. Retrieving enterprise knowledge and policies from pgvector.")
    chunks = retrieve_similar_chunks(db, query, user_id, top_k=3)
    rag_context = "\n".join([c.content for c in chunks])
    sources = [str(c.document_id) for c in chunks]
    
    # Step 3: Synthesis
    analysis_steps.append("3. Correlating data metrics with enterprise policies.")
    llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are CortexFlow AI. Answer the complex business query using the provided Data Metrics and Policy Context."),
        ("user", "Query: {query}\n\nData Metrics:\n{sql_results}\n\nPolicy Context:\n{rag_context}")
    ])
    
    chain = prompt | llm
    final_response = chain.invoke({
        "query": query, 
        "sql_results": str(sql_results), 
        "rag_context": rag_context
    })
    
    return {
        "answer": final_response.content,
        "sources": sources,
        "analysis_steps": analysis_steps,
        "engine": "COMPLEX_WORKFLOW"
    }

def orchestrate_query(db: Session, query: str, user_id: str) -> dict:
    """
    Main entrypoint for CortexFlow AI. Routes query to correct sub-agent.
    """
    intent = classify_intent(query)
    
    if intent == QueryIntent.DOCUMENT_QUESTION:
        chunks = retrieve_similar_chunks(db, query, user_id, top_k=5)
        if not chunks:
            return {"answer": "No relevant documents found.", "sources": [], "analysis_steps": ["Checked vector database."], "engine": "RAG"}
        rag_res = generate_rag_answer(query, chunks)
        return {
            "answer": rag_res["answer"],
            "sources": rag_res["sources"],
            "analysis_steps": ["Routed to RAG Engine.", f"Retrieved {len(chunks)} document chunks."],
            "engine": "RAG"
        }
        
    elif intent == QueryIntent.SQL_QUESTION:
        sql_query = generate_sql_from_nl(query)
        validate_sql_query(sql_query)
        raw_results = execute_safe_sql(db, sql_query)
        answer = synthesize_sql_answer(query, raw_results)
        return {
            "answer": answer,
            "sources": ["PostgreSQL Database"],
            "analysis_steps": ["Routed to SQL Agent.", "Generated and executed SELECT query."],
            "engine": "SQL"
        }
        
    elif intent == QueryIntent.ML_PREDICTION:
        # Simple heuristic: treat query as the document text to classify
        category = predict_document_category(query)
        return {
            "answer": f"The ML model predicted the category: **{category}**",
            "sources": ["MLflow DocumentClassifierModel"],
            "analysis_steps": ["Routed to ML Engine.", "Ran inference on text."],
            "engine": "ML"
        }
        
    elif intent == QueryIntent.COMPLEX_ANALYSIS:
        return run_complex_workflow(db, query, user_id)
        
    else:
        # GENERAL
        return {
            "answer": "I am CortexFlow AI. I can analyze documents, query business data, and run predictions. How can I help you?",
            "sources": [],
            "analysis_steps": ["General conversational response."],
            "engine": "GENERAL"
        }

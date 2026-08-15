from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

def execute_safe_sql(db: Session, query: str):
    """
    Executes a validated read-only SQL query against the database.
    In a real production environment, this `db` session would be bound 
    to a restricted database user with read-only permissions on a specific schema.
    """
    try:
        # Wrap query in text()
        sql_stmt = text(query)
        
        # Execute query
        result = db.execute(sql_stmt)
        
        # Fetch results
        columns = result.keys()
        rows = result.fetchall()
        
        # Format as list of dicts for the LLM
        formatted_results = [dict(zip(columns, row)) for row in rows]
        
        return formatted_results
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database execution error: {str(e)}")

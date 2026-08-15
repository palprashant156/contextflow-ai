import re
from fastapi import HTTPException

def validate_sql_query(query: str) -> bool:
    """
    Validates a SQL query to ensure it is a READ-ONLY SELECT statement.
    Rejects any queries containing destructive commands.
    """
    query_upper = query.upper()
    
    # Check if query starts with SELECT (ignoring leading whitespace)
    if not query_upper.strip().startswith("SELECT"):
        raise HTTPException(
            status_code=400, 
            detail="Only SELECT queries are allowed."
        )
    
    # List of prohibited keywords
    prohibited_keywords = [
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", 
        "GRANT", "REVOKE", "CREATE", "REPLACE", "EXEC"
    ]
    
    # Use word boundary regex to prevent false positives (e.g. "SELECT id from user_drops")
    for keyword in prohibited_keywords:
        pattern = r"\b" + keyword + r"\b"
        if re.search(pattern, query_upper):
            raise HTTPException(
                status_code=400, 
                detail=f"Security Violation: Prohibited SQL keyword '{keyword}' detected."
            )
            
    return True

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

from app.services.sql_agent.sql_generator import generate_sql_from_nl, synthesize_sql_answer
from app.services.sql_agent.sql_validator import validate_sql_query
from app.services.sql_agent.sql_execution import execute_safe_sql

router = APIRouter()

class SQLRequest(BaseModel):
    query: str

class SQLResponse(BaseModel):
    answer: str
    generated_sql: str
    raw_data: list

@router.post("/query", response_model=SQLResponse)
def query_database_via_nl(request: SQLRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Temporary standalone SQL Agent endpoint.
    Translates Natural Language to SQL, validates it, runs it, and synthesizes an answer.
    """
    try:
        # 1. Generate SQL
        sql_query = generate_sql_from_nl(request.query)
        
        # 2. Validate SQL (Ensure Read-Only)
        validate_sql_query(sql_query)
        
        # 3. Execute SQL
        raw_results = execute_safe_sql(db, sql_query)
        
        # 4. Synthesize Answer
        final_answer = synthesize_sql_answer(request.query, raw_results)
        
        return SQLResponse(
            answer=final_answer,
            generated_sql=sql_query,
            raw_data=raw_results
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL Agent Error: {str(e)}")

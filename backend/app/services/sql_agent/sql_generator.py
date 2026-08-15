from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_sql_from_nl(natural_language_query: str) -> str:
    """
    Uses an LLM to convert a Natural Language query into a Postgres SQL query.
    """
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
    
    # We provide a data dictionary/schema to the LLM
    schema_context = """
    Table: documents
    - id (UUID)
    - user_id (UUID)
    - filename (VARCHAR)
    - file_type (VARCHAR)
    - status (VARCHAR)
    - created_at (TIMESTAMP)
    
    Table: document_chunks
    - id (UUID)
    - document_id (UUID)
    - content (TEXT)
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert PostgreSQL developer. 
Given an input question, create a syntactically correct PostgreSQL query to run.
Unless the user specifies in their question a specific number of examples they wish to obtain, always limit your query to at most 10 results using the LIMIT clause.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
DO NOT wrap the SQL query in markdown formatting (no ```sql). Just return the raw SQL string.

Here is the database schema:
{schema}"""),
        ("user", "Question: {question}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    sql_query = chain.invoke({"schema": schema_context, "question": natural_language_query})
    
    # Clean up any potential markdown the LLM might have ignored instructions for
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    return sql_query

def synthesize_sql_answer(natural_language_query: str, sql_results: list) -> str:
    """
    Takes the JSON result from the SQL query and asks the LLM to formulate a human-readable answer.
    """
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are CortexFlow AI, a helpful business analyst.
You have translated a user's question into a SQL query, run it against the database, and received the following JSON results.
Your job is to read the results and answer the user's original question in a friendly, natural language format.
Do not mention SQL or databases in your response, just give the answer based on the data."""),
        ("user", "Question: {question}\n\nData Results:\n{results}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    answer = chain.invoke({"question": natural_language_query, "results": str(sql_results)})
    
    return answer

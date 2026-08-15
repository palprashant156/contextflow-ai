from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class QueryIntent(str, Enum):
    DOCUMENT_QUESTION = "DOCUMENT_QUESTION"
    SQL_QUESTION = "SQL_QUESTION"
    ML_PREDICTION = "ML_PREDICTION"
    COMPLEX_ANALYSIS = "COMPLEX_ANALYSIS"
    GENERAL = "GENERAL"

def classify_intent(user_query: str) -> QueryIntent:
    """
    Uses an LLM to classify the user's intent to route to the correct tool.
    """
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are the AI Orchestrator for CortexFlow.
Your job is to read the user's query and classify it into exactly ONE of the following categories:

DOCUMENT_QUESTION: Questions about company policies, text, paragraphs, unstructured documents, PDFs. (e.g. "What is our leave policy?")
SQL_QUESTION: Questions requiring counting, aggregations, database queries, structured numbers. (e.g. "How many users joined last month?", "Which department has highest turnover?")
ML_PREDICTION: Questions about predicting the future, classifying a new document, or estimating probability. (e.g. "What category does this document belong to?")
COMPLEX_ANALYSIS: Questions that require BOTH structured database data and unstructured document policies to answer. (e.g. "Why did complaints increase and what does our policy say about it?")
GENERAL: Simple greetings or questions that don't fit the above.

Return ONLY the category name. No other text."""),
        ("user", "{query}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke({"query": user_query}).strip()
    
    try:
        return QueryIntent(result)
    except ValueError:
        return QueryIntent.GENERAL

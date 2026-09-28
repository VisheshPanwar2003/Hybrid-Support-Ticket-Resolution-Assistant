from langchain_core.prompts import PromptTemplate

template = """You are a technical support assistant. Answer the user's question using ONLY the provided ticket context below. 
If the answer cannot be found in the context, state "I cannot answer this based on the retrieved tickets."
You MUST cite the ticket_id inline when referencing information (e.g., [Ticket 1042]).

Context:
{context}

Question: {question}

Answer:"""

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)
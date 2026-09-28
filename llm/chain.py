import os
import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.prompt_template import RAG_PROMPT
from retrieval.retrieve import retrieve_context

# Load GEMINI_API_KEY from .env
load_dotenv()

def format_docs(docs: list[dict]) -> str:
    """Formats the retrieved dictionary list into a readable string for the prompt."""
    if not docs:
        return "No relevant context found."
    
    formatted = []
    for doc in docs:
        formatted.append(
            f"[Ticket {doc['ticket_id']}]\n"
            f"Description: {doc['description']}\n"
            f"Resolution: {doc['resolution']}"
        )
    return "\n\n".join(formatted)

def ask_assistant(question: str) -> str:
    """End-to-end RAG chain: Retrieval -> Formatting -> Prompt -> LLM."""
    
    # 1. Retrieve raw context via hybrid search
    raw_context = retrieve_context(question)
    
    # 2. Format context for LangChain
    formatted_context = format_docs(raw_context)
    
    # 3. Stop early if no context is found (saves API costs)
    if formatted_context == "No relevant context found.":
        return "System: No matching tickets found to answer your question."
        
    # 4. Initialize Gemini LLM via LangChain
    llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)
    # 5. Build and invoke the LangChain pipeline
    chain = RAG_PROMPT | llm | StrOutputParser()
    
    print("\n[5] Calling LLM via LangChain...")
    response = chain.invoke({"context": formatted_context, "question": question})
    return response

if __name__ == "__main__":
    question = "How did we fix the mobile app login timeout?"
    answer = ask_assistant(question)
    print("\n🤖 FINAL ANSWER:")
    print(answer)
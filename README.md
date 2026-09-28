# 🚀 Hybrid Support Ticket Resolution Assistant (RAG)

An enterprise-grade, Hybrid Retrieval-Augmented Generation (RAG) pipeline designed to resolve technical support queries with zero hallucinations. 

Unlike standard vector-only RAG systems, this architecture combines **SQL metadata pre-filtering** with **ChromaDB semantic retrieval** to aggressively prune irrelevant data, save compute, and guarantee that the LLM (Google Gemini) grounds its answers in verified historical tickets.

## 🛠 Tech Stack
* **Language:** Python
* **Data Engineering:** Pandas, SQLite
* **Vector Database & NLP:** ChromaDB, HuggingFace Sentence-Transformers (`all-MiniLM-L6-v2`)
* **LLM Orchestration:** LangChain, Google Gemini 3.8-flash API
* **Evaluation & Math:** NumPy, SciPy, Python `unittest`

## 🧠 System Architecture

This project solves the three biggest flaws in standard RAG applications (Hallucinations, Context Loss, and Compute Waste) through a strict 4-step pipeline:

1. **Ingestion & Pandas Cleaning:** Raw ticket data (CSV) is parsed, deduplicated, and normalized (missing values handled, dates standardized) using Pandas before being relationalized into SQLite.
2. **"Whole-Ticket" Chunking:** Instead of arbitrarily splitting text every 1,000 characters (which separates problems from their solutions), the system fuses the `Description` and `Resolution` into a single semantic block to preserve complete context.
3. **Hybrid Retrieval (SQL -> Vector):** 
   * **SQL Gatekeeper:** Natural language queries are parsed for hard constraints (e.g., "UI", "Billing"). A SQL query filters the candidate pool. If zero match, the system halts—preventing the LLM from guessing.
   * **Semantic Search:** Only the verified SQL candidate IDs are passed to ChromaDB for high-dimensional cosine similarity matching.
4. **LLM Synthesis & Citation:** LangChain injects the retrieved context into a strict prompt template, forcing Gemini to generate an answer *only* from the context and explicitly cite the source `[Ticket ID]`.

## 📂 Project Structure

```text
├── config/
│   └── settings.py                 # Global paths and model configurations
├── data/
│   ├── generate_large_dataset.py   # Script to generate 1,000+ synthetic tickets
│   └── sample_queries.json         # Evaluation golden dataset
├── embeddings/
│   ├── chunk.py                    # Custom "Whole-Ticket" chunking logic
│   └── embed.py                    # HuggingFace vector encoding & ChromaDB upsertion
├── evaluation/
│   ├── chunking_comparison.py      # Math proof: Whole-ticket vs Split chunking
│   ├── embedding_wording_experiment.py # Semantic similarity wording tests
│   └── manual_cosine_check.py      # NumPy/SciPy exact cosine distance calculations
├── ingestion/
│   ├── clean.py                    # Pandas data normalization
│   └── load_sql.py                 # SQLite database schema and loading
├── llm/
│   ├── chain.py                    # LangChain LCEL orchestration
│   └── prompt_template.py          # Strict hallucination-resistant prompt
├── retrieval/
│   ├── query_parser.py             # NLP constraint extraction
│   └── retrieve.py                 # Hybrid SQL + ChromaDB search logic
├── tests/                          # Unit tests for chunking and parsing
├── main.py                         # Interactive CLI assistant
└── README.md


🚀 Installation & Setup
1. Clone the repository and set up a virtual environment:

Bash
git clone [https://github.com/yourusername/Hybrid-Support-Ticket-Resolution-Assistant.git](https://github.com/yourusername/Hybrid-Support-Ticket-Resolution-Assistant.git)
cd Hybrid-Support-Ticket-Resolution-Assistant
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
2. Install dependencies:

Bash
pip install pandas numpy scipy sentence-transformers chromadb langchain langchain-google-genai python-dotenv
3. Configure API Keys:
Create a .env file in the root directory and add your Google Gemini API key:

Code snippet
GEMINI_API_KEY=your_google_gemini_api_key_here

💻 Usage
Step 1: Generate Data & Populate Databases
Generate a synthetic dataset of 1,000 realistic support tickets, clean them, and load them into SQLite and ChromaDB.

Bash
python data/generate_large_dataset.py
python ingestion/load_sql.py
python embeddings/embed.py
Step 2: Run the Assistant
Start the interactive command-line interface.

Bash
python main.py
Example Query: `"How do we fix the mobile app login timeout?"*

🧪 Mathematical Evaluation
This system doesn't rely on "vibes." It includes an offline evaluation suite to mathematically prove retrieval accuracy:

Run python evaluation/manual_cosine_check.py to see the exact SciPy cosine distance calculations driving the vector search.

Run python evaluation/chunking_comparison.py to mathematically prove why whole-ticket chunking prevents context loss compared to traditional recursive text splitting.

Run python -m unittest discover tests/ to execute the automated unit testing suite.

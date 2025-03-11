# Import required libraries
import os
import random
import pandas as pd
import requests
from datetime import datetime
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import DensePassageRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline

# API key for real-time stock market data
API_KEY = "0L6PHZNXGSSIZAN9"
BASE_URL = "https://www.alphavantage.co/query"

# Fun financial tips
fun_facts = [
    "The 50/30/20 rule suggests allocating 50% of income to needs, 30% to wants, and 20% to savings!",
    "Start investing early to take advantage of compound interest!",
    "Avoid high-interest debt whenever possible.",
    "Automate your savings to ensure consistent contributions.",
    "Diversify your portfolio to minimize risk.",
]

# **STEP 1: Fix FAISS Mismatch (Delete & Reinitialize If Needed)**
if os.path.exists("faiss_document_store.db"):
    os.remove("faiss_document_store.db")
if os.path.exists("faiss_index"):
    os.remove("faiss_index")

# Initialize FAISS document store
document_store = FAISSDocumentStore(
    embedding_dim=768, 
    sql_url="sqlite:///faiss_document_store.db"
)

# **STEP 2: Create a Knowledge Base with Finance Knowledge**
data = [
    {"content": "Dollar-cost averaging is an investment strategy where you invest a fixed dollar amount regularly, regardless of market conditions.", "meta": {"topic": "investing"}},
    {"content": "A Roth IRA allows tax-free withdrawals for qualified expenses. Contributions are made with after-tax dollars.", "meta": {"topic": "retirement"}},
    {"content": "The 50/30/20 rule helps divide income efficiently across needs, wants, and savings.", "meta": {"topic": "budgeting"}},
    {"content": "High-yield savings accounts provide better interest rates than traditional savings accounts.", "meta": {"topic": "saving"}},
]
# Convert knowledge base to FAISS documents
documents = [{"content": row["content"], "meta": row["meta"]} for row in data]
document_store.write_documents(documents)

# **STEP 3: Initialize Dense Retriever & Update Embeddings**
retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    use_gpu=False
)

print("Updating FAISS document embeddings. This might take a few moments...")
document_store.update_embeddings(retriever)
print("FAISS embeddings updated successfully!")

# **STEP 4: Check FAISS Index Health**
print("Total Documents in FAISS:", document_store.get_document_count())
print("Total Embeddings in FAISS:", document_store.get_embedding_count())

# **STEP 5: Initialize Reader for Better Answers**
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

# **STEP 6: Create RAG-Based QA Pipeline**
qa_pipeline_rag = ExtractiveQAPipeline(reader, retriever)

# **STEP 7: Fetch Market Data Function**
def fetch_market_data():
    indices = {"S&P 500": "SPY", "Dow Jones": "DIA", "NASDAQ": "QQQ"}
    market_data = {}
    try:
        for name, symbol in indices.items():
            response = requests.get(BASE_URL, params={
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol,
                "interval": "5min",
                "apikey": API_KEY
            })
            data = response.json()
            if "Time Series (5min)" in data:
                latest_time = sorted(data["Time Series (5min)"].keys())[-1]
                latest_close = data["Time Series (5min)"][latest_time]["4. close"]
                market_data[name] = latest_close
            else:
                market_data[name] = "N/A"
    except Exception as e:
        print(f"Error fetching market data: {e}")
    return market_data

# **STEP 8: Format Market Data for Display**
def format_market_data(data):
    sp500 = data.get("S&P 500", "N/A")
    dow_jones = data.get("Dow Jones", "N/A")
    nasdaq = data.get("NASDAQ", "N/A")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    return f"Market status:\nS&P 500: ${sp500} (as of {timestamp})\nDow Jones: ${dow_jones} (as of {timestamp})\nNASDAQ: ${nasdaq} (as of {timestamp})"

# **STEP 9: Display Help Menu**
def display_help():
    print("""
    --- ChatBot Help Menu ---
    1. Ask finance-related questions (e.g., "How can I save more money?").
    2. Type 'market' to check live stock market data.
    3. Type 'tip' to get a random financial tip.
    4. Type 'help' to see this menu again.
    5. Type 'bye' to exit the chatbot.
    """)

# **STEP 10: Generate Response Using Both QA & RAG**
def get_response(user_input):
    """Retrieve an answer using both FAISS retrieval and QA pipeline."""
    try:
        # First, try FAISS-based retrieval
        result = qa_pipeline_rag.run(query=user_input, params={"Retriever": {"top_k": 3}, "Reader": {"top_k": 1}})
        
        # Debugging: Print retrieved documents
        print("Retrieved Documents:", [doc.content for doc in result["documents"]])

        # If FAISS returns results, use them
        if result["answers"] and result["answers"][0].answer:
            return result["answers"][0].answer

        # If FAISS fails, fallback to DistilBERT QA
        response = qa_pipeline(question=user_input, context="\n".join([doc["content"] for doc in documents]))
        return response["answer"] if response["score"] > 0.5 else "I'm not sure, could you clarify?"
    except Exception as e:
        print(f"Error in question-answering: {e}")
        return "Sorry, I couldn't process that. Please try again."

# **STEP 11: Chatbot Loop**
def chatbot():
    print("Hey there! Welcome to the Personal Finance Chatbot! How can I help you?")
    display_help()
    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "bye":
            print("ChatBot: Goodbye! Have a great day!")
            break
        elif user_input == "help":
            display_help()
        elif user_input == "tip":
            print("ChatBot:", random.choice(fun_facts))
        elif "market" in user_input:
            market_data = fetch_market_data()
            formatted_data = format_market_data(market_data)
            print("ChatBot:", formatted_data)
        else:
            print("ChatBot:", get_response(user_input))

# Run the chatbot
if __name__ == "__main__":
    chatbot()
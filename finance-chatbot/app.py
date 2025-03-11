from flask import Flask, request, jsonify, render_template
import os
import random
import requests
from datetime import datetime
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import DensePassageRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline

# Initialize Flask App
app = Flask(__name__, template_folder='templates')

# API key for stock market data
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

# **STEP 1: Initialize FAISS Document Store**
if os.path.exists("faiss_document_store.db"):
    os.remove("faiss_document_store.db")
if os.path.exists("faiss_index"):
    os.remove("faiss_index")

document_store = FAISSDocumentStore(
    embedding_dim=768, 
    sql_url="sqlite:///faiss_document_store.db",
    faiss_index_factory_str="Flat"
)

# **STEP 2: Load Financial Knowledge into FAISS**
data = [
    {"content": "Dollar-cost averaging is an investment strategy where you invest a fixed dollar amount regularly, regardless of market conditions. It helps reduce risk by spreading purchases over time."},
    {"content": "A Roth IRA is a retirement savings account that allows tax-free withdrawals for qualified expenses. Contributions are made with after-tax dollars, which means your money grows tax-free."},
    {"content": "The 50/30/20 rule suggests allocating 50% of income to needs, 30% to wants, and 20% to savings. This budgeting method helps balance spending and saving effectively."},
    {"content": "High-yield savings accounts offer better interest rates compared to traditional savings accounts. These accounts are great for emergency funds and short-term savings."},
    {"content": "Index funds are low-cost investment funds that track a market index such as the S&P 500. They provide diversification and require minimal management, making them ideal for long-term investing."},
    {"content": "Investing in ETFs (Exchange-Traded Funds) is a great way to diversify your portfolio while maintaining flexibility. ETFs trade like stocks but offer diversification similar to mutual funds."},
    {"content": "Bonds are fixed-income investments where investors lend money to entities in exchange for periodic interest payments and the return of the principal amount at maturity."},
    {"content": "Mutual funds pool money from many investors to invest in a diversified portfolio of stocks, bonds, or other assets. They are managed by professionals."},
    {"content": "A credit score is a measure of creditworthiness, ranging from 300-850. A higher score improves your chances of getting better interest rates on loans and credit cards."},
    {"content": "Diversification reduces investment risk by spreading assets across different asset classes, such as stocks, bonds, and real estate."},
    {"content": "Compounding interest allows your savings and investments to grow exponentially over time. The earlier you start, the more significant the impact of compounding."},
    {"content": "An emergency fund should cover 3-6 months of living expenses. It should be kept in a liquid, high-yield savings account for quick access."},
    {"content": "Stock market volatility refers to the frequent rise and fall of stock prices. Long-term investors should focus on overall market trends rather than short-term fluctuations."},
    {"content": "A 401(k) is an employer-sponsored retirement savings plan that allows pre-tax contributions, reducing taxable income while saving for retirement."},
    {"content": "Annuities are financial products that provide regular payments over a specified period, often used for retirement income."}
]

# 🟢 Debugging: Print each document before storing in FAISS
for i, doc in enumerate(data):
    print(f"📢 Storing Document {i+1}: {doc['content']}")

document_store.write_documents(data, duplicate_documents="skip")

# 🟢 Confirm how many documents are stored
print("✅ FAISS Total Documents:", document_store.get_document_count())



# **STEP 3: Initialize Retriever & Update FAISS Embeddings**
retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    use_gpu=False
)

print("Updating FAISS document embeddings...")
document_store.update_embeddings(retriever)
print("FAISS embeddings updated successfully!")

# **STEP 4: Initialize Reader & QA Pipeline**
reader = FARMReader(model_name_or_path="deepset/roberta-large-squad2", use_gpu=False, max_seq_len=512, doc_stride=128)
qa_pipeline_rag = ExtractiveQAPipeline(reader, retriever)

# **STEP 5: Fetch Market Data Function**
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

# **STEP 6: Serve Frontend UI**
@app.route("/")
def home():
    return render_template("index.html")

# **STEP 7: Chatbot API Endpoint**
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").lower()

    # Handle chatbot commands
    if user_input == "help":
        return jsonify({"response": """
        🤖 **Chatbot Commands:**
        1️⃣ **Ask finance questions** (e.g., "How do I save more money?")
        2️⃣ **Get live stock market updates** (Type 'market')
        3️⃣ **Receive a financial tip** (Type 'tip')
        4️⃣ **Exit chatbot** (Type 'bye')
        """})
    elif user_input == "tip":
        return jsonify({"response": random.choice(fun_facts)})
    elif "market" in user_input:
        return jsonify({"response": fetch_market_data()})

    # Run FAISS query
    result = qa_pipeline_rag.run(query=user_input, params={"Retriever": {"top_k": 20}, "Reader": {"top_k": 5}})

    # Print Retrieved Documents and Answers for Debugging
    retrieved_docs = [doc.content for doc in result.get("documents", [])]
    retrieved_answers = [ans.answer for ans in result.get("answers", [])]
    
    print("\n📢 Retrieved Docs:", retrieved_docs)
    print("📢 Retrieved Answers:", retrieved_answers)

    # Process FAISS Responses
    if retrieved_answers:
        detailed_answers = list(set([ans.strip() for ans in retrieved_answers if ans and len(ans) > 20]))

        # Combine and format responses
        if len(detailed_answers) > 1:
            full_response = "\n\n".join(detailed_answers[:3])  # Show up to 3 responses
        elif len(detailed_answers) == 1:
            full_response = detailed_answers[0]
        else:
            full_response = "I couldn't find a clear answer. Try rewording your question."

        return jsonify({"response": full_response})

    return jsonify({"response": "I'm not sure, but you can try rewording your question."})

# **Run Flask App**

if __name__ == "__main__":
    from waitress import serve  # Use a production-ready server
    serve(app, host="0.0.0.0", port=10000)

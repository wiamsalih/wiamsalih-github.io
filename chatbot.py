# Use a pipeline as a high-level helper
import random
import requests
from transformers import pipeline
from datetime import datetime

API_KEY = "0L6PHZNXGSSIZAN9"
BASE_URL = "https://www.alphavantage.co/query"

# Initialize QA pipeline with smaller model
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-uncased-distilled-squad",
    cache_dir="./models"  # Use a writable directory for model caching
)

# Financial tips or fun facts
fun_facts = [
    "Did you know? The 50/30/20 rule suggests allocating 50% of your income to needs, 30% to wants, and 20% to savings!",
    "Start investing early to take advantage of compound interest! It's the fastest way to grow steady wealth",
    "Saving small amounts consistently can lead to big results over time.",
    "Avoid high-interest debt whenever possible. Seriously.",
    "Emergency funds are your financial safety net. Start building one today!",
    "Automate your savings to ensure you consistently put money aside each month.",
    "Set short-term, mid-term, and long-term financial goals to stay motivated. You got this!",
    "Investment Tip: Diversify your investment portfolio to minimize risk.",
    "Investment Tip: Learn about dollar-cost averaging to invest in volatile markets like Bitcoin.",
    "Learn about compound interest its the most powerful tool in wealth building.",
    "Understand your credit score and work on improving it for better loan terms.",
    "Invest in your future self. Track all your expenses for a month to identify unnecessary spending.", 
    "If you are interested in investing and don't know where to start a Roth IRA is the best start, and then World Market ETFs! :)"

]
# Custom function to fetch market data
def fetch_market_data():
    """Fetches market data using the Alpha Vantage API."""
    indices = {"S&P 500": "SPY", "Dow Jones": "DIA", "NASDAQ": "QQQ"}
    market_data = {}
    
    try:
        for name, symbol in indices.items():
            params = {
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol,
                "interval": "5min",
                "apikey": API_KEY
            }
            response = requests.get(BASE_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                # Check for valid data in the response
                if "Time Series (5min)" in data:
                    time_series = data["Time Series (5min)"]
                    latest_time = sorted(time_series.keys())[-1]
                    latest_close = time_series[latest_time]["4. close"]
                    market_data[name] = latest_close
                else:
                    market_data[name] = "N/A"
            else:
                market_data[name] = "N/A"
    except Exception as e:
        print(f"Error fetching market data: {e}")
    
    return market_data


# Custom function to format market data
def format_market_data(data):
    sp500 = data.get("S&P 500", "N/A")
    dow_jones = data.get("Dow Jones", "N/A")
    nasdaq = data.get("NASDAQ", "N/A")
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Ensure values are formatted correctly and not 'N/A' before displaying
    return f"""Here's the latest market status:
S&P 500: ${sp500 if sp500 != "N/A" else 'N/A'} (as of {timestamp})
Dow Jones: ${dow_jones if dow_jones != "N/A" else 'N/A'} (as of {timestamp})
NASDAQ: ${nasdaq if nasdaq != "N/A" else 'N/A'} (as of {timestamp})"""

# Finance-related context
context = """Personal finance is about budgeting, saving, investing, managing loans, and planning for retirement. 
It helps individuals to make informed decisions to achieve financial goals, want a tip? For example, investing in a 401(k) 
is a common retirement planning strategy. Plus the current market status will help you make better and smarter investment descisions!
"""


# Help menu

def display_help():
    """Displays a help menu for the user."""
    help_text = """
    --- ChatBot Help Menu ---
    1. Ask finance-related questions (e.g., "How can I save more money?").
    2. Type 'market' to check how the market is doing today. 
    3. Type 'tip' to get a random financial tip.
    4. Type 'help' to see this menu again.
    5. Type 'bye' to exit the chatbot.
    -------------------------
    """
    print(help_text)


# Generate a response using the QA pipeline
def get_response(user_input):
    """Generate a response using the QA pipeline."""
    try:
        response = qa_pipeline(question=user_input, context=context)
        return response["answer"]
    except Exception as e:
        print(f"Error in question-answering: {e}")  # Log the exception
        return "Sorry, I couldn't process that. Please try again."



# Chatbot loop
def chatbot():
    print("Hey there! Welcome to the Personal Finance Chatbot! How can I help you?")
    display_help()

    keywords = ["finance", "money", "invest", "save", "budget", "market"]

    while True:
        user_input = input("You: ").strip().lower()

        if not user_input:
            print("ChatBot: Please enter a question or command so I can best assist you :)")
            continue
        elif user_input == "bye":
            print("ChatBot: Goodbye! Have a great day! :)")
            break
        elif user_input == "help":
            display_help()
        elif user_input == "tip":
            print("ChatBot:", random.choice(fun_facts))
        elif "market" in user_input:  
            market_data = fetch_market_data()
            if market_data:
                formatted_data = format_market_data(market_data)
                print("ChatBot:", formatted_data)
            else:
                print("ChatBot: There was an issue retrieving the market data. Can you please try again later.")
        elif any(keyword in user_input for keyword in keywords):
            print("ChatBot:", get_response(user_input))
        else:
            print("ChatBot: Sorry but I'm not sure about that. Try asking me a finance-related question or use the help menu! :)")
if __name__ == "__main__":
    chatbot()

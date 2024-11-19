# Use a pipeline as a high-level helper
import random
from transformers import pipeline

# Initialize QA pipeline with smaller model
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-uncased-distilled-squad",
    cache_dir="./models"  # Use a writable directory for model caching
)


# Finance-related context
context = """Personal finance is about budgeting, saving, investing, managing loans, and planning for retirement. 
It helps individuals make informed decisions to achieve financial goals. For example, investing in a 401(k) 
is a common retirement planning strategy.
"""
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
    "Learn about compound interest—its the most powerful tool in wealth building.",
    "Understand your credit score and work on improving it for better loan terms.",
    "Invest in your future self. Track all your expenses for a month to identify unnecessary spending.", 
    "If you are interested in investing and don't know where to start a Roth IRA is the best start, and then World Market ETFs! :)"

]
# Help menu

def display_help():
    """Displays a help menu for the user."""
    help_text = """
    --- ChatBot Help Menu ---
    1. Ask finance-related questions (e.g., "How can I save more money?").
    2. Type 'tip' to get a random financial tip.
    3. Type 'help' to see this menu again.
    4. Type 'bye' to exit the chatbot.
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
    print("Hey there! Welcome to the Personal Finance Chatbot!")
    display_help()

    keywords = ["finance", "money", "invest", "save", "budget"]

    while True:
        user_input = input("You: ").strip().lower()

        if not user_input:
            print("ChatBot: Please enter a question or command so I can best assist you.")
            continue
        elif user_input == "bye":
            print("ChatBot: Goodbye! Have a great day! :)")
            break
        elif user_input == "help":
            display_help()
        elif user_input == "tip":
            print("ChatBot:", random.choice(fun_facts))
        elif any(keyword in user_input for keyword in keywords):
            print("ChatBot:", get_response(user_input))
        else:
            print("ChatBot: I'm not sure about that. Try asking me a finance-related question or use the help menu! :)")

chatbot()

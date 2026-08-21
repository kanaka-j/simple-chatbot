import os
from dotenv import load_dotenv
from google import genai

#Load the secret API key form .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

#initialize Gemini AI Client 
client = genai.Client(api_key=api_key)

def response(user_input: str) -> str:
        """Sends user prompt to Gemini and returns the AI's answer."""
        try:
            res = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_input,
            )
            return res.text
        except Exception as e:
            return f"Error communicating with AI: {e}"
    
def main():
        print("🤖 Chatbot: Hello! I'm now powered by Google Gemini AI. Type 'bye' to exit.\n")
        while True:
            user_input = input("You: ")
            
            # Check if user wants to exit
            if user_input.lower().strip() in ["bye", "exit", "quit"]:
                print("🤖 Chatbot: Goodbye! Have a great day!")
                break
            
            # Skip empty inputs
            if not user_input.strip():
                continue
                
            # Get and display AI response
            print("🤖 Chatbot:", response(user_input))
            print("-" * 50)

if __name__ == "__main__":
        main()

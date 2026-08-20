import datetime
from fastapi import FastAPI

app= FastAPI()

def response(user_input):
    text=user_input.lower()
    if "hello" in text or "hi" in text:
        return "Hello! there  HOw can i help you?"
    elif "name" in text:
        return "I'm chatbot,your friendly python bot"
    elif "weather" in text:
        return "I am not sure about the weather, but I hope it's nice outside!"
    elif "bye" in text:
        return "Goodbye! see you soon"
    elif "time" in text:
        now=datetime.datetime.now()
        return "The time is "+now.strftime("%H:%M")
    elif "date" in text:
        now=datetime.datetime.now()
        return "Today's date is "+now.strftime("%Y-%m-%d")
    
        
    else:
        return "I'm sorry, I don't understand. Can you please rephrase?"

@app.post("/chat")
def chat(message:dict):
    reply=response(message["message"])
    return {"reply":reply}
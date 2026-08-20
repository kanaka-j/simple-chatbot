import datetime 
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


def main():
    print("Chatabot:Helo! Type 'bye' to exit")
    while True:
        user_input =input("You:")
        if "bye" in user_input.lower():
            print("Chatbot:Goodbye!")
            break
        print("Chatbot:", response(user_input))

if __name__ == "__main__":
    main()




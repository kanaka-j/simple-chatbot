import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# 2. Load API Key & Initialize Gemini Client
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in .env file. Please add it to continue.")
    st.stop()

client = genai.Client(api_key=api_key)

# 3. Sidebar Controls (Personas, Temperature, Clear Chat)
with st.sidebar:
    st.header("⚙️ Chatbot Settings")
    
    # Pre-defined System Instruction Personas
    personas = {
        "Python & GenAI Mentor 🐍": (
            "You are a friendly and encouraging Python and Generative AI teacher. "
            "Explain concepts simply using analogies, step-by-step explanations, and short code snippets. "
            "Always encourage the user and keep explanations easy for beginners to understand."
        ),
        "Helpful Assistant 🤖": (
            "You are a polite, helpful, and concise AI assistant. Answer questions clearly and accurately."
        ),
        "Strict Senior Developer 💻": (
            "You are a strict, pragmatic Senior Software Engineer. Give concise, production-ready code, "
            "point out edge cases, code smells, and performance bottlenecks. No fluff."
        ),
        "Creative Storyteller 📚": (
            "You are a creative writer and storyteller. Use vivid imagery, engaging dialogue, "
            "and imaginative metaphors in all your responses."
        ),
        "Custom Persona ✍️": ""
    }
    
    selected_persona_name = st.selectbox("Choose AI Persona:", list(personas.keys()), index=0)
    
    if selected_persona_name == "Custom Persona ✍️":
        system_instruction = st.text_area(
            "Enter custom system prompt:",
            value="You are an expert AI tutor.",
            help="Define how the AI should behave and what rules it should follow."
        )
    else:
        system_instruction = personas[selected_persona_name]
        st.info(f"**Persona Prompt:**\n{system_instruction}")

    st.markdown("---")
    
    # Temperature Slider (Creativity Control)
    temperature = st.slider(
        "🌡️ Temperature (Creativity):",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.1,
        help="Lower values (0.0 - 0.3) = factual and precise. Higher values (0.8 - 1.5) = creative and imaginative."
    )

    st.markdown("---")
    
    # Clear Conversation Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. Main Chat Interface
st.title("🤖 Hey, Kan")
st.caption(f"Active Persona: **{selected_persona_name}** | Temperature: **{temperature}**")

# 5. Initialize Conversation History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display previous chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User Input Box
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Prepare conversation history format for Gemini SDK
    contents = [
        types.Content(
            role=msg["role"],
            parts=[types.Part.from_text(text=msg["content"])]
        )
        for msg in st.session_state.messages
    ]

    # Configure Gemini with System Instruction and Temperature
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature
    )

    # Generate and stream response from Gemini
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # Stream response chunk-by-chunk
            response = client.models.generate_content_stream(
                model="gemini-3.6-flash",
                contents=contents,
                config=config
            )
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
            # Save assistant response to history
            st.session_state.messages.append({"role": "model", "content": full_response})

        except Exception as e:
            st.error(f"Error communicating with AI: {e}")
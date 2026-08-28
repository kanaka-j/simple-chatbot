# Frontend: Simplechatboat/app.py

import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Gemini AI Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Luxury Dark OLED / Glassmorphism Aesthetic CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Typography & Background */
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background-color: #0B0D14;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.08) 0px, transparent 50%);
        color: #E2E8F0;
    }

    /* Main Container max width and padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 6rem;
        max-width: 860px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0E101A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    [data-testid="stSidebar"] hr {
        margin: 1.25rem 0 !important;
        border-color: rgba(255, 255, 255, 0.06) !important;
    }

    /* Sidebar Buttons */
    [data-testid="stSidebar"] .stButton > button {
        border-radius: 12px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.6rem 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        color: #94A3B8 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99, 102, 241, 0.12) !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
        color: #FFFFFF !important;
        transform: translateX(3px);
    }

    /* Primary New Chat Button */
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* Gradient Hero Title */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #60A5FA 0%, #A855F7 50%, #F43F5E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        padding: 4px 12px;
        border-radius: 20px;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    /* User Profile Card */
    .profile-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        margin-bottom: 1rem;
    }

    .profile-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366F1, #A855F7);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.4);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        margin-left: auto;
        box-shadow: 0 0 8px #10B981;
    }

    /* Chat Messages Styling */
    .stChatMessage {
        border-radius: 18px !important;
        padding: 1.15rem 1.4rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* User Message Style */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: rgba(99, 102, 241, 0.1) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
    }

    /* Assistant Message Style */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: rgba(22, 25, 38, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* Starter suggestion buttons in main window */
    .main .stButton > button {
        border-radius: 16px !important;
        padding: 1rem !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        color: #E2E8F0 !important;
        font-weight: 500 !important;
        text-align: left !important;
        transition: all 0.2s ease !important;
    }

    .main .stButton > button:hover {
        background: rgba(99, 102, 241, 0.08) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
    }

    /* Floating Chat Input bar */
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
        background-color: #121522 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25), 0 10px 30px rgba(0, 0, 0, 0.3) !important;
    }

    /* ✨ Highlight the Attachment (+) Button inside the Chat Input Bar ✨ */
    [data-testid="stChatInput"] button {
        background: rgba(99, 102, 241, 0.15) !important;
        border-radius: 12px !important;
        color: #818CF8 !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stChatInput"] button:hover {
        background: rgba(99, 102, 241, 0.3) !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5) !important;
        transform: scale(1.08) !important;
    }

    [data-testid="stChatInput"] svg {
        fill: currentColor !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Load API Key & Gemini Client
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in .env file. Please add it to continue.")
    st.stop()

client = genai.Client(api_key=api_key)

# 4. Session State Initialization
if "user_name" not in st.session_state:
    st.session_state.user_name = "Kan"

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [
        {"id": 1, "title": "New Conversation", "messages": [], "time": datetime.now().strftime("%I:%M %p")}
    ]

if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = 1

# Helper: Get current active session
def get_active_session():
    for s in st.session_state.chat_sessions:
        if s["id"] == st.session_state.active_session_id:
            return s
    return st.session_state.chat_sessions[0]

active_session = get_active_session()

# ==========================================
# 🌟 LUXURY SIDEBAR
# ==========================================
with st.sidebar:
    # 1. User Profile Badge
    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-avatar">{st.session_state.user_name[:2].upper()}</div>
        <div style="flex-grow: 1;">
            <div style="font-weight: 700; font-size: 0.95rem; color: #FFFFFF;">{st.session_state.user_name}</div>
            <div style="font-size: 0.72rem; color: #818CF8;">Pro Developer</div>
        </div>
        <div class="status-dot" title="Active"></div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Primary New Chat Button
    if st.button("➕  Start New Chat", use_container_width=True, type="primary"):
        new_id = max([s["id"] for s in st.session_state.chat_sessions], default=0) + 1
        new_session = {
            "id": new_id,
            "title": f"Chat #{new_id}",
            "messages": [],
            "time": datetime.now().strftime("%I:%M %p")
        }
        st.session_state.chat_sessions.insert(0, new_session)
        st.session_state.active_session_id = new_id
        st.rerun()

    st.markdown("---")
    st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 0.75rem;'>💬 Recent Conversations</div>", unsafe_allow_html=True)

    # 3. Clean Session List
    for s in st.session_state.chat_sessions:
        is_active = s["id"] == st.session_state.active_session_id
        title = s["title"]
        if len(title) > 24:
            title = title[:21] + "..."
            
        icon = "✨" if is_active else "💬"
        button_label = f"{icon}  {title}"

        if st.button(button_label, key=f"session_btn_{s['id']}", use_container_width=True):
            st.session_state.active_session_id = s["id"]
            st.rerun()

    st.markdown("---")

    # 4. Engine Status Box
    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 14px; padding: 12px; font-size: 0.78rem; color: #818CF8; text-align: center; margin-bottom: 0.75rem;">
        ⚡ <b>Model:</b> Gemini 3.6 Flash<br>
        👁️ <b>Vision:</b> Multimodal Active
    </div>
    """, unsafe_allow_html=True)

    # 5. Clear All Chats Button
    if st.button("🗑️  Clear All History", use_container_width=True, help="Reset all chat history"):
        st.session_state.chat_sessions = [
            {"id": 1, "title": "New Conversation", "messages": [], "time": datetime.now().strftime("%I:%M %p")}
        ]
        st.session_state.active_session_id = 1
        st.rerun()


# ==========================================
# 💬 MAIN CHAT INTERFACE
# ==========================================

# Top Header Bar
col_h1, col_h2 = st.columns([5, 1], vertical_alignment="center")
with col_h1:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.3rem;">
        <span class="badge-pill">⚡ Gemini 3.6 Flash</span>
    </div>
    <div class="hero-title">{active_session['title']}</div>
    """, unsafe_allow_html=True)

with col_h2:
    if st.button("🧹 Clear", help="Clear current session"):
        active_session["messages"] = []
        st.rerun()

st.markdown("<hr style='margin-top: 0.4rem; margin-bottom: 1.8rem; border-color: rgba(255, 255, 255, 0.06);'>", unsafe_allow_html=True)

# Starter Suggestion Cards (Show only when current chat is empty)
if len(active_session["messages"]) == 0:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
        <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">✨</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #FFFFFF;">How can I assist you today?</div>
        <div style="font-size: 0.9rem; color: #94A3B8; margin-top: 0.2rem;">Type a question or click + below to attach an image:</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀  Explain Quantum Computing with analogies", use_container_width=True):
            st.session_state.starter_prompt = "Explain Quantum Computing in simple terms using 3 everyday analogies."
        if st.button("🐍  Design a production FastAPI microservice", use_container_width=True):
            st.session_state.starter_prompt = "Give me the architectural blueprint and folder structure for a production FastAPI microservice."
    with col2:
        if st.button("🧠  Why is Gemini 3.6 Flash so fast?", use_container_width=True):
            st.session_state.starter_prompt = "How does Google's Gemini Flash model achieve ultra-low latency and high token throughput?"
        if st.button("✍️  Write a creative cyberpunk story hook", use_container_width=True):
            st.session_state.starter_prompt = "Write an atmospheric opening scene for a neon-lit cyberpunk detective story."

# Display Previous Messages for active session
for message in active_session["messages"]:
    avatar = "👤" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        # If an image was uploaded with this message, display image preview
        if "image_bytes" in message and message["image_bytes"]:
            st.image(message["image_bytes"], width=320)
        st.markdown(message["content"])

# 📎 Clean Chat Input with Shortened Placeholder & Highlighted (+) Button
chat_input_response = st.chat_input(
    "Ask a question...",
    accept_file=True,
    file_type=["png", "jpg", "jpeg", "webp"]
)

# Handle starter prompt trigger
if "starter_prompt" in st.session_state and st.session_state.starter_prompt:
    chat_input_response = st.session_state.starter_prompt
    st.session_state.starter_prompt = None

if chat_input_response:
    # Handle both ChatInputValue object (with attached file) and plain string prompts
    if hasattr(chat_input_response, "text"):
        user_prompt = chat_input_response.text or "Describe this image in detail."
        attached_files = getattr(chat_input_response, "files", []) or []
    else:
        user_prompt = str(chat_input_response)
        attached_files = []

    # Extract image bytes if a file was attached inside the chat input bar
    img_bytes = None
    img_mime = None
    if attached_files and len(attached_files) > 0:
        first_file = attached_files[0]
        img_bytes = first_file.getvalue()
        img_mime = first_file.type

    # Auto-update session title based on first message
    if len(active_session["messages"]) == 0:
        active_session["title"] = (user_prompt[:25] + "...") if len(user_prompt) > 25 else user_prompt

    # Display user message immediately
    with st.chat_message("user", avatar="👤"):
        if img_bytes:
            st.image(img_bytes, width=320)
        st.markdown(user_prompt)
    
    # Save user message (with optional image) to history
    user_msg_entry = {
        "role": "user", 
        "content": user_prompt,
        "image_bytes": img_bytes,
        "image_mime": img_mime
    }
    active_session["messages"].append(user_msg_entry)

    # Build Gemini SDK contents list
    contents = []
    for msg in active_session["messages"]:
        role = "user" if msg["role"] == "user" else "model"
        parts = []
        
        # Attach image Part if this message had an image
        if msg.get("image_bytes"):
            parts.append(
                types.Part.from_bytes(
                    data=msg["image_bytes"],
                    mime_type=msg.get("image_mime", "image/jpeg")
                )
            )
        
        # Attach text Part
        parts.append(types.Part.from_text(text=msg["content"]))
        contents.append(types.Content(role=role, parts=parts))

    # Generate and stream response from Gemini
    with st.chat_message("assistant", avatar="✨"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # Stream response chunk-by-chunk
            response = client.models.generate_content_stream(
                model="gemini-3.6-flash",
                contents=contents
            )
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
            # Save assistant response to active session
            active_session["messages"].append({"role": "model", "content": full_response})

        except Exception as e:
            st.error(f"Error communicating with AI: {e}")
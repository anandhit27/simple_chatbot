import streamlit as st
import requests
import uuid
from datetime import datetime

# ================== CONFIG ==================

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Assistant Chatbot - Professional Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== CUSTOM CSS ==================

st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }

    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .sidebar-header h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
    }

    /* Thread buttons */
    .thread-button {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 0.4rem;
        margin: 0.15rem 0;
        width: 100%;
        text-align: left;
        transition: all 0.3s ease;
        font-size: 0.8rem;
        line-height: 1.2;
    }

    .thread-button:hover {
        background: #e3f2fd;
        border-color: #2196f3;
        transform: translateY(-1px);
    }

    .thread-button.active {
        background: #2196f3;
        color: white;
        border-color: #1976d2;
    }

    /* New thread button */
    .new-thread-btn {
        background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        width: 100%;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }

    .new-thread-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
    }

    /* Chat container */
    .chat-container {
        background: #ffffff;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        min-height: 400px;
    }

    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 5px 18px;
        margin: 0.5rem 0;
        max-width: 70%;
        float: right;
        clear: both;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .assistant-message {
        background: #f8f9fa;
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 5px;
        margin: 0.5rem 0;
        max-width: 70%;
        border-left: 4px solid #2196f3;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4caf50;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid #e9ecef;
        margin-top: 2rem;
    }

    /* Clear floats */
    .chat-messages::after {
        content: "";
        clear: both;
        display: table;
    }
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================

st.markdown("""
<div class="main-header">
    <h1>🤖 Assistant Chatbot</h1>
    <p>AI-powered conversational assistant with thread management</p>
</div>
""", unsafe_allow_html=True)

# ================== HELPERS ==================

def new_thread_id():
    return f"thread-{uuid.uuid4().hex[:8]}"

def get_threads():
    try:
        r = requests.get(f"{BASE_URL}/chat/threads", timeout=5)
        r.raise_for_status()
        return r.json()
    except:
        return []

def get_history(thread_id):
    try:
        r = requests.get(f"{BASE_URL}/chat/history/{thread_id}", timeout=5)
        r.raise_for_status()
        return r.json()["messages"]
    except:
        return []

# ================== SESSION STATE ==================

if "current_thread" not in st.session_state:
    st.session_state.current_thread = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ================== SIDEBAR ==================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3>💬 Conversation Threads</h3>
    </div>
    """, unsafe_allow_html=True)

    threads = get_threads()

    if not threads:
        st.info("📝 No conversations yet. Create your first thread!")

    else:
        st.markdown("### Active Threads")
        for tid in threads:
            is_active = tid == st.session_state.current_thread
            button_class = "thread-button active" if is_active else "thread-button"

            if st.button(
                f"{tid}",
                key=f"thread_{tid}",
                help=f"Switch to thread: {tid}"
            ):
                st.session_state.current_thread = tid
                st.session_state.messages = get_history(tid)
                st.rerun()

    st.markdown("---")

    if st.button("➕ Create New Thread", key="new_thread", help="Start a new conversation"):
        tid = new_thread_id()
        st.session_state.current_thread = tid
        st.session_state.messages = []
        st.rerun()

    # Status indicator
    st.markdown("---")
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center;">
        <div class="status-indicator"></div>
        <span style="color: #666; font-size: 0.9rem;">System Online</span>
    </div>
    """, unsafe_allow_html=True)

# ================== MAIN CHAT ==================

if not st.session_state.current_thread:
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h2 style="color: #666;">👋 Welcome to AI Assistant</h2>
        <p style="font-size: 1.1rem; color: #888;">Select a conversation thread from the sidebar or create a new one to get started.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Thread header
st.markdown(f"""
<div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 4px solid #2196f3;">
    <h3 style="margin: 0; color: #333;">📋 Thread: {st.session_state.current_thread}</h3>
    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">{len(st.session_state.messages)//2} messages • Last updated: {datetime.now().strftime('%H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

# Render chat history with professional styling
for msg in st.session_state.messages:
    role = msg.get("type")

    if role == "human":
        st.markdown(f"""
        <div class="user-message">
            <strong>You:</strong><br>{msg["content"]}
        </div>
        """, unsafe_allow_html=True)

    elif role == "ai":
        st.markdown(f"""
        <div class="assistant-message">
            <strong>🤖 AI Assistant:</strong><br>{msg["content"]}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ================== CHAT INPUT ==================

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

user_input = st.chat_input("💬 Type your message here...", key="chat_input")

if user_input:
    # ---- User message (optimistic render)
    st.session_state.messages.append({
        "type": "human",
        "content": user_input
    })

    st.markdown(f"""
    <div class="user-message">
        <strong>You:</strong><br>{user_input}
    </div>
    """, unsafe_allow_html=True)

    # ---- Assistant streaming with professional styling
    with st.container():
        st.markdown("""
        <div class="assistant-message" style="background: #e3f2fd; border-left-color: #2196f3;">
            <strong>🤖 AI Assistant:</strong><br>
        """, unsafe_allow_html=True)

        placeholder = st.empty()
        full_response = ""

        try:
            with requests.get(
                f"{BASE_URL}/chat/stream/{st.session_state.current_thread}",
                params={"message": user_input},
                stream=True,
                timeout=30
            ) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=None):
                    if not chunk:
                        continue
                    token = chunk.decode("utf-8")
                    full_response += token
                    placeholder.markdown(f"""
                    <div class="assistant-message" style="background: #e3f2fd; border-left-color: #2196f3;">
                        <strong>🤖 AI Assistant:</strong><br>{full_response}
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            placeholder.error(f"❌ Error: {str(e)}")
            full_response = f"I apologize, but I encountered an error: {str(e)}"

    # ---- Fetch fresh history from API to sync with backend
    try:
        st.session_state.messages = get_history(st.session_state.current_thread)
    except:
        # If API fails, keep the current messages
        pass

    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ================== FOOTER ==================

st.markdown("""
<div class="footer">
    <p>🚀 Powered by AI Assistant • Built with FastAPI & Streamlit</p>
</div>
""", unsafe_allow_html=True)

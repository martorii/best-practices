"""
Streamlit Frontend - Apple-style Chat Interface
"""

import json
from datetime import datetime

import requests
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apple-style CSS
st.markdown(
    """
<style>
    /* Import SF Pro font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        padding: 0;
    }

    /* Header */
    .header {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        padding: 20px 40px;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }

    .header h1 {
        font-size: 28px;
        font-weight: 600;
        color: #1d1d1f;
        margin: 0;
        letter-spacing: -0.5px;
    }

    /* Chat container */
    .chat-container {
        max-width: 900px;
        margin: 40px auto;
        padding: 0 20px;
        min-height: 60vh;
    }

    /* Message bubbles */
    .message {
        margin-bottom: 20px;
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .user-message {
        display: flex;
        justify-content: flex-end;
    }

    .assistant-message {
        display: flex;
        justify-content: flex-start;
    }

    .message-bubble {
        max-width: 70%;
        padding: 16px 20px;
        border-radius: 20px;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .user-bubble {
        background: #007AFF;
        color: white;
        border-bottom-right-radius: 4px;
    }

    .assistant-bubble {
        background: white;
        color: #1d1d1f;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(0, 0, 0, 0.06);
    }

    /* Tool usage indicators */
    .tool-indicator {
        display: inline-flex;
        align-items: center;
        background: rgba(0, 122, 255, 0.1);
        color: #007AFF;
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 13px;
        margin: 4px 0;
        font-weight: 500;
    }

    .tool-indicator:before {
        content: "🔧";
        margin-right: 6px;
    }

    /* Thinking indicator */
    .thinking {
        display: inline-flex;
        align-items: center;
        color: #86868b;
        font-size: 14px;
        font-style: italic;
        margin: 8px 0;
    }

    .thinking:before {
        content: "💭";
        margin-right: 8px;
    }

    /* Input area */
    .stTextInput {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid rgba(0, 0, 0, 0.08);
        padding: 20px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
    }

    .stTextInput > div > div > input {
        border-radius: 24px;
        border: 2px solid rgba(0, 0, 0, 0.1);
        padding: 14px 24px;
        font-size: 15px;
        transition: all 0.2s ease;
        background: white;
    }

    .stTextInput > div > div > input:focus {
        border-color: #007AFF;
        box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
        outline: none;
    }

    /* Button */
    .stButton > button {
        background: #007AFF;
        color: white;
        border: none;
        border-radius: 24px;
        padding: 12px 32px;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3);
    }

    .stButton > button:hover {
        background: #0051D5;
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.4);
        transform: translateY(-1px);
    }

    /* Sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Timestamp */
    .timestamp {
        font-size: 12px;
        color: #86868b;
        margin-top: 4px;
        text-align: right;
    }

    /* Loading dots */
    .loading-dots {
        display: inline-flex;
        gap: 4px;
    }

    .loading-dots span {
        width: 6px;
        height: 6px;
        background: #007AFF;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }

    .loading-dots span:nth-child(1) {
        animation-delay: -0.32s;
    }

    .loading-dots span:nth-child(2) {
        animation-delay: -0.16s;
    }

    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0);
        }
        40% {
            transform: scale(1);
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# Backend URL
BACKEND_URL = "http://backend:8000"


def format_message_html(message: dict) -> str:
    """Format message as HTML"""
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", "")

    if role == "user":
        return f"""
        <div class="message user-message">
            <div class="message-bubble user-bubble">
                {content}
                <div class="timestamp">{timestamp}</div>
            </div>
        </div>
        """
    else:
        # Check for tool indicators in metadata
        metadata = message.get("metadata", {})
        tools_used = metadata.get("tools_used", [])

        tools_html = ""
        if tools_used:
            tools_html = "<br>".join(
                [f'<div class="tool-indicator">{tool}</div>' for tool in tools_used]
            )

        return f"""
        <div class="message assistant-message">
            <div class="message-bubble assistant-bubble">
                {tools_html}
                {content}
                <div class="timestamp">{timestamp}</div>
            </div>
        </div>
        """


def stream_response(message: str):
    """Stream response from backend"""
    try:
        # Add user message
        timestamp = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append(
            {"role": "user", "content": message, "timestamp": timestamp}
        )

        # Create assistant message placeholder
        assistant_message = {
            "role": "assistant",
            "content": "",
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "metadata": {"tools_used": []},
        }
        st.session_state.messages.append(assistant_message)

        # Call backend
        response = requests.post(
            f"{BACKEND_URL}/chat", json={"message": message}, stream=True, timeout=60
        )

        current_content = ""
        tools_used = []

        # Process stream
        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = json.loads(line[6:])

                    if data["type"] == "tool_start":
                        tool_name = data.get("tool", "unknown")
                        tools_used.append(tool_name)
                        current_content += f"\n\n🔧 Using tool: **{tool_name}**\n"

                    elif data["type"] == "tool_end":
                        current_content += "\n✅ Tool completed\n"

                    elif data["type"] == "token":
                        current_content += data["content"]

                    elif data["type"] == "final_answer":
                        current_content = data["content"]

                    elif data["type"] == "error":
                        current_content = f"❌ Error: {data['content']}"

                    # Update message
                    st.session_state.messages[-1]["content"] = current_content
                    st.session_state.messages[-1]["metadata"]["tools_used"] = tools_used

    except Exception as e:
        st.session_state.messages[-1]["content"] = f"❌ Error: {e!s}"


# Header
st.markdown(
    """
<div class="header">
    <h1>🤖 AI Assistant</h1>
</div>
""",
    unsafe_allow_html=True,
)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display messages
for message in st.session_state.messages:
    st.markdown(format_message_html(message), unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input area
with st.container():
    col1, col2 = st.columns([6, 1])

    with col1:
        user_input = st.text_input(
            "Message",
            key="user_input",
            placeholder="Ask me anything...",
            label_visibility="collapsed",
        )

    with col2:
        send_button = st.button("Send", use_container_width=True)

# Handle send
if send_button and user_input and not st.session_state.is_processing:
    st.session_state.is_processing = True
    stream_response(user_input)
    st.session_state.is_processing = False
    st.rerun()

# Auto-scroll script
st.markdown(
    """
<script>
    window.scrollTo(0, document.body.scrollHeight);
</script>
""",
    unsafe_allow_html=True,
)

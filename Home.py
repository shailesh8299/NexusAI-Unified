import streamlit as st
import os
from dotenv import load_dotenv
from load_css import load_css, create_logo_html, create_tool_card

# 1. Load Environment Variables (The Security Step)
load_dotenv()

# 2. Page Configuration
st.set_page_config(page_title="NexusAI Unified", page_icon="🧠", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

# 3. Sidebar Logic
with st.sidebar:
    st.markdown(create_logo_html(), unsafe_allow_html=True)
    st.markdown("### 🔑 API Configuration")
    
    # --- GOOGLE KEY LOGIC ---
    # Check if key exists in .env
    env_google = os.getenv("GOOGLE_API_KEY")
    if env_google:
        st.session_state["GOOGLE_API_KEY"] = env_google
        st.success("Google Key Loaded from .env")
    else:
        # Fallback to manual input if .env is missing
        google_key = st.text_input("Google Gemini API Key", type="password")
        if google_key:
            st.session_state["GOOGLE_API_KEY"] = google_key
        
        st.markdown("""
        <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color: #22d3ee; font-size: 0.8rem; text-decoration: none;">
            
        </a>
        """, unsafe_allow_html=True)

    # --- SERPER KEY LOGIC ---
    env_serper = os.getenv("SERPER_API_KEY")
    if env_serper:
        st.session_state["SERPER_API_KEY"] = env_serper
        st.success("Serper Key Loaded from .env")
    else:
        serper_key = st.text_input("Serper API Key", type="password")
        if serper_key:
            st.session_state["SERPER_API_KEY"] = serper_key
            
        st.markdown("""
        <a href="https://serper.dev/" target="_blank" style="color: #22d3ee; font-size: 0.8rem; text-decoration: none;">
        👉 Get Serper Key
        </a>
        """, unsafe_allow_html=True)

# 4. Main Content Area
st.title("Welcome to NexusAI")
st.markdown("### Select a tool to get started")

col1, col2 = st.columns(2)

with col1:
    st.markdown(create_tool_card("⚡", "Super Summarizer", "Summarize Text, URLs, PDFs & News"), unsafe_allow_html=True)
    if st.button("Go to Summarizer", use_container_width=True):
        st.switch_page("pages/1_Super_Summarizer.py")

with col2:
    st.markdown(create_tool_card("💬", "Chat with PDF", "Deep dive Q&A with your documents"), unsafe_allow_html=True)
    if st.button("Go to Chat PDF", use_container_width=True):
        st.switch_page("pages/2_Chat_With_PDF.py")
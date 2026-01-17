import streamlit as st

def load_css():
    """
    Returns complete CSS styling that matches the React NexusAI UI.
    Includes fixes to hide the default Streamlit sidebar toggle.
    Call: st.markdown(load_css(), unsafe_allow_html=True)
    """
    return """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: hsl(280, 100%, 70%);
        --primary-glow: hsl(280, 100%, 80%);
        --secondary: hsl(200, 100%, 60%);
        --background: hsl(260, 30%, 6%);
        --card-bg: rgba(30, 25, 50, 0.6);
        --text-main: hsl(0, 0%, 98%);
        --text-muted: hsl(260, 10%, 60%);
        --border: rgba(139, 92, 246, 0.2);
    }

    /* GLOBAL STYLES */
    .stApp {
        background: linear-gradient(180deg, hsl(260, 30%, 6%) 0%, hsl(260, 25%, 4%) 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Animated Grid Background */
    .stApp::before {
        content: '';
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            linear-gradient(rgba(139, 92, 246, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(139, 92, 246, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }

    /* --- CRITICAL FIX: COMPLETELY REMOVE DEFAULT HEADER --- */
    [data-testid="stSidebarHeader"] {
        display: none !important;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 25, 50, 0.95) 0%, rgba(20, 15, 40, 0.98) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--border) !important;
        padding-top: 1rem; /* Add padding since we removed the header */
    }

    /* TYPOGRAPHY */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(135deg, hsl(280, 100%, 80%), hsl(200, 100%, 70%), hsl(320, 100%, 80%));
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    p, span, label, div, .stMarkdown p {
        color: var(--text-muted) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, hsl(280, 100%, 70%), hsl(320, 100%, 70%)) !important;
        border: none !important;
        border-radius: 0.75rem !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5) !important;
    }

    /* INPUTS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(20, 15, 40, 0.6) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-main) !important;
        border-radius: 0.75rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }
    
    /* CHAT MESSAGE */
    [data-testid="stChatMessage"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 1rem !important;
    }
    </style>
    """

def create_logo_html():
    return """
    <div style="display: flex; align-items: center; gap: 12px; padding: 1.5rem 0; margin-bottom: 1rem; border-bottom: 1px solid rgba(139, 92, 246, 0.2);">
        <div style="font-size: 2rem;">🧠</div>
        <div>
            <h1 style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">NexusAI</h1>
            <p style="font-size: 0.8rem; color: #94a3b8; margin: 0;">Unified Intelligence</p>
        </div>
    </div>
    """

def create_tool_card(icon, title, desc):
    return f"""
    <div style="background: rgba(30, 25, 50, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 1rem; padding: 1.5rem; margin-bottom: 1rem; transition: all 0.3s ease;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="margin: 0 0 0.5rem 0; font-family: 'Orbitron', sans-serif; font-size: 1.25rem; color: white;">{title}</h3>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">{desc}</p>
    </div>
    """
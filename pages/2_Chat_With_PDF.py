import streamlit as st
import tempfile
import os


import sys
#import os
sys.path.append(os.path.abspath('.')) # Ensures load_css can be imported from parent folder
from load_css import load_css, create_logo_html

# Apply Theme
st.markdown(load_css(), unsafe_allow_html=True)

# Sidebar Logo
with st.sidebar:
    st.markdown(create_logo_html(), unsafe_allow_html=True)



import json  # <--- NEW: Needed for saving history
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

# --- SAFE IMPORTS (Fixes for 2026 versions) ---
try:
    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain
except ImportError:
    try:
        from langchain.chains import create_retrieval_chain
        from langchain.chains.combine_documents import create_stuff_documents_chain
    except ImportError:
        st.error("CRITICAL ERROR: Please run 'pip install langchain-classic'")
        st.stop()

# --- CONFIGURATION ---
st.set_page_config(page_title="Chat PDF", page_icon="💬")
st.header("💬 Chat with your PDF (Persistent)")

# Define where to save the history locally
HISTORY_FILE = "chat_history.json"

# --- HELPER FUNCTIONS FOR SAVING/LOADING ---
def load_chat_history():
    """Loads chat history from local JSON file if it exists."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_chat_history(history):
    """Saves the current chat history to a local JSON file."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def clear_chat_history():
    """Deletes the local file and resets state."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.session_state.chat_history = []
    st.session_state.vector_store = None
    st.rerun()

# --- SIDEBAR: CLEAR HISTORY ---
with st.sidebar:
    if st.button("🗑️ Clear Chat History"):
        clear_chat_history()

# Check API Key
if "GOOGLE_API_KEY" not in st.session_state or not st.session_state.GOOGLE_API_KEY:
    st.error("⚠️ Please configure Google API Key in Settings.")
    st.stop()

# --- INITIALIZE STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()  # <--- LOAD FROM FILE

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    # Only process if we haven't already (or if the user uploaded a new file)
    if st.session_state.vector_store is None:
        with st.spinner("Processing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            try:
                loader = PyPDFLoader(tmp_path)
                docs = loader.load()
                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                splits = text_splitter.split_documents(docs)
                
                embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/text-embedding-004", 
                    google_api_key=st.session_state.GOOGLE_API_KEY
                )
                st.session_state.vector_store = FAISS.from_documents(splits, embeddings)
                st.success("PDF Ready!")
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

# --- DISPLAY CHAT HISTORY ---
# This ensures previous messages are shown immediately
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    with st.chat_message(role):
        st.write(content)

# --- CHAT INPUT ---
user_query = st.chat_input("Ask about the document...")

if user_query:
    if not st.session_state.vector_store:
        st.warning("Please upload a PDF first to enable the AI.")
    else:
        # 1. Show User Message
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        # 2. Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    llm = ChatGoogleGenerativeAI(
                        model="gemini-2.5-flash", 
                        temperature=0.3,
                        google_api_key=st.session_state.GOOGLE_API_KEY
                    )
                    retriever = st.session_state.vector_store.as_retriever()
                    
                    prompt = ChatPromptTemplate.from_template("""
                    Answer based on the context provided.
                    <context>
                    {context}
                    </context>
                    Question: {input}
                    """)
                    
                    document_chain = create_stuff_documents_chain(llm, prompt)
                    rag_chain = create_retrieval_chain(retriever, document_chain)
                    
                    response = rag_chain.invoke({"input": user_query})
                    answer = response["answer"]
                    
                    st.write(answer)
                    
                    # 3. SAVE TO HISTORY (Session + Local File)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    save_chat_history(st.session_state.chat_history)  # <--- SAVE TO FILE
                    
                except Exception as e:
                    st.error(f"Error: {e}")
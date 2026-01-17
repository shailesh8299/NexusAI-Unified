import streamlit as st
import validators
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



from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader, PyPDFLoader
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- FIX: Safe Import for Summarize Chain ---
try:
    # Try the new 2026 location first
    from langchain_classic.chains.summarize import load_summarize_chain
except ImportError:
    # Fallback to the old location
    from langchain.chains.summarize import load_summarize_chain

st.set_page_config(page_title="Super Summarizer", page_icon="⚡")
st.header("⚡ NexusAI Super Summarizer")

# 1. API Check
if "GOOGLE_API_KEY" not in st.session_state or not st.session_state.GOOGLE_API_KEY:
    st.error("⚠️ Please configure your Google API Key in Settings.")
    st.stop()

# 2. Input Selection
input_type = st.radio(
    "What do you want to summarize?",
    ["Website / YouTube URL", "Text / Article", "PDF Document", "Live News Topic"],
    horizontal=True
)

# 3. Dynamic Inputs
source_data = None
user_input = None

if input_type == "Website / YouTube URL":
    user_input = st.text_input("Enter URL (Article or YouTube Video)")
elif input_type == "Text / Article":
    user_input = st.text_area("Paste your text here", height=200)
elif input_type == "PDF Document":
    user_input = st.file_uploader("Upload PDF", type="pdf")
elif input_type == "Live News Topic":
    user_input = st.text_input("Enter a News Topic (e.g., 'Stock Market Today')")
    if "SERPER_API_KEY" not in st.session_state or not st.session_state.SERPER_API_KEY:
        st.warning("⚠️ You need a Serper API Key in Settings for News.")

# 4. Processing Logic
if st.button("Generate Summary") and user_input:
    try:
        with st.spinner(f"Processing {input_type}..."):
            docs = []
            
            # --- LOADER LOGIC ---
            if input_type == "Website / YouTube URL":
                if not validators.url(user_input):
                    st.error("Invalid URL")
                    st.stop()
                
                if "youtube.com" in user_input or "youtu.be" in user_input:
                    loader = YoutubeLoader.from_youtube_url(user_input, add_video_info=False)
                else:
                    loader = UnstructuredURLLoader(urls=[user_input], ssl_verify=False)
                docs = loader.load()

            elif input_type == "Text / Article":
                # Convert raw text to Document format
                from langchain_core.documents import Document
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000)
                texts = text_splitter.split_text(user_input)
                docs = [Document(page_content=t) for t in texts]

            elif input_type == "PDF Document":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(user_input.read())
                    tmp_path = tmp.name
                loader = PyPDFLoader(tmp_path)
                docs = loader.load()
                os.remove(tmp_path)

            elif input_type == "Live News Topic":
                search = GoogleSerperAPIWrapper(type="news", tbs="qdr:w1", serper_api_key=st.session_state.SERPER_API_KEY)
                results = search.results(user_input)
                if not results.get('news'):
                    st.error("No news found.")
                    st.stop()
                
                # Combine top 5 snippets into one text block
                combined_text = ""
                for item in results['news'][:5]:
                    combined_text += f"Title: {item['title']}\nSnippet: {item['snippet']}\nSource: {item['source']}\n\n"
                
                from langchain_core.documents import Document
                docs = [Document(page_content=combined_text)]

            # --- SUMMARIZATION LOGIC ---
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash", 
                temperature=0, 
                google_api_key=st.session_state.GOOGLE_API_KEY
            )

            # Use 'stuff' chain for speed (Gemini 2.5 has huge context window)
            prompt_template = """
            You are an expert summarizer. Write a comprehensive summary of the following content.
            Use bullet points for key insights and a bold title.
            
            Content:
            {text}
            
            Summary:
            """
            prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
            
            chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
            summary = chain.run(docs)

            st.success("Summary Generated Successfully!")
            st.markdown(summary)

    except Exception as e:
        st.error(f"An error occurred: {e}")
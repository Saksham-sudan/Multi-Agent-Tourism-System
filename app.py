import streamlit as st
import os
from dotenv import load_dotenv
from agents.langchain_agent import LangChainAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Tourism Assistant",
    page_icon="🌍",
    layout="centered"
)

# Title and description
st.title("🌍 AI Tourism Assistant")
st.markdown("Your intelligent travel companion powered by AI")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for agent
if "agent" not in st.session_state:
    try:
        st.session_state.agent = LangChainAgent()
    except ValueError as e:
        st.error(f"⚠️ {str(e)}")
        st.info("Please set your GITHUB_TOKEN in Streamlit Cloud secrets.")
        st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about weather, places to visit, or plan your trip..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.handle_request(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This AI Tourism Assistant can help you:
    - 🌤️ Check weather for any city
    - 🗺️ Discover tourist attractions
    - 📝 Plan your trips
    
    **Powered by:**
    - GPT-4o (GitHub Models)
    - Open-Meteo API
    - Overpass API
    - Nominatim API
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.agent = LangChainAgent()
        st.rerun()
    
    st.markdown("---")
    st.caption("Built with LangChain & Streamlit")

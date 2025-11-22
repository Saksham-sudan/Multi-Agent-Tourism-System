import streamlit as st
import os
from dotenv import load_dotenv
from agents.langchain_agent import LangChainAgent


load_dotenv()


st.set_page_config(
    page_title="AI Tourism Assistant",
    layout="centered"
)


st.title("AI Tourism Assistant")
st.markdown("Your intelligent travel companion powered by AI")


if "messages" not in st.session_state:
    st.session_state.messages = []


if "agent" not in st.session_state:
    try:
        st.session_state.agent = LangChainAgent()
    except ValueError as e:
        st.error(f"⚠️ {str(e)}")
        st.info("Please set your GITHUB_TOKEN in Streamlit Cloud secrets.")
        st.stop()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me about weather, places to visit, or plan your trip..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    

    with st.chat_message("user"):
        st.markdown(prompt)
    

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.handle_request(prompt)
        st.markdown(response)
    

    st.session_state.messages.append({"role": "assistant", "content": response})


with st.sidebar:
    st.header("About")
    st.markdown("""
    Created by Saksham Sudan
    USN-1CR22IS129
    for Inkle Assignment
    
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

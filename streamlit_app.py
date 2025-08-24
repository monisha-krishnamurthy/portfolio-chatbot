import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pypdf import PdfReader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity 
from database import get_answer, add_unknown_question, add_qa, get_session, add_session, save_unknown_question, increment_questions
import uuid

# Load environment variables (for local development)
load_dotenv(override=True)

# Configuration
ADMIN_SESSION_ID = "monisha_admin" 
MAX_QUESTIONS = 5

# Initialize OpenAI client - use Streamlit secrets if available, otherwise fall back to env vars
def get_openai_client():
    """Get OpenAI client with API key from Streamlit secrets or environment variables"""
    api_key = None
    
    # Try to get from Streamlit secrets first
    try:
        if hasattr(st, 'secrets') and st.secrets.get("OPENAI_API_KEY"):
            api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    
    # Fall back to environment variable
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("❌ OpenAI API key not found! Please set it in Streamlit Cloud secrets or as an environment variable.")
        st.stop()
    
    return OpenAI(api_key=api_key)

# Initialize OpenAI client
client = get_openai_client()

# Load embeddings and documents
def load_documents():
    """Load documents and embeddings for the chatbot"""
    try:
        with open("me/embeddings.json", "r") as f:
            embeddings_data = json.load(f)
        return embeddings_data
    except FileNotFoundError:
        st.warning("Warning: embeddings.json not found. Please ensure the file exists.")
        return {}

def load_summary():
    """Load the background summary"""
    try:
        with open("me/summary2.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        st.warning("Warning: summary2.txt not found. Please ensure the file exists.")
        return ""

# Load data
embeddings_data = load_documents()
background_summary = load_summary()

def chat(user_message, session_id):
    """Main chat function that handles user queries"""
    try:
        # Check question limit for non-admin users
        question_count = st.session_state.get("question_count", 0)
        if session_id != ADMIN_SESSION_ID and question_count >= MAX_QUESTIONS:
            return f"You've reached the limit of {MAX_QUESTIONS} questions for this session. Please contact me directly for more questions."
        
        # Check if we have a cached answer
        cached_answer = get_answer(user_message)
        if cached_answer:
            increment_questions(session_id)
            st.session_state.question_count += 1
            return cached_answer
        
        # Get relevant context from embeddings
        context = get_relevant_context(user_message)
        
        # Prepare the prompt
        system_prompt = f"""You are a helpful AI assistant that knows about my professional background. 
        
Background Information:
{background_summary}

Relevant Context:
{context}

Please answer questions about my resume, skills, experience, and career based on the information above. 
Be conversational, helpful, and accurate. If you don't know something, say so rather than making things up."""

        # Get response from OpenAI
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        # Cache the Q&A
        add_qa(user_message, answer)
        increment_questions(session_id)
        st.session_state.question_count += 1
        
        return answer
        
    except Exception as e:
        st.error(f"Error in chat: {e}")
        return "I apologize, but I encountered an error. Please try again."

def get_relevant_context(query):
    """Get relevant context from embeddings based on user query"""
    try:
        if not embeddings_data:
            return background_summary
        
        # For now, return the background summary since embeddings are just vectors
        # In a full implementation, you would use the embeddings for semantic search
        return background_summary
            
    except Exception as e:
        st.error(f"Error getting context: {e}")
        return background_summary

def push(text):
    """Send push notification (optional)"""
    try:
        # Try to get from Streamlit secrets first
        pushover_token = None
        pushover_user = None
        
        try:
            if hasattr(st, 'secrets'):
                pushover_token = st.secrets.get("PUSHOVER_TOKEN")
                pushover_user = st.secrets.get("PUSHOVER_USER")
        except:
            pass
        
        # Fall back to environment variables
        if not pushover_token:
            pushover_token = os.getenv("PUSHOVER_TOKEN")
        if not pushover_user:
            pushover_user = os.getenv("PUSHOVER_USER")
        
        if pushover_token and pushover_user:
            requests.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": pushover_token,
                    "user": pushover_user,
                    "message": text,
                }
            )
    except:
        pass  # Silently fail if push notifications aren't configured

# Streamlit interface
def main():
    st.set_page_config(
        page_title="Portfoilio Chatbot",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Portfoilio Chatbot")
    st.markdown("""
    Hi! I'm an AI assistant that knows all about my professional background, skills, experience, and career details. 
    Ask me anything about my resume, GitHub profile, or career journey!
    
    **Note:** Free users are limited to 5 questions per session. Contact me directly for unlimited access.
    """)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about my resume, skills, experience, or career..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            response = chat(prompt, st.session_state.session_id)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar with additional info
    with st.sidebar:
        st.header("Session Info")
        st.write(f"**Session ID:** {st.session_state.session_id[:8]}...")
        st.write(f"**Questions Asked:** {st.session_state.question_count}/{MAX_QUESTIONS}")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.question_count = 0
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This chatbot is powered by AI and built with Streamlit. 
        It knows about my professional background, skills, and experience!
        """)
        
        # Show remaining questions
        remaining = MAX_QUESTIONS - st.session_state.question_count
        if remaining > 0:
            st.info(f"🔄 {remaining} questions remaining in this session")
        else:
            st.warning("⚠️ Question limit reached for this session")

if __name__ == "__main__":
    main()

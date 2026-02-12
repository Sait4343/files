"""GPT-Visibility chat module."""
import streamlit as st
from core import SessionStateManager
from utils.api_clients import get_n8n_client

def show_chat_page():
    """Display chat page."""
    st.title("🤖 GPT-Visibility Assistant")
    project = SessionStateManager.get_current_project()
    if not project:
        st.warning("Проект не обрано")
        return
    
    messages = SessionStateManager.get_chat_messages()
    if not messages:
        SessionStateManager.add_chat_message("assistant", f"Вітаю! Я готовий відповісти на питання про {project['brand_name']}")
    
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Ваше питання..."):
        SessionStateManager.add_chat_message("user", prompt)
        
        client = get_n8n_client()
        response = client.chat_query(prompt, {
            "project_id": project["id"],
            "brand": project["brand_name"]
        })
        
        if response:
            SessionStateManager.add_chat_message("assistant", response)
        
        st.rerun()

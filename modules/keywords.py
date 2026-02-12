"""Keywords management module."""
import streamlit as st
from core import SessionStateManager
from core.database import get_database
from utils.api_clients import get_n8n_client

def show_keywords_page():
    """Display keywords management page."""
    st.title("🔍 Перелік запитів")
    project = SessionStateManager.get_current_project()
    if not project:
        st.warning("Проект не обрано")
        return
    
    db = get_database()
    keywords = db.get_keywords(project["id"])
    
    tab1, tab2 = st.tabs(["Список запитів", "Додати запити"])
    
    with tab1:
        if keywords:
            st.dataframe(keywords, use_container_width=True)
        else:
            st.info("Запитів ще немає")
    
    with tab2:
        with st.form("add_keywords"):
            st.markdown("### Генерація запитів через AI")
            products = st.text_area("Опишіть ваші продукти/послуги")
            submit = st.form_submit_button("Згенерувати")
            
            if submit and products:
                client = get_n8n_client()
                prompts = client.generate_prompts(
                    project["brand_name"],
                    project["domain"],
                    project.get("industry", ""),
                    products
                )
                
                if prompts:
                    st.success(f"Згенеровано {len(prompts)} запитів!")
                    keywords_data = [
                        {"project_id": project["id"], "keyword": p, "status": "active"}
                        for p in prompts
                    ]
                    db.create_keywords_batch(keywords_data)
                    st.rerun()

"""Sources management module."""
import streamlit as st
from core import SessionStateManager
from core.database import get_database

def show_sources_page():
    """Display sources management page."""
    st.title("🔗 Офіційні джерела")
    project = SessionStateManager.get_current_project()
    if not project:
        st.warning("Проект не обрано")
        return
    
    db = get_database()
    sources = db.get_sources(project["id"])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Список джерел")
        if sources:
            for source in sources:
                with st.expander(source.get("url", "Unknown")):
                    st.write(f"**Тип:** {source.get('type', 'N/A')}")
                    if st.button("Видалити", key=f"del_{source['id']}"):
                        db.delete_source(source["id"])
                        st.rerun()
        else:
            st.info("Джерел ще немає")
    
    with col2:
        st.markdown("### Додати джерело")
        with st.form("add_source"):
            url = st.text_input("URL")
            source_type = st.selectbox("Тип", ["website", "blog", "social", "documentation"])
            submit = st.form_submit_button("Додати")
            
            if submit and url:
                db.create_source({
                    "project_id": project["id"],
                    "url": url,
                    "type": source_type
                })
                st.success("Джерело додано!")
                st.rerun()

"""Projects management module."""
import streamlit as st
from core import SessionStateManager
from core.database import get_database

def show_my_projects_page():
    """Display projects management page."""
    st.title("📁 Мої проекти")
    
    user_id = SessionStateManager.get_user_id()
    db = get_database()
    projects = db.get_projects(user_id)
    
    tab1, tab2 = st.tabs(["Мої проекти", "Створити проект"])
    
    with tab1:
        if projects:
            for proj in projects:
                with st.expander(f"📁 {proj.get('brand_name')}"):
                    st.write(f"**Домен:** {proj.get('domain')}")
                    st.write(f"**Статус:** {proj.get('status')}")
                    if st.button("Обрати", key=f"select_{proj['id']}"):
                        SessionStateManager.update_project(proj)
                        st.success("Проект обрано!")
                        st.rerun()
        else:
            st.info("У вас ще немає проектів")
    
    with tab2:
        with st.form("create_project"):
            brand = st.text_input("Назва бренду")
            domain = st.text_input("Домен (example.com)")
            industry = st.text_input("Галузь")
            region = st.selectbox("Регіон", ["Україна", "США", "Європа", "Global"])
            description = st.text_area("Опис продуктів/послуг", height=100)
            
            submit = st.form_submit_button("Створити")
            
            if submit and brand and domain:
                project = db.create_project({
                    "user_id": user_id,
                    "brand_name": brand,
                    "domain": domain,
                    "industry": industry,
                    "region": region,
                    "description": description,
                    "status": "trial"
                })
                if project:
                    st.success("Проект створено!")
                    SessionStateManager.update_project(project)
                    st.rerun()

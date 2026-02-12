# AI Visibility Dashboard by Virshi

Production-ready Streamlit application for AI visibility monitoring and brand analysis.

## 📁 Project Structure

```
visibility_app/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── secrets.toml           # Supabase credentials (not in repo)
├── core/
│   ├── __init__.py
│   ├── auth.py                # Authentication & session management
│   ├── database.py            # Supabase client (Singleton pattern)
│   ├── config.py              # Configuration, constants, CSS styles
│   └── state.py               # Session state manager
├── modules/
│   ├── __init__.py
│   ├── dashboard.py           # Main dashboard page
│   ├── keywords.py            # Keywords management
│   ├── sources.py             # Sources page
│   ├── competitors.py         # Competitors analysis
│   ├── recommendations.py     # AI recommendations
│   ├── history.py             # Scan history
│   ├── reports.py             # Reports generation
│   ├── projects.py            # Project management
│   ├── chat.py                # GPT-Visibility chat
│   ├── faq.py                 # FAQ page
│   └── admin.py               # Admin panel
└── utils/
    ├── __init__.py
    ├── api_clients.py         # N8N webhook clients
    ├── helpers.py             # Helper functions
    └── charts.py              # Chart generation utilities
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure secrets:**
   Create `.streamlit/secrets.toml`:
   ```toml
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_key"
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🏗️ Architecture

- **Singleton Pattern**: Database connection uses singleton to prevent multiple connections
- **Type Hints**: Full typing support for better IDE integration
- **Error Handling**: Comprehensive try-catch blocks with user-friendly messages
- **Caching**: Strategic use of `@st.cache_data` and `@st.cache_resource`
- **Modular Design**: Clear separation of concerns across modules
- **Security**: All sensitive data via `st.secrets`, no hardcoded credentials

## 📝 Key Features

- Multi-project management
- Real-time AI visibility tracking
- Competitor analysis
- Source monitoring
- Automated recommendations
- Historical data analysis
- Interactive dashboards
- Admin panel for super users

## 🔒 Security

- Session-based authentication
- Cookie management with secure tokens
- Role-based access control (user, admin, super_admin)
- Input validation and sanitization
- API authorization headers

## 🛠️ Development

- Follow PEP 8 style guide
- Use type hints for all functions
- Document functions with docstrings
- Test database queries before deployment
- Use `st.fragment` for dynamic components

## 📧 Support

For issues or questions, contact: hi@virshi.ai

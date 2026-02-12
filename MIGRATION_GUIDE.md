# Migration Guide: From Monolith to Modular

## Overview

This guide explains how to migrate from the original monolithic `visibility_app.py` (6825 lines) to the new modular structure.

## What Changed?

### File Structure

**Before:**
```
visibility_app.py (6825 lines)
```

**After:**
```
visibility_app/
├── app.py (main entry)
├── core/ (infrastructure)
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   └── state.py
├── modules/ (pages)
│   ├── dashboard.py
│   ├── keywords.py
│   ├── sources.py
│   └── ... (10 more modules)
└── utils/ (helpers)
    ├── api_clients.py
    ├── charts.py
    └── helpers.py
```

## Key Improvements

### 1. Database Connection

**Before:**
```python
# Multiple connections created
supabase = create_client(URL, KEY)
# Used directly everywhere
```

**After:**
```python
# Singleton pattern
db = get_database()  # Always returns same instance
db.get_projects(user_id)  # Type-safe methods
```

### 2. Session State

**Before:**
```python
# Scattered initialization
if "user" not in st.session_state:
    st.session_state["user"] = None
# Direct access everywhere
```

**After:**
```python
# Centralized manager
SessionStateManager.initialize()
user = SessionStateManager.get("user")
SessionStateManager.is_authenticated()
```

### 3. API Calls

**Before:**
```python
# Inline requests
response = requests.post(N8N_URL, json=payload, headers=headers)
if response.status_code == 200:
    data = response.json()
```

**After:**
```python
# Client with retry logic
client = get_n8n_client()
data = client.generate_prompts(brand, domain, industry, products)
# Automatic error handling and retries
```

### 4. Configuration

**Before:**
```python
# Hardcoded values
N8N_GEN_URL = "https://..."
# Inline CSS (117 lines)
st.markdown("""<style>...</style>""")
```

**After:**
```python
# Config module
from core import Config
Config.apply_custom_css()
N8N_URLS["generate_prompts"]
```

## Migration Steps

### Step 1: Set Up New Structure

1. Create project directory:
   ```bash
   mkdir visibility_app
   cd visibility_app
   ```

2. Copy all files from the refactored version

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Configure Secrets

1. Copy secrets template:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Fill in your Supabase credentials:
   ```toml
   SUPABASE_URL = "your_url"
   SUPABASE_KEY = "your_key"
   ```

### Step 3: Database Tables

Ensure these tables exist in Supabase:

1. **profiles**
   ```sql
   CREATE TABLE profiles (
     id UUID PRIMARY KEY,
     email TEXT,
     name TEXT,
     role TEXT DEFAULT 'user'
   );
   ```

2. **projects**
   ```sql
   CREATE TABLE projects (
     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
     user_id UUID REFERENCES profiles(id),
     brand_name TEXT,
     domain TEXT,
     industry TEXT,
     status TEXT DEFAULT 'trial',
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

3. **keywords**
   ```sql
   CREATE TABLE keywords (
     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
     project_id UUID REFERENCES projects(id),
     keyword TEXT,
     status TEXT DEFAULT 'active',
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

4. **official_sources**
   ```sql
   CREATE TABLE official_sources (
     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
     project_id UUID REFERENCES projects(id),
     url TEXT,
     type TEXT,
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

5. **scan_results**
   ```sql
   CREATE TABLE scan_results (
     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
     project_id UUID REFERENCES projects(id),
     keyword_id UUID REFERENCES keywords(id),
     response TEXT,
     sentiment TEXT,
     mentioned BOOLEAN,
     position INTEGER,
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

### Step 4: Test Locally

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Test each module:
   - [ ] Authentication (login/register)
   - [ ] Project creation
   - [ ] Keyword generation
   - [ ] Sources management
   - [ ] Dashboard metrics
   - [ ] Chat interface

### Step 5: Deploy

Follow instructions in `DEPLOYMENT.md`

## Feature Mapping

### Authentication

**Before**: `show_auth_page()` function
**After**: `core/auth.py` module
- `check_session()`
- `logout()`
- `show_auth_page()`

### Dashboard

**Before**: `show_dashboard()` function
**After**: `modules/dashboard.py`
- Separated metrics calculation
- Reusable chart functions
- Type-safe data handling

### Keywords

**Before**: `show_keywords_page()` function
**After**: `modules/keywords.py`
- AI generation via N8NClient
- Batch operations
- Better error handling

### API Calls

**Before**: Inline requests with basic error handling
**After**: `utils/api_clients.py`
- N8NClient class
- Retry logic
- Comprehensive error handling
- Timeout management

## Troubleshooting

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'core'`

**Solution**:
```bash
# Ensure you're in project root
cd visibility_app
python -m streamlit run app.py
```

### Database Connection

**Error**: `Database connection failed`

**Solution**:
1. Check `.streamlit/secrets.toml` exists
2. Verify Supabase credentials
3. Test connection in Supabase dashboard

### Session State

**Error**: `KeyError: 'user'`

**Solution**:
```python
# Always initialize first
SessionStateManager.initialize()
```

### N8N API

**Error**: `403 Forbidden`

**Solution**:
1. Check N8N_AUTH_HEADER in `core/config.py`
2. Verify webhook URLs are correct
3. Test webhook in N8N dashboard

## Best Practices

### 1. Always Use Managers

**Don't**:
```python
st.session_state["user"] = user
response = requests.post(url, json=data)
```

**Do**:
```python
SessionStateManager.update_user(user, role)
client = get_n8n_client()
response = client.generate_prompts(...)
```

### 2. Handle Errors

**Don't**:
```python
data = db.get_projects(user_id)
```

**Do**:
```python
try:
    data = db.get_projects(user_id)
    if not data:
        st.info("No projects found")
except Exception as e:
    logger.error(f"Failed: {e}")
    st.error("Failed to load projects")
```

### 3. Use Type Hints

**Don't**:
```python
def get_data(id):
    return db.query(id)
```

**Do**:
```python
def get_data(id: str) -> Optional[Dict[str, Any]]:
    return db.query(id)
```

## Rolling Back

If you need to revert to the original:

1. Keep a backup of `visibility_app.py`
2. Note any data migrations needed
3. Document custom changes

## Support

For issues:
1. Check logs: `streamlit run app.py --logger.level=debug`
2. Review error messages
3. Contact: hi@virshi.ai

## Next Steps

After migration:
1. Test all features thoroughly
2. Monitor performance
3. Gather user feedback
4. Plan enhancements

## Checklist

- [ ] New structure set up
- [ ] Dependencies installed
- [ ] Secrets configured
- [ ] Database tables created
- [ ] Local testing passed
- [ ] Production deployed
- [ ] Monitoring configured
- [ ] Documentation updated

# Usage Guide - Complete Examples

## 🌍 Multi-Language (i18n) Usage

### Changing Language

The app supports Ukrainian (default) and English. Users can switch languages via:

1. **Sidebar selector**:
   - Look for 🌐 icon in sidebar
   - Select desired language
   - App instantly reloads in new language

2. **Programmatic**:
   ```python
   from core import I18n
   
   # Set language
   I18n.set_language('en')  # or 'uk'
   
   # Get current language
   current = I18n.get_current_language()
   ```

### Using Translations in Code

```python
from core import t

# Simple translation
title = t('dashboard.title')  # Returns: "Dashboard" or "Дашборд"

# With parameters
message = t('auth.login_success', email="user@example.com")
# Returns: "Welcome, user@example.com!" or "Вітаємо, user@example.com!"

# In Streamlit
st.title(t('menu.keywords'))
st.button(t('common.save'))
```

### Adding New Language

1. Create new JSON file in `locales/` (e.g., `de.json`):
```json
{
  "app": {
    "title": "AI Visibility by Virshi",
    "tagline": "Überwachen Sie die Präsenz Ihrer Marke in KI-Modellen"
  },
  "menu": {
    "dashboard": "Armaturenbrett"
  }
}
```

2. Register language:
```python
from core import I18n

I18n.add_language('de', 'Deutsch', translations_dict)
```

### Editing Translations

Simply edit the JSON files in `locales/` folder:
- `uk.json` - Ukrainian
- `en.json` - English

No code changes needed! Changes take effect on reload.

## 💳 Billing System Usage

### Checking Plan & Limits

```python
from core import BillingManager

# Get usage stats
stats = BillingManager.get_usage_stats(project_id)

print(f"Plan: {stats['plan_name']}")
print(f"Used: {stats['scans_used']}/{stats['scans_limit']}")
print(f"Remaining: {stats['scans_remaining']}")
```

### Before Running Analysis

```python
# Check if user can scan
can_scan, error = BillingManager.check_scan_limit(project_id, num_scans=5)

if can_scan:
    # Proceed with analysis
    run_analysis()
else:
    st.error(error)
    st.info("Please upgrade your plan")
```

### Recording Scans

```python
# After successful scan
BillingManager.record_scan(project_id, keyword_id, "perplexity")
```

### Upgrading Plan

```python
# Upgrade to professional
success = BillingManager.upgrade_plan(project_id, "professional")

if success:
    st.success("Upgraded to Professional!")
    st.rerun()
```

### Displaying Billing Info

```python
from core import show_billing_info

# In any module
show_billing_info(project_id)
```

## 🎨 Using Unified Styles

### Applying Styles

```python
from core import Styles

# Apply all styles (done automatically in app.py)
Styles.apply()
```

### Using Color Palette

```python
# Access colors
primary = Styles.COLORS['primary']  # "#8041F6"
success = Styles.COLORS['success']  # "#00C896"

# In custom HTML
st.markdown(
    f"<div style='color: {Styles.COLORS['primary']}'>Styled Text</div>",
    unsafe_allow_html=True
)
```

### Creating Badges

```python
# Status badge
badge_html = Styles.get_badge_html('trial', 'TRIAL')
st.markdown(badge_html, unsafe_allow_html=True)

# Custom badge
badge_html = Styles.get_badge_html('active', 'ACTIVE')
```

### Creating Metric Cards

```python
# Metric card
card_html = Styles.get_metric_card_html(
    label="Total Scans",
    value="147",
    icon="📊"
)
st.markdown(card_html, unsafe_allow_html=True)
```

## 📊 Dashboard Example

```python
from core import t, SessionStateManager
from utils import get_donut_chart

def show_my_dashboard():
    st.title(t('dashboard.title'))
    
    project = SessionStateManager.get_current_project()
    
    # Show metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=t('dashboard.sov'),
            value="67.5%",
            delta="+2.1%"
        )
    
    with col2:
        # Donut chart
        fig = get_donut_chart(75, color=Styles.COLORS['success'])
        st.plotly_chart(fig)
    
    with col3:
        # Show billing info
        from core import show_billing_info
        show_billing_info(project['id'])
```

## 🔍 Keywords with Billing Check

```python
from core import t, BillingManager
from utils.api_clients import get_n8n_client

def run_analysis_with_limit_check(project_id, keywords, models):
    # Check limit first
    can_scan, error = BillingManager.check_scan_limit(
        project_id,
        num_scans=len(keywords) * len(models)
    )
    
    if not can_scan:
        st.error(error)
        # Show upgrade options
        from core import show_plan_comparison
        show_plan_comparison()
        return
    
    # Proceed with analysis
    client = get_n8n_client()
    result = client.run_analysis(project_id, keywords, models)
    
    if result:
        st.success(t('keywords.analysis_started'))
        
        # Record scans for billing
        for kw in keywords:
            for model in models:
                BillingManager.record_scan(project_id, kw['id'], model)
```

## 💬 Chat with i18n

```python
from core import t, SessionStateManager

def show_multilingual_chat():
    st.title(t('chat.title'))
    
    project = SessionStateManager.get_current_project()
    
    # Welcome message
    welcome = t('chat.welcome', brand=project['brand_name'])
    
    # Chat interface
    if prompt := st.chat_input(t('chat.placeholder')):
        # Process message
        with st.spinner(t('chat.typing')):
            response = process_chat(prompt)
            st.chat_message("assistant").write(response)
```

## 🗃️ Database Operations

```python
from core import get_database

db = get_database()

# Get projects with error handling
try:
    projects = db.get_projects(user_id)
    if not projects:
        st.info(t('projects.no_projects'))
except Exception as e:
    st.error(t('errors.database'))
    logger.error(f"Database error: {e}")
```

## 🔐 Authentication with i18n

```python
from core import t

def show_login_form():
    st.markdown(f"### {t('auth.login_title')}")
    
    with st.form("login"):
        email = st.text_input(t('auth.email'))
        password = st.text_input(t('auth.password'), type="password")
        
        if st.form_submit_button(t('auth.login_button')):
            user = login_user(email, password)
            
            if user:
                st.success(t('auth.login_success', email=email))
            else:
                st.error(t('auth.login_error'))
```

## 🎨 Custom Styles Example

```python
from core import Styles

# Create custom metric card
def show_custom_metric(label, value, icon="📊"):
    html = f"""
    <div style="
        background-color: {Styles.COLORS['white']};
        border: 1px solid {Styles.COLORS['border']};
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    ">
        <div style="
            font-size: 12px;
            color: {Styles.COLORS['text_secondary']};
        ">{icon} {label}</div>
        <div style="
            font-size: 24px;
            font-weight: bold;
            color: {Styles.COLORS['primary']};
            margin-top: 10px;
        ">{value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
```

## 📱 Complete Example: Multi-Language Dashboard with Billing

```python
import streamlit as st
from core import (
    t, Styles, SessionStateManager, BillingManager,
    show_billing_info
)
from utils import get_donut_chart

def complete_dashboard():
    """Complete dashboard with i18n, billing, and styles."""
    
    # Apply styles
    Styles.apply()
    
    # Title
    st.title(t('dashboard.title'))
    
    # Get project
    project = SessionStateManager.get_current_project()
    
    if not project:
        st.warning(t('dashboard.no_project'))
        return
    
    # Show billing summary at top
    st.markdown(f"### {t('billing.title')}")
    show_billing_info(project['id'])
    
    st.markdown("---")
    
    # Key metrics
    st.markdown(f"### {t('dashboard.key_metrics')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=t('dashboard.sov'),
            value="67.5%",
            delta="+2.1%"
        )
        st.caption(t('tooltips.sov'))
    
    with col2:
        fig = get_donut_chart(75, Styles.COLORS['success'])
        st.plotly_chart(fig, use_container_width=True)
        st.caption(t('dashboard.presence'))
    
    with col3:
        st.metric(
            label=t('dashboard.avg_position'),
            value="2.3",
            delta="-0.2"
        )
        st.caption(t('tooltips.position'))
    
    with col4:
        # Show plan badge
        plan = project.get('status', 'trial')
        badge = Styles.get_badge_html(plan, plan.upper())
        st.markdown(badge, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("---")
    st.markdown(f"### {t('dashboard.quick_actions')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🔍 {t('dashboard.run_analysis')}", use_container_width=True):
            # Check billing first
            can_scan, error = BillingManager.check_scan_limit(project['id'])
            if can_scan:
                st.switch_page("modules/keywords.py")
            else:
                st.error(error)
    
    with col2:
        if st.button(f"📝 {t('dashboard.add_keywords')}", use_container_width=True):
            st.switch_page("modules/keywords.py")
    
    with col3:
        if st.button(f"📊 {t('dashboard.view_reports')}", use_container_width=True):
            st.switch_page("modules/reports.py")
```

## 🔄 Language Switching Example

```python
def language_switch_demo():
    """Demo of language switching."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🇺🇦 Українська"):
            I18n.set_language('uk')
            st.rerun()
    
    with col2:
        if st.button("🇬🇧 English"):
            I18n.set_language('en')
            st.rerun()
    
    # Show current language
    current = I18n.get_current_language()
    st.info(f"Current language: {current}")
    
    # Show translated text
    st.write(t('app.title'))
    st.write(t('app.tagline'))
```

## 🎯 Best Practices

### 1. Always Check Billing Before Operations
```python
# ✅ Good
can_scan, error = BillingManager.check_scan_limit(project_id, 5)
if can_scan:
    run_analysis()
else:
    st.error(error)

# ❌ Bad
run_analysis()  # No billing check
```

### 2. Use Translations Everywhere
```python
# ✅ Good
st.title(t('dashboard.title'))
st.button(t('common.save'))

# ❌ Bad
st.title("Dashboard")  # Hardcoded
st.button("Save")  # Hardcoded
```

### 3. Use Unified Styles
```python
# ✅ Good
badge = Styles.get_badge_html('trial')
st.markdown(badge, unsafe_allow_html=True)

# ❌ Bad
st.markdown('<span style="color: red;">TRIAL</span>')  # Inconsistent
```

### 4. Handle Errors Gracefully
```python
# ✅ Good
try:
    result = db.get_projects(user_id)
except Exception as e:
    st.error(t('errors.database'))
    logger.error(f"Error: {e}")

# ❌ Bad
result = db.get_projects(user_id)  # No error handling
```

---

**For more examples, see the code in `modules/` directory.**

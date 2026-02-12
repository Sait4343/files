# Architecture Documentation

## Overview

This is a production-ready Streamlit application for AI visibility monitoring, refactored from a monolithic 6800+ line file into a modular, maintainable architecture.

## Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Singleton Pattern**: Database connection uses singleton to prevent multiple connections
3. **Type Safety**: Full type hints for better IDE support and error prevention
4. **Error Handling**: Comprehensive try-catch blocks with user-friendly messages
5. **Caching**: Strategic use of Streamlit caching for performance
6. **Security**: All secrets via st.secrets, no hardcoded credentials

## Architecture Layers

### 1. Core Layer (`core/`)

**Purpose**: Fundamental application infrastructure

- `config.py`: Application configuration, constants
- `styles.py`: CSS styles and UI theming
- `auth.py`: Authentication logic, session management, decorators
- `database.py`: Supabase client (Singleton), CRUD operations
- `state.py`: Centralized session state management
- `i18n.py`: Internationalization and translation support
- `billing.py`: Billing logic and subscription management

**Key Features**:
- Singleton database connection prevents memory leaks
- Type-safe session state access
- Decorator-based auth requirements
- Comprehensive error logging

### 2. Utilities Layer (`utils/`)

**Purpose**: Reusable helper functions

- `api_clients.py`: N8N webhook clients with retry logic
- `helpers.py`: Data formatting, validation, sanitization
- `charts.py`: Plotly chart generation utilities

**Key Features**:
- Retry logic for API calls
- Input validation and sanitization
- Flexible chart generation
- Error handling with user feedback

### 3. Modules Layer (`modules/`)

**Purpose**: Individual page implementations

- `dashboard.py`: Main overview with key metrics
- `keywords.py`: Keyword management and AI generation
- `sources.py`: Official sources management
- `competitors.py`: Competitor analysis
- `recommendations.py`: AI-powered recommendations
- `history.py`: Scan history display
- `reports.py`: Report generation
- `projects.py`: Project CRUD operations
- `chat.py`: GPT-Visibility chat interface
- `faq.py`: FAQ page
- `admin.py`: Admin panel (role-restricted)
- `billing.py`: Billing and subscription page

**Key Features**:
- Each module is independent
- Consistent error handling
- User-friendly interfaces
- Role-based access control

### 4. Application Layer (`app.py`)

**Purpose**: Main entry point and routing

**Responsibilities**:
- Initialize configuration
- Handle authentication flow
- Route to appropriate pages
- Render sidebar navigation

## Data Flow

```
User Request → app.py → Authentication Check → Route to Module
                ↓
        Session State Manager
                ↓
        Database Layer (Singleton)
                ↓
        Supabase / N8N APIs
```

## Session Management

**SessionStateManager** provides:
- Centralized state initialization
- Type-safe state access
- User authentication state
- Project context
- Chat history

**Benefits**:
- No duplicate state keys
- Consistent state access
- Easy to extend
- Memory efficient

## Database Pattern

**Singleton Pattern** ensures:
- Single connection per session
- No connection pooling issues
- Reduced memory footprint
- Consistent connection state

**Methods**:
- Authentication: `sign_in()`, `sign_up()`, `sign_out()`
- Projects: `get_projects()`, `create_project()`, `update_project()`
- Keywords: `get_keywords()`, `create_keywords_batch()`
- Generic: `execute_query()` for custom queries

## API Client Pattern

**N8NClient** handles:
- Request retries (up to 3 attempts)
- Timeout management
- Error classification
- Response parsing

**Workflow**:
1. Build payload
2. Add auth headers
3. Make request with timeout
4. Handle response/errors
5. Retry on server errors
6. Return parsed data

## Error Handling Strategy

**Levels**:
1. **Try-Catch**: All database and API operations
2. **Logging**: Errors logged with context
3. **User Feedback**: st.error() for user-facing errors
4. **Graceful Degradation**: Return None/[] on failure

**Example**:
```python
try:
    result = db.get_projects(user_id)
except Exception as e:
    logger.error(f"Failed to fetch projects: {e}")
    st.error("Не вдалося завантажити проекти")
    return []
```

## Security Features

1. **Secrets Management**: All credentials via st.secrets
2. **Authentication**: Session-based with cookie support
3. **Role-Based Access**: Decorators for admin functions
4. **Input Validation**: All user inputs validated
5. **SQL Injection Prevention**: Parameterized queries

## Performance Optimizations

1. **Caching**:
   - Database connection: `@st.cache_resource`
   - Static data: `@st.cache_data`

2. **Query Optimization**:
   - Limit result sets
   - Use indexes
   - Batch operations

3. **UI Optimization**:
   - Use `st.fragment` for dynamic components
   - Lazy load data
   - Progressive rendering

## Testing Strategy

**Recommended Tests**:

1. **Unit Tests**:
   - Helper functions
   - Data validation
   - Chart generation

2. **Integration Tests**:
   - Database operations
   - API client calls
   - Authentication flow

3. **E2E Tests**:
   - User workflows
   - Page navigation
   - Form submissions

## Deployment Considerations

**Pre-Deployment Checklist**:
- [ ] All secrets configured
- [ ] Database tables created
- [ ] API endpoints accessible
- [ ] Error logging configured
- [ ] Performance tested
- [ ] Security audit completed

**Monitoring**:
- Application logs
- Database performance
- API response times
- Error rates

## Extending the Application

**Adding a New Page**:

1. Create module in `modules/`:
   ```python
   # modules/new_page.py
   def show_new_page():
       st.title("New Page")
       # Implementation
   ```

2. Register in `modules/__init__.py`:
   ```python
   from .new_page import show_new_page
   __all__ = [..., 'show_new_page']
   ```

3. Add to routing in `app.py`:
   ```python
   routing_map = {
       "New Page": show_new_page,
       # ...
   }
   ```

**Adding a New Database Table**:

1. Create table in Supabase
2. Add methods in `core/database.py`:
   ```python
   def get_items(self, filter_id: str):
       # Implementation
   ```

**Adding a New API Endpoint**:

1. Add URL to `core/config.py`:
   ```python
   N8N_URLS = {
       "new_endpoint": "https://..."
   }
   ```

2. Add method in `utils/api_clients.py`:
   ```python
   def new_operation(self, params):
       # Implementation
   ```

## Migration from Monolith

**Key Changes**:
1. ✅ Single file → Modular structure
2. ✅ Global variables → Session state manager
3. ✅ Inline CSS → Config module
4. ✅ Repeated code → Utility functions
5. ✅ No types → Full type hints
6. ✅ Basic errors → Comprehensive handling
7. ✅ Multiple DB connections → Singleton
8. ✅ Hardcoded values → Configuration

## Maintenance Guidelines

**Code Style**:
- Follow PEP 8
- Use type hints
- Document with docstrings
- Keep functions small (<50 lines)

**Git Workflow**:
- Feature branches
- Descriptive commits
- Code reviews
- CI/CD pipeline

**Version Control**:
- Semantic versioning
- Changelog maintenance
- Tag releases

## Future Enhancements

**Potential Features**:
1. User preferences storage
2. Export to PDF/Excel
4. Email notifications
5. Scheduled analyses
6. Advanced analytics
7. Mobile responsive design
8. API for external integrations

## Support & Documentation

- README.md: Quick start guide
- DEPLOYMENT.md: Deployment instructions
- ARCHITECTURE.md: This document
- Code comments: Inline documentation
- Docstrings: Function documentation

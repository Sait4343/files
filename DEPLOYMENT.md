# Deployment Guide

This guide describes how to run the AI Visibility Platform locally and deploy it to Streamlit Community Cloud.

## Prerequisites

- Python 3.9+
- Pip (Python package manager)
- A Supabase account and project
- An N8N workflow set up (optional, but required for AI features)

## Local Development

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-dir>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Secrets**:
    Create a file named `.streamlit/secrets.toml` in the project root.
    
    **Linux/Mac**:
    ```bash
    mkdir -p .streamlit
    touch .streamlit/secrets.toml
    ```
    
    **Windows**:
    Create a folder `.streamlit` and a file `secrets.toml` inside it.

    **Content of `secrets.toml`**:
    ```toml
    SUPABASE_URL = "your-supabase-url"
    SUPABASE_KEY = "your-supabase-anon-key"
    ```

4.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Deployment to Streamlit Community Cloud

1.  **Push your code to GitHub**. Ensure `requirements.txt` is in the root directory.
2.  **Sign in to [Streamlit Community Cloud](https://share.streamlit.io/)**.
3.  **Click "New app"**.
4.  **Select your repository, branch, and main file path** (e.g., `app.py`).
5.  **Configure Secrets**:
    - Go to "Advanced settings" -> "Secrets".
    - Paste the content of your `secrets.toml` (Supabase credentials) into the text area.
6.  **Click "Deploy"**.

## Verifying Deployment

- **Login**: Use a test account to sign in.
- **Projects**: Create a new project or select an existing one.
- **Dashboard**: Ensure metrics load without error.
- **N8N Features**: Test "Generate Prompts" in the Keywords page to verify external API connectivity.

## Environment Variables

| Variable | Description | Required |
| :--- | :--- | :--- |
| `SUPABASE_URL` | URL of your Supabase project | Yes |
| `SUPABASE_KEY` | Anon public key for Supabase | Yes |

*Note: N8N URLs and Auth headers are currently hardcoded in `core/config.py`. For production, consider moving them to secrets as well.*

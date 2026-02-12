"""
API clients for external services (N8N webhooks).
Handles all HTTP requests with proper error handling and retries.
"""

from typing import Dict, Any, Optional, List
import requests
import streamlit as st
import logging
from core.config import N8N_URLS, N8N_AUTH_HEADER, DEFAULTS

logger = logging.getLogger(__name__)


class N8NClient:
    """Client for N8N webhook operations."""
    
    def __init__(self):
        """Initialize N8N client with URLs and headers."""
        self.urls = N8N_URLS
        self.headers = N8N_AUTH_HEADER
        self.timeout_short = DEFAULTS["timeout_short"]
        self.timeout_long = DEFAULTS["timeout_long"]
        self.max_retries = DEFAULTS["max_retries"]
    
    def _make_request(
        self,
        url: str,
        payload: Dict[str, Any],
        timeout: int = None,
        retry: int = 0
    ) -> Optional[Dict[str, Any]]:
        """
        Make HTTP POST request with error handling and retries.
        
        Args:
            url: Webhook URL
            payload: Request payload
            timeout: Request timeout in seconds
            retry: Current retry attempt
            
        Returns:
            Response JSON or None on failure
        """
        timeout = timeout or self.timeout_short
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=timeout
            )
            
            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 403:
                logger.error("N8N API: 403 Forbidden - Check authentication")
                st.error("⛔ Помилка авторизації N8N API")
                return None
            
            elif response.status_code == 404:
                logger.error("N8N API: 404 Not Found")
                st.error("⚠️ N8N endpoint не знайдено")
                return None
            
            elif response.status_code >= 500:
                # Server error - retry
                if retry < self.max_retries:
                    logger.warning(f"N8N API server error, retry {retry + 1}/{self.max_retries}")
                    return self._make_request(url, payload, timeout, retry + 1)
                else:
                    logger.error(f"N8N API: {response.status_code} after {self.max_retries} retries")
                    st.error(f"⚠️ Помилка сервера N8N: {response.status_code}")
                    return None
            
            else:
                logger.error(f"N8N API: Unexpected status {response.status_code}")
                st.error(f"⚠️ Несподівана помилка: {response.status_code}")
                return None
        
        except requests.Timeout:
            logger.error(f"N8N API: Request timeout after {timeout}s")
            st.error("⏱️ Час очікування вичерпано. Спробуйте пізніше.")
            return None
        
        except requests.ConnectionError as e:
            logger.error(f"N8N API: Connection error - {e}")
            st.error("🔌 Помилка з'єднання з N8N API")
            return None
        
        except Exception as e:
            logger.error(f"N8N API: Unexpected error - {e}")
            st.error(f"⚠️ Несподівана помилка: {e}")
            return None
    
    def generate_prompts(
        self,
        brand: str,
        domain: str,
        industry: str,
        products: str
    ) -> Optional[List[str]]:
        """
        Generate AI prompts via N8N webhook.
        
        Args:
            brand: Brand name
            domain: Brand domain
            industry: Industry/niche
            products: Products/services description
            
        Returns:
            List of generated prompts or None
        """
        payload = {
            "brand": brand,
            "domain": domain,
            "industry": industry,
            "products": products
        }
        
        with st.spinner("🤖 Генерація промптів через AI..."):
            result = self._make_request(
                self.urls["generate_prompts"],
                payload,
                timeout=self.timeout_long
            )
        
        if result:
            # Extract prompts from response
            if isinstance(result, dict):
                prompts = result.get("prompts") or result.get("output") or result.get("data")
            else:
                prompts = result
            
            if isinstance(prompts, list):
                return prompts
            elif isinstance(prompts, str):
                # Try to parse as list
                import json
                try:
                    parsed = json.loads(prompts)
                    if isinstance(parsed, list):
                        return parsed
                except:
                    pass
                # Split by newlines as fallback
                return [p.strip() for p in prompts.split('\n') if p.strip()]
        
        return None
    
    def run_analysis(
        self,
        project_id: str,
        keyword_ids: List[str],
        project_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Run visibility analysis via N8N webhook.
        
        Args:
            project_id: Project ID
            keyword_ids: List of keyword IDs to analyze
            project_data: Project metadata (brand, domain, etc.)
            
        Returns:
            Analysis results or None
        """
        # Check Trial Limits
        try:
            from core.state import SessionStateManager
            from core.database import get_database
            
            user = SessionStateManager.get_user()
            if user and user.get("status") == "trial":
                db = get_database()
                # Check if any of these keywords have defined scan results
                # This is a simplification. Ideally check count of scans per keyword.
                # Assuming "Trial" means "One scan per keyword".
                
                # Fetch existing results for these keywords
                # We need a method in DB to check this efficiently, or query scan_results
                # filtered by project_id and keyword_id.
                
                # For now, let's use a query.
                for kid in keyword_ids:
                    existing = db.execute_query(
                        "scan_results",
                        {
                            "select": "id",
                            "filters": {"project_id": project_id, "keyword_id": kid},
                            "limit": 1
                        }
                    )
                    if existing:
                        st.warning(f"⚠️ Тріал-режим: Ключове слово (ID: {kid}) вже було проскановано.")
                        st.info("💎 Оновіть план до PRO для необмежених сканувань.")
                        return None

        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Failed to check trial limits: {e}")

        payload = {
            "project_id": project_id,
            "keyword_ids": keyword_ids,
            "brand_name": project_data.get("brand_name"),
            "domain": project_data.get("domain"),
            "official_sources": project_data.get("official_sources", []),
            "competitors": project_data.get("competitors", [])
        }
        
        with st.spinner("🔍 Запуск аналізу через AI..."):
            result = self._make_request(
                self.urls["analyze"],
                payload,
                timeout=self.timeout_long
            )
        
        return result
    
    def get_recommendations(
        self,
        project_id: str,
        analysis_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Get AI recommendations via N8N webhook.
        
        Args:
            project_id: Project ID
            analysis_data: Analysis results data
            
        Returns:
            Recommendations or None
        """
        payload = {
            "project_id": project_id,
            "analysis_data": analysis_data
        }
        
        with st.spinner("💡 Генерація рекомендацій..."):
            result = self._make_request(
                self.urls["recommendations"],
                payload,
                timeout=self.timeout_short
            )
        
        return result
    
    def chat_query(
        self,
        query: str,
        context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Send chat query to GPT-Visibility assistant.
        
        Args:
            query: User question
            context: Context data (project, user, etc.)
            
        Returns:
            AI response text or None
        """
        payload = {
            "query": query,
            **context
        }
        
        result = self._make_request(
            self.urls["chat"],
            payload,
            timeout=self.timeout_long
        )
        
        if result:
            # Extract response from various possible keys
            response = (
                result.get("output") or
                result.get("answer") or
                result.get("text") or
                result.get("response")
            )
            
            if isinstance(response, dict):
                response = str(response)
            
            return response if response else "⚠️ Отримано порожню відповідь"
        
        return None


# Global client instance
@st.cache_resource
def get_n8n_client() -> N8NClient:
    """Get cached N8N client instance."""
    return N8NClient()

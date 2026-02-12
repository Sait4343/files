"""
Database module with Singleton pattern for Supabase client.
Handles all database operations with error handling and caching.
"""

from typing import Optional, Dict, Any, List
import streamlit as st
from supabase import create_client, Client
import logging

# Configure logging
logger = logging.getLogger(__name__)


class Database:
    """
    Singleton Supabase client manager.
    Ensures only one database connection is created per session.
    """
    
    _instance: Optional['Database'] = None
    _client: Optional[Client] = None
    
    def __new__(cls) -> 'Database':
        """Implement Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection if not already done."""
        if self._client is None:
            self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Supabase client from secrets."""
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
            self._client = create_client(url, key)
            logger.info("✅ Database connection established")
        except KeyError as e:
            logger.error(f"❌ Missing Supabase credential: {e}")
            st.error(f"Database configuration error: Missing {e}")
            st.stop()
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            st.error(f"Failed to connect to database: {e}")
            st.stop()
    
    @property
    def client(self) -> Client:
        """Get Supabase client instance."""
        if self._client is None:
            self._initialize_client()
        return self._client
    
    # ==================== AUTH METHODS ====================
    
    def sign_in(self, email: str, password: str) -> Optional[Any]:
        """
        Sign in user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User object if successful, None otherwise
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response.user if response else None
        except Exception as e:
            logger.error(f"Sign in failed: {e}")
            return None
    
    def sign_up(self, email: str, password: str, metadata: Dict[str, Any] = None) -> Optional[Any]:
        """
        Register new user.
        
        Args:
            email: User email
            password: User password
            metadata: Additional user metadata
            
        Returns:
            User object if successful, None otherwise
        """
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": metadata} if metadata else {}
            })
            return response.user if response else None
        except Exception as e:
            logger.error(f"Sign up failed: {e}")
            return None
    
    def sign_out(self) -> bool:
        """
        Sign out current user.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.auth.sign_out()
            return True
        except Exception as e:
            logger.error(f"Sign out failed: {e}")
            return False
    
    # ==================== PROJECTS ====================
    
    def get_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all projects for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of project dictionaries
        """
        try:
            response = self.client.table("projects").select("*").eq("user_id", user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch projects: {e}")
            st.error(f"Помилка завантаження проектів: {e}")
            return []
    
    def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project dictionary or None
        """
        try:
            response = self.client.table("projects").select("*").eq("id", project_id).single().execute()
            return response.data if response.data else None
        except Exception as e:
            logger.error(f"Failed to fetch project: {e}")
            return None
    
    def create_project(self, project_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new project.
        
        Args:
            project_data: Project data dictionary
            
        Returns:
            Created project or None
        """
        try:
            response = self.client.table("projects").insert(project_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to create project: {e}")
            st.error(f"Помилка створення проекту: {e}")
            return None
    
    def update_project(self, project_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update project data.
        
        Args:
            project_id: Project ID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("projects").update(updates).eq("id", project_id).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to update project: {e}")
            st.error(f"Помилка оновлення проекту: {e}")
            return False
    
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("projects").delete().eq("id", project_id).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to delete project: {e}")
            st.error(f"Помилка видалення проекту: {e}")
            return False
    
    # ==================== KEYWORDS ====================
    
    def get_keywords(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all keywords for a project."""
        try:
            response = self.client.table("keywords").select("*").eq("project_id", project_id).execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch keywords: {e}")
            return []
    
    def create_keywords_batch(self, keywords_data: List[Dict[str, Any]]) -> bool:
        """Create multiple keywords at once."""
        try:
            self.client.table("keywords").insert(keywords_data).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to create keywords: {e}")
            return False
    
    def update_keyword(self, keyword_id: str, updates: Dict[str, Any]) -> bool:
        """Update keyword data."""
        try:
            self.client.table("keywords").update(updates).eq("id", keyword_id).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to update keyword: {e}")
            return False
    
    def delete_keyword(self, keyword_id: str) -> bool:
        """Delete a keyword."""
        try:
            self.client.table("keywords").delete().eq("id", keyword_id).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to delete keyword: {e}")
            return False
    
    # ==================== SOURCES ====================
    
    def get_sources(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all sources for a project."""
        try:
            response = self.client.table("official_sources").select("*").eq("project_id", project_id).execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch sources: {e}")
            return []
    
    def create_source(self, source_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new source."""
        try:
            response = self.client.table("official_sources").insert(source_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to create source: {e}")
            return None
    
    def delete_source(self, source_id: str) -> bool:
        """Delete a source."""
        try:
            self.client.table("official_sources").delete().eq("id", source_id).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to delete source: {e}")
            return False
    
    # ==================== SCAN RESULTS ====================
    
    def get_scan_results(self, project_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get scan results for a project."""
        try:
            response = (
                self.client.table("scan_results")
                .select("*")
                .eq("project_id", project_id)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch scan results: {e}")
            return []
    
    def create_scan_result(self, result_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new scan result."""
        try:
            response = self.client.table("scan_results").insert(result_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to create scan result: {e}")
            return None
    
    # ==================== RECOMMENDATIONS ====================
    
    def get_recommendations(self, project_id: str) -> List[Dict[str, Any]]:
        """Get recommendations for a project."""
        try:
            response = (
                self.client.table("recommendations")
                .select("*")
                .eq("project_id", project_id)
                .order("created_at", desc=True)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch recommendations: {e}")
            return []
            
    def create_recommendation(self, rec_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new recommendation."""
        try:
            response = self.client.table("recommendations").insert(rec_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to create recommendation: {e}")
            return None

    # ==================== REPORTS ====================

    def get_reports(self, project_id: str) -> List[Dict[str, Any]]:
        """Get reports for a project."""
        try:
            response = (
                self.client.table("reports")
                .select("*")
                .eq("project_id", project_id)
                .order("created_at", desc=True)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch reports: {e}")
            return []

    def create_report(self, report_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new report."""
        try:
            response = self.client.table("reports").insert(report_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to create report: {e}")
            return None
    
    # ==================== GENERIC METHODS ====================
    
    def execute_query(self, table: str, query_params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a generic query on any table.
        
        Args:
            table: Table name
            query_params: Query parameters (select, filters, etc.)
            
        Returns:
            Query results or None
        """
        try:
            query = self.client.table(table).select(query_params.get("select", "*"))
            
            # Apply filters
            if "filters" in query_params:
                for key, value in query_params["filters"].items():
                    query = query.eq(key, value)
            
            # Apply ordering
            if "order" in query_params:
                query = query.order(
                    query_params["order"].get("column", "created_at"),
                    desc=query_params["order"].get("desc", True)
                )
            
            # Apply limit
            if "limit" in query_params:
                query = query.limit(query_params["limit"])
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None


# Global database instance (initialized on first import)
@st.cache_resource
def get_database() -> Database:
    """Get cached database instance."""
    return Database()

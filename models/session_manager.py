from typing import Dict, List, Optional

from .auth import AuthenticationService
from .enum.roles import UserRole
from .session import Session


class SessionManager:
    """Singleton class for managing global session state"""
    
    _instance = None
    _auth_service = None
    _current_session = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._auth_service = AuthenticationService()
        return cls._instance
    
    def login_student(self, email: str, password: str, students: List['Student']) -> bool:
        """Login student and set current session"""
        session = self._auth_service.authenticate_student(email, password, students)
        if session:
            self._current_session = session
            return True
        return False
    
    def login_admin(self, admin_id: str, password: str, predefined_admins: Dict[str, Dict[str, str]]) -> bool:
        """Login admin and set current session"""
        session = self._auth_service.authenticate_admin(admin_id, password, predefined_admins)
        if session:
            self._current_session = session
            return True
        return False
    
    def logout(self) -> bool:
        """Logout current user"""
        if self._current_session:
            success = self._auth_service.logout(self._current_session.session_id)
            self._current_session = None
            return success
        return False
    
    def get_current_session(self) -> Optional[Session]:
        """Get current active session"""
        if self._current_session and self._current_session.is_valid():
            return self._current_session
        elif self._current_session:
            self._current_session = None
        return None
    
    def is_logged_in(self) -> bool:
        """Check if someone is currently logged in"""
        return self.get_current_session() is not None
    
    def get_current_user_id(self) -> Optional[str]:
        """Get current user ID"""
        session = self.get_current_session()
        return session.user_id if session else None
    
    def get_current_user_role(self) -> Optional[UserRole]:
        """Get current user role"""
        session = self.get_current_session()
        return session.user_role if session else None
    
    def get_current_user_name(self) -> Optional[str]:
        """Get current user name"""
        session = self.get_current_session()
        return session.user_name if session else None



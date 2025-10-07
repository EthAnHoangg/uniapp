import hashlib
import secrets
from typing import Dict, List, Optional

from .enum.roles import UserRole
from .session import Session


class AuthenticationService:
    """Service class for handling authentication and session management"""
    
    def __init__(self):
        self.active_sessions: Dict[str, Session] = {}
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            salt, password_hash = hashed_password.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash
        except ValueError:
            return False
    
    def authenticate_student(self, email: str, password: str, students: List['Student']) -> Optional[Session]:
        """Authenticate student and create session"""
        for student in students:
            if student.email == email and self.verify_password(password, student.password_hash):
                session = Session(student.student_id, UserRole.STUDENT, student.name)
                self.active_sessions[session.session_id] = session
                return session
        return None
    
    def authenticate_admin(self, admin_id: str, password: str, predefined_admins: Dict[str, Dict[str, str]]) -> Optional[Session]:
        """Authenticate admin and create session"""
        if admin_id in predefined_admins:
            admin_info = predefined_admins[admin_id]
            if admin_info["password"] == password:
                session = Session(admin_id, UserRole.ADMIN, admin_info["name"])
                self.active_sessions[session.session_id] = session
                return session
        return None
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        session = self.active_sessions.get(session_id)
        if session and session.is_valid():
            session.refresh()
            return session
        elif session:
            del self.active_sessions[session_id]
        return None
    
    def logout(self, session_id: str) -> bool:
        """Logout and invalidate session"""
        session = self.active_sessions.get(session_id)
        if session:
            session.invalidate()
            del self.active_sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        expired_sessions = [
            sid for sid, session in self.active_sessions.items()
            if not session.is_valid()
        ]
        for sid in expired_sessions:
            del self.active_sessions[sid]



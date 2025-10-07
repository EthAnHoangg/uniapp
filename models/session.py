import secrets
from datetime import datetime, timedelta
from typing import Optional

from .enum.roles import UserRole


class Session:
    """Represents a user session with token-based authentication"""
    
    def __init__(self, user_id: str, user_role: UserRole, user_name: str):
        self.session_id = secrets.token_urlsafe(32)
        self.user_id = user_id
        self.user_role = user_role
        self.user_name = user_name
        self.created_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(hours=24)
        self.is_active = True
    
    def is_valid(self) -> bool:
        """Check if session is still valid"""
        return self.is_active and datetime.now() < self.expires_at
    
    def refresh(self):
        """Refresh session expiry time"""
        if self.is_valid():
            self.expires_at = datetime.now() + timedelta(hours=24)
    
    def invalidate(self):
        """Invalidate the session"""
        self.is_active = False



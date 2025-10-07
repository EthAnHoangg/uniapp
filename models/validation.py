import re
import random
from typing import Dict, List


class ValidationService:
    """Service class for validating email and password formats."""
    
    def __init__(self):
        self.email_pattern = r'^[a-zA-Z0-9._%+-]+@university\.com$'
        self.password_pattern = r'^[A-Z][a-zA-Z]{4,}\d{3,}$'
    
    def validate_email(self, email: str) -> bool:
        """Validate email format - must end with @university.com"""
        return bool(re.match(self.email_pattern, email))
    
    def validate_password(self, password: str) -> bool:
        """Validate password format - starts with uppercase, 5+ letters, 3+ digits"""
        return bool(re.match(self.password_pattern, password))
    
    def validate_student_registration(self, name: str, email: str, password: str, existing_students: List['Student']) -> Dict[str, str]:
        """Centralized validation for student registration"""
        if not name or not email or not password:
            return {'valid': False, 'error': 'All fields are required!'}
        if not self.validate_email(email):
            return {'valid': False, 'error': 'Invalid email format. Must end with @university.com'}
        if not self.validate_password(password):
            return {'valid': False, 'error': 'Invalid password format. Must start with uppercase, have 5+ letters, and 3+ digits.'}
        for student in existing_students:
            if student.email == email:
                return {'valid': False, 'error': 'Email already registered.'}
        return {'valid': True, 'error': ''}
    
    def generate_student_id(self, existing_ids: List[str]) -> str:
        """Generate unique 6-digit student ID"""
        while True:
            student_id = str(random.randint(1, 999999)).zfill(6)
            if student_id not in existing_ids:
                return student_id



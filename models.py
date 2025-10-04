"""
University Enrollment System - Data Models
Contains all the core classes for the university enrollment system.
"""

import re
import random
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum


class UserRole(Enum):
    """User roles in the system"""
    STUDENT = "student"
    ADMIN = "admin"


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
            if admin_info["password"] == password:  # For simplicity, keeping plain text for predefined admins
                session = Session(admin_id, UserRole.ADMIN, admin_info["name"])
                self.active_sessions[session.session_id] = session
                return session
        return None
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        session = self.active_sessions.get(session_id)
        if session and session.is_valid():
            session.refresh()  # Auto-refresh on access
            return session
        elif session:
            # Clean up expired session
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
            # Session expired, clean up
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
        """Centralized validation for student registration
        
        Returns:
            Dict with 'valid' (bool) and 'error' (str) keys
        """
        # Check required fields
        if not name or not email or not password:
            return {'valid': False, 'error': 'All fields are required!'}
        
        # Validate email format
        if not self.validate_email(email):
            return {'valid': False, 'error': 'Invalid email format. Must end with @university.com'}
        
        # Validate password format
        if not self.validate_password(password):
            return {'valid': False, 'error': 'Invalid password format. Must start with uppercase, have 5+ letters, and 3+ digits.'}
        
        # Check if email already exists
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


class GradingService:
    """Service class for calculating grades based on marks."""
    
    def __init__(self):
        self.grade_rules = {
            'Z': (0, 49),
            'P': (50, 64),
            'C': (65, 74),
            'D': (75, 84),
            'HD': (85, 100)
        }
    
    def calculate_grade(self, mark: int) -> str:
        """Calculate grade based on mark according to UTS grading system"""
        for grade, (min_mark, max_mark) in self.grade_rules.items():
            if min_mark <= mark <= max_mark:
                return grade
        return 'Z'  # Default to Z if mark is invalid
    
    def get_grade_rules(self) -> Dict[str, tuple]:
        """Return grading rules"""
        return self.grade_rules.copy()


class Subject:
    """Represents a university subject/course."""
    
    def __init__(self, subject_id: str, name: str, description: str = "", credits: int = 3):
        self.subject_id = subject_id
        self.name = name
        self.description = description
        self.credits = credits
    
    @classmethod
    def create(cls, name: str, description: str = "", credits: int = 3) -> 'Subject':
        """Create a new subject"""
        subject_id = str(random.randint(1, 999)).zfill(3)
        return cls(subject_id, name, description, credits)
    
    def get_info(self) -> Dict[str, str]:
        """Return subject information"""
        return {
            'subject_id': self.subject_id,
            'name': self.name,
            'description': self.description,
            'credits': str(self.credits)
        }


class Enrollment:
    """Represents a student's enrollment in a subject."""
    
    def __init__(self, student_id: str, subject_id: str, mark: int = None, grade: str = None):
        self.student_id = student_id
        self.subject_id = subject_id
        self.mark = mark or random.randint(25, 100)
        self.grade = grade or GradingService().calculate_grade(self.mark)
        self.enrollment_date = datetime.now()
    
    def calculate_grade(self) -> str:
        """Calculate grade based on current mark"""
        self.grade = GradingService().calculate_grade(self.mark)
        return self.grade
    
    def get_info(self) -> Dict[str, str]:
        """Return enrollment details"""
        return {
            'student_id': self.student_id,
            'subject_id': self.subject_id,
            'mark': str(self.mark),
            'grade': self.grade,
            'enrollment_date': self.enrollment_date.strftime('%Y-%m-%d %H:%M:%S')
        }


class Student:
    """Represents a university student."""
    
    def __init__(self, student_id: str, name: str, email: str, password_hash: str):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password_hash = password_hash  # Store hashed password instead of plain text
        self.enrollments: List[Enrollment] = []
    
    @classmethod
    def create_student(cls, student_id: str, name: str, email: str, password: str) -> 'Student':
        """Factory method to create a new student with password hashing
        
        Note: Validation should be done before calling this method
        """
        password_hash = AuthenticationService.hash_password(password)
        return cls(student_id, name, email, password_hash)
    
    def enroll(self, subject: Subject) -> bool:
        """Enroll in a subject (maximum 4 subjects)"""
        if len(self.enrollments) >= 4:
            return False
        
        # Check if already enrolled in this subject
        for enrollment in self.enrollments:
            if enrollment.subject_id == subject.subject_id:
                return False
        
        enrollment = Enrollment(self.student_id, subject.subject_id)
        self.enrollments.append(enrollment)
        return True
    
    def enroll_random(self, available_subjects: List[Subject]) -> Optional[Subject]:
        """Enroll in a random subject from available subjects
        
        Args:
            available_subjects: List of all available subjects
            
        Returns:
            The subject enrolled in, or None if enrollment failed
        """
        if len(self.enrollments) >= 4:
            return None
        
        # Filter out subjects already enrolled in
        eligible_subjects = []
        enrolled_subject_ids = {enrollment.subject_id for enrollment in self.enrollments}
        
        for subject in available_subjects:
            if subject.subject_id not in enrolled_subject_ids:
                eligible_subjects.append(subject)
        
        if not eligible_subjects:
            return None  # No subjects available to enroll in
        
        # Select a random subject
        selected_subject = random.choice(eligible_subjects)
        
        # Enroll in the selected subject
        if self.enroll(selected_subject):
            return selected_subject
        
        return None
    
    def remove_subject(self, subject_id: str) -> bool:
        """Remove a subject from enrollment list"""
        for i, enrollment in enumerate(self.enrollments):
            if enrollment.subject_id == subject_id:
                del self.enrollments[i]
                return True
        return False
    
    def view_enrollments(self) -> List[Dict[str, str]]:
        """View current enrollment list"""
        return [enrollment.get_info() for enrollment in self.enrollments]
    
    def change_password(self, old_password: str, new_password: str, validation_service: ValidationService) -> bool:
        """Change student password with validation
        
        Args:
            old_password: Plain text current password
            new_password: Plain text new password  
            validation_service: Service to validate new password format
        
        Returns:
            bool: True if password changed successfully
        """
        # Verify current password (plain text against stored hash)
        if not AuthenticationService.verify_password(old_password, self.password_hash):
            return False
        
        # Validate new password format (plain text only)
        if not validation_service.validate_password(new_password):
            return False
        
        # Hash and store new password
        self.password_hash = AuthenticationService.hash_password(new_password)
        return True
    
    def get_info(self) -> Dict[str, str]:
        """Return student information"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'enrollment_count': str(len(self.enrollments))
        }


class Admin:
    """Represents a university administrator."""
    
    # Predefined admin credentials (existing university staff)
    PREDEFINED_ADMINS = {
        "admin001": {"name": "Dr. Sarah Johnson", "department": "IT Department", "password": "Admin123"},
        "admin002": {"name": "Prof. Michael Chen", "department": "Academic Affairs", "password": "Admin456"},
        "admin003": {"name": "Ms. Lisa Williams", "department": "Student Services", "password": "Admin789"}
    }
    
    def __init__(self, admin_id: str, name: str, department: str):
        self.admin_id = admin_id
        self.name = name
        self.department = department
    
    
    def view_students(self, students: List[Student]) -> List[Dict[str, str]]:
        """View all registered students"""
        return [student.get_info() for student in students]
    
    def view_by_grade(self, students: List[Student]) -> Dict[str, List[Dict[str, str]]]:
        """Organize and view students by grade"""
        grade_groups = {'Z': [], 'P': [], 'C': [], 'D': [], 'HD': []}
        
        for student in students:
            for enrollment in student.enrollments:
                grade = enrollment.grade
                if grade in grade_groups:
                    grade_groups[grade].append({
                        'student_id': student.student_id,
                        'name': student.name,
                        'subject_id': enrollment.subject_id,
                        'mark': str(enrollment.mark),
                        'grade': grade
                    })
        
        return grade_groups
    
    def categorize_pass_fail(self, students: List[Student]) -> Dict[str, List[Dict[str, str]]]:
        """Categorize students into PASS/FAIL categories"""
        pass_students = []
        fail_students = []
        
        for student in students:
            for enrollment in student.enrollments:
                if enrollment.mark >= 50:
                    pass_students.append({
                        'student_id': student.student_id,
                        'name': student.name,
                        'subject_id': enrollment.subject_id,
                        'mark': str(enrollment.mark),
                        'status': 'PASS'
                    })
                else:
                    fail_students.append({
                        'student_id': student.student_id,
                        'name': student.name,
                        'subject_id': enrollment.subject_id,
                        'mark': str(enrollment.mark),
                        'status': 'FAIL'
                    })
        
        return {'PASS': pass_students, 'FAIL': fail_students}
    
    def remove_student(self, student_id: str, students: List[Student]) -> bool:
        """Remove individual student"""
        for i, student in enumerate(students):
            if student.student_id == student_id:
                del students[i]
                return True
        return False
    
    def clear_all(self, students: List[Student]) -> bool:
        """Clear entire students list"""
        students.clear()
        return True

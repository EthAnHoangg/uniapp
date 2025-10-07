from typing import Dict, List, Optional

from .auth import AuthenticationService
from .enrollment import Enrollment
from .subject import Subject
from .validation import ValidationService


class Student:
    """Represents a university student."""
    
    def __init__(self, student_id: str, name: str, email: str, password_hash: str):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.enrollments: List[Enrollment] = []
    
    @classmethod
    def create_student(cls, student_id: str, name: str, email: str, password: str) -> 'Student':
        """Factory method to create a new student with password hashing"""
        password_hash = AuthenticationService.hash_password(password)
        return cls(student_id, name, email, password_hash)
    
    def enroll(self, subject: Subject) -> bool:
        """Enroll in a subject (maximum 4 subjects)"""
        if len(self.enrollments) >= 4:
            return False
        for enrollment in self.enrollments:
            if enrollment.subject_id == subject.subject_id:
                return False
        enrollment = Enrollment(self.student_id, subject.subject_id)
        self.enrollments.append(enrollment)
        return True
    
    def enroll_random(self, available_subjects: List[Subject]) -> Optional[Subject]:
        """Enroll in a random subject from available subjects"""
        if len(self.enrollments) >= 4:
            return None
        eligible_subjects: List[Subject] = []
        enrolled_subject_ids = {enrollment.subject_id for enrollment in self.enrollments}
        for subject in available_subjects:
            if subject.subject_id not in enrolled_subject_ids:
                eligible_subjects.append(subject)
        if not eligible_subjects:
            return None
        import random
        selected_subject = random.choice(eligible_subjects)
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
        """Change student password with validation"""
        if not AuthenticationService.verify_password(old_password, self.password_hash):
            return False
        if not validation_service.validate_password(new_password):
            return False
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



import random
from datetime import datetime
from typing import Dict, Optional

from .grading import GradingService


class Enrollment:
    """Represents a student's enrollment in a subject."""
    
    def __init__(self, student_id: str, subject_id: str, mark: Optional[int] = None, grade: Optional[str] = None):
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



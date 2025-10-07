import random
from typing import Dict


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



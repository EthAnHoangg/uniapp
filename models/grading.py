from typing import Dict, Tuple


class GradingService:
    """Service class for calculating grades based on marks."""
    
    def __init__(self):
        self.grade_rules: Dict[str, Tuple[int, int]] = {
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
        return 'Z'
    
    def get_grade_rules(self) -> Dict[str, Tuple[int, int]]:
        """Return grading rules"""
        return self.grade_rules.copy()



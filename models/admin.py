from typing import Dict, List

from .student import Student


class Admin:
    """Represents a university administrator."""
    
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
        grade_groups: Dict[str, List[Dict[str, str]]] = {'Z': [], 'P': [], 'C': [], 'D': [], 'HD': []}
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
        pass_students: List[Dict[str, str]] = []
        fail_students: List[Dict[str, str]] = []
        for student in students:
            for enrollment in student.enrollments:
                if enrollment.mark >= 50:
                    pass_students.append({
                        'student_id': student.student_id,
                        'name': student.name,
                        'subject_id': enrollment.subject_id,
                        'mark': str(enrollment.mark),
                        'grade': enrollment.grade,
                        'status': 'PASS'
                    })
                else:
                    fail_students.append({
                        'student_id': student.student_id,
                        'name': student.name,
                        'subject_id': enrollment.subject_id,
                        'mark': str(enrollment.mark),
                        'grade': enrollment.grade,
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



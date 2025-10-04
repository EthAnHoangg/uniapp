"""
Data Manager for University Enrollment System
Handles file operations for students.data persistence.
"""

import json
import os
from typing import List, Dict, Optional
from models import Student, Enrollment


class DataManager:
    """Manages data persistence for the university enrollment system."""
    
    def __init__(self, file_path: str = "students.data"):
        self.file_path = file_path
        self.data: Dict = {}
    
    def save_data(self, students: List[Student]) -> bool:
        """Save student data to students.data file"""
        try:
            # Convert students to serializable format
            students_data = []
            for student in students:
                student_data = {
                    'student_id': student.student_id,
                    'name': student.name,
                    'email': student.email,
                    'password_hash': student.password_hash,
                    'enrollments': []
                }
                
                # Convert enrollments
                for enrollment in student.enrollments:
                    enrollment_data = {
                        'student_id': enrollment.student_id,
                        'subject_id': enrollment.subject_id,
                        'mark': enrollment.mark,
                        'grade': enrollment.grade,
                        'enrollment_date': enrollment.enrollment_date.isoformat()
                    }
                    student_data['enrollments'].append(enrollment_data)
                
                students_data.append(student_data)
            
            # Save to file
            with open(self.file_path, 'w') as file:
                json.dump(students_data, file, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self) -> List[Student]:
        """Load student data from students.data file"""
        students = []
        
        try:
            if not os.path.exists(self.file_path):
                return students
            
            with open(self.file_path, 'r') as file:
                students_data = json.load(file)
            
            # Convert back to Student objects
            for student_data in students_data:
                # Handle backward compatibility: old files may have 'password' instead of 'password_hash'
                password_hash = student_data.get('password_hash') or student_data.get('password', '')
                
                student = Student(
                    student_data['student_id'],
                    student_data['name'],
                    student_data['email'],
                    password_hash
                )
                
                # Convert enrollments back
                for enrollment_data in student_data['enrollments']:
                    enrollment = Enrollment(
                        enrollment_data['student_id'],
                        enrollment_data['subject_id'],
                        enrollment_data['mark'],
                        enrollment_data['grade']
                    )
                    # Restore enrollment date
                    from datetime import datetime
                    enrollment.enrollment_date = datetime.fromisoformat(enrollment_data['enrollment_date'])
                    student.enrollments.append(enrollment)
                
                students.append(student)
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
        
        return students
    
    def delete_student(self, student_id: str, students: List[Student]) -> bool:
        """Remove student from data and save"""
        for i, student in enumerate(students):
            if student.student_id == student_id:
                del students[i]
                return self.save_data(students)
        return False
    
    def clear_data(self) -> bool:
        """Clear entire students.data file"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump([], file)
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
    
    def find_student_by_email(self, email: str, students: List[Student]) -> Optional[Student]:
        """Find student by email address"""
        for student in students:
            if student.email == email:
                return student
        return None
    
    def find_student_by_id(self, student_id: str, students: List[Student]) -> Optional[Student]:
        """Find student by student ID"""
        for student in students:
            if student.student_id == student_id:
                return student
        return None
    
    def get_student_count(self) -> int:
        """Get total number of students in data file"""
        students = self.load_data()
        return len(students)
    
    def backup_data(self, backup_path: str = None) -> bool:
        """Create backup of current data"""
        if backup_path is None:
            backup_path = f"{self.file_path}.backup"
        
        try:
            if os.path.exists(self.file_path):
                import shutil
                shutil.copy2(self.file_path, backup_path)
                return True
        except Exception as e:
            print(f"Error creating backup: {e}")
        
        return False

"""
CLI University Application
Command-line interface for the university enrollment system.
"""

from typing import List, Optional
from models.student import Student
from models.subject import Subject
from models.admin import Admin
from models.validation import ValidationService
from models.auth import AuthenticationService
from models.session_manager import SessionManager
from models.enum.roles import UserRole
from repository.data_manager import DataManager


class CLIUniApp:
    """Command-line interface for the university enrollment system."""
    class Color:
        RESET = "\033[0m"
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"

    @staticmethod
    def _c(text: str, color: str) -> str:
        return f"{color}{text}{CLIUniApp.Color.RESET}"
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.data_manager = DataManager()
        self.validation_service = ValidationService()
        self.students: List[Student] = []
        self.subjects: List[Subject] = []
        
        # Initialize with some sample subjects
        self._initialize_subjects()
        
        # Load existing students
        self.students = self.data_manager.load_data()
    
    def _initialize_subjects(self):
        """Initialize with sample subjects"""
        sample_subjects = [
            ("101", "Introduction to Programming"),
            ("102", "Data Structures"),
            ("201", "Software Engineering"),
            ("301", "Database Systems"),
            ("401", "Machine Learning"),
            ("111", "Calculus I"),
            ("112", "Calculus II"),
            ("121", "Physics I"),
            ("131", "Chemistry I"),
            ("141", "English Composition")
        ]
        
        for subject_id, name in sample_subjects:
            subject = Subject(subject_id, name, f"Description for {name}")
            self.subjects.append(subject)
    
    def _get_current_student(self) -> Optional[Student]:
        """Get current student from session"""
        session = self.session_manager.get_current_session()
        if session and session.user_role == UserRole.STUDENT:
            # Find student by ID
            for student in self.students:
                if student.student_id == session.user_id:
                    return student
        return None
    
    def _get_current_admin(self) -> Optional[Admin]:
        """Get current admin from session"""
        session = self.session_manager.get_current_session()
        if session and session.user_role == UserRole.ADMIN:
            admin_info = Admin.PREDEFINED_ADMINS.get(session.user_id)
            if admin_info:
                return Admin(session.user_id, admin_info["name"], admin_info["department"])
        return None
    
    def run(self):
        """Main application loop"""
        
        while True:
            # One-line, colored prompt like sample I/O
            prompt = self._c("University System: (A)dmin, (S)tudent, or X : ", self.Color.CYAN)
            choice = input(prompt).strip().upper()
            
            if choice == "A":
                self._admin_system()
            elif choice == "S":
                self._student_system()
            elif choice == "X":
                print(self._c("Thank You", self.Color.YELLOW))
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _admin_system(self):
        """Admin system - direct access without login"""
        self._admin_menu()
    
    def _student_system(self):
        """Student system with login/register options"""
        while True:
            # Colored one-line student menu
            prompt = self._c("      Student System (l/r/x): ", self.Color.CYAN)
            choice = input(prompt).strip().lower()
            
            if choice == "l":
                login_success = self._student_login()
                if login_success:
                    break
                else:
                    continue
            elif choice == "r":
                self._student_registration()
            elif choice == "x":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _student_login(self):
        """Handle student login"""
        indent = "      "
        print(indent + self._c("Student Sign In", self.Color.GREEN))
        
        # Loop until valid formats
        while True:
            email = input(indent + "Email: ").strip()
            password = input(indent + "Password: ").strip()
            if not (self.validation_service.validate_email(email) and self.validation_service.validate_password(password)):
                print(indent + self._c("Incorrect email or password format", self.Color.RED))
                continue
            else:
                print(indent + self._c("email and password formats acceptable", self.Color.YELLOW))
                break
        
        # Authenticate student using session manager
        if self.session_manager.login_student(email, password, self.students):
            self._subject_enrolment_system()
            return True
        else:
            print(indent + self._c("Student does not exist", self.Color.RED))
            return False
    
    def _student_registration(self):
        """Handle student registration"""
        indent = "      "
        print(indent + self._c("Student Sign Up", self.Color.GREEN))
        
        # Ask for email and password, loop until formats are acceptable
        while True:
            email = input(indent + "Email: ").strip()
            password = input(indent + "Password: ").strip()
            if not (self.validation_service.validate_email(email) and self.validation_service.validate_password(password)):
                print(indent + self._c("Incorrect email or password format", self.Color.RED))
                continue
            else:
                print(indent + self._c("email and password formats acceptable", self.Color.YELLOW))
                break
        
        # Check existing email
        existing = next((s for s in self.students if s.email == email), None)
        if existing:
            print(indent + self._c(f"Student {existing.name} already exists", self.Color.RED))
            return
        
        # Ask for name after formats are accepted
        name = input(indent + "Name: ").strip()
        print(indent + self._c(f"Enrolling Student {name}", self.Color.YELLOW))
        
        # Final centralized validation for completeness
        validation_result = self.validation_service.validate_student_registration(name, email, password, self.students)
        if not validation_result['valid']:
            print(self._c(validation_result['error'], self.Color.RED))
            return
        
        # Generate unique student ID
        existing_ids = [s.student_id for s in self.students]
        student_id = self.validation_service.generate_student_id(existing_ids)
        
        # Create new student with hashed password
        new_student = Student.create_student(student_id, name, email, password)
        self.students.append(new_student)
        
        # Save to file
        if self.data_manager.save_data(self.students):
            pass  # Registration successful - no message displayed
        else:
            print("Registration failed. Please try again.")
            self.students.remove(new_student)
    
    def _subject_enrolment_system(self):
        """Subject Enrolment System operations menu"""
        while self.session_manager.is_logged_in() and self.session_manager.get_current_user_role() == UserRole.STUDENT:
            indent = "            "
            prompt = self._c(indent + "Student Course Menu (c/e/r/s/x): ", self.Color.CYAN)
            choice = input(prompt).strip().lower()
            
            if choice == "c":
                self._change_password()
            elif choice == "e":
                self._enroll_subject()
            elif choice == "r":
                self._remove_subject()
            elif choice == "s":
                self._view_enrollments()
            elif choice == "x":
                self.session_manager.logout()
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _enroll_subject(self):
        """Enroll in a random subject"""
        # Get current student from session
        current_student = self._get_current_student()
        if not current_student:
            print("Session expired. Please log in again.")
            return
        
        # Check enrollment limit
        indent = "            "
        if len(current_student.enrollments) >= 4:
            print(indent + self._c("Students are allowed to enrol in 4 subjects only", self.Color.RED))
            return
        
        # Enroll in a random subject
        enrolled_subject = current_student.enroll_random(self.subjects)
        
        if enrolled_subject:
            self.data_manager.save_data(self.students)
            print(indent + self._c(f"Enrolling in Subject-{enrolled_subject.subject_id}", self.Color.YELLOW))
            print(indent + self._c(f"You are now enrolled in {len(current_student.enrollments)} out of 4 subjects", self.Color.YELLOW))
        else:
            print(indent + "No subjects available for enrollment. You may already be enrolled in all available subjects.")
    
    def _remove_subject(self):
        """Remove a subject from enrollment"""
        current_student = self._get_current_student()
        if not current_student:
            print("Session expired. Please log in again.")
            return
        
        indent = "            "
        # Prompt for subject id directly, matching sample I/O style
        subject_id = input(indent + "Remove Subject by ID: ").strip()
        if not subject_id:
            return
        
        if current_student.remove_subject(subject_id):
            self.data_manager.save_data(self.students)
            print(indent + self._c(f"Dropping Subject-{subject_id}", self.Color.YELLOW))
            print(indent + self._c(f"You are now enrolled in {len(current_student.enrollments)} out of 4 subjects", self.Color.YELLOW))
        else:
            print(indent + self._c("Failed to remove subject.", self.Color.RED))
    
    def _view_enrollments(self):
        """View current enrollments"""
        current_student = self._get_current_student()
        if not current_student:
            print("Session expired. Please log in again.")
            return
            
        enrollments = current_student.view_enrollments()
        
        indent = "            "
        print(indent + self._c(f"Showing {len(enrollments)} subjects", self.Color.YELLOW))
        for enrollment in enrollments:
            subject_id = enrollment['subject_id']
            mark = enrollment['mark']
            grade = enrollment['grade']
            # Normalize grade width so closing brackets align (e.g., 'P' vs 'HD')
            grade_display = str(grade).rjust(2)
            print(indent + f"[ Subject::{subject_id} -- mark = {mark} -- grade =  {grade_display} ]")
    
    def _change_password(self):
        """Change student password"""
        current_student = self._get_current_student()
        if not current_student:
            print("Session expired. Please log in again.")
            return
        
        indent = "            "
        print(indent + self._c("Updating Password", self.Color.YELLOW))
        
        new_password = input(indent + "New Password: ").strip()
        confirm_password = input(indent + "Confirm Password: ").strip()
        while confirm_password != new_password:
            print(indent + self._c("Password does not match – try again", self.Color.RED))
            confirm_password = input(indent + "Confirm Password: ").strip()
        
        # Validate new password format
        if not self.validation_service.validate_password(new_password):
            print(self._c("Incorrect password format", self.Color.RED))
            return
        
        # Apply change directly without asking for the old password
        current_student.password_hash = AuthenticationService.hash_password(new_password)
        self.data_manager.save_data(self.students)
    
    def _admin_menu(self):
        """Admin operations menu"""
        while True:
            choice = input(self._c("      Admin System (c/g/p/r/s/x): ", self.Color.CYAN)).strip().lower()
            
            if choice == "c":
                self._clear_all_data()
            elif choice == "g":
                self._view_students_by_grade()
            elif choice == "p":
                self._categorize_students()
            elif choice == "r":
                self._remove_student()
            elif choice == "s":
                self._view_all_students()
            elif choice == "x":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _view_all_students(self):
        """View all registered students"""
        indent = "      "
        print(indent + self._c("Student List", self.Color.YELLOW))
        if not self.students:
            print(indent + "      " + "< Nothing to Display >")
            return
        for s in self.students:
            print(indent + f"{s.name} ::  {s.student_id} --> Email: {s.email}")
    
    def _view_students_by_grade(self):
        """View students organized by grade"""
        admin = Admin("admin", "System Admin", "IT Department")
        grade_groups = admin.view_by_grade(self.students)
        indent = "      "
        print(indent + self._c("Grade Grouping", self.Color.YELLOW))
        all_empty = True
        for grade_key in ['P','C','D','HD','Z']:
            students = grade_groups.get(grade_key, [])
            if students:
                all_empty = False
                parts = []
                for st in students:
                    parts.append(f"{st['name']} ::  {st['student_id']} --> GRADE:  {grade_key} - MARK:  {float(st['mark']):.2f}")
                print(indent + f"{grade_key}  --> [" + ", ".join(parts) + "]")
        if all_empty:
            print(indent + "      " + "< Nothing to Display >")
    
    def _categorize_students(self):
        """Categorize students into PASS/FAIL"""
        admin = Admin("admin", "System Admin", "IT Department")
        categories = admin.categorize_pass_fail(self.students)
        indent = "      "
        print(indent + self._c("PASS/FAIL Partition", self.Color.YELLOW))
        def fmt(listing):
            if not listing:
                return ""
            parts = []
            for st in listing:
                parts.append(f"{st['name']} ::  {st['student_id']} --> GRADE:  {st.get('grade','')} - MARK:  {float(st['mark']):.2f}")
            return ", ".join(parts)
        fail_list = categories.get("FAIL", [])
        pass_list = categories.get("PASS", [])
        print(indent + f"FAIL --> [{fmt(fail_list)}]")
        print(indent + f"PASS --> [{fmt(pass_list)}]")
    
    def _remove_student(self):
        """Remove individual student"""
        # Create a temporary admin instance for operations
        admin = Admin("admin", "System Admin", "IT Department")
        indent = "      "
        student_id = input(indent + "Remove by ID: ").strip()
        
        if admin.remove_student(student_id, self.students):
            self.data_manager.save_data(self.students)
            print(indent + self._c(f"Removing Student {student_id} Account", self.Color.YELLOW))
        else:
            print(indent + self._c(f"Student {student_id} does not exist", self.Color.RED))
    
    def _clear_all_data(self):
        """Clear entire students.data file"""
        admin = Admin("admin", "System Admin", "IT Department")
        indent = "      "
        print(indent + self._c("Clearing students database", self.Color.YELLOW))
        confirm = input(indent + self._c("Are you sure you want to clear the database (Y)ES/(N)O: ", self.Color.RED)).strip().lower()
        if confirm == "y" or confirm == "yes":
            if admin.clear_all(self.students):
                self.data_manager.clear_data()
                print(indent + self._c("Students data cleared", self.Color.YELLOW))
            else:
                print(indent + "Failed to clear data.")


if __name__ == "__main__":
    app = CLIUniApp()
    app.run()

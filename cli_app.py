"""
CLI University Application
Command-line interface for the university enrollment system.
"""

from typing import List, Optional
from models.student import Student
from models.subject import Subject
from models.admin import Admin
from models.validation import ValidationService
from models.session_manager import SessionManager
from models.enum.roles import UserRole
from repository.data_manager import DataManager
from colorama import Fore, Style, init
init(autoreset=True) 


class CLIUniApp:
    """Command-line interface for the university enrollment system."""
    
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
        """Main application loop with precise color formatting"""

    
        print(Fore.YELLOW + "Starting CLI Application...\n")

    
        print(Fore.MAGENTA + "University Enrollment System")
        print(Fore.CYAN + "=" * 60)

        while True:
        
            choice = input(
                Fore.CYAN + "University System: "
                + Fore.CYAN + "(A)"
                + Fore.CYAN + "dmin, "
                + Fore.CYAN + "(S)"
                + Fore.CYAN + "tudent, or "
                + Fore.CYAN + "X"
                + Fore.CYAN + " : "
                + Style.RESET_ALL
            ).strip().lower()

            if choice == "a":
            
                while True:
                    admin_choice = input(
                        Fore.CYAN + "Admin System "
                        + Fore.CYAN + "(c/g/p/r/s/x)"
                        + Fore.CYAN + ": "
                        + Style.RESET_ALL
                    ).strip().lower()

                    if admin_choice == "x":
                        break
                    elif admin_choice == "c":
                        self._clear_all_data()
                    elif admin_choice == "g":
                        self._view_students_by_grade()
                    elif admin_choice == "p":
                        self._categorize_students()
                    elif admin_choice == "r":
                        self._remove_student()
                    elif admin_choice == "s":
                        self._view_all_students()
                    else:
                        print(Fore.RED + "Invalid option. Try again.")

            elif choice == "s":
            
                while True:
                    student_choice = input(
                        Fore.CYAN + "Student System "
                        + Fore.CYAN  + "(l/r/x)"
                        + Fore.CYAN + ": "
                        + Style.RESET_ALL
                    ).strip().lower()

                    if student_choice == "x":
                        break
                    elif student_choice == "l":
                        self._student_login()
                    elif student_choice == "r":
                        self._student_registration()
                    else:
                        print(Fore.RED + "Invalid option. Try again.")

            elif choice == "x":
                print(Fore.YELLOW + "Thank You" + Style.RESET_ALL)
                break

            else:
                print(Fore.RED + "Invalid choice. Try again.")

    
    def _admin_system(self):
        """Admin system - direct access without login"""
        print("\n" + "=" * 40)
        print("Admin System")
        print("=" * 40)
        self._admin_menu()
    
    def _student_system(self):
        """Student system with login/register options"""
        while True:
            print("\n" + "=" * 40)
            print("Student System")
            print("=" * 40)
            print("(l) login")
            print("(r) register")
            print("(x) exit")
            
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice == "l":
                self._student_login()
                break
            elif choice == "r":
                self._student_registration()
            elif choice == "x":
                break
            else:
                print("Invalid choice. Please try again.")
             
    def _student_registration(self):
        """Handle student registration with colored output"""
        print(Fore.GREEN + "Student Sign Up")

        
        while True:
            email = input(Fore.WHITE + "Email: ").strip()
            password = input(Fore.WHITE + "Password: ").strip()

            
            valid_email = email.endswith("@university.com")
            valid_password = (
                len(password) >= 8 and password[0].isupper()
                and sum(ch.isdigit() for ch in password) >= 3
                and sum(ch.isalpha() for ch in password) >= 5
            )

            if not valid_email or not valid_password:
                print(Fore.RED + "Incorrect email or password format\n")
                continue
            else:
                print(Fore.YELLOW + "email and password formats acceptable")

            
            for student in self.students:
                if student.email == email:
                    print(Fore.RED + f"Student {student.name} already exists\n")
                    return

            
            name = input(Fore.WHITE + "Name: ").strip()
            print(Fore.GREEN + f"Enrolling student {name}")

            new_student = Student.create_student(name, email, password)
            self.students.append(new_student)
            self.data_manager.save_data(self.students)
            print(Fore.GREEN + "Student registration successful!\n")
            break


    def _student_login(self):
        """Handle student login with colored feedback"""
        print(Fore.GREEN + "Student Sign In")

        while True:
            email = input(Fore.WHITE + "Email: ").strip()
            password = input(Fore.WHITE + "Password: ").strip()

            valid_email = email.endswith("@university.com")
            valid_password = (
                len(password) >= 8 and password[0].isupper()
                and sum(ch.isdigit() for ch in password) >= 3
                and sum(ch.isalpha() for ch in password) >= 5
            )

            if not valid_email or not valid_password:
                print(Fore.RED + "Incorrect email or password format\n")
                continue
            else:
                print(Fore.YELLOW + "email and password formats acceptable")

            
            login_success = self.session_manager.login_student(email, password, self.students)

            if login_success:
                current_student = next((s for s in self.students if s.email == email), None)
                
                self._subject_enrolment_system()
                break
            else:
                print(Fore.RED + "Student does not exist\n")
                return

    
    def _subject_enrolment_system(self):
        """Subject Enrolment System operations menu"""
        while self.session_manager.is_logged_in() and self.session_manager.get_current_user_role() == UserRole.STUDENT:
            print("\n" + "=" * 40)
            print("Subject Enrolment System")
            print("=" * 40)
            print("(c) change: Change the password")
            print("(e) enrol: Enrol in a random subject")
            print("(r) remove: Remove a subject from the enrolment list")
            print("(s) show: Shows the enrolled subjects with their marks and grades")
            print("(x) exit")
            
            choice = input("\nEnter your choice: ").strip().lower()
            
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
        if len(current_student.enrollments) >= 4:
            print("You have reached the maximum enrollment limit of 4 subjects.")
            return
            
        print("\nEnrolling in a random subject...")
        
        # Enroll in a random subject
        enrolled_subject = current_student.enroll_random(self.subjects)
        
        if enrolled_subject:
            self.data_manager.save_data(self.students)
            print(f"Successfully enrolled in {enrolled_subject.name} (ID: {enrolled_subject.subject_id})!")
        else:
            print("No subjects available for enrollment. You may already be enrolled in all available subjects.")
    
    def _remove_subject(self):
        """Remove a subject from enrollment"""
        current_student = self._get_current_student()
        if not current_student:
            print("Session expired. Please log in again.")
            return
            
        enrollments = current_student.view_enrollments()
        
        if not enrollments:
            print("No enrollments found.")
            return
        
        print("\nCurrent Enrollments:")
        for i, enrollment in enumerate(enrollments, 1):
            subject_name = next((s.name for s in self.subjects if s.subject_id == enrollment['subject_id']), "Unknown")
            print(f"{i}. {enrollment['subject_id']} - {subject_name} (Mark: {enrollment['mark']}, Grade: {enrollment['grade']})")
        
        try:
            choice = int(input("\nSelect enrollment to remove: ")) - 1
            if 0 <= choice < len(enrollments):
                subject_id = enrollments[choice]['subject_id']
                
                if current_student.remove_subject(subject_id):
                    self.data_manager.save_data(self.students)
                    print("Subject removed successfully!")
                else:
                    print("Failed to remove subject.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
    
    def _view_enrollments(self):
        """View current enrollments"""
        current_student = self._get_current_student()
        if not current_student:
            print("Session expired. Please log in again.")
            return
            
        enrollments = current_student.view_enrollments()
        
        if not enrollments:
            print("No enrollments found.")
            return
        
        print("\nCurrent Enrollments:")
        print("-" * 60)
        print(f"{'Subject ID':<12} {'Subject Name':<20} {'Mark':<6} {'Grade':<6}")
        print("-" * 60)
        
        for enrollment in enrollments:
            subject_name = next((s.name for s in self.subjects if s.subject_id == enrollment['subject_id']), "Unknown")
            print(f"{enrollment['subject_id']:<12} {subject_name:<20} {enrollment['mark']:<6} {enrollment['grade']:<6}")
    
    def _change_password(self):
        """Change student password"""
        current_student = self._get_current_student()
        if not current_student:
            print("Session expired. Please log in again.")
            return
            
        old_password = input("Enter current password: ").strip()
        new_password = input("Enter new password: ").strip()
        
        if current_student.change_password(old_password, new_password, self.validation_service):
            self.data_manager.save_data(self.students)
            print("Password changed successfully!")
        else:
            print("Password change failed. Check your current password and new password format.")
    
    def _admin_menu(self):
        """Admin operations menu"""
        while True:
            print("\n" + "=" * 40)
            print("Admin System")
            print("=" * 40)
            print("(c) clear database: Clear all data on students.data")
            print("(g) group students: Groups students by grade")
            print("(p) partition students: Partition students to PASS/FAIL categories")
            print("(r) remove student: Remove a student by ID")
            print("(s) show: Show all students")
            print("(x) exit")
            
            choice = input("\nEnter your choice: ").strip().lower()
            
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
        # Create a temporary admin instance for operations
        admin = Admin("admin", "System Admin", "IT Department")
        students_info = admin.view_students(self.students)
        
        if not students_info:
            print("No students found.")
            return
        
        print("\nAll Registered Students:")
        print("-" * 80)
        print(f"{'Student ID':<12} {'Name':<25} {'Email':<30} {'Enrollments':<12}")
        print("-" * 80)
        
        for student_info in students_info:
            print(f"{student_info['student_id']:<12} {student_info['name']:<25} {student_info['email']:<30} {student_info['enrollment_count']:<12}")
    
    def _view_students_by_grade(self):
        """View students organized by grade"""
        # Create a temporary admin instance for operations
        admin = Admin("admin", "System Admin", "IT Department")
        grade_groups = admin.view_by_grade(self.students)
        
        print("\nStudents Organized by Grade:")
        print("=" * 60)
        
        for grade, students in grade_groups.items():
            if students:
                print(f"\n{grade} Grade Students:")
                print("-" * 40)
                print(f"{'Student ID':<12} {'Name':<20} {'Subject':<10} {'Mark':<6}")
                print("-" * 40)
                
                for student in students:
                    print(f"{student['student_id']:<12} {student['name']:<20} {student['subject_id']:<10} {student['mark']:<6}")
    
    def _categorize_students(self):
        """Categorize students into PASS/FAIL"""
        # Create a temporary admin instance for operations
        admin = Admin("admin", "System Admin", "IT Department")
        categories = admin.categorize_pass_fail(self.students)
        
        print("\nStudents Categorized by PASS/FAIL:")
        print("=" * 50)
        
        for status, students in categories.items():
            if students:
                print(f"\n{status} Students:")
                print("-" * 30)
                print(f"{'Student ID':<12} {'Name':<20} {'Subject':<10} {'Mark':<6}")
                print("-" * 30)
                
                for student in students:
                    print(f"{student['student_id']:<12} {student['name']:<20} {student['subject_id']:<10} {student['mark']:<6}")
    
    def _remove_student(self):
        """Remove individual student"""
        # Create a temporary admin instance for operations
        admin = Admin("admin", "System Admin", "IT Department")
        student_id = input("Enter student ID to remove: ").strip()
        
        if admin.remove_student(student_id, self.students):
            self.data_manager.save_data(self.students)
            print(f"Student {student_id} removed successfully!")
        else:
            print("Student not found.")
    
    def _clear_all_data(self):
        """Clear entire students.data file"""
        # Create a temporary admin instance for operations
        admin = Admin("admin", "System Admin", "IT Department")
        confirm = input("Are you sure you want to clear all data? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            if admin.clear_all(self.students):
                self.data_manager.clear_data()
                print("All data cleared successfully!")
            else:
                print("Failed to clear data.")
        else:
            print("Operation cancelled.")


if __name__ == "__main__":
    app = CLIUniApp()
    app.run()

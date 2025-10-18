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
            print(Fore.YELLOW + f"Enrolling student {name}")
            existing_ids = [s.student_id for s in self.students]
            student_id = self.validation_service.generate_student_id(existing_ids)

            new_student = Student.create_student(student_id, name, email, password)
            self.students.append(new_student)
            self.data_manager.save_data(self.students)
            
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
            
            choice = input(Fore.CYAN + "Student Course Menu (c/e/r/s/x): " + Style.RESET_ALL).strip().lower()


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
                print(Fore.GREEN + "Logged out successfully." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

    
    def _enroll_subject(self):
        """Enroll in a random subject with colored CLI feedback"""
        current_student = self._get_current_student()
        if not current_student:
            print(Fore.RED + "Session expired. Please log in again." + Style.RESET_ALL)
            return
    
        # Check enrollment limit
        if len(current_student.enrollments) >= 4:
            print(Fore.RED + "Students are allowed to enroll in 4 subjects only." + Style.RESET_ALL)
            return
    
        
        print(Fore.CYAN + "Enrolling in a random subject..." + Style.RESET_ALL)

        
        enrolled_subject = current_student.enroll_random(self.subjects)

        if enrolled_subject:
            
            self.data_manager.save_data(self.students)

        
            print(
                Fore.YELLOW
                + f"Enrolling in Subject-{enrolled_subject.subject_id}"
                + Style.RESET_ALL
            )

            print(
                Fore.YELLOW
                + f"You are now enrolled in {len(current_student.enrollments)} out of 4 subjects"
                + Style.RESET_ALL
            )

        else:
            print(
                Fore.RED
                + "No subjects available for enrollment. You may already be enrolled in all available subjects."
                + Style.RESET_ALL
            )

    def _remove_subject(self):
        """Remove a subject from enrollment (formatted exactly like screenshot)"""
        current_student = self._get_current_student()
        if not current_student:
            print(Fore.RED + "Session expired. Please log in again." + Style.RESET_ALL)
            return

        enrollments = current_student.view_enrollments()
        if not enrollments:
            print(Fore.RED + "No enrollments found." + Style.RESET_ALL)
            return

        
        try:
            subject_id = input( "Remove Subject by ID: " + Style.RESET_ALL).strip()

            
            existing_ids = [e["subject_id"] for e in enrollments]
            if subject_id not in existing_ids:
                print(Fore.RED + f"Subject ID {subject_id} not found." + Style.RESET_ALL)
                return

            
            removed = current_student.remove_subject(subject_id)
            if removed:
                self.data_manager.save_data(self.students)

             
                print(Fore.YELLOW + f"Droping Subject-{subject_id}" + Style.RESET_ALL)
                print(
                    Fore.GREEN
                    + f"You are now enrolled in {len(current_student.enrollments)} out of 4 subjects"
                    + Style.RESET_ALL
                )
            else:
                print(Fore.RED + "Failed to remove subject." + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)

    
    def _view_enrollments(self):
        """View current enrollments (formatted exactly like screenshot)"""
        current_student = self._get_current_student()
        if not current_student:
            print(Fore.RED + "Session expired. Please log in again." + Style.RESET_ALL)
            return

        enrollments = current_student.view_enrollments()

        
        if not enrollments:
            print(Fore.YELLOW + "Showing 0 subjects" + Style.RESET_ALL)
            return

        
        print(Fore.YELLOW + f"Showing {len(enrollments)} subjects" + Style.RESET_ALL)

        
        for enrollment in enrollments:
            subject_id = enrollment["subject_id"]
            mark = enrollment["mark"]
            grade = enrollment["grade"]
            print(               
                 f"[ Subject::{subject_id} -- mark = {mark} -- grade =  {grade} ]"
                + Style.RESET_ALL
            )

    
    def _change_password(self):
        """Change student password (no old password required, formatted like screenshot)"""
        current_student = self._get_current_student()
        if not current_student:
            print(Fore.RED + "Session expired. Please log in again." + Style.RESET_ALL)
            return

    
        print(Fore.YELLOW + "Updating Password" + Style.RESET_ALL)

    
        new_password = input("New Password: ").strip()
        confirm_password = input("Confirm Password: ").strip()

    
        if new_password != confirm_password:
            print(Fore.RED + "Password does not match - try again" + Style.RESET_ALL)
            return

    
        if not self.validation_service.validate_password(new_password):
            print(Fore.RED + "Invalid password format - must start with uppercase, include letters and digits" + Style.RESET_ALL)
            return

    
        from models.auth import AuthenticationService
        current_student.password_hash = AuthenticationService.hash_password(new_password)

    
        self.data_manager.save_data(self.students)
       


    
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
        """View all registered students (formatted exactly like screenshot)"""
        admin = Admin("admin", "System Admin", "IT Department")
        students_info = admin.view_students(self.students)

        if not students_info:
            print( "< Nothing to Display >  " + Style.RESET_ALL)
            return

    
        print(Fore.YELLOW + "Student list" + Style.RESET_ALL)

    
        for student_info in students_info:
            print(                
                 f"{student_info['name']} :: {student_info['student_id']} --> "
                +f"Email: {student_info['email']}"
                + Style.RESET_ALL
            )

    
    def _view_students_by_grade(self):
        """View students organized by grade (formatted exactly like screenshot)"""
        admin = Admin("admin", "System Admin", "IT Department")
        grade_groups = admin.view_by_grade(self.students)

    
        print(Fore.YELLOW + "Grade Grouping" + Style.RESET_ALL)
        if not any(grade_groups.values()):
            print( "< Nothing to Display >" + Style.RESET_ALL)
            return
    
        for grade, students in grade_groups.items():
            if students:
                for student in students:
                
                    mark_value = student.get("mark", "")
                    try:
                        mark_value = float(mark_value)
                        mark_text = f"{mark_value:.2f}"
                    except (ValueError, TypeError):
                        mark_text = str(mark_value)

                
                    print(
                        Fore.CYAN
                        + f"{grade} --> "
                        + Fore.WHITE
                        + f"({student['name']} :: {student['student_id']} --> "                       
                        + f"GRADE:  {grade} = MARK: {mark_text})"
                        + Style.RESET_ALL
                    )


    
    def _categorize_students(self):
        """Categorize students into PASS/FAIL (auto-generate grade, same logic as _view_students_by_grade)"""
        admin = Admin("admin", "System Admin", "IT Department")
        categories = admin.categorize_pass_fail(self.students)

    
        print(Fore.YELLOW + "PASS/FAIL Partition" + Style.RESET_ALL)
        
    
        for status in ["FAIL", "PASS"]:
            students = categories.get(status, [])
            if not students:
                print(      f"{status} --> []" + Style.RESET_ALL)
                continue

            formatted_students = []
            for student in students:
                mark_value = student.get("mark", "")
                try:
                    mark_value = float(mark_value)
                    mark_text = f"{mark_value:.2f}"
                except (ValueError, TypeError):
                    mark_value = None
                    mark_text = "N/A"

            
                if mark_value is not None:
                    if mark_value < 50:
                        grade = "Z"
                    elif mark_value < 65:
                        grade = "P"
                    elif mark_value < 75:
                        grade = "C"
                    elif mark_value < 85:
                        grade = "D"
                    else:
                        grade = "HD"
                else:
                    grade = "N/A"

                formatted_students.append(
                    f"{student['name']} :: {student['student_id']} --> GRADE:  {grade} - MARK: {mark_text}"
                )

        
            student_str = ", ".join(formatted_students)
            
            print(Fore.CYAN + f"{status} --> " + Fore.WHITE + f"[{student_str}]" + Style.RESET_ALL)





    
    def _remove_student(self):
        """Remove individual student (formatted exactly like screenshot)"""
        admin = Admin("admin", "System Admin", "IT Department")

    
        student_id = input("Remove by ID: " + Style.RESET_ALL).strip()

    
        if admin.remove_student(student_id, self.students):
            self.data_manager.save_data(self.students)
        
            print(Fore.YELLOW + f"Removing Student {student_id} Account" + Style.RESET_ALL)
        else:
        
            print(Fore.RED + f"Student {student_id} does not exist" + Style.RESET_ALL)

    
    def _clear_all_data(self):
        """Clear entire students.data file (formatted exactly like screenshot)"""
        admin = Admin("admin", "System Admin", "IT Department")

    
        print(Fore.YELLOW + "Clearing students database" + Style.RESET_ALL)

    
        confirm = input(Fore.RED + "Are you sure you want to clear the database (Y)ES/(N)O: " + Style.RESET_ALL).strip().lower()
    
        if confirm == "y":
            if admin.clear_all(self.students):
                self.data_manager.clear_data()
                print( Fore.YELLOW + "students data cleared" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Failed to clear data." + Style.RESET_ALL)
       
        
           



if __name__ == "__main__":
    app = CLIUniApp()
    app.run()

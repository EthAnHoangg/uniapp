"""
GUI University Application
Graphical user interface for the university enrollment system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from models import Student, Subject, ValidationService, SessionManager
from data_manager import DataManager


class GUIUniApp:
    """Graphical user interface for the university enrollment system."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI University Enrollment System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.session_manager = SessionManager()
        self.current_user: Optional[Student] = None
        self.data_manager = DataManager()
        self.validation_service = ValidationService()
        self.students: List[Student] = []
        self.subjects: List[Subject] = []
        
        # Initialize with sample subjects
        self._initialize_subjects()
        
        # Load existing students
        self.students = self.data_manager.load_data()
        
        # Start with login window
        self._create_login_window()
    
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
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()
    
    def _create_login_window(self):
        """Create the login window"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Login - Registered Students Only", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Login form
        ttk.Label(main_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(main_frame, width=30)
        self.email_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(main_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Login", command=self._handle_login).pack(pady=10)
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                                 text="For registered students only\nEmail must end with @university.com\nPassword: Uppercase start, 5+ letters, 3+ digits",
                                 font=("Arial", 9), foreground="gray")
        instructions.grid(row=4, column=0, columnspan=2, pady=10)
    
    def _handle_login(self):
        """Handle login attempt"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
        
        # Authenticate student using session manager
        if self.session_manager.login_student(email, password, self.students):
            session = self.session_manager.get_current_session()
            # Find the student object
            for student in self.students:
                if student.student_id == session.user_id:
                    self.current_user = student
                    break
            messagebox.showinfo("Success", f"Welcome, {session.user_name}!")
            self._create_enrollment_window()
        else:
            messagebox.showerror("Error", "Invalid email or password.")
    
    def _create_enrollment_window(self):
        """Create the enrollment window"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # Welcome message
        welcome_label = ttk.Label(header_frame, text=f"Welcome, {self.current_user.name}!", 
                                 font=("Arial", 14, "bold"))
        welcome_label.grid(row=0, column=0, sticky=tk.W)
        
        # Logout button
        ttk.Button(header_frame, text="Logout", command=self._logout).grid(row=0, column=1, sticky=tk.E)
        
        # Student info frame
        info_frame = ttk.LabelFrame(main_frame, text="Student Information", padding="10")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(info_frame, text=self.current_user.student_id).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(info_frame, text=self.current_user.email).grid(row=1, column=1, sticky=tk.W)
        
        # Main content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(content_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Enroll tab
        enroll_frame = ttk.Frame(notebook, padding="10")
        notebook.add(enroll_frame, text="Random Enrollment")
        self._create_enroll_tab(enroll_frame)
        
        # View enrollments tab
        view_frame = ttk.Frame(notebook, padding="10")
        notebook.add(view_frame, text="View Enrollments")
        self._create_view_tab(view_frame)
    
    def _create_enroll_tab(self, parent):
        """Create the enroll tab"""
        # Information frame
        info_frame = ttk.LabelFrame(parent, text="Random Enrollment", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Information text
        info_text = ttk.Label(info_frame, 
                             text="Click the button below to enroll in a random subject.\n"
                                  "The system will automatically select an available subject for you.",
                             font=("Arial", 10))
        info_text.pack(pady=10)
        
        # Available subjects frame (for display only)
        subjects_frame = ttk.LabelFrame(parent, text="Available Subjects (Reference Only)", padding="10")
        subjects_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for subjects (display only)
        columns = ("ID", "Name", "Description")
        self.subjects_tree = ttk.Treeview(subjects_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        self.subjects_tree.heading("ID", text="Subject ID")
        self.subjects_tree.heading("Name", text="Subject Name")
        self.subjects_tree.heading("Description", text="Description")
        
        self.subjects_tree.column("ID", width=100)
        self.subjects_tree.column("Name", width=200)
        self.subjects_tree.column("Description", width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(subjects_frame, orient=tk.VERTICAL, command=self.subjects_tree.yview)
        self.subjects_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.subjects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate subjects
        self._populate_subjects()
        
        # Enroll button
        enroll_button = ttk.Button(parent, text="Enroll in Random Subject", 
                                  command=self._enroll_subject)
        enroll_button.pack(pady=10)
    
    def _create_view_tab(self, parent):
        """Create the view enrollments tab"""
        # Current enrollments frame
        enrollments_frame = ttk.LabelFrame(parent, text="Current Enrollments", padding="10")
        enrollments_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for enrollments
        columns = ("Subject ID", "Subject Name", "Mark", "Grade", "Date")
        self.enrollments_tree = ttk.Treeview(enrollments_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        self.enrollments_tree.heading("Subject ID", text="Subject ID")
        self.enrollments_tree.heading("Subject Name", text="Subject Name")
        self.enrollments_tree.heading("Mark", text="Mark")
        self.enrollments_tree.heading("Grade", text="Grade")
        self.enrollments_tree.heading("Date", text="Enrollment Date")
        
        self.enrollments_tree.column("Subject ID", width=100)
        self.enrollments_tree.column("Subject Name", width=200)
        self.enrollments_tree.column("Mark", width=80)
        self.enrollments_tree.column("Grade", width=80)
        self.enrollments_tree.column("Date", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(enrollments_frame, orient=tk.VERTICAL, command=self.enrollments_tree.yview)
        self.enrollments_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.enrollments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate enrollments
        self._populate_enrollments()
        
        # Remove button
        remove_button = ttk.Button(parent, text="Remove Selected Enrollment", 
                                  command=self._remove_enrollment)
        remove_button.pack(pady=10)
    
    def _populate_subjects(self):
        """Populate the subjects treeview"""
        # Clear existing items
        for item in self.subjects_tree.get_children():
            self.subjects_tree.delete(item)
        
        # Add subjects
        for subject in self.subjects:
            self.subjects_tree.insert("", tk.END, values=(
                subject.subject_id,
                subject.name,
                subject.description
            ))
    
    def _populate_enrollments(self):
        """Populate the enrollments treeview"""
        # Clear existing items
        for item in self.enrollments_tree.get_children():
            self.enrollments_tree.delete(item)
        
        # Add enrollments
        for enrollment in self.current_user.enrollments:
            subject_name = next((s.name for s in self.subjects if s.subject_id == enrollment.subject_id), "Unknown")
            self.enrollments_tree.insert("", tk.END, values=(
                enrollment.subject_id,
                subject_name,
                enrollment.mark,
                enrollment.grade,
                enrollment.enrollment_date.strftime('%Y-%m-%d')
            ))
    
    def _enroll_subject(self):
        """Handle random subject enrollment"""
        # Check enrollment limit
        if len(self.current_user.enrollments) >= 4:
            messagebox.showerror("Error", "You have reached the maximum enrollment limit of 4 subjects.")
            return
        
        # Enroll in a random subject
        enrolled_subject = self.current_user.enroll_random(self.subjects)
        
        if enrolled_subject:
            self.data_manager.save_data(self.students)
            messagebox.showinfo("Success", f"Successfully enrolled in {enrolled_subject.name}!")
            self._populate_enrollments()
        else:
            if len(self.current_user.enrollments) >= 4:
                messagebox.showerror("Error", "You have reached the maximum enrollment limit of 4 subjects.")
            else:
                messagebox.showerror("Error", "No subjects available for enrollment.")
    
    def _remove_enrollment(self):
        """Handle enrollment removal"""
        selection = self.enrollments_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an enrollment to remove.")
            return
        
        # Get selected enrollment
        item = self.enrollments_tree.item(selection[0])
        subject_id = str(item['values'][0])
        subject_name = item['values'][1]
        
        # Confirm removal
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove {subject_name}?"):
            if self.current_user.remove_subject(subject_id):
                self.data_manager.save_data(self.students)
                messagebox.showinfo("Success", f"Successfully removed {subject_name}!")
                self._populate_enrollments()
            else:
                messagebox.showerror("Error", "Failed to remove enrollment.")
    
    def _logout(self):
        """Handle student logout"""
        self.current_user = None
        self._create_login_window()


if __name__ == "__main__":
    app = GUIUniApp()
    app.run()

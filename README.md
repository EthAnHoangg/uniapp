# University Enrollment System

A comprehensive university enrollment system built with Python, featuring both Command Line Interface (CLI) and Graphical User Interface (GUI) applications.

## Features

### Student Features
- **Registration**: Students can register with validated email (@university.com) and password
- **Login**: Secure authentication system
- **Subject Enrollment**: Enroll in up to 4 subjects per semester
- **Enrollment Management**: View and remove subjects from enrollment list
- **Password Management**: Change password with validation
- **Automatic Grading**: Random marks (25-100) with automatic grade calculation

### Admin Features
- **Student Management**: View all registered students
- **Grade Organization**: Organize students by grade (Z, P, C, D, HD)
- **Pass/Fail Categorization**: Categorize students as PASS/FAIL based on marks
- **Student Removal**: Remove individual students
- **Data Management**: Clear entire student database

### System Features
- **Data Persistence**: All data saved to `students.data` file
- **Input Validation**: Email and password format validation
- **Unique ID Generation**: Automatic 6-digit student IDs and 3-digit subject IDs
- **UTS Grading System**: Mark < 50 → Z; 50-64 → P; 65-74 → C; 75-84 → D; 85+ → HD

## Project Structure

```
uniapp/
├── main.py              # Main entry point
├── models/              # Core data models and business logic
│   ├── enum/
│   │   └── roles.py     # User role enumerations
│   ├── auth.py          # Authentication service
│   ├── session.py       # Session management
│   ├── session_manager.py # Global session manager
│   ├── validation.py    # Input validation service
│   ├── grading.py       # Grade calculation service
│   ├── subject.py       # Subject/course model
│   ├── enrollment.py    # Student enrollment model
│   ├── student.py       # Student model
│   └── admin.py         # Administrator model
├── repository/          # Data persistence layer
│   └── data_manager.py  # Data manager for file operations
├── cli_app.py          # Command Line Interface
├── gui_app.py          # Graphical User Interface
├── pyproject.toml     # Project configuration and dependencies
├── uv.lock            # Dependency lock file
├── students.data      # Student data file (created automatically)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Installation and Setup

1. **Clone or download the project**
2. **Ensure Python 3.12+ is installed**
3. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
4. **Install dependencies**:
   ```bash
   uv sync
   ```
5. **Run the application**:
   ```bash
   uv run main.py
   ```

## Usage

### Running the Application

```bash
uv run main.py
```

Choose your preferred interface:
- **Option 1**: Command Line Interface (CLI)
- **Option 2**: Graphical User Interface (GUI)

### CLI Application

The CLI application provides a menu-driven interface:

1. **Student Registration**: Register with name, email, and password
2. **Student Login**: Access student features
3. **Admin Login**: Access admin features
4. **Student Operations**:
   - Enroll in random subjects
   - Remove subjects
   - View enrollments
   - Change password
5. **Admin Operations**:
   - View all students
   - Organize by grade
   - Categorize PASS/FAIL
   - Remove students
   - Clear all data

### GUI Application

The GUI application provides a modern graphical interface designed exclusively for registered students (Assessment 1 - Part 2):

1. **Login Window**: Main window for student authentication (registered students only)
2. **Enrollment Window**: Tabbed interface with:
   - **Random Enrollment Tab**: One-click enrollment in random subjects
   - **View Enrollments Tab**: View and manage current enrollments
3. **Student Information Display**: Shows student ID, email, and enrollment status
4. **Enrollment Management**: Remove subjects from enrollment list

## Data Validation Rules

### Email Validation
- Must end with `@university.com`
- Example: `john.doe@university.com`

### Password Validation
- Must start with an uppercase letter
- Must contain at least 5 letters
- Must be followed by 3 or more digits
- Example: `Password123`

### Student ID Generation
- Automatically generated 6-digit unique ID
- Range: 000001 to 999999
- Padded with zeros if necessary

### Subject ID Generation
- Automatically generated 3-digit unique ID
- Range: 001 to 999

## Grading System

Based on UTS grading standards:

| Mark Range | Grade | Description |
|------------|-------|-------------|
| 0-49       | Z     | Fail        |
| 50-64      | P     | Pass        |
| 65-74      | C     | Credit      |
| 75-84      | D     | Distinction |
| 85-100     | HD    | High Distinction |

## Data Storage

- All student data is stored in `students.data` file
- JSON format for easy reading and debugging
- Automatic backup capabilities
- Persistent across application sessions

## Error Handling

The application includes comprehensive error handling for:
- Invalid input formats
- Duplicate registrations
- Enrollment limits
- File I/O operations
- Authentication failures

## Sample Data

The application comes pre-loaded with sample subjects:
- 101: Introduction to Programming
- 102: Data Structures
- 201: Software Engineering
- 301: Database Systems
- 401: Machine Learning
- 111: Calculus I
- 112: Calculus II
- 121: Physics I
- 131: Chemistry I
- 141: English Composition

## Technical Architecture

### Key Classes
- **Student**: Core student entity with enrollment management
- **Subject**: University course representation
- **Enrollment**: Junction entity linking students to subjects
- **Admin**: Administrator with student management capabilities
- **DataManager**: Handles file operations and data persistence
- **ValidationService**: Input validation and ID generation
- **GradingService**: Grade calculation based on marks
- **CLIUniApp**: Command-line interface implementation
- **GUIUniApp**: Graphical user interface implementation

## Development Notes

- Built using Python 3.12+ standard library
- Package management with uv
- GUI implemented with tkinter
- Object-oriented design with clear separation of concerns
- Comprehensive error handling and user feedback
- Extensible architecture for future enhancements

## Future Enhancements

Potential improvements could include:
- Database integration (SQLite, PostgreSQL)
- Enhanced GUI with themes and styling
- Email notifications
- Course prerequisites
- Semester management
- Grade analytics and reporting
- Multi-language support
- Web-based interface

"""
Main entry point for the University Enrollment System
Provides options to run either CLI or GUI application.
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cli_app import CLIUniApp
from gui_app import GUIUniApp


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("University Enrollment System")
    print("=" * 60)
    print("Choose your preferred interface:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\nStarting CLI Application...")
                cli_app = CLIUniApp()
                cli_app.run()
                break
            elif choice == "2":
                print("\nStarting GUI Application...")
                gui_app = GUIUniApp()
                gui_app.run()
                break
            elif choice == "3":
                print("Thank you for using the University Enrollment System!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    main()
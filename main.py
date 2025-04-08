import tkinter as tk
from tkinter import ttk
from database import Database

class CourseSelectionPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create title label
        title_label = ttk.Label(self.frame, text="Select a Course", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create course buttons
        courses = [
            "DS 3850", "FIN 3210", "DS 3620",
            "DS 3841", "DS 3520", "DS 3860"
        ]
        
        self.buttons = []
        for i, course in enumerate(courses):
            row = (i // 2) + 1
            col = i % 2
            btn = ttk.Button(
                self.frame,
                text=course,
                command=lambda c=course: self.select_course(c),
                width=15
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.buttons.append(btn)
        
        # Create back button
        back_button = ttk.Button(
            self.frame,
            text="Back",
            command=self.go_back,
            width=10
        )
        back_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")
        
        # Configure grid weights
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        for i in range(5):  # Increased range to include back button row
            self.frame.rowconfigure(i, weight=1)
    
    def select_course(self, course):
        questions = self.main_app.db.get_questions(course)
        if questions:
            print(f"Found {len(questions)} questions for {course}")
            # TODO: Show quiz interface with these questions
        else:
            print(f"No questions found for {course}")
    
    def go_back(self):
        self.hide()
        self.main_app.main_frame.lift()
    
    def show(self):
        self.frame.lift()
    
    def hide(self):
        self.frame.lower()

class QuizBowlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Bowl")
        
        # Initialize database connection
        self.db = Database()
        
        # Configure window size and position
        window_width = 400
        window_height = 400  # Increased height for course selection
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons with fixed width
        take_quiz_button = ttk.Button(self.main_frame, text="Take Quiz", command=self.take_quiz, width=15)
        admin_button = ttk.Button(self.main_frame, text="Admin", command=self.admin, width=15)
        
        # Configure grid for horizontal layout with equal spacing
        self.main_frame.grid_rowconfigure(0, weight=1)  # Vertical centering
        self.main_frame.grid_columnconfigure(0, weight=1)  # Left space
        self.main_frame.grid_columnconfigure(1, weight=0)  # Left button
        self.main_frame.grid_columnconfigure(2, weight=1)  # Middle space
        self.main_frame.grid_columnconfigure(3, weight=0)  # Right button
        self.main_frame.grid_columnconfigure(4, weight=1)  # Right space
        
        # Place buttons with equal spacing
        take_quiz_button.grid(row=0, column=1, padx=10)
        admin_button.grid(row=0, column=3, padx=10)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Create course selection page
        self.course_selection_page = CourseSelectionPage(root, self)
        self.course_selection_page.hide()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def take_quiz(self):
        self.main_frame.lower()
        self.course_selection_page.show()
    
    def admin(self):
        # Placeholder for admin functionality
        print("Admin button clicked")
    
    def on_closing(self):
        """Handle window closing event"""
        self.db.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizBowlApp(root)
    root.mainloop()

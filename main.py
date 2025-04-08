import tkinter as tk
from tkinter import ttk
from database import Database
import random
from tkinter import messagebox

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
        questions_data = self.main_app.db.get_questions(course)
        if questions_data:
            print(f"Starting quiz for {course} with {len(questions_data)} questions.")
            self.hide()
            self.main_app.start_quiz(course, questions_data)
        else:
            messagebox.showinfo("No Questions", f"No questions found for {course}.")
    
    def go_back(self):
        self.hide()
        self.main_app.main_frame.lift()
    
    def show(self):
        self.frame.lift()
    
    def hide(self):
        self.frame.lower()

class QuizPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.course = ""
        self.questions = []
        self.current_question_index = 0
        self.user_answers = {}
        
        # Widgets
        self.question_label = ttk.Label(self.frame, text="", wraplength=350, font=("Arial", 14))
        self.question_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        self.selected_answer = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self.frame, text="", variable=self.selected_answer, value="")
            rb.grid(row=i + 1, column=0, columnspan=2, pady=5, sticky="w")
            self.radio_buttons.append(rb)
            
        self.feedback_label = ttk.Label(self.frame, text="", font=("Arial", 10))
        self.feedback_label.grid(row=5, column=0, columnspan=2, pady=10)
            
        self.next_button = ttk.Button(self.frame, text="Next", command=self.next_question, width=10)
        self.next_button.grid(row=6, column=1, padx=10, pady=10, sticky="e")
        
        self.submit_button = ttk.Button(self.frame, text="Submit", command=self.submit_quiz, width=10)
        # Submit button is initially hidden, shown on last question
        
        # Configure grid weights
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=0)
        for i in range(1, 5): # Radio buttons
            self.frame.rowconfigure(i, weight=0)
        self.frame.rowconfigure(5, weight=0) # Feedback
        self.frame.rowconfigure(6, weight=1) # Buttons row

    def load_quiz(self, course, questions_data):
        self.course = course
        # Format questions: (id, question, correct_ans, opt1, opt2, opt3, opt4)
        # Shuffle options for display
        self.questions = []
        for q_data in questions_data:
            options = list(q_data[3:])
            random.shuffle(options)
            self.questions.append({
                "id": q_data[0],
                "text": q_data[1],
                "correct": q_data[2],
                "options": options
            })
        
        random.shuffle(self.questions) # Shuffle question order
        self.current_question_index = 0
        self.user_answers = {}
        self.display_question()

    def display_question(self):
        self.feedback_label.config(text="")
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {question['text']}")
            
            self.selected_answer.set(None) # Deselect previous answer
            
            options = question['options']
            for i, rb in enumerate(self.radio_buttons):
                if i < len(options):
                    rb.config(text=options[i], value=options[i], state="normal")
                else:
                    rb.config(text="", value="", state="disabled") # Hide unused radio buttons
            
            # Restore previous answer if navigating back
            if self.current_question_index in self.user_answers:
                 self.selected_answer.set(self.user_answers[self.current_question_index])
                 
            # Button visibility
            self.submit_button.grid_remove()
            self.next_button.grid(row=6, column=1, padx=10, pady=10, sticky="e")
            if self.current_question_index == len(self.questions) - 1:
                self.next_button.grid_remove()
                self.submit_button.grid(row=6, column=1, padx=10, pady=10, sticky="e")
        else:
            # Should not happen if navigation is correct
            print("Error: Question index out of bounds")

    def next_question(self):
        selected = self.selected_answer.get()
        if not selected or selected == 'None': # Check if an answer was selected
            self.feedback_label.config(text="Please select an answer.", foreground="red")
            return
            
        self.user_answers[self.current_question_index] = selected
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            # This case should be handled by the submit button visibility logic
            self.submit_quiz()

    def submit_quiz(self):
        # Ensure last question answer is saved
        selected = self.selected_answer.get()
        if not selected or selected == 'None':
            self.feedback_label.config(text="Please select an answer for the last question.", foreground="red")
            return
        self.user_answers[self.current_question_index] = selected

        # Check if all questions answered (although logic prevents skipping)
        if len(self.user_answers) != len(self.questions):
             messagebox.showwarning("Incomplete Quiz", "Please answer all questions before submitting.")
             return

        # Calculate score
        score = 0
        for i, question in enumerate(self.questions):
            if self.user_answers.get(i) == question['correct']:
                score += 1
        
        self.hide()
        self.main_app.show_score(score, len(self.questions), self.course)

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
        window_width = 500 # Adjusted width for quiz page
        window_height = 500 # Adjusted height for quiz page
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
        
        # Create quiz page
        self.quiz_page = QuizPage(root, self)
        self.quiz_page.hide()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def take_quiz(self):
        self.main_frame.lower()
        self.course_selection_page.show()
    
    def admin(self):
        # Placeholder for admin functionality
        messagebox.showinfo("Admin Area", "Admin functionality not yet implemented.")

    def start_quiz(self, course, questions_data):
        self.quiz_page.load_quiz(course, questions_data)
        self.quiz_page.show()

    def show_score(self, score, total_questions, course):
        messagebox.showinfo(
            "Quiz Complete", 
            f"You completed the {course} quiz!\n\nYour score: {score}/{total_questions}"
        )
        # Go back to course selection after showing score
        self.course_selection_page.show()
    
    def on_closing(self):
        """Handle window closing event"""
        if self.db:
            self.db.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizBowlApp(root)
    root.mainloop()

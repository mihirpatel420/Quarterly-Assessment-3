import tkinter as tk
from tkinter import ttk
from database import Database
import random
from tkinter import messagebox
from tkinter import scrolledtext # For multiline question entry

class CourseSelectionPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create title label
        title_label = ttk.Label(self.frame, text="Select a Course", font=("Arial", 35, "bold"))
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
        self.main_app.show_main_page()
    
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
        self.question_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w") # Span 3 columns
        
        self.selected_answer = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self.frame, text="", variable=self.selected_answer, value="")
            rb.grid(row=i + 1, column=0, columnspan=3, pady=5, sticky="w") # Span 3 columns
            self.radio_buttons.append(rb)
            
        self.feedback_label = ttk.Label(self.frame, text="", font=("Arial", 10))
        self.feedback_label.grid(row=5, column=0, columnspan=3, pady=10) # Span 3 columns
        
        self.back_button = ttk.Button(self.frame, text="Back", command=self.previous_question, width=10)
        # Back button is placed in display_question
            
        self.next_button = ttk.Button(self.frame, text="Next", command=self.next_question, width=10)
        # Next button is placed in display_question
        
        self.submit_button = ttk.Button(self.frame, text="Submit", command=self.submit_quiz, width=10)
        # Submit button is placed in display_question
        
        # Configure grid weights
        self.frame.columnconfigure(0, weight=1) # Space for back button
        self.frame.columnconfigure(1, weight=1) # Space for label/radios
        self.frame.columnconfigure(2, weight=1) # Space for next/submit button
        self.frame.rowconfigure(0, weight=0)
        for i in range(1, 5): # Radio buttons
            self.frame.rowconfigure(i, weight=0)
        self.frame.rowconfigure(5, weight=0) # Feedback
        self.frame.rowconfigure(6, weight=1) # Buttons row

    def load_quiz(self, course, questions_data):
        self.course = course
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
        self.feedback_label.config(text="") # Clear feedback
        if 0 <= self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {question['text']}")
            
            self.selected_answer.set(None) # Deselect previous answer (unless restoring below)
            
            # Check if this question has already been answered/feedback given
            already_answered = self.current_question_index in self.user_answers
            
            options = question['options']
            for i, rb in enumerate(self.radio_buttons):
                # Enable only if not already answered
                rb_state = "disabled" if already_answered else "normal"
                rb.config(state=rb_state) 
                if i < len(options):
                    rb.config(text=options[i], value=options[i])
                else:
                    # Ensure unused buttons are disabled regardless
                    rb.config(text="", value="", state="disabled") 
            
            # Restore previous answer if exists 
            if already_answered:
                 self.selected_answer.set(self.user_answers[self.current_question_index])
                 # Show feedback again if navigating back to an answered question
                 correct_answer = question['correct']
                 if self.user_answers[self.current_question_index] == correct_answer:
                    self.feedback_label.config(text="Correct!", foreground="green")
                 else:
                    self.feedback_label.config(text=f"Incorrect. Correct answer: {correct_answer}", foreground="red")
                 
            # --- Button Visibility Logic --- 
            self.back_button.grid_remove()
            self.next_button.grid_remove()
            self.submit_button.grid_remove()
            
            if self.current_question_index > 0:
                self.back_button.grid(row=6, column=0, padx=10, pady=10, sticky="w")
            
            if self.current_question_index < len(self.questions) - 1:
                self.next_button.grid(row=6, column=2, padx=10, pady=10, sticky="e")
            elif self.current_question_index == len(self.questions) - 1:
                self.submit_button.grid(row=6, column=2, padx=10, pady=10, sticky="e")
        else:
            print("Error: Question index out of bounds")

    def previous_question(self):
        # Allow going back, clearing feedback and enabling options on the previous question
        if self.current_question_index > 0:
            # No need to save answer here if we allow changing on return
            self.current_question_index -= 1
            self.display_question()

    def next_question(self):
        # If feedback was just shown (answer is in user_answers), proceed to next
        if self.current_question_index in self.user_answers: 
            self.current_question_index += 1
            if self.current_question_index < len(self.questions):
                self.display_question()
            # This else shouldn't be reached due to button logic, but safeguard:
            else:
                 self.submit_quiz() 
            return

        # --- First click: Check answer and show feedback --- 
        selected = self.selected_answer.get()
        if not selected or selected == 'None':
            self.feedback_label.config(text="Please select an answer.", foreground="red")
            return
            
        # Save the answer
        self.user_answers[self.current_question_index] = selected
        
        # Check correctness
        question = self.questions[self.current_question_index]
        correct_answer = question['correct']
        
        if selected == correct_answer:
            self.feedback_label.config(text="Correct!", foreground="green")
        else:
            self.feedback_label.config(text=f"Incorrect. Correct answer: {correct_answer}", foreground="red")
            
        # Disable options after answering
        for rb in self.radio_buttons:
            rb.config(state="disabled")
        
        # Note: We don't increment current_question_index here. 
        # The next click on this same button will trigger the first part of this function.

    def submit_quiz(self):
        # If feedback was just shown for the last question, calculate score
        if self.current_question_index in self.user_answers and self.current_question_index == len(self.questions) - 1:
            # Calculate score
            score = 0
            for i, question in enumerate(self.questions):
                if self.user_answers.get(i) == question['correct']:
                    score += 1
            
            self.hide()
            self.main_app.show_score(score, len(self.questions), self.course)
            return
            
        # --- First click on Submit: Check answer and show feedback --- 
        selected = self.selected_answer.get()
        if not selected or selected == 'None':
            self.feedback_label.config(text="Please select an answer for the last question.", foreground="red")
            return
            
        # Save the answer
        self.user_answers[self.current_question_index] = selected

        # Check correctness
        question = self.questions[self.current_question_index]
        correct_answer = question['correct']
        
        if selected == correct_answer:
            self.feedback_label.config(text="Correct!", foreground="green")
        else:
            self.feedback_label.config(text=f"Incorrect. Correct answer: {correct_answer}", foreground="red")
            
        # Disable options after answering
        for rb in self.radio_buttons:
            rb.config(state="disabled")
            
        # Note: We don't submit yet. The next click on this button will trigger the first part.

    def show(self):
        self.frame.lift()
    
    def hide(self):
        self.frame.lower()

class AdminLoginPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Widgets
        title_label = ttk.Label(self.frame, text="Admin Login", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        username_label = ttk.Label(self.frame, text="Username:")
        username_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = ttk.Entry(self.frame, width=30)
        self.username_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        password_label = ttk.Label(self.frame, text="Password:")
        password_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = ttk.Entry(self.frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        self.error_label = ttk.Label(self.frame, text="", foreground="red")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        login_button = ttk.Button(self.frame, text="Login", command=self.attempt_login, width=10)
        login_button.grid(row=4, column=1, sticky="e", padx=5, pady=10)
        
        back_button = ttk.Button(self.frame, text="Back", command=self.go_back, width=10)
        back_button.grid(row=4, column=0, sticky="w", padx=5, pady=10)
        
        # Configure grid weights
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=0)
        self.frame.rowconfigure(4, weight=1) # Push buttons down

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Simple hardcoded credentials
        if username == "Admin" and password == "Password123":
            self.error_label.config(text="")
            self.hide()
            self.main_app.show_admin_dashboard()
        else:
            self.error_label.config(text="Invalid username or password")
            self.password_entry.delete(0, tk.END) # Clear password field

    def go_back(self):
        self.hide()
        self.main_app.show_main_page()
        
    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.error_label.config(text="")

    def show(self):
        self.clear_fields()
        self.frame.lift()
    
    def hide(self):
        self.frame.lower()

class AdminDashboardPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Widgets
        title_label = ttk.Label(self.frame, text="Admin Dashboard", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        add_button = ttk.Button(self.frame, text="Add new questions", command=self.add_questions, width=25)
        add_button.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        view_button = ttk.Button(self.frame, text="View existing question", command=self.view_questions, width=25)
        view_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        modify_button = ttk.Button(self.frame, text="Delete/Modify questions", command=self.manage_questions, width=25)
        modify_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        logout_button = ttk.Button(self.frame, text="Logout", command=self.logout, width=10)
        logout_button.grid(row=4, column=1, sticky="e", padx=5, pady=20)
        
        # Configure grid weights
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=0)
        self.frame.rowconfigure(4, weight=1) # Push logout down

    def add_questions(self):
        self.hide()
        self.main_app.show_add_question_page()

    def view_questions(self):
        self.hide()
        self.main_app.show_view_questions_page() # Navigate to View-Only page

    def manage_questions(self):
        self.hide()
        self.main_app.show_manage_questions_page() # Navigate to Manage page

    def logout(self):
        self.hide()
        self.main_app.show_main_page()

    def show(self):
        self.frame.lift()
    
    def hide(self):
        self.frame.lower()

class AddQuestionPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.courses = [
            "DS 3850", "FIN 3210", "DS 3620",
            "DS 3841", "DS 3520", "DS 3860"
        ]
        
        # Mode: 'add' or 'edit'
        self.mode = 'add'
        self.edit_question_id = None
        
        # Widgets
        self.title_label = ttk.Label(self.frame, text="Add New Question", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        course_label = ttk.Label(self.frame, text="Course:")
        course_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.course_var = tk.StringVar()
        self.course_combobox = ttk.Combobox(self.frame, textvariable=self.course_var, values=self.courses, state="readonly", width=37)
        self.course_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.course_combobox.set(self.courses[0]) # Default value
        
        question_label = ttk.Label(self.frame, text="Question:")
        question_label.grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.question_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=40, height=5)
        self.question_text.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # --- Options Entries (Define before Correct Answer Combobox) ---
        self.option_entries = []
        self.option_vars = [] # Store StringVars for options
        for i in range(4):
            option_label = ttk.Label(self.frame, text=f"Option {i+1}:")
            option_label.grid(row=3+i, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar()
            entry = ttk.Entry(self.frame, width=40, textvariable=var)
            entry.grid(row=3+i, column=1, sticky="ew", padx=5, pady=5)
            # Update dropdown when option text changes
            var.trace_add("write", self._update_correct_answer_choices) 
            self.option_entries.append(entry)
            self.option_vars.append(var)
            
        # --- Correct Answer Combobox --- 
        correct_ans_label = ttk.Label(self.frame, text="Correct Answer:")
        correct_ans_label.grid(row=7, column=0, sticky="w", padx=5, pady=5) # Adjusted row
        self.correct_ans_var = tk.StringVar()
        self.correct_ans_combobox = ttk.Combobox(self.frame, textvariable=self.correct_ans_var, state="readonly", width=37)
        self.correct_ans_combobox.grid(row=7, column=1, sticky="ew", padx=5, pady=5) # Adjusted row
        self._update_correct_answer_choices() # Initial population
        
        self.feedback_label = ttk.Label(self.frame, text="", font=("Arial", 10))
        self.feedback_label.grid(row=8, column=0, columnspan=2, pady=10)

        self.save_button = ttk.Button(self.frame, text="Save Question", command=self.save_or_update_question, width=15)
        self.save_button.grid(row=9, column=1, sticky="e", padx=5, pady=20)
        
        self.back_button = ttk.Button(self.frame, text="Back", command=self.go_back, width=10)
        self.back_button.grid(row=9, column=0, sticky="w", padx=5, pady=20)
        
        # Configure grid weights
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=1)
        # Rows configured implicitly by widget placement

    def _update_correct_answer_choices(self, *args): # Accept trace args
        """Update the values in the correct answer combobox based on option entries."""
        current_options = [var.get().strip() for var in self.option_vars if var.get().strip()] # Get non-empty options
        
        # Keep track of the currently selected correct answer
        current_selection = self.correct_ans_var.get()
        
        # Update combobox values
        if current_options:
            self.correct_ans_combobox["values"] = current_options
            self.correct_ans_combobox.config(state="readonly")
            # If previous selection is still valid, restore it
            if current_selection in current_options:
                self.correct_ans_var.set(current_selection)
            else:
                # Optionally set to first available option or leave blank?
                # Setting to first option for now
                 self.correct_ans_var.set(current_options[0])
        else:
            # No options entered yet, disable combobox
            self.correct_ans_combobox["values"] = []
            self.correct_ans_var.set("")
            self.correct_ans_combobox.config(state="disabled")

    def load_for_edit(self, question_details):
        self.mode = 'edit'
        self.edit_question_id = question_details["id"]
        self.title_label.config(text="Edit Question")
        self.save_button.config(text="Update Question")
        self.feedback_label.config(text="")
        self.course_var.set(question_details["course"])
        self.question_text.delete("1.0", tk.END)
        self.question_text.insert("1.0", question_details["question"])
        
        # Load options first
        for i, var in enumerate(self.option_vars):
            if i < len(question_details["options"]):
                var.set(question_details["options"][i])
            else:
                var.set("")
        
        # Set correct answer AFTER options are loaded and dropdown is populated
        # _update_correct_answer_choices should be triggered by setting option vars
        # Now set the correct answer variable
        if question_details["correct_answer"] in question_details["options"]:
            self.correct_ans_var.set(question_details["correct_answer"])
        else:
             self.correct_ans_var.set("") # Handle potential inconsistency
             
        # Final update just in case trace didn't catch everything
        self._update_correct_answer_choices()

    def save_or_update_question(self):
        course = self.course_var.get()
        question = self.question_text.get("1.0", tk.END).strip()
        # Get correct answer from combobox variable
        correct_answer = self.correct_ans_var.get().strip()
        options = [var.get().strip() for var in self.option_vars]
        
        # Validation 
        if not course or not question or not correct_answer or not all(options):
            self.feedback_label.config(text="Error: All fields are required.", foreground="red")
            return
            
        if len(options) != 4:
             self.feedback_label.config(text="Error: Exactly 4 options are required.", foreground="red")
             return
             
        # Validation: correct_answer must be one of the non-empty options
        # (Handled implicitly by how the dropdown is populated, but good check)
        valid_options = [opt for opt in options if opt]
        if correct_answer not in valid_options:
             self.feedback_label.config(text="Error: Correct answer must be selected from the dropdown.", foreground="red")
             return

        if self.mode == 'edit' and self.edit_question_id is not None:
            success = self.main_app.db.update_question(
                course, self.edit_question_id, question, correct_answer, options
            )
            if success:
                self.feedback_label.config(text=f"Question ID {self.edit_question_id} updated successfully!", foreground="green")
            else:
                self.feedback_label.config(text="Error: Failed to update question.", foreground="red")

        elif self.mode == 'add':
            success = self.main_app.db.add_question(course, question, correct_answer, options)
            if success:
                self.feedback_label.config(text=f"Question added successfully to {course}!", foreground="green")
                self.clear_fields(reset_mode=False) 
            else:
                self.feedback_label.config(text="Error: Failed to add question to database.", foreground="red")
        else:
             self.feedback_label.config(text="Error: Invalid mode.", foreground="red")

    def clear_fields(self, reset_mode=True):
        if reset_mode:
            self.mode = 'add'
            self.edit_question_id = None
            self.title_label.config(text="Add New Question")
            self.save_button.config(text="Save Question")
            
        self.question_text.delete("1.0", tk.END)
        # Clear option variables (this will trigger update for correct answer dropdown)
        for var in self.option_vars:
            var.set("")
        self.course_combobox.set(self.courses[0]) 
        self.feedback_label.config(text="") 
        # Correct answer var/combo will be cleared by _update_correct_answer_choices

    def go_back(self):
        self.clear_fields(reset_mode=True) 
        self.hide()
        self.main_app.show_admin_dashboard()

    def show(self):
        if self.mode == 'add':
             self.clear_fields(reset_mode=True)
        self.feedback_label.config(text="") 
        self.frame.lift()
    
    def hide(self):
        self.frame.lower()

class ManageQuestionsPage: 
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.courses = [
            "DS 3850", "FIN 3210", "DS 3620",
            "DS 3841", "DS 3520", "DS 3860"
        ]
        
        # Widgets
        title_label = ttk.Label(self.frame, text="Manage Questions (Delete/Modify)", font=("Arial", 16, "bold")) # Updated title
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        course_label = ttk.Label(self.frame, text="Select Course:")
        course_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.course_var = tk.StringVar()
        self.course_combobox = ttk.Combobox(self.frame, textvariable=self.course_var, values=self.courses, state="readonly", width=30)
        self.course_combobox.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=5) # Span 2 for better alignment
        self.course_combobox.set(self.courses[0]) # Default value
        self.course_combobox.bind("<<ComboboxSelected>>", self.load_questions)
        
        # Treeview for displaying questions
        columns = ("id", "question", "correct_answer", "option1", "option2", "option3", "option4")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=15)
        
        # Define headings and column widths (same as before)
        self.tree.heading("id", text="ID")
        self.tree.heading("question", text="Question")
        self.tree.heading("correct_answer", text="Correct Ans")
        self.tree.heading("option1", text="Opt 1")
        self.tree.heading("option2", text="Opt 2")
        self.tree.heading("option3", text="Opt 3")
        self.tree.heading("option4", text="Opt 4")
        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("question", width=250)
        self.tree.column("correct_answer", width=100)
        self.tree.column("option1", width=100)
        self.tree.column("option2", width=100)
        self.tree.column("option3", width=100)
        self.tree.column("option4", width=100)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=10)
        scrollbar.grid(row=2, column=3, sticky=(tk.N, tk.S))
        
        # Buttons Frame
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=10)
        
        self.back_button = ttk.Button(button_frame, text="Back", command=self.go_back, width=10)
        self.back_button.pack(side=tk.LEFT, padx=5)
        
        # Add Edit Button
        self.edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_selected_question, width=15, state=tk.DISABLED)
        self.edit_button.pack(side=tk.RIGHT, padx=5)
        
        self.delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_question, width=15, state=tk.DISABLED)
        self.delete_button.pack(side=tk.RIGHT, padx=5) # Place delete next to edit
        
        # Configure grid weights
        self.frame.columnconfigure(0, weight=1) # Allow treeview to expand
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(0, weight=0) # Title
        self.frame.rowconfigure(1, weight=0) # Combobox
        self.frame.rowconfigure(2, weight=1) # Treeview (expand vertically)
        self.frame.rowconfigure(3, weight=0) # Button Frame

    def on_tree_select(self, event=None):
        # Enable delete/edit buttons only if an item is selected
        if self.tree.selection():
            self.delete_button.config(state=tk.NORMAL)
            self.edit_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.DISABLED)

    def load_questions(self, event=None):
        # Clear existing items in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.delete_button.config(state=tk.DISABLED) # Disable buttons on load
        self.edit_button.config(state=tk.DISABLED)
            
        course = self.course_var.get()
        if not course:
            return
            
        questions_data = self.main_app.db.get_questions(course)
        
        if questions_data:
            for question in questions_data:
                self.tree.insert("", tk.END, values=question)
        else:
            self.tree.insert("", tk.END, values=("", "No questions found for this course.", "", "", "", "", ""))

    def delete_selected_question(self):
        selected_item = self.tree.selection() 
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a question to delete.")
            return
        
        item_data = self.tree.item(selected_item[0])
        question_id = item_data["values"][0]
        question_text = item_data["values"][1][:50] + "..." 
        
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete question ID {question_id}?\n\n'{question_text}'"
        )
        
        if confirm:
            course = self.course_var.get()
            success = self.main_app.db.delete_question(course, question_id)
            if success:
                messagebox.showinfo("Success", f"Question ID {question_id} deleted successfully.")
                self.load_questions() # Refresh the list
            else:
                messagebox.showerror("Error", f"Failed to delete question ID {question_id}.")

    def edit_selected_question(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a question to edit.")
            return
            
        item_data = self.tree.item(selected_item[0])["values"]
        question_details = {
            "id": item_data[0],
            "course": self.course_var.get(),
            "question": item_data[1],
            "correct_answer": item_data[2],
            "options": list(item_data[3:])
        }
        
        self.hide()
        self.main_app.show_edit_question_page(question_details)
        
    def go_back(self):
        self.hide()
        self.main_app.show_admin_dashboard()

    def show(self):
        self.course_combobox.set(self.courses[0]) 
        self.load_questions() 
        self.delete_button.config(state=tk.DISABLED) 
        self.edit_button.config(state=tk.DISABLED)
        self.frame.lift()
    
    def hide(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.delete_button.config(state=tk.DISABLED)
        self.edit_button.config(state=tk.DISABLED)
        self.frame.lower()

class ViewQuestionsPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.courses = [
            "DS 3850", "FIN 3210", "DS 3620",
            "DS 3841", "DS 3520", "DS 3860"
        ]
        
        # Widgets
        title_label = ttk.Label(self.frame, text="View Questions", font=("Arial", 16, "bold")) 
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        course_label = ttk.Label(self.frame, text="Select Course:")
        course_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.course_var = tk.StringVar()
        self.course_combobox = ttk.Combobox(self.frame, textvariable=self.course_var, values=self.courses, state="readonly", width=30)
        self.course_combobox.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        self.course_combobox.set(self.courses[0]) # Default value
        self.course_combobox.bind("<<ComboboxSelected>>", self.load_questions)
        
        # Treeview for displaying questions
        columns = ("id", "question", "correct_answer", "option1", "option2", "option3", "option4")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=15)
        
        # Define headings and column widths (same as before)
        self.tree.heading("id", text="ID")
        self.tree.heading("question", text="Question")
        self.tree.heading("correct_answer", text="Correct Ans")
        self.tree.heading("option1", text="Opt 1")
        self.tree.heading("option2", text="Opt 2")
        self.tree.heading("option3", text="Opt 3")
        self.tree.heading("option4", text="Opt 4")
        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("question", width=250)
        self.tree.column("correct_answer", width=100)
        self.tree.column("option1", width=100)
        self.tree.column("option2", width=100)
        self.tree.column("option3", width=100)
        self.tree.column("option4", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=10)
        scrollbar.grid(row=2, column=3, sticky=(tk.N, tk.S))
        
        # Buttons Frame
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=10)
        
        self.back_button = ttk.Button(button_frame, text="Back", command=self.go_back, width=10)
        self.back_button.pack(side=tk.LEFT, padx=5)
                
        # Configure grid weights
        self.frame.columnconfigure(0, weight=1) 
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(0, weight=0) 
        self.frame.rowconfigure(1, weight=0) 
        self.frame.rowconfigure(2, weight=1) 
        self.frame.rowconfigure(3, weight=0) 

    def load_questions(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
                    
        course = self.course_var.get()
        if not course:
            return
            
        questions_data = self.main_app.db.get_questions(course)
        
        if questions_data:
            for question in questions_data:
                self.tree.insert("", tk.END, values=question)
        else:
            self.tree.insert("", tk.END, values=("", "No questions found for this course.", "", "", "", "", ""))

    def go_back(self):
        self.hide()
        self.main_app.show_admin_dashboard()

    def show(self):
        self.course_combobox.set(self.courses[0]) 
        self.load_questions() 
        self.frame.lift()
    
    def hide(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.frame.lower()
        
class QuizBowlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Bowl")
        
        # --- Style Configuration --- 
        style = ttk.Style(root)
        try:
            # Attempt to use a cleaner theme
            style.theme_use('clam') 
        except tk.TclError:
            print("Theme 'clam' not available, using default.")
            
        # Set a consistent background color
        background_color = "#f0f0f0"
        self.root.config(bg=background_color)
        style.configure('.', background=background_color) # Apply to root style
        style.configure('TFrame', background=background_color) # Apply to Frames
        style.configure('TLabel', background=background_color) # Apply to Labels
        style.configure('TRadiobutton', background=background_color) # Apply to Radiobuttons
        # Note: TButton background might be theme-specific, but let's try
        style.configure('TButton', background=background_color) 

        # Define a custom style for larger buttons with bigger font
        # Inherit background from default TButton if possible
        style.configure("Large.TButton", font=("Arial", 30), padding=(60, 120)) 
        
        # Initialize database connection
        self.db = Database()
        
        # Configure window size and position
        window_width = 900 
        window_height = 600 
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame (will inherit background from TFrame style)
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add decorative welcome label (will inherit background from TLabel style)
        welcome_label = ttk.Label(self.main_frame, text="Welcome to the Quiz Bowl", font=("Arial", 50, "bold")) 
        welcome_label.grid(row=0, column=0, columnspan=5, pady=(10, 30)) 
        
        # Create buttons with fixed width and apply the custom style
        take_quiz_button = ttk.Button(self.main_frame, text="Take Quiz", command=self.take_quiz, style="Large.TButton") 
        admin_button = ttk.Button(self.main_frame, text="Admin", command=self.admin_login, style="Large.TButton") 
        
        # Configure grid for horizontal layout with equal spacing
        self.main_frame.grid_rowconfigure(0, weight=1)  # Welcome Label row (pushes down)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Button row (centers vertically)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Space below buttons (pushes up)
        
        self.main_frame.grid_columnconfigure(0, weight=1)  # Left space
        self.main_frame.grid_columnconfigure(1, weight=0)  # Left button
        self.main_frame.grid_columnconfigure(2, weight=1)  # Middle space
        self.main_frame.grid_columnconfigure(3, weight=0)  # Right button
        self.main_frame.grid_columnconfigure(4, weight=1)  # Right space
        
        # Place buttons with equal spacing (now on row 1)
        take_quiz_button.grid(row=1, column=1, padx=10, sticky="nsew") # Changed sticky to nsew
        admin_button.grid(row=1, column=3, padx=10, sticky="nsew") # Changed sticky to nsew
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # --- Initialize Pages --- 
        self.course_selection_page = CourseSelectionPage(root, self)
        self.course_selection_page.hide()
        
        self.quiz_page = QuizPage(root, self)
        self.quiz_page.hide()
        
        self.admin_login_page = AdminLoginPage(root, self)
        self.admin_login_page.hide()
        
        self.admin_dashboard_page = AdminDashboardPage(root, self)
        self.admin_dashboard_page.hide()
        
        self.add_question_page = AddQuestionPage(root, self)
        self.add_question_page.hide()
        
        self.view_questions_page = ViewQuestionsPage(root, self) # View Only
        self.view_questions_page.hide()
        
        self.manage_questions_page = ManageQuestionsPage(root, self) # Delete/Modify
        self.manage_questions_page.hide()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Show main page initially
        self.show_main_page()
    
    def show_main_page(self):
        # Hide all other pages
        self.course_selection_page.hide()
        self.quiz_page.hide()
        self.admin_login_page.hide()
        self.admin_dashboard_page.hide()
        self.add_question_page.hide() 
        self.view_questions_page.hide() 
        self.manage_questions_page.hide() # Hide manage page too
        # Show main frame
        self.main_frame.lift()
    
    def take_quiz(self):
        self.main_frame.lower()
        self.course_selection_page.show()
    
    def admin_login(self):
        self.main_frame.lower()
        self.admin_login_page.show()

    def show_admin_dashboard(self):
        # Hide pages admin might be coming from
        self.admin_login_page.hide()
        self.add_question_page.hide() 
        self.view_questions_page.hide()
        self.manage_questions_page.hide()
        # Show dashboard
        self.admin_dashboard_page.show()
        
    def show_add_question_page(self):
        self.admin_dashboard_page.hide()
        # Ensure Add page is in 'add' mode
        self.add_question_page.clear_fields(reset_mode=True)
        self.add_question_page.show()
        
    def show_view_questions_page(self):
        self.admin_dashboard_page.hide()
        self.manage_questions_page.hide() # Ensure manage page is hidden
        self.view_questions_page.show()
        
    def show_manage_questions_page(self):
        self.admin_dashboard_page.hide()
        self.view_questions_page.hide() # Ensure view page is hidden
        self.manage_questions_page.show()
        
    def show_edit_question_page(self, question_details):
        self.manage_questions_page.hide()
        # Load data into AddQuestionPage and show it
        self.add_question_page.load_for_edit(question_details) 
        self.add_question_page.show()

    def start_quiz(self, course, questions_data):
        self.course_selection_page.hide() # Ensure course selection is hidden
        self.quiz_page.load_quiz(course, questions_data)
        self.quiz_page.show()

    def show_score(self, score, total_questions, course):
        self.quiz_page.hide() # Hide quiz page before showing score
        messagebox.showinfo(
            "Quiz Complete", 
            f"You completed the {course} quiz!\n\nYour score: {score}/{total_questions}"
        )
        self.course_selection_page.show() # Return to course selection
    
    def on_closing(self):
        """Handle window closing event"""
        if self.db:
            self.db.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizBowlApp(root)
    root.mainloop()

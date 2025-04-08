import tkinter as tk
from tkinter import ttk

class QuizBowlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Bowl")
        
        # Configure window size and position
        window_width = 300
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create and configure main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons
        take_quiz_button = ttk.Button(main_frame, text="Take Quiz", command=self.take_quiz)
        admin_button = ttk.Button(main_frame, text="Admin", command=self.admin)
        
        # Configure grid for horizontal layout
        main_frame.grid_rowconfigure(0, weight=1)  # Vertical centering
        main_frame.grid_columnconfigure(0, weight=1)  # Left button
        main_frame.grid_columnconfigure(1, weight=1)  # Space between
        main_frame.grid_columnconfigure(2, weight=1)  # Right button
        
        # Place buttons with padding
        take_quiz_button.grid(row=0, column=0, padx=10, sticky="ew")
        admin_button.grid(row=0, column=2, padx=10, sticky="ew")
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
    
    def take_quiz(self):
        # Placeholder for take quiz functionality
        print("Take Quiz button clicked")
    
    def admin(self):
        # Placeholder for admin functionality
        print("Admin button clicked")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizBowlApp(root)
    root.mainloop()

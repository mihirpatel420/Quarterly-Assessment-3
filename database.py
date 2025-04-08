import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file="quiz_bowl.db"):
        self.db_file = db_file
        self.conn = None
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        """Create a database connection to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Successfully connected to SQLite database: {self.db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        """Create tables for each course"""
        try:
            cursor = self.conn.cursor()
            
            # Create table for DS 3850
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ds3850 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    option1 TEXT NOT NULL,
                    option2 TEXT NOT NULL,
                    option3 TEXT NOT NULL,
                    option4 TEXT NOT NULL
                )
            ''')
            
            # Create table for FIN 3210
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fin3210 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    option1 TEXT NOT NULL,
                    option2 TEXT NOT NULL,
                    option3 TEXT NOT NULL,
                    option4 TEXT NOT NULL
                )
            ''')
            
            # Create table for DS 3620
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ds3620 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    option1 TEXT NOT NULL,
                    option2 TEXT NOT NULL,
                    option3 TEXT NOT NULL,
                    option4 TEXT NOT NULL
                )
            ''')
            
            # Create table for DS 3841
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ds3841 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    option1 TEXT NOT NULL,
                    option2 TEXT NOT NULL,
                    option3 TEXT NOT NULL,
                    option4 TEXT NOT NULL
                )
            ''')
            
            # Create table for DS 3520
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ds3520 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    option1 TEXT NOT NULL,
                    option2 TEXT NOT NULL,
                    option3 TEXT NOT NULL,
                    option4 TEXT NOT NULL
                )
            ''')
            
            # Create table for DS 3860
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ds3860 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    option1 TEXT NOT NULL,
                    option2 TEXT NOT NULL,
                    option3 TEXT NOT NULL,
                    option4 TEXT NOT NULL
                )
            ''')
            
            self.conn.commit()
            print("Course tables created successfully")
        except Error as e:
            print(f"Error creating tables: {e}")

    def add_question(self, course, question_text, correct_answer, options):
        """Add a question to a specific course table"""
        try:
            cursor = self.conn.cursor()
            table_name = course.lower().replace(" ", "")
            cursor.execute(f'''
                INSERT INTO {table_name} 
                (question_text, correct_answer, option1, option2, option3, option4)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (question_text, correct_answer, *options))
            self.conn.commit()
            return True
        except Error as e:
            print(f"Error adding question: {e}")
            return False

    def get_questions(self, course):
        """Get all questions for a specific course"""
        try:
            cursor = self.conn.cursor()
            table_name = course.lower().replace(" ", "")
            cursor.execute(f'SELECT * FROM {table_name}')
            return cursor.fetchall()
        except Error as e:
            print(f"Error getting questions: {e}")
            return []

    def close_connection(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed") 
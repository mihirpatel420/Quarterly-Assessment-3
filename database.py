import sqlite3
from sqlite3 import Error
import os # Import os module

class Database:
    def __init__(self, db_file="quiz_bowl.db"):
        self.db_file = db_file
        # Check if the database file already exists *before* connecting
        db_existed = os.path.exists(self.db_file)
        
        self.conn = None
        self.create_connection()
        self.create_tables()
        
        # Only populate if the database did NOT exist before this run
        if not db_existed:
            print("Database file not found, populating with initial questions...")
            self.populate_all_questions()
        else:
            print("Database file found, skipping population.")

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

    def populate_all_questions(self):
        """Populate all course tables with sample questions"""
        self.populate_ds3850_questions()
        self.populate_fin3210_questions()
        self.populate_ds3620_questions()
        self.populate_ds3841_questions()
        self.populate_ds3520_questions()
        self.populate_ds3860_questions()

    def populate_ds3850_questions(self):
        """Populate DS 3850 table with sample questions"""
        questions = [
            {
                "question": "What is the primary purpose of a Business Requirements Document (BRD)?",
                "correct": "To define the business needs and objectives of a project",
                "options": [
                    "To define the business needs and objectives of a project",
                    "To list all technical specifications",
                    "To document the project budget",
                    "To track project milestones"
                ]
            },
            {
                "question": "Which of the following is NOT a common phase in the Software Development Life Cycle (SDLC)?",
                "correct": "Marketing",
                "options": [
                    "Planning",
                    "Analysis",
                    "Marketing",
                    "Implementation"
                ]
            },
            {
                "question": "What is the main advantage of using Agile methodology in business application development?",
                "correct": "Flexibility to adapt to changing requirements",
                "options": [
                    "Fixed project timeline",
                    "Flexibility to adapt to changing requirements",
                    "Lower development costs",
                    "Fewer team meetings"
                ]
            },
            {
                "question": "In database design, what is the purpose of normalization?",
                "correct": "To reduce data redundancy and improve data integrity",
                "options": [
                    "To increase storage space",
                    "To reduce data redundancy and improve data integrity",
                    "To speed up data retrieval",
                    "To simplify database queries"
                ]
            },
            {
                "question": "What is the role of a Business Analyst in application development?",
                "correct": "To bridge the gap between business stakeholders and technical teams",
                "options": [
                    "To write code for the application",
                    "To manage the project budget",
                    "To bridge the gap between business stakeholders and technical teams",
                    "To test the final application"
                ]
            },
            {
                "question": "Which of these is NOT a common type of business application?",
                "correct": "Video Game",
                "options": [
                    "Customer Relationship Management (CRM)",
                    "Enterprise Resource Planning (ERP)",
                    "Video Game",
                    "Human Resource Management System (HRMS)"
                ]
            },
            {
                "question": "What is the purpose of User Acceptance Testing (UAT)?",
                "correct": "To verify that the system meets business requirements",
                "options": [
                    "To find all bugs in the system",
                    "To verify that the system meets business requirements",
                    "To test system performance",
                    "To document system features"
                ]
            },
            {
                "question": "In business application security, what does 'RBAC' stand for?",
                "correct": "Role-Based Access Control",
                "options": [
                    "Role-Based Access Control",
                    "Random Basic Access Control",
                    "Remote Backup Access Control",
                    "Role-Based Authentication Control"
                ]
            },
            {
                "question": "What is the primary goal of Business Process Reengineering (BPR)?",
                "correct": "To redesign business processes for significant improvement",
                "options": [
                    "To maintain existing processes",
                    "To reduce employee count",
                    "To redesign business processes for significant improvement",
                    "To increase IT infrastructure"
                ]
            },
            {
                "question": "Which of these is a key characteristic of a good business application?",
                "correct": "Scalability",
                "options": [
                    "Complexity",
                    "High cost",
                    "Scalability",
                    "Long development time"
                ]
            }
        ]
        self._populate_course_questions("DS 3850", questions)

    def populate_fin3210_questions(self):
        """Populate FIN 3210 table with sample questions"""
        questions = [
            {
                "question": "What is the primary goal of financial management?",
                "correct": "Maximize shareholder wealth",
                "options": [
                    "Maximize shareholder wealth",
                    "Minimize employee costs",
                    "Maximize market share",
                    "Minimize tax payments"
                ]
            },
            {
                "question": "Which of these is NOT a component of working capital management?",
                "correct": "Long-term debt",
                "options": [
                    "Accounts receivable",
                    "Inventory",
                    "Long-term debt",
                    "Accounts payable"
                ]
            },
            {
                "question": "What does the Time Value of Money principle state?",
                "correct": "Money available now is worth more than the same amount in the future",
                "options": [
                    "Money available now is worth more than the same amount in the future",
                    "All money has equal value regardless of timing",
                    "Future money is always worth more than present money",
                    "Money value is constant over time"
                ]
            },
            {
                "question": "What is the purpose of capital budgeting?",
                "correct": "To evaluate long-term investment decisions",
                "options": [
                    "To manage daily operations",
                    "To evaluate long-term investment decisions",
                    "To track employee expenses",
                    "To calculate tax liabilities"
                ]
            },
            {
                "question": "Which ratio measures a company's ability to pay short-term obligations?",
                "correct": "Current ratio",
                "options": [
                    "Debt-to-equity ratio",
                    "Current ratio",
                    "Return on equity",
                    "Gross profit margin"
                ]
            },
            {
                "question": "What is the main purpose of financial forecasting?",
                "correct": "To predict future financial performance",
                "options": [
                    "To record past transactions",
                    "To predict future financial performance",
                    "To calculate current taxes",
                    "To track employee attendance"
                ]
            },
            {
                "question": "Which of these is a source of long-term financing?",
                "correct": "Common stock",
                "options": [
                    "Accounts payable",
                    "Common stock",
                    "Short-term loans",
                    "Accrued expenses"
                ]
            },
            {
                "question": "What does the term 'leverage' refer to in finance?",
                "correct": "The use of debt to finance assets",
                "options": [
                    "The use of debt to finance assets",
                    "The total number of employees",
                    "The company's market share",
                    "The amount of cash on hand"
                ]
            },
            {
                "question": "Which of these is NOT a capital budgeting technique?",
                "correct": "Inventory turnover",
                "options": [
                    "Net Present Value",
                    "Internal Rate of Return",
                    "Inventory turnover",
                    "Payback Period"
                ]
            },
            {
                "question": "What is the primary purpose of financial statement analysis?",
                "correct": "To evaluate a company's financial health",
                "options": [
                    "To calculate employee bonuses",
                    "To evaluate a company's financial health",
                    "To track daily sales",
                    "To manage inventory levels"
                ]
            }
        ]
        self._populate_course_questions("FIN 3210", questions)

    def populate_ds3620_questions(self):
        """Populate DS 3620 table with sample questions"""
        questions = [
            {
                "question": "What is the primary goal of business analytics?",
                "correct": "To make data-driven business decisions",
                "options": [
                    "To make data-driven business decisions",
                    "To store large amounts of data",
                    "To create visual reports",
                    "To manage IT infrastructure"
                ]
            },
            {
                "question": "Which of these is NOT a type of business analytics?",
                "correct": "Speculative analytics",
                "options": [
                    "Descriptive analytics",
                    "Predictive analytics",
                    "Speculative analytics",
                    "Prescriptive analytics"
                ]
            },
            {
                "question": "What is the purpose of data visualization in business analytics?",
                "correct": "To communicate insights effectively",
                "options": [
                    "To store data securely",
                    "To communicate insights effectively",
                    "To process data faster",
                    "To reduce data size"
                ]
            },
            {
                "question": "Which tool is commonly used for business analytics?",
                "correct": "Tableau",
                "options": [
                    "Photoshop",
                    "Tableau",
                    "Word",
                    "PowerPoint"
                ]
            },
            {
                "question": "What is the first step in the analytics process?",
                "correct": "Define the business problem",
                "options": [
                    "Define the business problem",
                    "Collect data",
                    "Analyze data",
                    "Present results"
                ]
            },
            {
                "question": "Which of these is a key performance indicator (KPI)?",
                "correct": "Customer retention rate",
                "options": [
                    "Office temperature",
                    "Employee lunch breaks",
                    "Customer retention rate",
                    "Number of meetings"
                ]
            },
            {
                "question": "What is the purpose of predictive analytics?",
                "correct": "To forecast future outcomes",
                "options": [
                    "To describe past events",
                    "To store historical data",
                    "To forecast future outcomes",
                    "To create visualizations"
                ]
            },
            {
                "question": "Which of these is NOT a data analysis technique?",
                "correct": "Data deletion",
                "options": [
                    "Regression analysis",
                    "Cluster analysis",
                    "Data deletion",
                    "Time series analysis"
                ]
            },
            {
                "question": "What is the role of data mining in business analytics?",
                "correct": "To discover patterns in large datasets",
                "options": [
                    "To delete unnecessary data",
                    "To create data backups",
                    "To discover patterns in large datasets",
                    "To format data for storage"
                ]
            },
            {
                "question": "Which of these is a benefit of business analytics?",
                "correct": "Improved decision-making",
                "options": [
                    "Reduced data storage",
                    "Improved decision-making",
                    "Fewer employees needed",
                    "Lower IT costs"
                ]
            }
        ]
        self._populate_course_questions("DS 3620", questions)

    def populate_ds3841_questions(self):
        """Populate DS 3841 table with sample questions"""
        questions = [
            {
                "question": "What is the primary purpose of a Management Information System?",
                "correct": "To support decision-making and business operations",
                "options": [
                    "To support decision-making and business operations",
                    "To replace human managers",
                    "To store employee records",
                    "To manage social media"
                ]
            },
            {
                "question": "Which of these is NOT a component of an MIS?",
                "correct": "Employee lunch schedules",
                "options": [
                    "Hardware",
                    "Software",
                    "Employee lunch schedules",
                    "Data"
                ]
            },
            {
                "question": "What is the role of a Database Management System in MIS?",
                "correct": "To organize and manage data efficiently",
                "options": [
                    "To organize and manage data efficiently",
                    "To create PowerPoint presentations",
                    "To manage employee schedules",
                    "To design company logos"
                ]
            },
            {
                "question": "Which of these is a type of MIS?",
                "correct": "Transaction Processing System",
                "options": [
                    "Employee Scheduling System",
                    "Transaction Processing System",
                    "Social Media System",
                    "Email System"
                ]
            },
            {
                "question": "What is the purpose of system integration in MIS?",
                "correct": "To ensure different systems work together",
                "options": [
                    "To ensure different systems work together",
                    "To create separate systems",
                    "To reduce system functionality",
                    "To increase system complexity"
                ]
            },
            {
                "question": "Which of these is a benefit of MIS?",
                "correct": "Improved decision-making",
                "options": [
                    "Reduced employee count",
                    "Improved decision-making",
                    "Lower electricity costs",
                    "Fewer meetings"
                ]
            },
            {
                "question": "What is the role of business intelligence in MIS?",
                "correct": "To analyze and present business information",
                "options": [
                    "To analyze and present business information",
                    "To manage employee benefits",
                    "To track office supplies",
                    "To schedule meetings"
                ]
            },
            {
                "question": "Which of these is NOT a characteristic of a good MIS?",
                "correct": "Complexity",
                "options": [
                    "Accuracy",
                    "Timeliness",
                    "Complexity",
                    "Relevance"
                ]
            },
            {
                "question": "What is the purpose of data security in MIS?",
                "correct": "To protect sensitive business information",
                "options": [
                    "To protect sensitive business information",
                    "To increase data storage",
                    "To speed up data processing",
                    "To reduce system costs"
                ]
            },
            {
                "question": "Which of these is a challenge in implementing MIS?",
                "correct": "User resistance to change",
                "options": [
                    "User resistance to change",
                    "Too much data storage",
                    "Low electricity costs",
                    "Excess employee training"
                ]
            }
        ]
        self._populate_course_questions("DS 3841", questions)

    def populate_ds3520_questions(self):
        """Populate DS 3520 table with sample questions"""
        questions = [
            {
                "question": "What is the primary goal of supply chain management?",
                "correct": "To optimize the flow of goods and services",
                "options": [
                    "To optimize the flow of goods and services",
                    "To maximize employee benefits",
                    "To reduce office space",
                    "To increase meeting frequency"
                ]
            },
            {
                "question": "Which of these is NOT a component of logistics?",
                "correct": "Employee training",
                "options": [
                    "Transportation",
                    "Warehousing",
                    "Employee training",
                    "Inventory management"
                ]
            },
            {
                "question": "What is the purpose of inventory management?",
                "correct": "To maintain optimal stock levels",
                "options": [
                    "To maintain optimal stock levels",
                    "To reduce employee count",
                    "To increase office space",
                    "To schedule meetings"
                ]
            },
            {
                "question": "Which of these is a key performance indicator in SCM?",
                "correct": "Order fulfillment rate",
                "options": [
                    "Employee satisfaction",
                    "Office temperature",
                    "Order fulfillment rate",
                    "Meeting attendance"
                ]
            },
            {
                "question": "What is the role of transportation in logistics?",
                "correct": "To move goods efficiently",
                "options": [
                    "To move goods efficiently",
                    "To train employees",
                    "To manage office space",
                    "To schedule meetings"
                ]
            },
            {
                "question": "Which of these is a benefit of effective SCM?",
                "correct": "Reduced costs",
                "options": [
                    "More meetings",
                    "Reduced costs",
                    "Larger offices",
                    "More paperwork"
                ]
            },
            {
                "question": "What is the purpose of demand forecasting in SCM?",
                "correct": "To predict future product needs",
                "options": [
                    "To predict future product needs",
                    "To schedule employee vacations",
                    "To plan office parties",
                    "To organize meetings"
                ]
            },
            {
                "question": "Which of these is NOT a supply chain risk?",
                "correct": "Employee birthdays",
                "options": [
                    "Supplier failure",
                    "Transportation delays",
                    "Employee birthdays",
                    "Natural disasters"
                ]
            },
            {
                "question": "What is the role of warehousing in logistics?",
                "correct": "To store and manage inventory",
                "options": [
                    "To store and manage inventory",
                    "To train employees",
                    "To schedule meetings",
                    "To manage office space"
                ]
            },
            {
                "question": "Which of these is a trend in modern SCM?",
                "correct": "Digital transformation",
                "options": [
                    "More paperwork",
                    "Digital transformation",
                    "Less technology",
                    "More meetings"
                ]
            }
        ]
        self._populate_course_questions("DS 3520", questions)

    def populate_ds3860_questions(self):
        """Populate DS 3860 table with sample questions"""
        questions = [
            {
                "question": "What is the primary purpose of a database management system?",
                "correct": "To organize and manage data efficiently",
                "options": [
                    "To organize and manage data efficiently",
                    "To create PowerPoint presentations",
                    "To manage employee schedules",
                    "To design company logos"
                ]
            },
            {
                "question": "Which of these is NOT a type of database model?",
                "correct": "Circular model",
                "options": [
                    "Relational model",
                    "Hierarchical model",
                    "Circular model",
                    "Network model"
                ]
            },
            {
                "question": "What is the purpose of database normalization?",
                "correct": "To reduce data redundancy",
                "options": [
                    "To increase storage space",
                    "To reduce data redundancy",
                    "To slow down queries",
                    "To complicate the database"
                ]
            },
            {
                "question": "Which of these is a key component of a relational database?",
                "correct": "Tables",
                "options": [
                    "PowerPoint slides",
                    "Word documents",
                    "Tables",
                    "Email messages"
                ]
            },
            {
                "question": "What is the role of SQL in database management?",
                "correct": "To query and manipulate data",
                "options": [
                    "To query and manipulate data",
                    "To create presentations",
                    "To manage employees",
                    "To design websites"
                ]
            },
            {
                "question": "Which of these is a benefit of using a DBMS?",
                "correct": "Data integrity",
                "options": [
                    "More paperwork",
                    "Data integrity",
                    "Slower processing",
                    "Higher costs"
                ]
            },
            {
                "question": "What is the purpose of database indexing?",
                "correct": "To improve query performance",
                "options": [
                    "To improve query performance",
                    "To increase storage space",
                    "To slow down queries",
                    "To complicate the database"
                ]
            },
            {
                "question": "Which of these is NOT a database constraint?",
                "correct": "Meeting constraint",
                "options": [
                    "Primary key",
                    "Foreign key",
                    "Meeting constraint",
                    "Unique constraint"
                ]
            },
            {
                "question": "What is the role of transactions in database management?",
                "correct": "To ensure data consistency",
                "options": [
                    "To ensure data consistency",
                    "To schedule meetings",
                    "To manage employees",
                    "To create reports"
                ]
            },
            {
                "question": "Which of these is a trend in modern database management?",
                "correct": "Cloud databases",
                "options": [
                    "Paper databases",
                    "Cloud databases",
                    "Typewriter databases",
                    "Fax databases"
                ]
            }
        ]
        self._populate_course_questions("DS 3860", questions)

    def _populate_course_questions(self, course, questions):
        """Helper method to populate questions for a specific course (ONLY RUN IF DB IS NEW)"""
        # We no longer need to delete here because this method is only called for a new DB
        # cursor = self.conn.cursor()
        # table_name = course.lower().replace(" ", "")
        # cursor.execute(f"DELETE FROM {table_name}") 
        # self.conn.commit()

        # Add new questions
        print(f"Populating {course}...")
        for q in questions:
            self.add_question(course, q["question"], q["correct"], q["options"])
        # Removed the print statement from here, it's called after populate_all_questions finishes

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

    def delete_question(self, course, question_id):
        """Delete a question from a specific course table by its ID"""
        try:
            cursor = self.conn.cursor()
            table_name = course.lower().replace(" ", "")
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (question_id,))
            self.conn.commit()
            print(f"Deleted question ID {question_id} from {table_name}")
            return True
        except Error as e:
            print(f"Error deleting question ID {question_id} from {table_name}: {e}")
            return False

    def update_question(self, course, question_id, question_text, correct_answer, options):
        """Update an existing question in a specific course table"""
        try:
            cursor = self.conn.cursor()
            table_name = course.lower().replace(" ", "")
            cursor.execute(f'''
                UPDATE {table_name} 
                SET question_text = ?,
                    correct_answer = ?,
                    option1 = ?,
                    option2 = ?,
                    option3 = ?,
                    option4 = ?
                WHERE id = ?
            ''', (question_text, correct_answer, *options, question_id))
            self.conn.commit()
            print(f"Updated question ID {question_id} in {table_name}")
            return True
        except Error as e:
            print(f"Error updating question ID {question_id} in {table_name}: {e}")
            return False

    def close_connection(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed") 
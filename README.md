# Quarterly-Assessment-3

Comprehensive Quiz Bowl application with a graphical user interface (GUI)

# File overview

The main.py file is the file that is designed to be ran for the GUI to open.

The database.py file is the file that has the code relative to the database.

The quiz_bowl.db file is the file that contains the populated tables for each of the courses.

# Instructions for operating the GUI

Once you have ran the main.py file and the GUI window is displayed on your screen you will be welcomed by the home page of the Quiz Bowl which has two options.

Option 1: Take Quiz
- When this button is clicked the user is navigated to the next page which displays all the courses the user can take a quiz on. 
- Once the user clicks the course of their choosing they will be faced with n number of questions relative to the topic chosen.
- As the user attempts each problem they will recieve immediate feedback and will not be able to alter an answer choice one they submit their answer to each problem.
- Once the user has answered all questions and has submitted the quiz they will recieve an overall final score.

Option2: Admin
- When this button is clicked the user is navigated to the next page which displays a login screen. The user must get both required credentials corrent to proceed to the next page and see the 3 different options.
- The username is "Admin" and the password is "Password123"
- The first option is to add questions, when this button is clicked they will be able to add questions to specific courses and provide options and specific a correct answer. 
- The second option is the view questions, when this button is clicked the user may filter through courses to view all questions and options.
- The third option is delete/modify questions, when this button is clicked the user will be able to select a question from a specific course and can edit the question and option or delete the question.

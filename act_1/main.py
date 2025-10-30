from tkinter import *
from random import *
from time import *

# FUNCTIONS -----

def select_diff(level):
    # since this will be the first function to be run per round, we can set our score here
    global score, question_count, max_questions
    score = 0 # set baseline score
    question_count = 0 # set baseline question count
    max_questions = 3 # CONFIGURABLE - defines how many questions there are per run, made it configurable for debug purposes
    start(level)

def random_int(difficulty): # function establishes the different number values based on the passed on difficulty
    if difficulty == 'easy':
        return randint(1,9), randint(1,9)
    elif difficulty == 'moderate':
        return randint(10,99), randint(10,99)
    elif difficulty == 'advanced':
        return randint(1000,9999), randint(1000,9999)

def decide_op(): # randomizes the operation
    if randint(0,1) == 0:
        return '+'
    else:
        return '-'

def generate_question(difficulty): # creates the question given the difficulty
    x, y = random_int(difficulty) # establishes numbers
    op = decide_op() # fetches randomize operation
    question = f"{x} {op} {y}" # creates the question as a string  
    answer = eval(question) # computes the answer by using the eval function
    return question, answer

def result_display(user_score, max_count): # screen that displays once all questions are done
    result_label = Label(root, text=f"You scored: {user_score} / {max_count}!", font=("Arial", 24))
    result_label.pack(pady=15)

    # button to restart
    retry_button = Button(root, width=33, text="Try again?", command=selection)
    retry_button.pack(pady=15)


# main func, will begin when difficulty is selected.
def start(difficulty):
    for w in root.winfo_children(): # clears the current screen
        w.destroy()
    
    # setting up variables
    global c_difficulty, c_question, c_answer, score, question_count, max_questions # establishes these variables as global variables since they are used in other functions
    c_difficulty = difficulty
    c_question, c_answer = generate_question(c_difficulty) # generates the question and answer and saves it as their own respective variables

    # stops and displays results when question count matches max question count, marking the end of the current run
    if question_count >= max_questions:
        result_display(score, max_questions)
        return # prevents the rest of the function to keep running after the results

    # displays problem
    diff_display = Label(root, text=f"Difficulty: {c_difficulty}", font=("Arial", 12))
    question_label = Label(root, text=c_question, font=("Arial", 25))
    diff_display.pack(pady=15)
    question_label.pack(pady=25)

    # for user response
    response_box = Entry(root, font=("Arial", 15))
    response_box.pack(pady=5)

    # button to check/finalize answer
    submit_button = Button(root, text="Submit")
    submit_button.pack(pady=5)

    # result box, shows if correct or wrong. is hidden/blank by default
    result_label = Label(root, text="", font=("Arial", 15))
    result_label.pack(pady=15)
    
    # function for validating user answer
    def check_answer(answer):
        global score, question_count, max_questions, reattempt
        try:
            response = int(response_box.get()) # fetches the response inside the box as an integer
        except ValueError:
            result_label.config(text="Please enter a valid number.", fg="orange", font=("Arial", 25))
            return

        if answer == response:
            print('Correct!') # used for debug purposes
            result_label.config(text="Correct!", fg="green", font=("Arial", 25)) # this line of code / solution is creditted to ChatGPT, where i asked it for methods on how to make a dynamically updating display for answer results
            score += 1 # adds 1 to score

        else:
            if 'reattempt' not in globals(): # checks if the 'reattempt' variable exists, if it doesnt, then the code below will run and create the variable, this is my way of making '1 extra attempt' without making extra variable checks
                reattempt = True
                print('Incorrect!') # for debug purposes
                result_label.config(text="Incorrect! Try again.", fg="red", font=("Arial", 25))
                return # this ends this script, and makes the user try again with the same question.
            else: 
                del reattempt # following my 'existing var' logic, i delete the var so that with the logic above, reattempt will not exist for the next questions.
                print('Incorrect!') # for debug purposes
                result_label.config(text="Incorrect!", fg="red", font=("Arial", 25))

        submit_button.pack_forget() # for cleanliness and error tracing, i remove the submit button
        question_count += 1 # adds an iteration to the current question count

        print(f"{score} / {max_questions} - question {question_count}") # debug score
        
        root.after(1200, lambda: start(c_difficulty)) # makes use of the 'time' library to add a short delay when a question is finished, giving time to present the outcome
    
    submit_button.config(command=lambda: check_answer(c_answer)) # i had to configure the button to have the function AFTER the function, because inside the check_answer, i hide the button, so i had to define the button first, then the function, then insert the function into the button.

# INITIAL DIFF SELECTION -----

def selection(): # first func to run
    for w in root.winfo_children(): # clears the window
        w.destroy()
    # initial screen for choosing difficulty --
    title_label = Label(root, text="Select Difficulty", font=("Arial", 14))
    title_label.pack(pady=15)

    # different buttons for each difficulty level
    btn_easy = Button(root, text="Easy", width=33, command=lambda: select_diff('easy'))
    btn_moderate = Button(root, text="Moderate", width=33, command=lambda: select_diff('moderate'))
    btn_advanced = Button(root, text="Advanced", width=33, command=lambda: select_diff('advanced'))

    btn_easy.pack(pady=5)
    btn_moderate.pack(pady=5)
    btn_advanced.pack(pady=5)

# WINDOW PARAMETERS + SETUP -----

root = Tk()
root.geometry('455x455')
root.resizable(False,False)
root.title('Math Quiz')

# MAIN -----

selection()
root.mainloop()

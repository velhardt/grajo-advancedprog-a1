from tkinter import *
from random import *
import os

# setup, reading the files -----
script_dir = os.path.dirname(os.path.abspath(__file__)) # used, because of a problem with vsc, where the working directory is the parent directory and disables the use of relative paths within a child folder.
file_path = os.path.join(script_dir, "randomJokes.txt") # this solution is creditted to ChatGPT, with the prompt: 'upon trying to open a file in python, the file is located in the same folder as the python file, and it doesnt open. the working directory seems to be the parent folder and not in the folder where the py file is located'

with open(file_path, "r") as file:
    jokes = file.readlines()

# FUNCTIONS -----

def random_joke():
    joke = choice(jokes)
    setup, punchline = joke.split('?')
    return f'{setup}?', punchline

def display_setup():
    for w in root.winfo_children(): # clears the window
        w.destroy()
    setup, punchline = random_joke()
    setup_label = Label(root, text=setup, width=55, font=("Arial", 15))
    setup_label.place(anchor=CENTER, relx=0.5, rely=0.3)

    response_button = Button(root, text="Why?", width=55, justify=CENTER, command=lambda: display_punchline(punchline))
    response_button.place(anchor=CENTER,relx=0.5,rely=0.5)

    def display_punchline(punchline):
        punchline_label = Label(root, text=punchline, width=55, font=("Arial", 15))
        punchline_label.place(anchor=CENTER, relx=0.5, rely=0.7)
        response_button.config(text="Tell me another joke!", command=display_setup)  #changes the 'why' button back into the 'tell me a joke' button

# INITIALIZE -----

def start():
    # establish first text button
    btn_joke = Button(root, text="Tell me a joke?", width=55, justify=CENTER, command=display_setup)
    btn_joke.place(anchor=CENTER,relx=0.5,rely=0.5)

# WINDOW PARAMETERS + SETUP -----

root = Tk()
root.geometry('600x455')
root.resizable(False,False)
root.title('Jokes')

start()
root.mainloop()
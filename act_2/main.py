from tkinter import *
from random import *
import os

# setup, reading the files -----
script_dir = os.path.dirname(os.path.abspath(__file__)) # used, because of a problem with vsc, where the working directory is the parent directory and disables the use of relative paths within a child folder.
file_path = os.path.join(script_dir, "randomJokes.txt") # this solution is creditted to ChatGPT, with the prompt: 'upon trying to open a file in python, the file is located in the same folder as the python file, and it doesnt open. the working directory seems to be the parent folder and not in the folder where the py file is located'

with open(file_path, "r") as file:
    jokes = file.readlines()

# FUNCTIONS -----

def random_joke(): # function to generate the joke
    joke = choice(jokes) # a function from the random library, which just fetches a random entry from a list
    setup, punchline = joke.split('?') # splits the entry into 2 values, split based on the '?' since all jokes in the given txt file follow the same format
    return f'{setup}?', punchline # returns 2 values

def display_setup():
    for w in root.winfo_children(): # clears the window
        w.destroy()
    setup, punchline = random_joke() # establishes the two variables
    setup_label = Label(root, text=setup, width=55, font=("Arial", 15))
    setup_label.place(anchor=CENTER, relx=0.5, rely=0.3)

    response_button = Button(root, text="Why?", width=55, justify=CENTER, command=lambda: display_punchline(punchline))
    response_button.place(anchor=CENTER,relx=0.5,rely=0.5)

    def display_punchline(punchline): # displays the punchline, as well as replaces the central button, prompting the user to ask for another joke if wanted
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

from tkinter import *
from tkinter import ttk as ttk
from tkinter import messagebox
import os

# setup, reading the files -----
script_dir = os.path.dirname(os.path.abspath(__file__)) # used, because of a problem with vsc, where the working directory is the parent directory and disables the use of relative paths within a child folder.
file_path = os.path.join(script_dir, "studentMarks.txt") # creditted to chatgpt, same solution used in activity 2

with open(file_path, "r") as file:
    marks = file.readlines()

# data interpretation, establishes data
student_count = marks.pop(0) # extracts the index number
student_dict = {} # creates empty dictionary. student data will be inserted here
for student in marks: #
    separated_data = student.strip().split(',')
    
    separated_data[0] = int(separated_data[0])
    separated_data[2:] = [int(x) for x in separated_data[2:]]
    
    coursework_total = separated_data[2] + separated_data[3] + separated_data[4]
    ov_perc = (( coursework_total + separated_data[5] ) / 160) * 100
    ov_perc = round(ov_perc, 2) # rounds percentage value to the 2nd decimal place
    student_grade = lambda x: 'A' if x  >= 70 else 'B' if x >= 60 else 'C' if x >= 50 else 'D' if x >= 40 else 'F' # lambda function to return the grade

    student_dict[separated_data[0]] = { # saves new dictionary entry with student id
        "Id Number" : separated_data[0],
        "Name" : separated_data[1],
        "Coursework Total" : coursework_total,
        "Exam Mark" : separated_data[5],
        "Overall Percentage" : f"{ov_perc}%", # formats nicely
        "Student Grade" : student_grade(ov_perc)
    }


# window setup + params
root = Tk()
root.geometry('750x400')
root.configure(bg='#e8e8e8')
root.resizable(False,False)

# setting up grid
pad = Frame(root, padx=20, pady=20)
pad.grid(row=0, column=0, sticky='nsew', rowspan=15, columnspan=65)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

for i in range(65):  # columns 0–20
    pad.grid_columnconfigure(i, weight=1)
pad.grid_rowconfigure(15, weight=1)
pad.grid_rowconfigure(6, weight=1)



def main_ui():

    ## functions
    def update_text(text):
        text_box.config(state=NORMAL)
        text_box.delete('1.0', END)
        text_box.insert('1.0', text)
        text_box.config(state=DISABLED)

    def get_readable_info(data):
        lines = [f"{k}: {v}" for k, v in data.items()]
        return ("\n".join(lines))

    # viewing funcs
    def view_all_func():
        text = ""
        for id, info in student_dict.items():
            text += f"{get_readable_info(info)}\n\n"
        update_text(text)

    def view_highest_student():
        highest_id = max(student_dict, key=lambda id: float(student_dict[id]["Overall Percentage"].rstrip('%')))
        update_text(get_readable_info(student_dict[highest_id]))
            
    def view_lowest_student():
        lowest_id = min(student_dict, key=lambda id: float(student_dict[id]["Overall Percentage"].rstrip('%')))
        update_text(get_readable_info(student_dict[lowest_id]))

    def select_specific_student():
        try:
            selected_id = int(student_listbox.get().split('-')[0].strip())
        except ValueError:
            messagebox.showerror("Error", "No student selected")
            return
        if not selected_id:
            messagebox.showerror("Error", "No student selected")
            return
        update_text(get_readable_info(student_dict[selected_id]))

    def view_sorted(): #0 ascend 1 descend
        selected_sort = view_sort.current()
        if selected_sort == 1: # descending
            sorted_dict = dict(sorted(student_dict.items(), key=lambda i: float(i[1]['Overall Percentage'].rstrip('%'))))
        else: # ascending
            sorted_dict = dict(sorted(student_dict.items(), key=lambda i: float(i[1]['Overall Percentage'].rstrip('%')), reverse=True))
        text = ""
        for id, info in sorted_dict.items():
            text += f"{get_readable_info(info)}\n\n"
        update_text(text)

    def add_new_student():
        def validate_add():
            #recolors all fields to white just in case
            for e in [id_field, name_field, g1_field, g2_field, g3_field, exam_field]:
                e.config(bg="white")
            def mark_check(m): # for the 4 different marks, since they all need the same requirements
                if not (0 <= m <= 20):
                    return True
                return False
            
            error_list = []
            valid = True

            ## student id checking 
            try:
                id = int(id_field.get())
                existing_ids = []
                with open(file_path, "r") as file:
                    for line in file:
                        line = line.strip().split(',')
                        line[0] = int(line[0])
                        existing_ids.append(line[0]) # makes list of existing ids
                if id in existing_ids: # checks if id already exists.
                    raise ValueError
                if not (1000 <= id <= 9999): # checks if id is valid
                    raise ValueError
            except ValueError:
                valid = False
                id_field.config(bg="#ffcccc") 
                error_list.append("Student ID already exists or is not a valid ID (ID must be between 1000 and 9999).")

            ## student name checking
            name = name_field.get().strip()
            if not name: # checks if name field is empty
                valid = False
                name_field.config(bg="#ffcccc") 
                error_list.append("Student name cannot be empty.")

            ## CW grades checking
            # grade 1
            try:
                g1 =  int(g1_field.get())
                if mark_check(g1):
                    raise ValueError
            except ValueError:
                valid = False
                g1_field.config(bg="#ffcccc")
                error_list.append("Grade 1 is not a valid number (Grades must be between 0 and 20).")

            # grade 2
            try:
                g2 =  int(g2_field.get())
                if mark_check(g2):
                    raise ValueError
            except ValueError:
                valid = False
                g2_field.config(bg="#ffcccc")
                error_list.append("Grade 2 is not a valid number (Grades must be between 0 and 20).")

            # grade 3
            try:
                g3 =  int(g3_field.get())
                if mark_check(g3):
                    raise ValueError
            except ValueError:
                valid = False
                g3_field.config(bg="#ffcccc")
                error_list.append("Grade 3 is not a valid number (Grades must be between 0 and 20).")

            # exam grade
            try:
                exam =  int(exam_field.get())
                if not (0 <= exam <= 100):
                    raise ValueError
            except ValueError:
                valid = False
                exam_field.config(bg="#ffcccc")
                error_list.append("Exam mark is not a valid number (Grades must be between 0 and 100).")

            # final check
            if valid:
                added_string = f"{id},{name},{g1},{g2},{g3},{exam}"
                messagebox.showinfo("Success", "Successfully added new student")
                with open(file_path, 'a') as file:
                    file.write(f'\n{added_string}') # adds the new student to the txt
                
                with open(file_path, 'r') as file: # will update the total number of students at the top of the txt.
                    lines = file.readlines()

                lines[0] = str(int(lines[0].strip()) + 1) + '\n'
                with open(file_path, 'w') as file:
                    file.writelines(lines)

                add_window.destroy()
            else:
                messagebox.showerror("Invalid", f"{'\n'.join(error_list)}")

        add_window = Toplevel(root)
        add_window.title("Add new student")

        for i in range(2):  # columns 0–2
            add_window.grid_columnconfigure(i, weight=1)

        id_label = Label(add_window, text="Student ID:")
        id_label.grid(row=0, column=0, sticky='e',padx=5, pady=5)
        id_field = Entry(add_window)
        id_field.grid(row=0, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        name_label = Label(add_window, text="Student name:")
        name_label.grid(row=1, column=0, sticky='e',padx=5, pady=5)
        name_field = Entry(add_window)
        name_field.grid(row=1, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        g1_label = Label(add_window, text="CW Grade 1:")
        g1_label.grid(row=2, column=0, sticky='e',padx=5, pady=5)
        g1_field = Entry(add_window)
        g1_field.grid(row=2, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        g2_label = Label(add_window, text="CW Grade 2:")
        g2_label.grid(row=3, column=0, sticky='e',padx=5, pady=5)
        g2_field = Entry(add_window)
        g2_field.grid(row=3, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        g3_label = Label(add_window, text="CW Grade 3:")
        g3_label.grid(row=4, column=0, sticky='e',padx=5, pady=5)
        g3_field = Entry(add_window)
        g3_field.grid(row=4, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        exam_label = Label(add_window, text="Exam mark:")
        exam_label.grid(row=5, column=0, sticky='e',padx=5, pady=5)
        exam_field = Entry(add_window)
        exam_field.grid(row=5, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        submit_button = Button(add_window, text="Add student", command=validate_add)
        submit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='we')

    def delete_student():
        deleted_id = delete_listbox.get().split('-')[0].strip()
        if not deleted_id:
            messagebox.showerror("Error", "No student selected")
            return
        existing_ids = []
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip().split(',')
                line[0] = int(line[0])
                existing_ids.append(line[0])
        if int(deleted_id) not in existing_ids:
            messagebox.showerror("Error", "Student doesn't exist")
            return
        with open(file_path, 'r') as file:
            lines =  file.readlines()
        
        lines = [line for line in lines if not line.startswith(f"{deleted_id},")] # rewrites/reintegrates all content in the file, EXCEPT for the selected id

        with open(file_path, 'w') as file:
            file.writelines(lines)
        messagebox.showinfo("Success", "Deleted student succesfully.")        
        with open(file_path, 'r') as file: # will update the total number of students at the top of the txt.
            lines = file.readlines()

        lines[0] = str(int(lines[0].strip()) - 1) + '\n'
        with open(file_path, 'w') as file:
            file.writelines(lines)

    def update_student():
        def validate_update(select_id): # reused from the add student function.
            for e in [id_field, name_field, g1_field, g2_field, g3_field, exam_field]:
                e.config(bg="white")
            def mark_check(m): # for the 4 different marks, since they all need the same requirements
                if not (0 <= m <= 20):
                    return True
                return False
            
            error_list = []
            valid = True

            ## student id checking 
            try:
                id = int(id_field.get())
                existing_ids = []
                with open(file_path, "r") as file:
                    for line in file:
                        line = line.strip().split(',')
                        line[0] = int(line[0])
                        existing_ids.append(line[0]) # makes list of existing ids
                if id in existing_ids and id != int(select_id): # checks if id already exists.
                    raise ValueError
                if not (1000 <= id <= 9999): # checks if id is valid
                    raise ValueError
            except ValueError:
                valid = False
                id_field.config(bg="#ffcccc") 
                error_list.append("Student ID already exists or is not a valid ID (ID must be between 1000 and 9999).")

            ## student name checking
            name = name_field.get().strip()
            if not name: # checks if name field is empty
                valid = False
                name_field.config(bg="#ffcccc") 
                error_list.append("Student name cannot be empty.")

            ## CW grades checking
            # grade 1
            try:
                g1 =  int(g1_field.get())
                if mark_check(g1):
                    raise ValueError
            except ValueError:
                valid = False
                g1_field.config(bg="#ffcccc")
                error_list.append("Grade 1 is not a valid number (Grades must be between 0 and 20).")

            # grade 2
            try:
                g2 =  int(g2_field.get())
                if mark_check(g2):
                    raise ValueError
            except ValueError:
                valid = False
                g2_field.config(bg="#ffcccc")
                error_list.append("Grade 2 is not a valid number (Grades must be between 0 and 20).")

            # grade 3
            try:
                g3 =  int(g3_field.get())
                if mark_check(g3):
                    raise ValueError
            except ValueError:
                valid = False
                g3_field.config(bg="#ffcccc")
                error_list.append("Grade 3 is not a valid number (Grades must be between 0 and 20).")

            # exam grade
            try:
                exam =  int(exam_field.get())
                if not (0 <= exam <= 100):
                    raise ValueError
            except ValueError:
                valid = False
                exam_field.config(bg="#ffcccc")
                error_list.append("Exam mark is not a valid number (Grades must be between 0 and 100).")

            # final check
            if valid:
                updated_string = f"{id},{name},{g1},{g2},{g3},{exam}\n"
                messagebox.showinfo("Success", "Successfully added new student")
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                selected_student_index = [lines.index(l) for l in lines if l.startswith(selected_id)]
                lines[selected_student_index[0]] = updated_string
                with open(file_path, 'w') as file:
                    file.writelines(lines)

                update_window.destroy()
            else:
                messagebox.showerror("Invalid", f"{'\n'.join(error_list)}")

        ###

        selected_id = update_listbox.get().split('-')[0].strip()
        if not selected_id:
            messagebox.showerror("Error", "No student selected")
            return
        existing_ids = []
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip().split(',')
                line[0] = int(line[0])
                existing_ids.append(line[0])
        if int(selected_id) not in existing_ids:
            messagebox.showerror("Error", "Student doesn't exist")
            return
        update_window = Toplevel(root)
        update_window.title("Add new student")

        for i in range(2):  # columns 0–2
            update_window.grid_columnconfigure(i, weight=1)
        
        id_label = Label(update_window, text="Student ID:")
        id_label.grid(row=0, column=0, sticky='e',padx=5, pady=5)
        id_field = Entry(update_window)
        id_field.grid(row=0, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        name_label = Label(update_window, text="Student name:")
        name_label.grid(row=1, column=0, sticky='e',padx=5, pady=5)
        name_field = Entry(update_window)
        name_field.grid(row=1, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        g1_label = Label(update_window, text="CW Grade 1:")
        g1_label.grid(row=2, column=0, sticky='e',padx=5, pady=5)
        g1_field = Entry(update_window)
        g1_field.grid(row=2, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        g2_label = Label(update_window, text="CW Grade 2:")
        g2_label.grid(row=3, column=0, sticky='e',padx=5, pady=5)
        g2_field = Entry(update_window)
        g2_field.grid(row=3, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        g3_label = Label(update_window, text="CW Grade 3:")
        g3_label.grid(row=4, column=0, sticky='e',padx=5, pady=5)
        g3_field = Entry(update_window)
        g3_field.grid(row=4, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        exam_label = Label(update_window, text="Exam mark:")
        exam_label.grid(row=5, column=0, sticky='e',padx=5, pady=5)
        exam_field = Entry(update_window)
        exam_field.grid(row=5, column=1, sticky='we',padx=5, pady=5, columnspan=2)

        submit_button = Button(update_window, text="Update student", command=lambda: validate_update(selected_id))
        submit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='we')

        # fetches data of selected student and readies them as variables
        with open(file_path, 'r') as file:
            lines =  file.readlines()
        lines = [line for line in lines if line.startswith(f"{selected_id}")]
        lines = lines[0].strip().split(',')

        s_id = lines[0]
        s_name = lines[1]
        s_cw1 = lines[2]
        s_cw2 = lines[3]
        s_cw3 = lines[4]
        s_exam = lines[5]

        id_field.insert(0, s_id)
        name_field.insert(0, s_name)
        g1_field.insert(0, s_cw1)
        g2_field.insert(0, s_cw2)
        g3_field.insert(0, s_cw3)
        exam_field.insert(0, s_exam)

    ### main contents ###
    # initialize, clear current window
    # big box on right
    text_box = Text(pad, borderwidth=1,relief="solid", bg='#f7f7f7', font=("Courier New", 12))
    text_box.delete('1.0', END)
    text_box.config(state=DISABLED)
    text_box.grid(row=0, column=2, sticky='nsew',rowspan=20, columnspan=65, padx=5)
    ## buttons
    # first row
    view_all = Button(pad, text="View all student records", command=view_all_func)
    view_all.grid(row=0, column=0, sticky='we', padx=5, pady=5, columnspan=2)

    # sec row
    view_highest = Button(pad, text="View student with highest total score", command=view_highest_student)
    view_highest.grid(row=1, column=0, sticky='we', padx=5, pady=5, columnspan=2)

    # th row
    view_lowest = Button(pad, text="View student with lowest total score", command=view_lowest_student)
    view_lowest.grid(row=2, column=0, sticky='we', padx=5, pady=5, columnspan=2)

    # fourth row
    view_student = Button(pad, text="View specific record", command=select_specific_student)
    view_student.grid(row=3, column=1, sticky='we', padx=5, pady=5)
    student_listbox = ttk.Combobox(pad, state='readonly')
    student_listbox.grid(row=3, column=0, sticky='we', padx=5, pady=5)

    # fifth row
    view_sort = ttk.Combobox(pad, state='readonly', values=['Descending', 'Ascending'])
    view_sort.current(0)
    view_sort.grid(row=4, column=0, sticky='we', padx=5, pady=5)
    view_button = Button(pad, text="Sort by grade", command=view_sorted)
    view_button.grid(row=4, column=1, sticky='we', padx=5, pady=5)

    

    # seventh row
    add_student = Button(pad, text="Add new student", command=add_new_student)
    add_student.grid(row=6, column=0, sticky='we', padx=5, pady=5, columnspan=2)

    # eighth row
    update_listbox = ttk.Combobox(pad, state='readonly')
    update_listbox.grid(row=7, column=0, sticky='we', padx=5, pady=5)
    update_button = Button(pad, text="Update student", command=update_student)
    update_button.grid(row=7, column=1, sticky='we', padx=5, pady=5)

    # ninth row
    delete_listbox = ttk.Combobox(pad, state='readonly')
    delete_listbox.grid(row=8, column=0, sticky='we', padx=5, pady=5)
    delete_button = Button(pad, text="Delete student", command=delete_student)
    delete_button.grid(row=8, column=1, sticky='we', padx=5, pady=5)


    # contents for dropdown
    student_list = []
    for k, v in student_dict.items():
        student_list.append(f"{k} - {v["Name"]}")
    student_listbox['values'] = student_list
    delete_listbox['values'] = student_list
    update_listbox['values'] = student_list

main_ui()
root.mainloop()
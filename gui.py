import time
import FreeSimpleGUI as sg
import functions
import os

# Ensure the file exists
if not os.path.exists("todo_items.txt"):
    with open('todo_items.txt', 'w') as file:
        pass

# Define the GUI theme and layout
sg.theme("Black")
clock = sg.Text('', key='clock')
label = sg.Text("Type in a To-do")
input_box = sg.InputText(tooltip="Enter To-do", key="todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values=functions.get_todos(), key='todos',
                      enable_events=True, size=(45, 10))
edit_button = sg.Button("Edit")
complete_button = sg.Button("Complete")
exit_button = sg.Button("Exit")

# Create the window
window = sg.Window('My To-do App',
                   layout=[[clock],
                           [label],
                           [input_box],
                           [add_button],
                           [list_box, edit_button, complete_button],
                           [exit_button]],
                   font=('Helvetica', 15))

# Event loop
while True:
    try:
        event, values = window.read(timeout=100)
        # Update the clock
        if event != sg.WINDOW_CLOSED:
            window["clock"].update(value=time.strftime("%b %d, %Y %H:%M:%S"))

        # Debugging output
        print(event)
        print(values)

        # Event handling
        match event:
            case "Add":
                todos = functions.get_todos()
                new_todo = values['todo'] + "\n"
                todos.append(new_todo)
                functions.write_todos(todos)
                window['todos'].update(values=todos)

            case "Edit":
                try:
                    todo_edit = values['todos'][0]
                    new_todo = values['todo'] + "\n"

                    todos = functions.get_todos()
                    index = todos.index(todo_edit)
                    todos[index] = new_todo
                    functions.write_todos(todos)
                    window['todos'].update(values=todos)
                    window['todo'].update(value="")
                except IndexError:
                    sg.popup("Please select an Item", font=('Helvetica', 10))

            case "Complete":
                try:
                    todo_complete = values['todos'][0]
                    todos = functions.get_todos()
                    todos.remove(todo_complete)
                    functions.write_todos(todos)
                    window['todos'].update(values=todos)
                    window['todo'].update(value="")
                except IndexError:
                    sg.popup("Please select an Item", font=('Helvetica', 10))

            case "Exit":
                break

            case 'todos':
                try:
                    window['todo'].update(value=values['todos'][0].strip("\n"))
                except IndexError:
                    pass

            case sg.WINDOW_CLOSED:
                break

    except Exception as e:
        print(f"An error occurred: {e}")
        break

window.close()

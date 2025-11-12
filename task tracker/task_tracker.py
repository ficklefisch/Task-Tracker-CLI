from colorama import init
from tasks import Task
import os

init()
def start_window():
    print("Starting Task Tracker")
    
def menu():
    print("")
    print("What would you like to do? (enter index)")
    print("1. Create new task")
    print("2. Edit task")
    print("3. Delete tasks")
    print("4. Display tasks")
    print("5. Save")
    print("6. Options")
    print("7. Quit")

def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print(f"Error raised in {func.__name__}.")
    return wrapper

def menu_selection(task):
    c = input()
    os.system('cls')
    match int(c[0]):
        case 1:
            new(task)
        case 2:
            edit(task)
        case 3:
            delete(task)
        case 4:
            display(task)
        case 5:
            task.save()
        case 6:
            options(task)
        case 7:
            return True

@try_except
def new(task):
    print("Insert in the following format: title, status. Enter 'cancel' to cancel.")
    c = input().split(",")
    if c[0].lower() != 'cancel':
        c = [x.strip() for x in c]
        task.new(c[0], c[1])

@try_except
def edit(task):
    print("Insert in the following format: id, title, status. Enter 'cancel' to cancel, or '-' if you wish to not change that field.")
    c = input().split(",")
    if c[0].lower() != 'cancel':
        c = [x.strip() for x in c]
        task.edit(int(c[0]), None if c[1] == '-' else c[1], None if c[2] == '-' else c[2])

@try_except
def delete(task):
    if len(task.tasks) > 0:
        print("Select task to be deleted. Enter 'cancel' to cancel, or 'all' to delete all.")
        c = input().strip()
        if c.lower() != 'cancel':
            if c.lower() == 'all':
                print("The following tasks will be deleted: ")
                task.display_all()
                print("Are you sure?")
                if input()[0].lower() == 'y':
                    for n in range(len(task.tasks)):
                        task.delete(n + 1)
                else:
                    print("Deletion cancelled.")
            else:
                c = int(c)
                print("The following task will be deleted: ")
                task.display_short(c)
                print("Are you sure?")
                if input()[0].lower() == 'y':
                    task.delete(c)
                else:
                    print("Deletion cancelled.")
    else:
        print("There are no more tasks.")

@try_except
def options(task):
    print(f"1. Autosave: {task.autosave}")
    print(f"2. Go back...")
    print("Select options.")
    c = input().strip()
    c = int(c)
    if c == 1:
        task.autosave = not task.autosave
        os.system('cls')
        options(task)
    elif c == 2:
        pass
    else:
        print("Invalid option.")
        options(task)

@try_except
def display(task):
    print("Choose display option: ")
    print("1. Display singular")
    print("2. Display all (shortened)")
    print("3. Go back...")
    c = input().strip()
    c = int(c)
    if c == 1:
        print("Input task ID.")
        c = int(input().strip())
        task.display(c)
    elif c == 2:
        task.display_all()

task = Task()
start_window()
while(True):
    menu()
    if menu_selection(task):
        break
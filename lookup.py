import datetime

import db
import functions
import re
import task


def employee():
    functions.header_line("Enter an employee name to search for.")
    search_term = input("Enter the employee name: ")

    # Get a list of employees
    employee_list = []
    names = db.Task.select(db.Task.user_name).distinct().where(db.Task.user_name.startswith(search_term)).group_by(db.Task.user_name)
    for name in names:
        employee_list.append(name.user_name)

    if len(employee_list) == 0:
        functions.header_line("No records for employee found.")
        input("Press enter to continue.")
        return

    if len(employee_list) == 1:
        # Display the results
        display_tasks(db.Task.select().where(db.Task.user_name == employee_list[0]))

    if len(employee_list) > 1:
        # Display a list of employees
        menu_employee = functions.menu(
            "Select a employee to view tasks.",
            *employee_list,
            "Return to reports menu."
            )

        # Quit option
        if int(menu_employee) > len(employee_list):
            return

        # Display the results
        display_tasks(db.Task.select().where(db.Task.user_name == employee_list[int(menu_employee)-1]))


def date():
    while True:
        # Get a list of dates
        date_list = []
        dates = db.Task.select(db.Task.date).distinct().group_by(db.Task.date)
        for date in dates:
            date_list.append(str(date.date))

        # Display a list of employees§
        menu_date = functions.menu(
            "Select a date to view tasks.",
            *date_list,
            "Return to reports menu."
            )

        # Quit option
        if int(menu_date) > len(date_list):
            break

        # Display the results
        display_tasks(db.Task.select().where(db.Task.date == date_list[int(menu_date)-1]))


def date_range():
    message = ""
    while True:
        functions.header_line("Lookup tasks by date range.")
        functions.display_message(message)

        print("Enter the start date  in the format YYYY-MM-DD.")
        start_date = input("Leave blank for today: ").strip()
        if start_date == "":
            start_date = datetime.date.today().strftime('%Y-%m-%d')
        elif (not re.match(r'\d{4}-\d{2}-\d{2}', start_date) or
              int(start_date[5:7]) > 12 or int(start_date[8:10]) > 31):
            message = ("Invalid date {}. Date must be in the format "
                       "YYYY-MM-DD.".format(start_date))
            continue
        break

    message = ""
    while True:
        functions.header_line("Lookup tasks by date range.")
        functions.display_message(message)

        print("Enter the end date  in the format YYYY-MM-DD.")
        end_date = input("Leave blank for today: ").strip()
        if end_date == "":
            end_date = datetime.date.today().strftime('%Y-%m-%d')
        elif (not re.match(r'\d{4}-\d{2}-\d{2}', end_date) or
              int(end_date[5:7]) > 12 or int(end_date[8:10]) > 31):
            message = ("Invalid date {}. Date must be in the format "
                       "YYYY-MM-DD.".format(end_date))
            continue
        break

    display_tasks(db.Task.select().where(db.Task.date.between(start_date, end_date)))

def term():
    functions.header_line("Enter a search term to look for in the task names and notes.")
    search_term = input("Enter a term: ")

    # Display the results
    display_tasks(db.Task.select().where((db.Task.task_name.contains(search_term))|(db.Task.notes.contains(search_term))))



def display_tasks(data):
    # convert data to a list
    task_list = []
    for item in data:
        task_list.append(item)

    if len(task_list) == 0:
        functions.header_line("No results found")
        input("Press enter to continue.")
        return

    task_position = 0
    error = ""

    # Create an object for viewing and editing
    while True:
        display_task = task.Task(task=task_list[task_position],
                        header_line="Displaying task {} of {}."
                        .format(task_position + 1, len(task_list)))
        display_task.view_task()

        print("Options:")
        print("========")

        # Display options
        if task_position != 0:
            print("P: Previous task.")
        if task_position < len(data) - 1:
            print("N: Next Task.")
        print("D: Delete Task.")
        print("E: Edit Task.")
        print("Q: Return to Previous Menu.\n")

        # Display error message
        functions.display_message(error)

        # Get user choice
        select = input("Select an option: ").lower().strip()
        if select not in ('pndeq'):
            error = "Invalid option. Please select from options provided."
            continue

        # Exit menu
        if select == "q":
            break

        # Handle previous and next
        if select == "p" and task_position > 0:
            task_position -= 1
        if select == "n" and task_position < len(data) - 1:
            task_position += 1

        # Handle delete
        if select == "d":
            db.delete(task_list[task_position])
            break

        # Handle editing
        if select == "e":
            display_task.edit_task()
            break

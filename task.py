import datetime
import db
import functions
import re

class Task():
    header_line = ""
    def __init__(self, **kwargs):
        if kwargs:
            self.task = kwargs['task']
            self.header_line = kwargs['header_line']
        else:
            self.new_task()

    def new_task(self):
        """Create a new task."""
        self.header_line = "Add new task."
        task_name = self.edit("name")
        user_name = self.edit("user name")
        minutes = self.edit("minutes", "number")
        notes = self.edit("notes", "text", False)
        date = datetime.date.today().strftime('%Y-%m-%d')

        # Save
        db.save(dict([('task_name', task_name),
                ('user_name', user_name),
                ('minutes', minutes),
                ('notes', notes),
                ('date', date)]))


    def edit_task(self):
        """Edit an existing task."""
        self.header_line = ("Edit existing task: {}."
                            .format(self.task.task_name))
        self.task.date = self.edit("date", "date", True,
                                    str(self.task.date))
        self.task.task_name = self.edit("task name", "text", True,
                                    str(self.task.task_name))
        self.task.user_name = self.edit("user name", "text", True,
                                    str(self.task.user_name))
        self.task.minutes = self.edit("minutes", "number", True,
                                    str(self.task.minutes))
        self.task.notes = self.edit("notes", "text", False,
                                    str(self.task.notes))

        # Confirm screen
        self.view_task()
        if (input("Confirm the above task is correct to save Y/n: ")
            .strip().lower() != "n"):
            self.task.save()


    def view_task(self):
        """View an existing task"""
        functions.header_line(self.header_line)
        print("Date: {}".format(self.task.date))
        print("Task Name: {}".format(self.task.task_name))
        print("User Name: {}".format(self.task.user_name))
        print("Minutes Taken: {}".format(self.task.minutes))
        print("Additional Notes: {}\n".format(self.task.notes))


    def edit(self, title, type="text", required=True, value=""):
        """Handles user input"""
        message = ""
        while True:
            functions.header_line(self.header_line)
            functions.display_message(message)
            if  value!="":
                print("Leave empty for current: {}".format(value))
            text = input("Enter the task {}: ".format(title))
            if text.strip() == "":
                if value != "":
                    text = value
                elif required is True:
                    message = "Task {} cannot be empty.".format(title)
                    continue
            if type == "number" and not text.isnumeric():
                message = "Task {} must be a number.".format(title)
                continue
            if (type == "date" and (not re.match(r'\d{4}-\d{2}-\d{2}', text) or
                                    int(text[5:7]) > 12 or
                                    int(text[8:10]) > 31)):
                message = ("Invalid date {}. Date must be in the format "
                           "YYYY-MM-DD.".format(text))
                continue
            return text

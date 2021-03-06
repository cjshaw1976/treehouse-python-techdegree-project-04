import datetime
import db
import functions


class Task:
    header_line = ""

    def __init__(self, **kwargs):
        if kwargs:
            self.task = kwargs['task']
            self.header_line = kwargs['header_line']
        else:
            self.task = self.new_task()

    def new_task(self):
        """Create a new task."""
        self.header_line = "Add new task."
        task_name = functions.edit("name", self.header_line)
        user_name = functions.edit("user name", self.header_line)
        minutes = functions.edit("minutes", self.header_line, "number")
        notes = functions.edit("notes", self.header_line, "text", False)
        date = datetime.date.today().strftime('%Y-%m-%d')

        # Save
        return db.save(dict([('task_name', task_name),
                       ('user_name', user_name),
                       ('minutes', minutes),
                       ('notes', notes),
                       ('date', date)]))

    def delete_task(self):
        self.task.delete_instance()

    def edit_task(self):
        """Edit an existing task."""
        self.header_line = ("Edit existing task: {}."
                            .format(self.task.task_name))
        self.task.date = functions.edit("date", self.header_line, "date", True,
                                        str(self.task.date))
        self.task.task_name = functions.edit("task name",
                                             self.header_line, "text", True,
                                             str(self.task.task_name))
        self.task.user_name = functions.edit("user name",
                                             self.header_line, "text", True,
                                             str(self.task.user_name))
        self.task.minutes = functions.edit("minutes",
                                           self.header_line, "number", True,
                                           str(self.task.minutes))
        self.task.notes = functions.edit("notes", self.header_line,
                                         "text", False,
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

#!/usr/bin/env python3
""" Timesheet with database

C. J. Shaw
Feb 2017
"""

import db
import functions
import lookup
import task


def program_loop():
    while True:
        menu_choice = functions.menu(
            "Main Menu:",
            "Record a new task entry.",
            "Lookup previous task entries.",
            "Exit the program."
            )

        if int(menu_choice) == 1:
            new_task = task.Task()

        if int(menu_choice) == 2:
            reports_menu()

        if int(menu_choice) == 3:
            functions.clear_screen()
            break


def reports_menu():
    while True:
        menu_search = functions.menu(
            "Lookup previous task entries:",
            "Find by employee.",
            "Find by date.",
            "Find by search term.",
            "Find by date range.",
            "Return to main menu."
            )

        if int(menu_search) == 1:
            result = lookup.employee()

        if int(menu_search) == 2:
            result = lookup.date()

        if int(menu_search) == 3:
            result = lookup.term()

        if int(menu_search) == 4:
            result = lookup.date_range()

        if int(menu_search) == 5:
            functions.clear_screen()
            break

# Call the main function if run directly
if __name__ == '__main__':
    program_loop()

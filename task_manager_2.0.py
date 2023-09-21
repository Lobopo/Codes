def load_credentials(file):
    """
    Load user credentials from user.txt and return as a dictionary.

    Args:
        file (str): Filename containing user credentials.

    Returns:
        dict: Dictionary of usernames and passwords.
    """

    with open("user.txt", "r") as file:
        user_credentials = {}
        for line in file:
            username, password = line.strip().split(", ")
            user_credentials[username] = password
        return user_credentials  


def login(user_credentials):
    """
    Ask user to enter their username and password and validate against provided credentials.

    Args:
        user_credentials (dict): Dictionary containing valid usernames and passwords.

    Returns:
        str: Username of the successfully logged-in user.
    """

    while True:
        entered_username = input("Enter your username:")
        entered_password = input("Enter your password:")
        if entered_username in user_credentials and user_credentials[entered_username] == entered_password:
            print("Login successful")
            return entered_username
        else:
            print("Invalid username or password. Please try again")


def reg_user(user_credentials):
    """
    Register a new user. Asks for username and password, and saves them to a file.

    Args:
        user_credentials (dict): Dictionary containing valid usernames and passwords.
    """

    while True:
        r_username = input("Enter a new username:")
        if r_username in user_credentials:
            print("That username already exists. Please enter a different username.")
            continue
        r_password = input("Enter a new password:")
        r_password_2 = input("Confirm password:")

        while r_password_2 != r_password:
            print("Your passwords do not match, please try again")
            r_password = input("Enter a new password:")
            r_password_2 = input("Confirm password:")
        print("Thank you")
        
        with open("user.txt", "a") as file:
            user_info = f"{r_username}, {r_password}\n"
            file.write(user_info)
            break


def add_task():
    """
    Add a new task. Asks user for task details and saves them to tasks.txt file.
    """

    username = input("Enter username of assignee:")
    task_title = input("Enter the title of the task:")
    task_description = input("Enter description of task:")
    due_date = input("Enter task due date:")
    current_date = input("Enter the current date:")
    task_completed = "No"
    with open("tasks.txt", "a") as file_2:
        file_2.write(f"{username}, {task_title}, {task_description}, {due_date}, {current_date}, {task_completed}\n")


def view_all():
    """
    Display all tasks from the tasks file.
    """

    tasks = [] 
    with open("tasks.txt", "r") as task_file:
        for line in task_file:
            if not line.strip():
                continue
            details = line.strip().split(", ")
            if len(details) != 6:
                continue
            tasks.append(details)
                       
            for index, details in enumerate(tasks, 1):
                print(f"Task {index}:")               
                print("Title: \t" + details[1])
                print("Assigned to: \t" + details[0])
                print("Date Assigned: \t" + details[4])
                print("Due Date: \t" + details[3])
                print("Task Complete? \t" + details[5])
                print("Task Description: \t" + details[2])
                print('-----------------------------------')
        return tasks    


def view_mine(entered_username):
    """
    Display tasks assigned to the currently logged in user and allow them to mark tasks as completed or edit them.

    Args:
        entered_username (str): Username of the currently logged in user.
    """

    with open("tasks.txt", "r") as task_file:
        tasks = []
        task_number = 0

        for line in task_file:
            details = line.strip().split(", ")

            if details[0] == entered_username:
                tasks.append(details)
                task_number += 1

                for index, details in enumerate(tasks, 1):
    
                    print(f'Task {index}')
                    print("Title: \t" + details[1])
                    print("Assigned to: \t" + details[0])
                    print("Date Assigned: \t" + details[4])
                    print("Due Date: \t" + details[3])
                    print("Task Complete? \t" + details[5])
                    print("Task Description: \t" + details[2])
                    print('-----------------------------------')
    
    while True:
        choice = input(f'Enter the task number (1 to {len(tasks)} you want to mark as complete or enter "-1" to return to main menu:')
        if choice == '-1':
            break
    
        if choice.isdigit() and 1 <= int(choice) <= len(tasks):
            task_index = int(choice) - 1
            
            if tasks[task_index][5] == "Yes":
                print("This task is already completed and cannot be edited.")
                continue
            
            action = input("Do you want to (1) mark as complete or (2) edit the task? Enter the number: ")
            if action == "1":
                tasks[task_index][5] = 'Yes'
                print(f'Task {choice} marked as complete.')

            elif action == "2":
                edit_choice = input("Do you want to edit the (1) assigned username or (2) due date? Enter the number: ")
                
                if edit_choice == "1":
                    new_username = input("Enter new username for this task: ")
                    tasks[task_index][0] = new_username
                    print("Assigned username updated.")

                elif edit_choice == "2":
                    new_due_date = input("Enter new due date for this task: ")
                    tasks[task_index][3] = new_due_date
                    print("Due date updated.")

                else:
                    print("Invalid choice for editing. Skipping.")

            else:
                print("Invalid action. Skipping.")

            with open("tasks.txt", "w") as task_file:
                for task in tasks:
                    task_file.write(", ".join(task) + "\n")
        else:
            print("Invalid choice. Please try again.")

    return


def display_stats():
    """
    Display the number of tasks and users.
    
    Reads tasks and users from their respective files, and displays 
    a count for both.
    """
     
    with open("tasks.txt", "r") as task_file:
        total_tasks = sum(1 for line in task_file)
    
    with open("user.txt", "r") as user_file:
        total_users = sum(1 for line in user_file)
        print(f"Total Tasks: {total_tasks}")
        print(f"Total Users: {total_users}")
      

from datetime import datetime
def generate_response():
    """
    Generate statistics about tasks and write them to an overview file.
    
    Calculate task related statistics like number of completed, incomplete,
    overdue tasks, and more. Then, it writes these statistics to 
    'user_overview.txt' and 'task_overview.txt'. It also prints out the 
    information to the console.
    """

    total_tasks = 0
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0
    user_tasks = {}
    current_date = datetime.now()

    with open("tasks.txt", "r") as task_file:
        for line in task_file:           
            if line.strip():
                total_tasks += 1
                details = line.strip().split(", ")
                if len(details) == 6:

                    assigned_user = details[0]
                    completed = details[5].strip() == "Yes"
                    due_date = datetime.strptime(details[3], "%d %b %Y")
                    current_date = datetime.now()

                    if details[5].strip() == "Yes":
                        completed_tasks += 1
                    else:
                        incomplete_tasks += 1
                        if current_date > due_date:
                            overdue_tasks += 1

                    if assigned_user not in user_tasks:
                        user_tasks[assigned_user] = {'total': 0, 'completed': 0, 'incomplete': 0, 'overdue': 0}
                   
                    user_tasks[assigned_user]['total'] += 1
                    
                    if completed:
                        user_tasks[assigned_user]['completed'] += 1
                    else:
                        user_tasks[assigned_user]['incomplete'] += 1
                        if current_date > due_date:
                            user_tasks[assigned_user]['overdue'] += 1

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total number of tasks: {total_tasks}")
        
        for user, stats in user_tasks.items():
            total_user = stats['total']
            completed_percentages = (stats['completed'] / total_user) * 100
            incomplete_percentages = (stats['incomplete'] / total_user) * 100
            overdue_percentages = (stats['overdue'] / total_user) * 100
            task_assigned_percentages = (total_user / total_tasks) * 100


            user_overview_file.write(f"User: {user}")
            user_overview_file.write(f"Total tasks assigned: {total_user}")
            user_overview_file.write(f"Percentage of total tasks assigned: {task_assigned_percentages}%")
            user_overview_file.write(f"Percentage of tasks completed: {completed_percentages}%")
            user_overview_file.write(f"Percentage of tasks incomplete: {incomplete_percentages}%")
            user_overview_file.write(f"Percentage of tasks overdue: {overdue_percentages}%")
            user_overview_file.write("--------------------------------------\n")  

            print(f'User: {user}')
            print(f'Total tasks assigned to user: {total_user}')
            print(f'Percentage of total tasks assigned to user: {task_assigned_percentages}')
            print(f'Percentage of total tasks completed: {completed_percentages}%')
            print(f'Percentage of total tasks incomplete: {incomplete_percentages}%')
            print(f'Percentage of total tasks overdue: {overdue_percentages}%')
            print("_____________________________________________________________________________")


    percentage_incomplete = (incomplete_tasks / total_tasks) * 100 if total_tasks else 0
    percentage_overdue = (overdue_tasks / total_tasks) * 100 if total_tasks else 0                            

    with open("task_overview.txt", "w") as overview_file:
        overview_file.write(f"Total Number of tasks: {total_tasks}")
        overview_file.write(f"Total Number of completed tasks: {completed_tasks}")
        overview_file.write(f"Total Number of overdue tasks: {overdue_tasks}")
        overview_file.write(f"Total Number of incomplete tasks: {incomplete_tasks}")
        overview_file.write(f"Percentage of tasks that aren't complete: {percentage_incomplete}")
        overview_file.write(f"Percentage of tasks that are overdue: {percentage_overdue}")

        print(f"The total number of tasks: {total_tasks}")
        print(f"The total number of completed tasks: {completed_tasks}") 
        print(f"The total number of overdue tasks: {overdue_tasks}")
        print(f"The total number of incomplete tasks: {incomplete_tasks}")
        print(f"Percentage of incomplete tasks: {percentage_incomplete}%")
        print(f"Percentage of overdue tasks: {percentage_overdue}%")
               
            
def main():
    """ 
    Main program function
    Loads user credentials from the file, authenticates the user's login
    presents menu options to user
    Takes appropriate actions depending on user's choice.
    """
    user_credentials = load_credentials("user.txt")
    current_user = login(user_credentials)

    while True:

        if current_user == 'admin':
            menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks 
s - show statistics
gr - Generate Response                                                                     
e - exit
: ''').lower()
        else:
            menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks                                             
e - exit
: ''').lower()


        if menu == 'r':
            reg_user(user_credentials)

        elif menu == 'a':
            add_task() 

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine(current_user)

        elif menu == 's' and current_user == 'admin':
            display_stats()

        elif menu == 'gr' and current_user == 'admin':
            generate_response()
                
                
        elif menu == 'e':
            print("Goodbye!!!")
            break

        else:
            print("You have made an invalid input. Please try again")

if __name__ == '__main__':
    main()

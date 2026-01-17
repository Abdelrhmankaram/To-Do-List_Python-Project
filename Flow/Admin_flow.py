import inquirer
from Task import Task_Operations
from User import Admin_operations

def view_all_users(admin):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    users = Admin_operations.view_all_users()

    users_questions = [
        inquirer.List(
            name="user",
            message="Choose task to manage",
            choices=[f"{int(j[0])}: {j[1]} {j[2]} - {j[3]} - {j[-2]}" for i, j in users.iterrows() if j[-1] == "User"] + ["Back"]
        ),
        inquirer.List(
            name="operation",
            message="Activate/Deactive User?",
            choices=["Yes", "No"]
        ),
    ]

    task_choice = inquirer.prompt(users_questions[:1])["user"]

    if task_choice == "Back":
        import os; os.system('cls' if os.name == 'nt' else 'clear')
        return

    user_id = int(task_choice.split(":")[0])
    print(type(user_id))
    print(user_id)

    operation = inquirer.prompt(users_questions[1:])["operation"]

    if operation == "Yes":
        Admin_operations.Activate_deactivate_account(user_id)

    else:
        return

def view_all_tasks(admin):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    tasks = Admin_operations.view_all_tasks()

    tasks_questions = [
        inquirer.List(
            name="task",
            message="Choose task to manage",
            choices=[f"{j[0]}: {j[1]} - {j[6]}" for i, j in tasks.iterrows()] + ["Back"]
        ),
        inquirer.List(
            name="operation",
            message="Delete This Task?",
            choices=["Yes", "No"]
        ),
    ]

    task_choice = inquirer.prompt(tasks_questions[:1])["task"]

    if task_choice == "Back":
        import os; os.system('cls' if os.name == 'nt' else 'clear')
        return

    task_id = int(task_choice.split(":")[0])

    print(task_id)

    operation = inquirer.prompt(tasks_questions[1:])["operation"]

    if operation == "Yes":
        Admin_operations.delete_task(task_id)

def Admin_flow(admin):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    questions = [
        inquirer.List(
            name="choice",
            message="Choose what you want to do",
            choices=["View All Users", "View All Tasks", "Back"]
        )
    ]

    while True:
        answers = inquirer.prompt(questions)

        if answers["choice"] == "View All Users":
            view_all_users(admin)

        elif answers["choice"] == "View All Tasks":
            view_all_tasks(admin)
        
        else:
            return
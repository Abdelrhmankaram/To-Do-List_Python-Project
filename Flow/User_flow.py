import inquirer
from Task import Task_Operations, Task
from Data_Validators import task_data_validators, user_data_validators

def Add_task(user):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    questions = [
        inquirer.Text(
            name="title",
            message="Enter task title: "
        ),
        inquirer.Text(
            name="description",
            message="Enter task description"
        ),
        inquirer.List(
            name="priority",
            message="Choose task priority",
            choices=["Low", "Medium", "High"]
        ),
        inquirer.List(
            name="status",
            message="Choose task status",
            choices=["Pending", "In Progress", "Open", "Completed"]
        ),
        inquirer.Text(
            name="due_date",
            message="Enter task due date",
            validate=lambda answers, current: task_data_validators.validate_due_date(current)
        )
    ]
    
    answers = inquirer.prompt(questions)

    task = Task(answers["title"], answers["description"], answers["priority"], answers["status"], answers["due_date"], int(user.ID))

    task.save_task()

def View_tasks(user):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    tasks = user.get_tasks()

    tasks_questions = [
        inquirer.List(
            name="task",
            message="Choose task to manage",
            choices=[f"{j[0]}: {j[1]} - {j[6]}" for i, j in tasks.iterrows()] + ["Back"]
        ),
        inquirer.List(
            name="operation",
            message="What operation whould you like to do?",
            choices=["Edit", "Delete", "Back"]
        ),
    ]

    task_choice = inquirer.prompt(tasks_questions[:1])["task"]

    if task_choice == "Back":
        import os; os.system('cls' if os.name == 'nt' else 'clear')
        return
    
    task_id = int(task_choice.split(":")[0])

    operation = inquirer.prompt(tasks_questions[1:])["operation"]

    if operation == "Edit":
        from prompt_toolkit import PromptSession

        print("Edit task info")
        session = PromptSession()
        old_task = dict(tasks[tasks["Task ID"] == task_id].iloc[0])

        # Title
        while True:
            new_title = session.prompt(f"Title> ", default=old_task["Title"])
            if len(new_title) != 0:
                break
            else:
                print("Title Can't be empty")

        # Description
        while True:
            new_desc = session.prompt(f"Description> ", default=old_task["Description"])
            if len(new_desc) != 0:
                break
            else:
                print("Description Can't be empty")

        new_answers = inquirer.prompt([
            inquirer.List(
                name="priority",
                message="Change task priority",
                choices=["Low", "Medium", "High"]
            ),
            inquirer.List(
                name="status",
                message="Change task status",
                choices=["Pending", "In Progress", "Open", "Completed"]
            )
        ])

        # Due Date
        while True:
            new_due_date = session.prompt(f"Due Date> ", default=old_task["Due Date"])
            if task_data_validators.validate_due_date(due_date=new_due_date):
                break
            else:
                print("Invalid Date\n")

        Task_Operations.modify_Task(task_id, new_title, new_desc, new_answers["status"], new_answers["priority"], new_due_date)

    elif operation == "Back":
        import os; os.system('cls' if os.name == 'nt' else 'clear')
        View_tasks(user)
    else:
        Task_Operations.delete_task(task_id)

def Search_tasks(user):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    tasks = user.get_tasks()
    search_keyword = [
        inquirer.Text(
            name="keyword",
            message="Enter title to search for",
        ),
        inquirer.List(
            name="done",
            choices=["Back"]
        )
    ]
    keyword = inquirer.prompt(search_keyword[:1])["keyword"]
    result = Task_Operations.search_tasks(tasks, keyword)
    print(result)
    inquirer.prompt(search_keyword[1:])
    import os; os.system('cls' if os.name == 'nt' else 'clear')

def Sort_tasks(user):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    tasks = user.get_tasks()
    sort = [
        inquirer.List(
            name="sort",
            message="Sort by what",
            choices=["Date", "Priority", "Status"]
        ),
        inquirer.List(
            name="done",
            choices=["Ok"]
        )
    ]

    keyword = inquirer.prompt(sort[:1])["sort"]
    sorted_tasks = None

    if keyword == "Date":
        sorted_tasks = Task_Operations.sort_tasks(tasks)

    if keyword == "Priority":
        sorted_tasks = Task_Operations.sort_tasks(tasks, "priority")
    
    if keyword == "Status":
        sorted_tasks = Task_Operations.sort_tasks(tasks, "status")
        
    print(sorted_tasks)
    inquirer.prompt(sort[1:])
    import os; os.system('cls' if os.name == 'nt' else 'clear')

def Filter_tasks(user):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    tasks = user.get_tasks()
    
    filters = [
        inquirer.Checkbox(
            name="priority",
            message="Choose priorities to filter by",
            choices=Task_Operations.get_unique_priority()
        ),
        
        inquirer.Checkbox(
            name="status",
            message="Choose status to filter by",
            choices=Task_Operations.get_unique_status()
        ),

        inquirer.Checkbox(
            name="due_date",
            message="Choose dates to filter by",
            choices=Task_Operations.get_unique_due_date()
        ),
    ]

    filters_answers = inquirer.prompt(filters)

    filtered_tasks = Task_Operations.filter_tasks(
        tasks,
        due_date=filters_answers["due_date"],
        priority=filters_answers["priority"],
        status=filters_answers["status"],
    )
        
    print(filtered_tasks)
    inquirer.prompt([inquirer.List(name="done", choices=["Ok"])])
    import os; os.system('cls' if os.name == 'nt' else 'clear')

def Update_Profile(user):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    from prompt_toolkit import PromptSession

    print("Edit your info\n")
    session = PromptSession()

    # First Name
    while True:
        new_fname = session.prompt(f"First Name> ", default=user.fname)
        if user_data_validators.validate_name(new_fname) != 0:
            break
        else:
            print("Invalid First Name")

    # Last Name
    while True:
        new_lname = session.prompt(f"Last Name> ", default=user.lname)
        if user_data_validators.validate_name(new_lname) != 0:
            break
        else:
            print("Invalid Last Name")

    # Mobile Number
    while True:
        print(user.mobile_number)
        new_mobile_number = session.prompt(f"Phone Number> ", default="0"+str(user.mobile_number))
        if user_data_validators.validate_egyptian_mobile(new_mobile_number) != 0:
            break
        else:
            print("Invalid Phone Number")
    
    user.update_profile(new_fname, new_lname, new_mobile_number)

    print("All info updated!")
    inquirer.prompt([inquirer.List(name="done", choices=["Ok"])])
    import os; os.system('cls' if os.name == 'nt' else 'clear')

def print_tasks(title, df):
    print(f"{title}\n")

    if df.empty:
        print("No tasks found.\n")
        return

    cols = ["Title", "Priority", "Status", "Due Date"]
    df = df[cols].copy()

    df["Due Date"] = df["Due Date"].dt.strftime("%d-%m-%Y %H:%M")

    print(df.to_string(index=False))
    print()

def User_flow(user):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    print("Incoming Deadlines")
    print("------------------")
    print_tasks(
        "Tasks due within 24 hours:",
        Task_Operations.display_upcoming_deadlines(user.ID)
    )

    print("------------------------------------------------------------\n")

    print("Overdue Tasks")
    print("-------------")
    print_tasks(
        "Overdue tasks:",
        Task_Operations.display_overdue_tasks(user.ID)
    )
    
    questions = [
        inquirer.List(
            name="choice",
            message="Choose what you want to do",
            choices=["Add New Task", "View Tasks", "Search Tasks", "Sort Tasks", "Filter Tasks", "Update Profile", "Back"]
        )
    ]

    while True:
        answers = inquirer.prompt(questions)

        if answers["choice"] == "Add New Task":
            Add_task(user)
        
        elif answers["choice"] == "View Tasks":
            View_tasks(user)

        elif answers["choice"] == "Search Tasks":
            Search_tasks(user)

        elif answers["choice"] == "Sort Tasks":
            Sort_tasks(user)

        elif answers["choice"] == "Filter Tasks":
            Filter_tasks(user)

        elif answers["choice"] == "Update Profile":
            Update_Profile(user)
        else:
            import os; os.system('cls' if os.name == 'nt' else 'clear')
            return
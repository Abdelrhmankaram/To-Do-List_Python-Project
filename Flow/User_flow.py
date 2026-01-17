import inquirer
from Task import Task_Operations, Task
from Data_Validators import task_data_validators, user_data_validators

def Add_task(user):
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
    tasks = user.get_tasks()

    tasks_questions = [
        inquirer.List(
            name="task",
            message="Choose task to manage",
            choices=[f"{j[0]}: {j[1]} - {j[6]}" for i, j in tasks.iterrows()]
        ),
        inquirer.List(
            name="operation",
            message="What operation whould you like to do?",
            choices=["Edit", "Delete"]
        ),
    ]

    task_id = int(inquirer.prompt(tasks_questions[:1])["task"].split(":")[0])

    print(task_id)

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

    else:
        Task_Operations.delete_task(task_id)

def Search_tasks(user):
    tasks = user.get_tasks()
    search_keyword = [
        inquirer.Text(
            name="keyword",
            message="Enter title to search for",
        ),
        inquirer.Confirm(
            name="done"
        )
    ]
    keyword = inquirer.prompt(search_keyword[:1])["keyword"]
    result = Task_Operations.search_tasks(tasks, keyword)
    print(result)
    inquirer.prompt(search_keyword[1:])

def Sort_tasks(user):
    tasks = user.get_tasks()
    sort = [
        inquirer.List(
            name="sort",
            message="Sort by what",
            choices=["Date", "Priority", "Status"]
        ),
        inquirer.Confirm(
            name="done"
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

def Filter_tasks(user):
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
    inquirer.prompt([inquirer.List(name="done", choices=["Back"])])

def Update_Profile(user):
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

def User_flow(user):
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
            return
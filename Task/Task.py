from Data_Operations import *
from datetime import date
import pandas as pd

class Task:
    def __init__(self, title, description, priority, status, due_date, owner):
        self.task_id = Task_Operations.get_next_id()
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.date_created = date.today()
        self.due_date = due_date
        self.owner = owner
    
    def save_task(self):
        data = read_tasks_data()
        new_row = pd.DataFrame([{
            "Task ID": self.task_id,
            "Title": self.title,
            "Description": self.description,
            "Priority": self.priority,
            "Date Created": self.date_created,
            "Due Date": self.due_date,
            "Owner": self.owner
        }])
        
        data = pd.concat([data, new_row], ignore_index=True)

        save_tasks_data(data)



class Task_Operations:
    @staticmethod
    def retrieve_tasks_by_userid(id):
        """
        Retrieve tasks data based on user's id
        
        :param id: ID of the logged in user to retrieve his tasks data
        """
        data = read_tasks_data()
        return data[data["Owner"] == id]

    
    @staticmethod
    def delete_task(task_id):
        """
        Delete task based on it's id
        
        :param task_id: ID of the task to be deleted
        """
        data = read_tasks_data()
        data = data[data["Task ID"] != task_id]
        save_tasks_data(data)
        return 

    @staticmethod
    def search_tasks(tasks, task_name):
        """
        Search for tasks with title
        
        :param tasks: Tasks data for the logged in user
        :param task_name: Search tasks that has a title that contains the `task_name`
        """
        search_result = tasks[tasks["Title"].str.contains(task_name, case=False, na=False)]

        return search_result


    @staticmethod
    def sort_tasks(tasks, option="due_date"):
        """
        Sort tasks based on options
        
        :param tasks: Tasks data for the logged in user
        :param option: Sort tasks by `due_date`, `priority`, or `status`
        """
        if option == "due_date":
            return tasks.sort_values(by="Due Date")

        if option == "priority":
            return tasks.sort_values(by="Priority")
        
        if option == "status":
            return tasks.sort_values(by="Status")

    @staticmethod
    def filter_tasks(tasks, priority=None, status=None, due_date=None):
        """
        Filter tasks based on multiple values per field.

        :param tasks: pandas DataFrame of tasks
        :param priority: list[str] | str | None
        :param status: list[str] | str | None
        :param due_date: list[str] | str | None
        """
        filter_result = tasks

        def normalize(value):
            if value is None:
                return None
            if isinstance(value, (list, tuple, set)):
                return list(value)
            return [value]

        priority = normalize(priority)
        status = normalize(status)
        due_date = normalize(due_date)

        if priority:
            pattern = "|".join(priority)
            filter_result = filter_result[
                filter_result["Priority"].str.contains(pattern, case=False, na=False)
            ]

        if status:
            pattern = "|".join(status)
            filter_result = filter_result[
                filter_result["Status"].str.contains(pattern, case=False, na=False)
            ]

        if due_date:
            pattern = "|".join(due_date)
            filter_result = filter_result[
                filter_result["Due Date"].str.contains(pattern, case=False, na=False)
            ]

        return filter_result

        

    @staticmethod
    def get_next_id():
        """
        Performs as an auto increamnt id for the tasks data
        """
        data = read_tasks_data()
        return int(data.tail(1)['Task ID'].iloc[0]) + 1
    
    @staticmethod
    def modify_Task(task_id, title, desc, status, prio, date):
        data = read_tasks_data()
        idx = data.index[data["Task ID"] == task_id][0]

        data.at[idx, "Title"] = title
        data.at[idx, "Description"] = desc
        data.at[idx, "Status"] = status
        data.at[idx, "Priority"] = prio
        data.at[idx, "Due Date"] = date

        save_tasks_data(data)
    
    @staticmethod
    def get_unique_priority():
        data = read_tasks_data()
        unique = list(data["Priority"].unique())

        return unique
    
    @staticmethod
    def get_unique_status():
        data = read_tasks_data()
        unique = list(data["Status"].unique())

        return unique
    
    @staticmethod
    def get_unique_due_date():
        data = read_tasks_data()
        unique = list(data["Due Date"].unique())

        return unique
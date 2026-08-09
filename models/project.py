import re
from datetime import datetime

from termcolor import cprint, colored

from utils.utils import add_data, edit_data, fetch_data, remove_data

class Project:
    TABLE = "projects"
    def __init__(self, name, _due_date, tasks = None, users = None, completed = False, id = None, debug = False):
        self.name = name
        self.tasks = [] if tasks is None else tasks
        self.users = [] if users is None else users
        self.completed = completed
        self.due_date = _due_date
        self.id = id
        
        if debug:
            add_data(Project.TABLE,self.__dict__)

    @property
    def due_date(self):
        return self._due_date
    @due_date.setter
    def due_date(self,value):
        if not datetime.strptime(value,"%m/%d/%Y").date():
            raise ValueError(colored("due_date must be a valid date formatted mm/dd/yyyy"))
        else:
            self._due_date = value


    #add user to project and vice versa
    def add_user(self,user):
        if user.id in self.users:
            print(f"User '{user.name}' already assigned to this project.")
        else:
            self.users.append(user.id)
            edit_data(Project.TABLE,self.id,{"users":self.users})
            user.add_project(self)
            cprint(f"User '{user.name}' added to project '{self.name}'","green")            

    #mark project as complete
    def complete_project(self):
        self.completed = True
        edit_data(Project.TABLE,self.id,{"completed":self.completed})
        cprint(f"Project '{self.name}' completed!","green")

    #add task to project and set task.project to this project
    def add_task(self,task):
        if task.id in self.tasks:
            cprint(f"Task '{task.title}' already attached to project '{self.name}'","red")
        else:
            self.tasks.append(task.id)
            task.set_project(self.id)
            edit_data(Project.TABLE,self.id,{"tasks":self.tasks})
            cprint(f"Task '{task.title}' added to project '{self.name}'","green")

    #remove task from project and set task.project to -1
    def remove_task(self,task):
        if task.id not in self.tasks:
            cprint(f"Task '{task.title}' not part of project '{self.name}'","red")
            return
        self.tasks.remove(task.id)
        task.set_project(-1)
        edit_data(Project.TABLE,self.id,{"tasks":self.tasks})

    #set task.assigned_to to user and add task to user.tasks
    def assign_task(self,task,user):
        if task.id not in self.tasks:
            cprint(f"Task '{task.title}' is not part of project '{self.name}'.","red")
            return
        if user.id not in self.users:
            while True:
                should_add = input(colored(f"User '{user.name}' is not assigned to this project. Add them? [y/n]: ","yellow"))
                if should_add.lower() == 'y':
                    self.add_user(user)
                    break
                elif should_add.lower() == 'n':
                    cprint(f"Task '{task.title}' not assigned to user '{user.name}'","red")
                    return
                else:
                    cprint("Please enter 'y' or 'n'","red")
        task.assign_user(user.id)
        user.add_task(task)
        cprint(f"Task '{task.title}' assigned to '{user.name}'","green")

    #remove user from project and vice versa
    def remove_user(self,user):
        from models.user import User
        if user.id not in self.users:
            cprint(f"User '{user.name}' not part of project '{self.name}'","red")
            return
        self.users.remove(user.id)
        user_isntance = fetch_data(User.TABLE,user.id)
        user_isntance.remove_project(self)
        edit_data(Project.TABLE,self.id,{"users":self.users})
        cprint(f"User '{user.name}' removed from project '{self.name}'","green") 

    #delete this project and remove its links to tasks and users
    def delete(self):
        from models.user import User
        from models.task import Task
        for user in self.users:
            user_instance = fetch_data(User.TABLE,user,"id")
            if user_instance:
                user_instance.remove_project(self)
        for task in self.tasks:
            task_instance = fetch_data(Task.TABLE,task,"id")
            if task_instance:
                task_instance.set_project(-1)
        remove_data(Project.TABLE,self.id)
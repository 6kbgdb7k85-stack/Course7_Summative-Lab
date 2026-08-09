import re

from utils.utils import add_data, edit_data, fetch_data, remove_data

class User:
    TABLE = "users"
    def __init__(self, name, id = None, projects = None, tasks = None, debug = False):
        self.name = name
        self.projects = [] if projects is None else projects
        self.tasks = [] if tasks is None else tasks
        self.id = id
        if debug:
            add_data(User.TABLE,self.__dict__)

    #make sure user name is something that could possibly be a name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        if not re.match("^[a-zA-Z ]+$",value):
            raise TypeError("Name can only contain letters and spaces")
        else:
            self._name = value

    #add project to user. adding user to project handled by project
    def add_project(self,project):
        if project.id in self.projects:
            print(f"User '{self.name}' already assigned to project '{project.name}'.")
        else:
            self.projects.append(project.id)
            edit_data(User.TABLE,self.id,{"projects":self.projects})

    #add task to user. adding user to task handled by project
    def add_task(self,task):
        if task.id in self.tasks:
            print(f"User '{self.name}' already assigned to task '{task.title}'.")
        else:
            self.tasks.append(task.id)
            edit_data(User.TABLE,self.id,{"tasks":self.tasks})

    #remove project from user. removing user from project handled by project
    def remove_project(self,project):
        if project.id not in self.projects:
            print(f"User '{self.name}' not assigned to project '{project.name}'.")
            return
        self.projects.remove(project.id)
        edit_data(User.TABLE,self.id,{"projects":self.projects})

    #remove task from user and set task.assigned_to to -1
    def remove_task(self,task):
        if task.id not in self.tasks:
            print(f"User '{self.name}' not assigned to task '{task.title}'.")
            return
        self.tasks.remove(task.id)
        task.assign_user(-1)
        edit_data(User.TABLE,self.id,{"tasks":self.tasks})

    #delete user and remove links to projects and tasks
    def delete(self):
        from models.project import Project
        from models.task import Task
        for project in self.projects:
            project_instance = fetch_data(Project.TABLE,project)
            if project_instance:
                project_instance.remove_user(self)
        for task in self.tasks:
            task_instance = fetch_data(Task.TABLE,task)
            if task_instance:
                task_instance.assign_user(-1)
        remove_data(User.TABLE,self.id)
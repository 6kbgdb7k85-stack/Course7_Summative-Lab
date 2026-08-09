from utils.utils import add_data, edit_data, fetch_data, remove_data

from termcolor import cprint

class Task:
    TABLE="tasks"
    def __init__(self, title, completed = False, assigned_to = -1, id = None, project=-1, debug = False): #assigned_to and project assigned to -1 as default so pandas uses type int for those columns
        self.title = title
        self.completed = completed
        self.assigned_to = assigned_to
        self.id = id
        self.project = project
        if debug:
            add_data(Task.TABLE,self.__dict__)

    #set assigned_to value and save to table.
    def assign_user(self,value):
        self.assigned_to = value
        edit_data(Task.TABLE, self.id, {"assigned_to":value})

    #set set_project value and save to table.
    def set_project(self,value):
        self.project = value
        edit_data(Task.TABLE,self.id,{"project":value})

    #set task to complete
    def complete_task(self):
        self.completed = True
        edit_data(Task.TABLE,self.id,{"completed":True})
        cprint(f"Task {self.title} completed!","green")

    #delete task and remove links to user and project
    def delete(self):
        from models.user import User
        from models.project import Project
        if self.assigned_to != -1:
            user_instance = fetch_data(User.TABLE,self.assigned_to)
            if user_instance:
                user_instance.remove_task(self)
        if self.project != -1:
            project_instance = fetch_data(Project.TABLE,self.project)
            if project_instance:
                project_instance.remove_task(self)
        remove_data(Task.TABLE,self.id)
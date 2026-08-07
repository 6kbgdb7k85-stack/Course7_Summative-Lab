from utils.utils import add_data, edit_data, fetch_data

class Project:
    TABLE = "projects"
    def __init__(self, name, due_date, tasks = [], users = [], completed = False, id = None, add_on_create = True):
        self.name = name
        self.tasks = tasks
        self.users = users
        self.completed = completed
        self.due_date = due_date
        self.id = id
        if add_on_create:
            add_data(Project.TABLE,self.__dict__)

    def add_user(self,user):
        if user in self.users:
            print(f"User '{user}' already assigned to this project.")
        else:
            self.users.append(user)
            edit_data(Project.TABLE,self.id,{"users":self.users})            

    def complete_project(self):
        self.completed = True
        edit_data(Project.TABLE,self.id,{"completed":self.completed})

    def add_task(self,task):
        if task in self.tasks:
            print(f"Task '{task}' already exists")
        else:
            self.tasks.append(task)
            edit_data(Project.TABLE,self.id,{"tasks":self.tasks})

    def assign_task(self,task,user):
        if user not in self.users:
            while True:
                should_add = input(f"User '{user}' is not assigned to this project. Add them? [y/n]: ")
                if should_add.lower() == 'y':
                    self.add_user(user)
                    break
                elif should_add.lower() == 'n':
                    print(f"Task '{task}' not assigned to user '{user}'")
                    return
                else:
                    print("Please enter 'y' or 'n'")
        print(f"Task '{task}' assigned to '{user}'")
from utils.utils import add_data, edit_data

class Task:
    TABLE="tasks"
    def __init__(self, title, completed = False, assigned_to = None, id = None):
        self.title = title
        self.completed = completed
        self.assigned_to = assigned_to
        self.id = id
        add_data(Task.TABLE,self.__dict__)

    @property
    def assigned_to(self):
        return self._assigned_to
    @assigned_to.setter
    def assigned_to(self,value):
        #TODO validation
        self._assigned_to = value

    def complete_task(self):
        self.completed = True
        edit_data(Task.TABLE,self.id,{"completed":True})
        print(f"Task {self.title} completed.")
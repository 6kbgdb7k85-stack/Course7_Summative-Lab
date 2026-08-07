from utils.utils import add_data

class Task:
    id = 0
    def __init__(self, title):
        self.id = Task.id
        self.title = title
        self.completed = False
        self.assigned_to = None
        Task.id += 1
        add_data("tasks",self.__dict__)

    def complete_task(self):
        self.completed = True
        print(f"Task {self.title} completed.")

    @property
    def assigned_to(self):
        return self._assigned_to
    @assigned_to.setter
    def assigned_to(self,value):
        #TODO validation
        self._assigned_to = value
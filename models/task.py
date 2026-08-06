

class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False
        self.assigned_to = None

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
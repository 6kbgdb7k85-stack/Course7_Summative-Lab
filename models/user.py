import re

class User:
    def __init__(self, name):
        self.name = name
        self. projects = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        if not re.match("^[a-zA-Z ]+$",value):
            raise TypeError("Name can only contain letters and spaces")
        else:
            self._name = value

    def add_project(self,project):
        if project in self.projects:
            print(f"User '{self.name} already assigned to project '{project}'.")
        else:
            self.projects.append(project) 
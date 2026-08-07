import re

from utils.utils import add_data

class User:
    id = 0
    def __init__(self, name):
        self.id = User.id
        self.name = name
        self. projects = []
        User.id += 1
        add_data("users",self.__dict__)

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
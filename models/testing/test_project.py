import pytest

from models.project import Project
from models.task import Task
from models.user import User

from utils.utils import add_data

@pytest.fixture
def test_data():
    test_user = User("project test user",debug=True)
    test_task = Task("project test task",debug=True)
    test_project = Project("test-project","01-02-30", debug=True)

    yield (test_project, test_task, test_user)

    if test_user:
        test_user.delete()
        del test_user
    if test_task:
        test_task.delete()
        del test_task
    if test_project:
        test_project.delete()
        del test_project

def test_delete(test_data, capsys):
    test_project = test_data[0]
    test_project.delete()
    logs = capsys.readouterr()
    assert f"ID '{test_project.id}' removed from table '{Project.TABLE}'" in logs.out.strip()
    del test_project

def test_complete_project(test_data):
    test_project = test_data[0]
    test_project.complete_project()
    assert test_project.completed == True

def test_add_task(test_data):
    test_project, test_task, test_user = test_data
    test_project.add_task(test_task)
    assert test_task.id in test_project.tasks

def test_remove_task(test_data):
    test_project, test_task, test_user = test_data
    test_project.add_task(test_task)
    test_project.remove_task(test_task)
    assert test_task.id not in test_project.tasks

def test_add_task_duplicate(test_data, capsys):
    test_project, test_task, test_user = test_data
    test_project.add_task(test_task)
    test_project.add_task(test_task)
    logs = capsys.readouterr()
    assert f"Task '{test_task.title}' already attached to project '{test_project.name}'" in logs.out.strip()
    assert test_project.tasks == [test_task.id]

def test_add_user(test_data):
    test_project, test_task, test_user = test_data
    test_project.add_user(test_user)
    assert test_user.id in test_project.users

def test_add_user_duplicate(test_data, capsys):
    test_project, test_task, test_user = test_data
    test_project.add_user(test_user)
    test_project.add_user(test_user)
    logs = capsys.readouterr()
    assert f"User '{test_user.name}' already assigned to this project." in logs.out.strip()
    assert test_project.users == [test_user.id]

def test_remove_user(test_data):
    test_project, test_task, test_user = test_data
    test_project.add_user(test_user)
    test_project.remove_user(test_user)
    assert test_user.id not in test_project.users

def test_assign_task(test_data, capsys):
    test_project, test_task, test_user = test_data
    test_project.add_task(test_task)
    test_project.add_user(test_user)
    test_project.assign_task(test_task,test_user)
    logs = capsys.readouterr()
    assert f"Task '{test_task.title}' assigned to '{test_user.name}'" in logs.out.strip()

def test_assign_task_not_project_task(test_data,capsys):
    test_project, test_task, test_user = test_data
    test_project.assign_task(test_task,test_user)
    logs = capsys.readouterr()
    assert f"Task '{test_task.title}' is not part of project '{test_project.name}'." in logs.out.strip()

def test_assign_task_not_project_user_accept(test_data, capsys, monkeypatch):
    test_project, test_task, test_user = test_data
    test_project.add_task(test_task)
    monkeypatch.setattr("builtins.input",lambda _: "y")
    test_project.assign_task(test_task,test_user)
    logs = capsys.readouterr()
    assert f"Task '{test_task.title}' assigned to '{test_user.name}'" in logs.out.strip()

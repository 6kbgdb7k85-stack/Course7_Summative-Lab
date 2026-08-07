import pytest

from models.project import Project

@pytest.fixture
def test_project():
    return Project('test-project','01/02/27',add_on_create=True)

def test_complete_project(test_project):
    test_project.complete_project()
    assert test_project.completed == True

def test_add_task(test_project, capsys):
    task = 'test-task'
    test_project.add_task(task)
    assert task in test_project.tasks

def test_add_task_duplicate(test_project, capsys):
    task = 'test-task'
    test_project.add_task(task)
    test_project.add_task(task)
    logs = capsys.readouterr()
    assert f"Task '{task}' already exists" in logs.out.strip()
    assert test_project.tasks == [task]

def test_add_user(test_project):
    user = 'test-user'
    test_project.add_user(user)
    assert user in test_project.users

def test_add_user_duplicate(test_project, capsys):
    user = 'test-user'
    test_project.add_user(user)
    test_project.add_user(user)
    logs = capsys.readouterr()
    assert f"User '{user}' already assigned to this project." in logs.out.strip()
    assert test_project.users == [user]

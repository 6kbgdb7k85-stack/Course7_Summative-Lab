import pytest

from models.user import User
from models.project import Project
from models.task import Task

@pytest.fixture
def test_data():
    #DEBUG added to test entry names to easily find in data if cleanup fails due to error in testing
    test_user = User("DEBUG project test user",debug=True)
    test_task = Task("DEBUG project test task",debug=True)
    test_project = Project("DEBUG test-project","01/02/2030", debug=True)

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

def test_add_project(test_data):
    test_project, test_task, test_user = test_data
    test_user.add_project(test_project)
    assert test_project.id in test_user.projects


def test_invalid_name_raises_type_error():
    with pytest.raises(TypeError, match="Name can only contain letters and spaces"):
        User("Invalid123")


def test_remove_project(test_data):
    test_project, test_task, test_user = test_data
    test_user.add_project(test_project)

    test_user.remove_project(test_project)

    assert test_project.id not in test_user.projects


def test_add_task_duplicate(test_data, capsys):
    test_project, test_task, test_user = test_data
    test_user.add_task(test_task)
    test_user.add_task(test_task)

    logs = capsys.readouterr()
    assert f"User '{test_user.name}' already assigned to task '{test_task.title}'." in logs.out.strip()
    assert test_user.tasks == [test_task.id]


def test_remove_task(test_data):
    test_project, test_task, test_user = test_data
    test_user.add_task(test_task)

    test_user.remove_task(test_task)

    assert test_task.id not in test_user.tasks
    assert test_task.assigned_to == -1

def test_get_assigned_tasks(test_data, capsys):
    test_project, test_task, test_user = test_data
    test_user.add_task(test_task)
    test_user.get_assigned_tasks()
    logs = capsys.readouterr()
    expected_log = {'title': test_task.title, 'completed': False, 'project': "None"}
    assert str(expected_log) in logs.out.strip()

def test_get_assigned_projects(test_data, capsys):
    test_project, test_task, test_user = test_data
    test_user.add_project(test_project)
    test_user.get_assigned_projects()
    logs = capsys.readouterr()
    expected_log = {"name":test_project.name, "due_date":test_project.due_date, "completed":str(test_project.completed)}
    assert str(expected_log) in logs.out.strip()
import pytest

from models.task import Task
from models.project import Project
from models.user import User
from utils.utils import fetch_data

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

def test_complete_task(test_data):
    test_task = test_data[1]
    test_task.complete_task()
    assert test_task.completed == True


def test_assign_user_and_set_project(test_data):
    test_task = test_data[1]
    user_id = 99
    project_id = 42

    test_task.assign_user(user_id)
    test_task.set_project(project_id)

    assert test_task.assigned_to == user_id
    assert test_task.project == project_id


def test_delete_task_removes_links(test_data):
    test_project, test_task, test_user = test_data
    test_project.add_user(test_user)
    test_project.add_task(test_task)
    test_user.add_task(test_task)
    test_task.assign_user(test_user.id)

    test_task.delete()

    updated_user = fetch_data(User.TABLE, test_user.id)
    updated_project = fetch_data(Project.TABLE, test_project.id)

    assert test_task.id not in updated_user.tasks
    assert test_task.id not in updated_project.tasks
    assert updated_user.tasks == [] or test_task.id not in updated_user.tasks
    assert updated_project.tasks == [] or test_task.id not in updated_project.tasks
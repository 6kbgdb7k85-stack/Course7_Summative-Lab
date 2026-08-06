import pytest

from models.project import Project
from models.task import Task


@pytest.fixture
def test_project():
    return Project('test-project')

def test_complete_project(test_project):
    test_project.complete_project()
    assert test_project.completed == True

def test_add_task(test_project):
    task = Task('test-task')
    test_project.add_task(task)
    assert task in test_project.tasks
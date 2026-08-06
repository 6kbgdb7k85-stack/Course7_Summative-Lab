import pytest

from models.task import Task

@pytest.fixture
def test_task():
    return Task("test-task")

def test_complete_task(test_task):
    test_task.complete_task()
    assert test_task.completed == True
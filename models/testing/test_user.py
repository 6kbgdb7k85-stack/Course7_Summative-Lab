import pytest

from models.user import User
from models.project import Project

@pytest.fixture
def test_user():
    return User('test-user')

def test_add_project(test_user):
    project = Project('test-project')
    test_user.add_project(project)
    assert project in test_user.projects
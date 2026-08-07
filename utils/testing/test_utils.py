import pytest
import os
import json

from utils.utils import add_data, edit_data, remove_data

@pytest.fixture
def test_data():
    return {"id":None,"testkey1":"testval1","testkey2":"testval2","testkey3":['testlist1','testlist2']}

def test_add_data(test_data):
    filename = add_data("test",test_data)
    assert os.path.exists(filename)
    with open(filename, "r") as file:
        data = json.load(file)
        assert test_data in data
        assert len(data) == 1
    add_data("test",test_data)
    with open(filename,"r") as file:
        data = json.load(file)
        assert len(data) == 2
    if os.path.exists(filename):
        os.remove(filename)    
    
def test_edit_data(test_data):
    filename = add_data("test",test_data)
    new_data = test_data.copy()
    new_data["testkey2"] = "changedval"
    test_data["testkey1"] = "testval1B"
    add_data("test", test_data)
    edit_data("test",0,{"testkey2":new_data["testkey2"]})
    with open(filename,"r") as file:
        data = json.load(file)
        assert new_data in data
    if os.path.exists(filename):
            os.remove(filename)

def test_remove_data(test_data):
    filename = add_data("test",test_data)
    remove_data("test",0)
    with open(filename,"r") as file:
        data = json.load(file)
        assert test_data not in data
    if os.path.exists(filename):
                os.remove(filename)
        
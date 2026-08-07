import pytest
import os
import csv
import ast

from utils.utils import add_data, edit_data, remove_data

@pytest.fixture
def test_data():
    return {"testkey1":"testval1","testkey2":"testval2","testkey3":['testlist1','testlist2']}

def test_add_data_(test_data):
    filename = add_data('test',test_data)
    keys = test_data.keys()
    assert os.path.exists(filename)
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file, fieldnames=keys)
        rows = []
        for row in reader:
            row_obj = {}
            for key in keys:
                if '[' in row[key]:
                    row_obj[key] = ast.literal_eval(row[key])
                else:
                    row_obj[key] = row[key]
            rows.append(row_obj)
        assert test_data in rows
        assert len(rows) == 2
    add_data('test',test_data)
    with open(filename,"r") as file:
        reader = csv.DictReader(file, fieldnames=keys)
        rows = []
        for row in reader:
            rows.append(row)
        assert len(rows) == 3
    if os.path.exists(filename):
        os.remove(filename)

def test_edit_data(test_data):
    filename = add_data("test",test_data)
    new_data = test_data.copy()
    new_data["testkey2"] = "changedval"
    test_data["testkey1"] = "testval1B"
    add_data("test", test_data)
    row_key = {"id":"testkey1","value":"testval1"}
    keys = test_data.keys()
    edit_data("test",row_key,{"testkey2":new_data["testkey2"]})
    with open(filename,"r",newline="") as file:
        reader = csv.DictReader(file,keys)
        rows = []
        for row in reader:
            row_obj = {}
            for key in keys:
                if '[' in row[key]:
                    row_obj[key] = ast.literal_eval(row[key])
                else:
                    row_obj[key] = row[key]
            rows.append(row_obj)
        assert new_data in rows
    if os.path.exists(filename):
            os.remove(filename)

def test_remove_data(test_data):
    filename = add_data("test",test_data)
    remove_data("test",{"id":"testkey1","value":"testval1"})
    with open(filename,"r") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            row_obj = {}
            for key in reader.keys():
                if '[' in row[key]:
                    row_obj[key] = ast.literal_eval(row[key])
                else:
                    row_obj[key] = row[key]
            rows.append(row_obj)
        assert test_data not in rows
    if os.path.exists(filename):
                os.remove(filename)
        
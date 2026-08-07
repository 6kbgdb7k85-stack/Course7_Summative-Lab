import csv
import os
import json

import pandas as pd

JSON_INDENT = 2

def add_data(table,data):
    filename = f"data/{table}.json"
    del data["id"]
    if os.path.exists(filename):
        table_data = pd.read_json(filename, orient="records")
        data["id"] = table_data.iloc[-1]["id"] + 1
        row = pd.DataFrame([data])
        new_data = pd.concat([table_data, row], ignore_index=True)
        new_data.to_json(filename, orient="records", indent=JSON_INDENT)
    else:
        data["id"] = 0
        row = pd.DataFrame([data])
        row.to_json(filename, orient="records", indent=JSON_INDENT)       
    print(f"Entry saved to data/{table}.csv")
    return filename

def edit_data(table,change_id,change_data):
    filename = f"data/{table}.json"
    try:
        table_data = pd.read_json(filename)
        index = table_data.index[table_data["id"] == change_id][0]
        for key,val in change_data.items():
            if key == "id":
                print("'id' is immutable")
            else:
                table_data.at[index, key] = val
        table_data.to_json(filename, orient="records", indent=JSON_INDENT)          
    except FileNotFoundError:
        print(f"Table '{table}' not found")

def remove_data(table,delete_id):
    filename = f"data/{table}.json"
    try:
        table_data = pd.read_json(filename)
        table_data = table_data[table_data["id"] != delete_id]
        table_data.to_json(filename, orient="records", indent=JSON_INDENT)          
    except FileNotFoundError:
        print(f"Table '{table}' not found")

def fetch_data(table,lookup_value,lookup_key = "id"):
    filename = f"data/{table}.json"
    try:
        table_data = pd.read_json(filename)
        entry = table_data[table_data[lookup_key] == lookup_value]
        return data_to_instance(table,entry.to_dict())    
    except FileNotFoundError:
        print(f"Table '{table}' not found")

def fetch_table(table):
    filename = f"data/{table}.json"
    try:
        with open(filename,"r") as file:
            table_data = json.load(file)
            return table_data      
    except FileNotFoundError:
        print(f"Table '{table}' not found")

def data_to_instance(table,data):
    from models.project import Project
    from models.task import Task
    from models.user import User

    match table:
        case "projects":
            return Project(**data).__dict__
        case "tasks":
            return Task(**data).__dict__
        case "users":
            return User(**data).__dict__
        case _:
            return data

def parse_int(value):
    try:
        return int(value)
    except:
        return value

import csv
import os
import json

import pandas as pd
from termcolor import cprint

JSON_INDENT = 2

def add_data(table,data):
    filename = f"data/{table}.json"
    #if file exists add to otherwise create new table file
    if os.path.exists(filename):
        table_data = pd.read_json(filename, orient="records")
        try:
            data["id"] = table_data.iloc[-1]["id"] + 1
        except:
            data["id"] = 0
        row = pd.DataFrame([data])
        new_data = pd.concat([table_data, row], ignore_index=True)
        new_data.to_json(filename, orient="records", indent=JSON_INDENT)
    else:
        data["id"] = 0
        row = pd.DataFrame([data])
        row.to_json(filename, orient="records", indent=JSON_INDENT)       
    cprint(f"Entry saved to data/{table}.json","green")
    return filename

#edit data in table
def edit_data(table,change_id,change_data):
    filename = f"data/{table}.json"
    try:
        table_data = pd.read_json(filename)
        try:
            index = table_data.index[table_data["id"] == change_id][0]
        except:
            cprint(f"Index '{change_id}' not found","red")
        for key,val in change_data.items():
            if key == "id":
                cprint("'id' is immutable","red")
            else:
                print('test')
                table_data.at[index, key] = val
        table_data.to_json(filename, orient="records", indent=JSON_INDENT)
    except FileNotFoundError:
        cprint(f"Table '{table}' not found","red")

#remove data from table
def remove_data(table,delete_id):
    filename = f"data/{table}.json"
    try:
        table_data = pd.read_json(filename)
        try:
            table_data = table_data[table_data["id"] != delete_id]
            table_data.to_json(filename, orient="records", indent=JSON_INDENT)
            cprint(f"ID '{delete_id}' removed from table '{table}'","green")  
        except:
            cprint(f"Entry with ID '{delete_id}' not found in table '{table}'","red")
            return
                
    except FileNotFoundError:
        cprint(f"Table '{table}' not found","red")

#fetch item in table
def fetch_data(table,lookup_value,lookup_key = "id"):
    filename = f"data/{table}.json"
    try:
        table_data = pd.read_json(filename)
        try:
            index = table_data.index[table_data[lookup_key] == lookup_value][0]
        except:
            cprint(f"Entry with key '{lookup_key}' as '{lookup_value}' not found in table '{table}'","red")
            return
        entry = table_data.iloc[index]
        if not entry.empty:
            return data_to_instance(table,entry.to_dict())
        cprint(f"Entry '{lookup_value}' not found in table '{table}'","red")
        return None    
    except FileNotFoundError:
        cprint(f"Table '{table}' not found","red")

#fetch whole table
def fetch_table(table):
    filename = f"data/{table}.json"
    try:
        with open(filename,"r") as file:
            table_data = json.load(file) #pandas not needed for just reading raw data
            return table_data      
    except FileNotFoundError:
        cprint(f"Table '{table}' not found","red")

#convert table row data into matching class instance so the instance methods can be used to manipulate the object
def data_to_instance(table,data):
    from models.project import Project
    from models.task import Task
    from models.user import User
    match table:
        case "projects":
            return Project(**data)
        case "tasks":
            return Task(**data)
        case "users":
            parsed_data = {key: val for key, val in data.items() if key != "_name"}
            parsed_data["name"] = data["_name"]
            return User(**parsed_data)
        case _:
            return data

#if value is numeric make it int otherwise leave it alone
def parse_int(value):
    try:
        return int(value)
    except:
        return value

#set keys for table lookup based on command argument flags
def get_keys(args):
    if hasattr(args,"tid") and args.tid:
        task_key = "id"
    else:
        task_key = "title"
    if hasattr(args,"uid") and args.uid:
        user_key = "id"
    else:
        user_key = "_name"
    if hasattr(args,"pid") and args.pid:
        project_key = "id"
    else:
        project_key = "name"
    return {"task_key":task_key,"user_key":user_key,"project_key":project_key}

import csv
import os
import json

import pandas as pd

JSON_INDENT = 2

def add_data(table,data):
    filename = f"data/{table}.json"
    row = pd.DataFrame([data])
    if os.path.exists(filename):
        table_data = pd.read_json(filename, orient="records")
        new_data = pd.concat([table_data, row], ignore_index=True)
        new_data.to_json(filename, orient="records", indent=JSON_INDENT)
    else:
        row.to_json(filename, orient="records", indent=JSON_INDENT)       
    print(f"Entry saved to data/{table}.csv")
    return filename

def edit_data(table,change_id,change_data):
    filename = f"data/{table}.json"
    try:
        table = pd.read_json(filename)
        index = table.index[table["id"] == change_id][0]
        for key,val in change_data.items():
            table.at[index, key] = val
        table.to_json(filename, orient="records", indent=JSON_INDENT)          
    except FileNotFoundError:
        print(f"Table '{table}' not found")

def remove_data(table,delete_id):
    filename = f"data/{table}.json"
    try:
        table = pd.read_json(filename)
        table = table[table["id"] != delete_id]
        table.to_json(filename, orient="records", indent=JSON_INDENT)          
    except FileNotFoundError:
        print(f"Table '{table}' not found")

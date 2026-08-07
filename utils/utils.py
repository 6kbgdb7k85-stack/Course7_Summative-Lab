import csv
import os

import pandas as pd

def add_data(table,data):
    filename = f"data/{table}.csv"
    row = pd.DataFrame([data])
    if os.path.exists(filename):
        row.to_csv(filename, mode="a", header=False, index=False)
    else:
        row.to_csv(filename, index=False)       
    print(f"Entry saved to data/{table}.csv")
    return filename

def edit_data(table,row_id,change_data):
    filename = f"data/{table}.csv"
    id_key = row_id["id"]
    id_value = row_id["value"]
    try:
        table = pd.read_csv(filepath_or_buffer=filename)
        change_keys = list(change_data.keys())
        change_vals = list(change_data.values())
        table.loc[table[id_key] == id_value, change_keys] = change_vals
        table.to_csv(filename, index=False)          
    except FileNotFoundError:
        print(f"Table '{table}' not found")

def remove_data(table,row_id):
    filename = f"data/{table}.csv"
    id_key = row_id["id"]
    id_value = row_id["value"]
    try:
        table = pd.read_csv(filepath_or_buffer=filename)
        table = table[table[id_key] != id_value]
        table.to_csv(filename, index=False)          
    except FileNotFoundError:
        print(f"Table '{table}' not found")

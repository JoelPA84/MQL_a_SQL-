import re
import tkinter as tk
from tkinter import ttk

def convert_mql_to_sql(mql_query):
    sql_query = "SELECT * FROM table WHERE "
    fields = re.findall(r'(\w+):', mql_query)
    values = re.findall(r"['\"](.*?)['\"]", mql_query)
    conditions = []

    for field, value in zip(fields, values):
        if value.startswith('$gt:'):
            value = value.replace('$gt:', '').strip()
            condition = f"{field} > {value}"
        elif value.startswith('$'):
            condition = f"{field} {value.replace('$', '')}"
        else:
            condition = f"{field} = '{value}'"  # Agregamos comillas alrededor del valor
        conditions.append(condition)

    sql_query += " AND ".join(conditions)
    return sql_query

def convert_insert_mql_to_sql(mql_query):
    table_name = re.findall(r'INSERT INTO (\w+)', mql_query)[0]
    fields = re.findall(r'\((.*?)\)', mql_query)[0].split(', ')
    values = re.findall(r'VALUES \((.*?)\)', mql_query)[0].split(', ')

    sql_values = []
    for value in values:
        value = value.strip()
        if value.startswith("'") and value.endswith("'"):
            sql_values.append(value)
        else:
            sql_values.append(value)
    
    sql_query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(sql_values)})"
    return sql_query

def convert_update_mql_to_sql(mql_query):
    table_name = re.findall(r'UPDATE (\w+)', mql_query)[0]
    set_values = re.findall(r'{ \$set: {(.*?)} }', mql_query)[0].split(', ')
    
    set_conditions = []
    for value in set_values:
        field, value = value.split(':')
        field = field.strip()
        value = value.strip()
        if value.startswith("'") and value.endswith("'"):
            set_conditions.append(f"{field} = {value}")
        else:
            set_conditions.append(f"{field} = {value}")
    
    where_conditions = re.findall(r'\{ (.*?) \}', mql_query)[1].split(', ')
    where_conditions = [condition.strip() for condition in where_conditions]
    
    sql_query = f"UPDATE {table_name} SET {', '.join(set_conditions)} WHERE {' AND '.join(where_conditions)}"
    return sql_query

def convert_delete_mql_to_sql(mql_query):
    table_name = re.findall(r'DELETE FROM (\w+)', mql_query)[0]
    where_conditions = re.findall(r'\{ (.*?) \}', mql_query)[0].split(', ')
    where_conditions = [condition.strip() for condition in where_conditions]

    sql_query = f"DELETE FROM {table_name} WHERE {' AND '.join(where_conditions)}"
    return sql_query

def on_convert_button_click():
    mql_query = mql_entry.get()
    if mql_query.startswith("INSERT INTO"):
        sql_query = convert_insert_mql_to_sql(mql_query)
    elif mql_query.startswith("UPDATE"):
        sql_query = convert_update_mql_to_sql(mql_query)
    elif mql_query.startswith("DELETE FROM"):
        sql_query = convert_delete_mql_to_sql(mql_query)
    else:
        sql_query = convert_mql_to_sql(mql_query)
    sql_label.config(text="SQL Query: " + sql_query)

root = tk.Tk()
root.title("Transpilador MQL a SQL")

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky="nsew")

mql_label = ttk.Label(main_frame, text="Consulta MQL:")
mql_label.grid(row=0, column=0, sticky="w")

mql_entry = ttk.Entry(main_frame, width=50)
mql_entry.grid(row=1, column=0, sticky="we", padx=5, pady=5)

convert_button = ttk.Button(main_frame, text="Convertir", command=on_convert_button_click)
convert_button.grid(row=2, column=0, sticky="e", padx=5, pady=5)

sql_label = ttk.Label(main_frame, text="SQL Query: None")
sql_label.grid(row=3, column=0, sticky="w")

root.mainloop()

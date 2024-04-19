import pandas as pd
import numpy as np
from flask import request
def runstatement(statement, mysql):
    cursor = mysql.connection.cursor()
    cursor.execute(statement)
    results = cursor.fetchall()
    mysql.connection.commit()
    df = ""
    if (cursor.description):
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=column_names)
    cursor.close()
    return df

def simple_hash(s):
    hash_value = 0
    for char in s:
        hash_value += ord(char)
    return hash_value

def return_table(df):
    table = "<table>"
    df_arr = df.to_numpy()
    table+=f"<tr>"
    for i in df.columns:
        table+=f"<th>{i}</th>"
    table+=f"</tr>"

    for i in df_arr:
        table+=f"<tr>"
        for j in i:
            table+=f"<td>{j}</td>"
        table+=f"</tr>"
    table += "</table>"
    return table

def make_search_statement(table):
    search_statment = f"Select * from {table} WHERE "
    for i in request.form.keys():
        if (i != "items"):
            search_statment+=str(i)
            search_statment+=f" = '{request.form.get(i)}' AND "
        else:
            search_statment+="1=1"
            break
    filter_attr = request.form.get("items")
    attr_value = request.form.get("attr_value")
    if (filter_attr != "None"):
        search_statment+= f" AND {filter_attr}='{attr_value}'"
    
    return search_statment
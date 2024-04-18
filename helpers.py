import pandas as pd
import numpy as np
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
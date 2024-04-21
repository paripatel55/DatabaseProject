from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pandas as pd

app = Flask(__name__)
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["PASSWORD"] = ""
app.config["MY_SQLDB"] = 'criminal'

from helpers import runstatement, simple_hash, return_table
from markupsafe import Markup
def get_db_connection():
    return pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['PASSWORD'],
                           db=app.config['MY_SQLDB'])

def runstatement(statement):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("Start TRANSACTION;") #Transaction
    cursor.execute(statement)
    results = cursor.fetchall()
    df = pd.DataFrame()  
    if results and cursor.description: 
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=column_names) 
    conn.commit() #Commit
    cursor.close()
    conn.close() 
    return df

def check_existance(db, attr_selection, attr_value):
    try:
        db = runstatement(f"SELECT * FROM {db}")
    except Exception:
        return False
    for i, j in db.iterrows():
        if str(j[attr_selection]) == str(attr_value):
            return True
    return False

@app.route("/")  # First page the user will see is login 
def login_page():
    return render_template("Officers/Update_Officer.html")

# This file only has Update functions!!
# Starts Here

@app.route('/Update_Criminal', methods=["POST"])
def Update_Criminal():
    return render_template('Officer/Update_Criminal.html')
            
@app.route('/Update_Criminal_Pressed', methods=["POST"])
def Update_Criminal_Pressed():
    Criminal_ID = request.form.get("Criminal_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    statement = f"UPDATE Criminal SET {attr_selection} = '{attr_value}' WHERE Criminal_ID = {Criminal_ID};"
    try: # If it fails, it'd go back to the original page
        runstatement(statement) 
    except Exception:
        return Update_Criminal()
    return Update_Criminal()

@app.route('/Update_Officer', methods=["POST"])
def Update_Officer():
    return render_template('Officer/Update_Officer.html')
            
@app.route('/Update_Officer_Pressed', methods=["POST"])
def Update_Officer_Pressed():
    Officer_ID = request.form.get("Officer_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    statement = f"UPDATE Officer SET {attr_selection} = '{attr_value}' WHERE Officer_ID = {Officer_ID};"
    try: # If it fails, it'd go back to the original page
        runstatement(statement) 
    except Exception:
        return Update_Officer()
    return Update_Officer()

@app.route('/Update_Alias', methods=["POST"])
def Update_Alias():
    return render_template('Officer/Update_Alias.html')


@app.route('/Update_Alias_Pressed', methods=["POST"])
def Update_Alias_Pressed():
    Alias_ID = request.form.get("Alias_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")

    if attr_selection == "Criminal_ID":
        if not (check_existance("Criminal", attr_selection, attr_value)):
            return Update_Alias()

    statement = f"UPDATE Alias SET {attr_selection} = '{attr_value}' WHERE Alias_ID = {Alias_ID};"
    try: # If it fails, it'd go back to the original page
        runstatement(statement) 
    except Exception:
        return Update_Alias()
    return Update_Alias()

@app.route('/Update_Appeals', methods=["POST"])
def Update_Appeals():
    return render_template('Officer/Update_Appeals.html')
            
@app.route('/Update_Appeals_Pressed', methods=["POST"])
def Update_Appeals_Pressed():
    Appeals_ID = request.form.get("Appeals_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    attr_value_date = request.form.get("attr_value_date")
    attr_selection_date = request.form.get("attr_selection_date")

    if attr_selection == "Crime_ID":
        if not (check_existance("Crime", attr_selection, attr_value)):
            return Update_Appeals()
        
    if attr_selection != 'None' and attr_selection_date != 'None':
        statement = f"UPDATE Appeals SET {attr_selection} = '{attr_value}', {attr_selection_date} = '{attr_value_date}' WHERE Appeal_ID = {Appeals_ID};"
    elif attr_selection_date != 'None':
        statement = f"UPDATE Appeals SET {attr_selection_date} = '{attr_value_date}' WHERE Appeal_ID = {Appeals_ID};"
    elif attr_selection != 'None':
        statement = f"UPDATE Appeals SET {attr_selection} = '{attr_value}' WHERE Appeal_ID = {Appeals_ID};"
    try: # If it fails, it'd go back to the original page
        runstatement(statement) 
        print(statement)
    except Exception:
        return Update_Appeals()
    return Update_Appeals()

@app.route('/Update_Crime_Charges', methods=["POST"])
def Update_Crime_Charges():
    return render_template('Officer/Update_Crime_Charges.html')
            
@app.route('/Update_Crime_Charges_Pressed', methods=["POST"])
def Update_Crime_Charges_Pressed():
    Charge_ID = request.form.get("Charge_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    attr_value_date = request.form.get("attr_value_date")
    attr_selection_date = request.form.get("attr_selection_date")
    
    if attr_selection == "Crime_ID":
        if not (check_existance("Crime", attr_selection, attr_value)):
            return Update_Crime_Charges()
    if attr_selection == "Crime_code":
        if not (check_existance("Crime_code", attr_selection, attr_value)):
            return Update_Crime_Charges()

    if attr_selection != 'None' and attr_selection_date != 'None':
        statement = f"UPDATE Crime_charges SET {attr_selection} = '{attr_value}', {attr_selection_date} = '{attr_value_date}' WHERE Charge_ID = {Charge_ID};"
    elif attr_selection_date != 'None':
        statement = f"UPDATE Crime_charges SET {attr_selection_date} = '{attr_value_date}' WHERE Charge_ID = {Charge_ID};"
    elif attr_selection != 'None':
        statement = f"UPDATE Crime_Charges SET {attr_selection} = '{attr_value}' WHERE Charge_ID = {Charge_ID};"
    try: # If it fails, it'd go back to the original page
        runstatement(statement) 
    except Exception:
        return Update_Crime_Charges()
    return Update_Crime_Charges()

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, redirect
import pymysql
import pandas as pd
from markupsafe import Markup
from flask import Blueprint, send_from_directory


app = Flask(__name__)
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["PASSWORD"] = ""
app.config["MY_SQLDB"] = 'criminal_DB'

def get_db_connection():
    return pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['PASSWORD'],
                           db=app.config['MY_SQLDB'])

def runstatement(statement):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(statement)
    results = cursor.fetchall()
    df = pd.DataFrame()  
    if results and cursor.description: 
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=column_names) 
    cursor.close()
    conn.close() 
    return df

def print_criminal_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM criminal")
    results = cursor.fetchall()

    if results:
        print("Contents of the 'criminal' table:")
        for row in results:
            print(row)
    else:
        print("The 'criminal' table is empty.")

    cursor.close()
    conn.close()

static_bp = Blueprint('static', __name__, static_folder='static')

@static_bp.route('/static/')
def static_files(filename):
    return send_from_directory(static_bp.static_folder, filename)

app.register_blueprint(static_bp)

@app.route('/addCriminal', methods = ["GET", "POST"])
def addCriminal(): 
    # first check if it is a post or get request (meaning as the form been submitted yet?)
    if request.method == "POST":
        # get data from form 
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        alias = request.form.get("alias")
        street = request.form.get("street")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")
        phone = request.form.get("phone")
        C_ID = request.form.get("C_ID")
        offender_status = request.form.get("offender_status")
        probation_status = request.form.get("probation_status")

        # Check if C_ID is not empty
        if C_ID:
            # Construct SQL INSERT statement using an f-string
            sql = f"INSERT INTO Criminal (Criminal_ID, Last, First, Street, City, State, Zip, Phone, V_status, P_status) VALUES ('{C_ID}', '{last_name}', '{first_name}', '{street}', '{city}', '{state}', '{zipcode}', '{phone}', '{offender_status}', '{probation_status}')"

            # Connect to the database and execute INSERT statement
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

            # Close cursor and connection
            cursor.close()
            conn.close()

            # display all the criminals including the one just added 
            return render_template('addCriminal.html')
        else:
            # Handle case where C_ID is empty
            return "Error: Criminal ID cannot be empty"
    else:
        # Handle GET request
        return render_template('addCriminal.html')

@app.route('/view_criminals')
def viewCriminals(): 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Criminal")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_criminals.html', criminals=results)

@app.route('/')
def helloworld():
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)

print_criminal_table()
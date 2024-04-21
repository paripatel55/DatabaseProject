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

def runstatement(statement, fetch_results=True):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(statement)
    if fetch_results: 
        results = cursor.fetchall()
        df = pd.DataFrame()  
        if results and cursor.description: 
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=column_names) 
        cursor.close()
        conn.commit()
        conn.close() 
        return df
    else:  
        cursor.close()
        conn.commit()
        conn.close() 
        return pd.DataFrame()  # Return an empty DataFrame

def printCriminals(): 
    sql = f"SELECT * FROM Criminal"
    result = runstatement(sql)
    print(result)
    

def criminal_exists(criminal_id):
    sql_query = f"SELECT Criminal_ID FROM Criminal WHERE Criminal_ID = '{criminal_id}'"
    result = runstatement(sql_query, fetch_results=True)
    return not result.empty

def existing_crime(crime_id):
    sql_query = f"SELECT * FROM Crime WHERE Crime_ID = {crime_id}"
    result = runstatement(sql_query)
    return not result.empty

def officer_exists(officer_id):
    sql_query = f"SELECT * FROM Officer WHERE Officer_ID = '{officer_id}'"
    result = runstatement(sql_query)
    return not result.empty


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
            if not (criminal_exists(C_ID)):
                # Construct SQL INSERT statement using an f-string
                sql = f"INSERT INTO Criminal (Criminal_ID, Last, First, Street, City, State, Zip, Phone, V_status, P_status) VALUES ('{C_ID}', '{last_name}', '{first_name}', '{street}', '{city}', '{state}', '{zipcode}', '{phone}', '{offender_status}', '{probation_status}')"
                print("Executing SQL statement:")
                print(sql)
                runstatement(sql, fetch_results=False)
                print("Criminal added successfully.")
                # display all the criminals including the one just added 
                return redirect('/criminal')
            else: 
                return "Error: Criminal ID already exists"
        else:
            # Handle case where C_ID is empty
            return "Error: Criminal ID cannot be empty"
    else:
        # Handle GET request
        return render_template('addCriminal.html')

# Route to handle adding a new crime
@app.route('/addCrime', methods=["GET", "POST"])
def addCrime():
   
    if request.method == "POST":
       
        crime_id = request.form.get("Crime_ID")
        criminal_id = request.form.get("Criminal_ID")
        classification = request.form.get("Classification")
        date_charged = request.form.get("Date_charged")
        status = request.form.get("Status")
        hearing_date = request.form.get("Hearing_date")
        appeal_out_date = request.form.get("Appeal_out_date")
        # check if criminal Id exists
        if criminal_exists(criminal_id):
           
            sql = f"INSERT INTO Crime (Crime_ID, Criminal_ID, Classification, Date_charged, Status, Hearing_date, Appeal_out_date) VALUES ('{crime_id}', '{criminal_id}', '{classification}', '{date_charged}', '{status}', '{hearing_date}', '{appeal_out_date}')"
            runstatement(sql, fetch_results=False)
           
            return redirect('/crime')
        else: 
             return "Error: Criminal ID does not exist"
    else:
        # Handle GET request
        return render_template('addCrime.html')
    
    
@app.route('/addOfficer', methods=["GET", "POST"])
def addOfficer():
    if request.method == "POST":
        officer_id = request.form.get("Officer_ID")
        last_name = request.form.get("Last")
        first_name = request.form.get("First")
        precinct = request.form.get("Precinct")
        badge = request.form.get("Badge")
        phone = request.form.get("Phone")
        status = request.form.get("Status")
        
        if officer_exists(officer_id):
            return "Error: Officer ID already exists. "
        else:
            sql = f"INSERT INTO Officer (Officer_ID, Last, First, Precinct, Badge, Phone, Status) VALUES ('{officer_id}', '{last_name}', '{first_name}', '{precinct}', '{badge}', '{phone}', '{status}')"
            runstatement(sql, fetch_results=False)
            return redirect('/officer')
    else:
        return render_template('addOfficer.html')
    
@app.route('/criminal', methods = ["GET"])
def criminal(): 
     # Execute raw SQL query to fetch all records from the Criminal table
    sql_query = "SELECT * FROM Criminal"
    result = runstatement(sql_query)

    # Convert the result to a list of dictionaries
    criminals = [dict(row) for _, row in result.iterrows()]

    return render_template('criminal.html', criminals=criminals)

@app.route('/crimecharge', methods = ["GET"])
def crimecharge(): 
    
    sql_query = "SELECT * FROM Crime_charges"
    result = runstatement(sql_query)

    ccharges = [dict(row) for _, row in result.iterrows()]

    return render_template('crimecharge.html', ccharges=ccharges)

@app.route('/crime', methods = ["GET"])
def crime(): 
   
    sql_query = "SELECT * FROM Crime"
    result = runstatement(sql_query)

    crimes = [dict(row) for _, row in result.iterrows()]

    return render_template('crime.html', crimes=crimes)

@app.route('/pbO', methods = ["GET"])
def pbO(): 
  
    sql_query = "SELECT * FROM Prob_officer"
    result = runstatement(sql_query)

    pb = [dict(row) for _, row in result.iterrows()]

    return render_template('pbO.html', pb=pb)

@app.route('/appeal', methods = ["GET"])
def appeal(): 

    sql_query = "SELECT * FROM Appeals"
    result = runstatement(sql_query)

    appeals = [dict(row) for _, row in result.iterrows()]

    return render_template('appeal.html', appeals=appeals)

@app.route('/officer', methods = ["GET"])
def officer(): 

    sql_query = "SELECT * FROM Officer"
    result = runstatement(sql_query)

    officers = [dict(row) for _, row in result.iterrows()]

    return render_template('officer.html', officers=officers)

@app.route('/sentence', methods = ["GET"])
def sentence(): 
  
    sql_query = "SELECT * FROM Sentences"
    result = runstatement(sql_query)

    sentences = [dict(row) for _, row in result.iterrows()]

    return render_template('sentence.html', sentences=sentences)

@app.route('/home')
def home():
     return render_template('home.html')

@app.route('/')
def helloworld():
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)

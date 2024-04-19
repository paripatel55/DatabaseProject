from flask import Flask, render_template, request, redirect
import pymysql
from markupsafe import Markup

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "project"

connection = pymysql.connect(
    host=app.config["MYSQL_HOST"],
    user=app.config["MYSQL_USER"],
    password=app.config["MYSQL_PASSWORD"],
    database=app.config["MYSQL_DB"]
)

# Create a cursor object
cursor = connection.cursor()

@app.route('/Search_Sentences', methods = ["GET","POST"])
def Search_Sentences():
    if (request.method == "GET"):
        return render_template('Officer/Search_Sentences.html')
    elif (request.method == "POST"):
        start_date = request.form.get("Start_Date")
        end_date = request.form.get("End_date")
        filter_attr = request.form.get("items")
        attr_value = request.form.get("attr_value")
        if (filter_attr != "None"):
            search_statment = f"SELECT * from sentences WHERE Start_date <= '{start_date}' AND End_date >= '{end_date}' AND {filter_attr}='{attr_value}'"
        else:
            search_statment = f"SELECT * from sentences WHERE Start_date <= '{start_date}' AND End_date >= '{end_date}'"

        df_output = runstatement(search_statment, mysql)
        return render_template('Officer/Search_Sentences.html', extra_rows=Markup(return_table(df_output)))

@app.route('/addCriminal', methods = ["POST"])
def addCriminal(): 
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
    

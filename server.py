from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from helpers import runstatement, simple_hash, return_table, make_search_statement, exec
from markupsafe import Markup

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "project"

mysql = MySQL(app)


@app.route("/") # first page the user will see is login
def login_page():
    return render_template("login.html")

@app.route("/login_pressed", methods = ["POST"])
# route to a page that handles when the login button is pressed
def login_pressed():
    # get the username and password from frontend
    username = request.form.get("username")
    password = request.form.get("password")  

    # sql statement to check if user and password match up
    authenticate_login = f"SELECT user_type, id from users WHERE username='{username}' AND password='{simple_hash(password)}'"
    df_output = runstatement(authenticate_login, mysql) # get output as dataframe
    if (not df_output.empty): # check if nothing was returned(authentication failed)
        user = df_output.loc[0][0] # get the user type
        user_id = df_output.loc[0][1]
        session['user_id'] = user_id
        session['user_type'] = user
        return redirect(f"/home") # redirect to home page for that user type
    return login_page() # otherwise if authentication failed, stay at login page

@app.route("/signup")
# a page where a new user and register in the database
def signup_page():
    return render_template("signup.html")

@app.route("/signup_pressed", methods = ["POST"]) # handle when the "submit" button is pressed
def signup_pressed():
    # get info from front end
    username = request.form.get("username")
    password = request.form.get("password")   
    criminal_select = request.form.get("criminal_select")
    user_type = "Officer" if criminal_select is None else "Criminal"
    id = request.form.get("ID")
    # based on which type of user they are our search will change
    token = "criminal_id" if user_type != "Officer" else "officer_id"
    table = "criminal" if user_type != "Officer" else "officer"

    # statement to check if they are already in the database
    check_existance_in_database = f"SELECT {token} from {table} WHERE {token}={id}"
    # statement to check if they already have an accoount
    check_existance_in_user_table = f"SELECT id from users WHERE id={id}"
    cursor = mysql.connection.cursor()
    if (not exec(check_existance_in_database, cursor).empty 
        and exec(check_existance_in_user_table, cursor).empty):
        # if they are in the db and are not already registered, add them to the user table
        insert_user_statment = f"INSERT INTO users VALUES('{username}','{simple_hash(password)}', '{id}', '{user_type}')"
        exec(insert_user_statment, cursor)
        mysql.connection.commit()
        cursor.close()
    else: # otherwise keep them at the sign up page
        mysql.connection.commit()
        cursor.close()
        return signup_page()
    
    # if everything works out fine, redirect to login page
    return redirect("/")

@app.route('/home', methods = ["GET","POST"])
def home():
    user = session.get("user_type")
    user_id = session.get("user_id")
    if (user == "Officer"):
        return render_template("Officer/home.html") # render officer home page
        
    elif (user == "Criminal"):
        app.config["MYSQL_USER"] = "criminal"

        if (request.method == "POST"):
            amount = request.form.get("Amount")
            if (int(amount) < 0):
                return render_template("Criminal/criminal_home.html", message = "lmao what?")
            get_crime_charge_id = f"Select charge_id from crime_charges WHERE crime_id IN (SELECT crime.crime_id from crime, criminal WHERE crime.Criminal_ID = {user_id})"
            cursor = mysql.connection.cursor()
            crime_charge_id = exec(get_crime_charge_id, cursor).loc[0][0]
            pay_fine_statement = f"Select payFine({amount}, {crime_charge_id})"
            df_output = exec(pay_fine_statement, cursor)

            mysql.connection.commit()
            cursor.close()

            amount_left = int(df_output.loc[0][0])
            message = f"Amount Left: {amount_left}"
            if (amount_left < 0):
                message = f"Amount returned: {amount_left}"
            return render_template("Criminal/criminal_home.html", message = message)
        return render_template("Criminal/criminal_home.html", message="") # reder criminal home page



@app.route('/Search_Criminal',  methods = ["GET","POST"])
def Search_Criminal():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Criminal.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        search_statment = make_search_statement("criminal")
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search/Search_Criminal.html', extra_rows=Markup(return_table(df_output)))

@app.route('/Search_Officer',  methods = ["GET","POST"])
def Search_Officer():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Officer.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        search_statment = make_search_statement("officer")
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search/Search_Officer.html', extra_rows=Markup(return_table(df_output)))

@app.route('/Search_Prob_Officer',  methods = ["GET","POST"])
def Search_Prob_Officer():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Prob_Officer.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        search_statment = make_search_statement("prob_officer")
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search/Search_Prob_Officer.html', extra_rows=Markup(return_table(df_output)))

@app.route('/Search_Crime',  methods = ["GET","POST"])
def Search_Crime():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Crime.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        search_statment = make_search_statement("crime")
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search/Search_Crime.html', extra_rows=Markup(return_table(df_output)))

@app.route('/Search_Appeals',  methods = ["GET","POST"])
def Search_Appeals():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Appeals.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        search_statment = make_search_statement("appeals")
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search/Search_Appeals.html', extra_rows=Markup(return_table(df_output)))

@app.route('/Search_Crime_Charges',  methods = ["GET","POST"])
def Search_Crime_Charges():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Crime_Charges.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        search_statment = make_search_statement("Crime_charges")
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search/Search_Crime_Charges.html', extra_rows=Markup(return_table(df_output)))

@app.route('/Search_Alias',  methods = ["GET","POST"])
def Search_Alias():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Alias.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        first = request.form.get("First Letter(s)")
       

        filter_attr = request.form.get("items")
        attr_value = request.form.get("attr_value")
        if (filter_attr == "None"):
            search_statment = f"SELECT * From alias WHERE alias.Alias LIKE '{first}%'"
        else:    
            search_statment = f"SELECT * From alias WHERE alias.Alias LIKE '{first}%' AND {filter_attr}='{attr_value}'"
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search/Search_Alias.html', extra_rows=Markup(return_table(df_output)))

@app.route('/Search_Crime_Code',  methods = ["GET","POST"])
def Search_Crime_Code():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Crime_Code.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        word = request.form.get("Word")
        search_statment = f"SELECT * FROM crime_code WHERE Code_description LIKE '%{word}%'"
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search/Search_Crime_Code.html', extra_rows=Markup(return_table(df_output)))





@app.route('/Search_Sentences', methods = ["GET","POST"])
def Search_Sentences():
    if (request.method == "GET"):
        return render_template('Officer/Search/Search_Sentences.html')
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
        return render_template('Officer/Search/Search_Sentences.html', extra_rows=Markup(return_table(df_output)))










































@app.route('/Delete_Criminal', methods = ["GET","POST"])
def Delete_Criminal():
    if (request.method == 'POST'):
        id = request.form.get("ID")
        cursor = mysql.connection.cursor()
        exec("Start TRANSACTION;", cursor)
        if (not exec(f"Select * from users WHERE id = {id}", cursor).empty):
            exec(f"DELTE FROM users WHERE id={id}", cursor)
        statement = f"call deleteCriminal({id})"
        exec(statement, cursor)
        exec("Commit;", cursor)
        
    return render_template("Officer/Delete.html", url = "Delete_Criminal", attr = "Criminal_ID", table="Criminal")

@app.route('/Delete_Officer', methods = ["GET","POST"])
def Delete_Officer():
    user_id = session.get('user_id')
    if (request.method == 'POST'):
        id = request.form.get("ID")
        if (id != user_id):
            cursor = mysql.connection.cursor()
            exec("Start TRANSACTION;", cursor)
            if (not exec(f"Select * from users WHERE id = {id}", cursor).empty):
                exec(f"DELETE FROM users WHERE id = {id}", cursor)
            statement = f"DELETE FROM officer WHERE officer.Officer_ID = {id};"
            statement += f"DELETE FROM crime_officers WHERE Officer_ID = {id};"
            exec(statement, cursor)
            exec("Commit;", cursor)
            cursor.close()

    return render_template("Officer/Delete.html",url = "Delete_Officer", attr = "Officer_ID", table="Officer")

@app.route('/Delete_Alias', methods = ["GET","POST"])
def Delete_Alias():
    if (request.method == 'POST'):
        id = request.form.get("ID")
        statement = f"DELETE FROM alias WHERE alias.Alias_ID = {id}"
        runstatement(statement, mysql)
        
    return render_template("Officer/Delete.html", url = "Delete_Alias", attr = "Alias_ID", table="Alias")

@app.route('/Delete_Sentence', methods = ["GET","POST"])
def Delete_Sentence():
    if (request.method == 'POST'):
        id = request.form.get("ID")
        statement = f"DELETE FROM sentences WHERE sentences.Sentenece_ID = {id}"
        runstatement(statement, mysql)
        
    return render_template("Officer/Delete.html",url = "Delete_Sentence", attr = "Sentenece_ID", table="Sentence")

@app.route('/Delete_Crime', methods = ["GET","POST"])
def Delete_Crime():
    if (request.method == 'POST'):
        id = request.form.get("ID")
        statement = f"DELETE FROM crime_charges WHERE Crime_ID = {id};"
        statement += f"DELETE FROM crime_officers WHERE Crime_ID = {id};"
        statement += f"DELETE FROM appeals WHERE Crime_ID = {id};"
        statement += f"DELETE FROM crime WHERE crime.Crime_ID = {id};"
        runstatement(statement, mysql)
        
    return render_template("Officer/Delete.html",url = "Delete_Crime", attr = "Crime_ID", table="Crime")

@app.route('/Delete_Crime_Charges', methods = ["GET","POST"])
def Delete_Crime_Charges():
    if (request.method == 'POST'):
        id = request.form.get("ID")
        statement = f"DELETE FROM sentences WHERE sentences.Sentenece_ID = {id}"
        runstatement(statement, mysql)
        
    return render_template("Officer/Delete.html",url = "Delete_Crime_Charges", attr = "Crime_Charges_ID", table="Crime Charge")

@app.route('/Delete_Crime_Code', methods = ["GET","POST"])
def Delete_Crime_Code():
    if (request.method == 'POST'):
        id = request.form.get("ID")
        statement = f"DELETE FROM crime_code WHERE crime_code.crime_code = {id};"
        statement+= f"DELETE FROM crime_charges WHERE crime_code = {id};"
        runstatement(statement, mysql)
        
    return render_template("Officer/Delete.html",url = "Delete_Crime_Code", attr = "Crime_code", table="Crime Code")


@app.route('/Delete_Prob_Officer', methods = ["GET","POST"])
def Delete_Prob_Officer():
    if (request.method == 'POST'):
        id = request.form.get("ID")
        statement = f"DELETE FROM prob_officer WHERE prob_id = {id};"
        statement+= f"DELETE FROM sentences WHERE prob_id = {id};"
        runstatement(statement, mysql)
        
    return render_template("Officer/Delete.html",url = "Delete_Prob_Officer", attr = "Prob_Officer", table="Prob_Officer")

@app.route('/Delete_Appeal', methods = ["GET","POST"])
def Delete_Appeal():
    if (request.method == 'POST'):
        id = request.form.get("ID")
        statement = f"DELETE FROM appeals WHERE Appeal_ID = {id};"
        runstatement(statement, mysql)
        
    return render_template("Officer/Delete.html",url = "Delete_Appeal", attr = "Appeal_ID", table="Appeal")



























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
            cursor = mysql.connection.cursor()
            if (exec(f"SELECT * FROM Criminal WHERE Criminal_ID = '{C_ID}'", cursor).empty):
                # Construct SQL INSERT statement using an f-string
                sql = f"INSERT INTO Criminal (Criminal_ID, Last, First, Street, City, State, Zip, Phone, V_status, P_status) VALUES ('{C_ID}', '{last_name}', '{first_name}', '{street}', '{city}', '{state}', '{zipcode}', '{phone}', '{offender_status}', '{probation_status}')"
                #print("Executing SQL statement:")
                #print(sql)
                exec(sql, cursor)
                mysql.connection.commit()
                cursor.close()
                #print("Criminal added successfully.")
                # display all the criminals including the one just added 
                return redirect('/criminal')
            else: 
                mysql.connection.commit()
                cursor.close()
                return "Error: Criminal ID already exists"
        else:
            # Handle case where C_ID is empty
            return "Error: Criminal ID cannot be empty"
    else:
        # Handle GET request
        return render_template('Officer/Add/addCriminal.html')

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
        cursor = mysql.connection.cursor()
        if exec(f"SELECT Criminal_ID FROM Criminal WHERE Criminal_ID = '{criminal_id}'", cursor).empty:
           
            sql = f"INSERT INTO Crime (Crime_ID, Criminal_ID, Classification, Date_charged, Status, Hearing_date, Appeal_out_date) VALUES ('{crime_id}', '{criminal_id}', '{classification}', '{date_charged}', '{status}', '{hearing_date}', '{appeal_out_date}')"
            exec(sql, cursor)

            mysql.connection.commit()
            cursor.close()   
            return redirect('/crime')
        else: 
            mysql.connection.commit()
            cursor.close()
            return "Error: Criminal ID does not exist"
    else:
        # Handle GET request
        return render_template('Officer/Add/addCrime.html')
    
    
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
        cursor = mysql.connection.cursor()
        
        if not exec(f"SELECT * FROM Officer WHERE Officer_ID = '{officer_id}'",cursor).empty:
            sql = f"INSERT INTO Officer (Officer_ID, Last, First, Precinct, Badge, Phone, Status) VALUES ('{officer_id}', '{last_name}', '{first_name}', '{precinct}', '{badge}', '{phone}', '{status}')"
            exec(sql, cursor)
            mysql.connection.commit()
            cursor.close()
            return redirect('/officer')
        else:
            mysql.connection.commit()
            cursor.close()
            return "Error: Officer ID already exists. "
    else:
        return render_template('Officer/Add/addOfficer.html')
    


































@app.route('/Update_Criminal', methods=["GET", "POST"])
def Update_Criminal():
    return render_template('Officer/Update/Update_Criminal.html')
            
@app.route('/Update_Criminal_Pressed', methods=["POST"])
def Update_Criminal_Pressed():
    Criminal_ID = request.form.get("Criminal_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    statement = f"UPDATE Criminal SET {attr_selection} = '{attr_value}' WHERE Criminal_ID = {Criminal_ID};"
    try: # If it fails, it'd go back to the original page
        runstatement(statement, mysql) 
    except Exception:
        return Update_Criminal()
    return Update_Criminal()

@app.route('/Update_Officer', methods=["GET", "POST"])
def Update_Officer():
    return render_template('Officer/Update/Update_Officer.html')
            
@app.route('/Update_Officer_Pressed', methods=["POST"])
def Update_Officer_Pressed():
    Officer_ID = request.form.get("Officer_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    statement = f"UPDATE Officer SET {attr_selection} = '{attr_value}' WHERE Officer_ID = {Officer_ID};"
    try: # If it fails, it'd go back to the original page
        runstatement(statement, mysql) 
    except Exception:
        return Update_Officer()
    return Update_Officer()

@app.route('/Update_Alias', methods=["GET", "POST"])
def Update_Alias():
    return render_template('Officer/Update/Update_Alias.html')


@app.route('/Update_Alias_Pressed', methods=["POST"])
def Update_Alias_Pressed():
    Alias_ID = request.form.get("Alias_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    cursor = mysql.connection.cursor()

    if attr_selection == "Criminal_ID":
        if not (exec(f"SELECT * FROM crime WHERE {attr_selection} = {attr_value}", cursor).empty):
            return Update_Alias()

    statement = f"UPDATE Alias SET {attr_selection} = '{attr_value}' WHERE Alias_ID = {Alias_ID};"
    try: # If it fails, it'd go back to the original page
        exec(statement, cursor) 
        mysql.connection.commit()
        cursor.close()
    except Exception:
        return Update_Alias()
    return Update_Alias()

@app.route('/Update_Appeals', methods=["GET", "POST"])
def Update_Appeals():
    return render_template('Officer/Update/Update_Appeals.html')
            
@app.route('/Update_Appeals_Pressed', methods=["POST"])
def Update_Appeals_Pressed():
    Appeals_ID = request.form.get("Appeals_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    attr_value_date = request.form.get("attr_value_date")
    attr_selection_date = request.form.get("attr_selection_date")
    cursor = mysql.connection.cursor()
    if attr_selection == "Crime_ID":
        if not (exec(f"SELECT * FROM crime WHERE {attr_selection} = {attr_value}", cursor).empty):
            return Update_Appeals()
        
    if attr_selection != 'None' and attr_selection_date != 'None':
        statement = f"UPDATE Appeals SET {attr_selection} = '{attr_value}', {attr_selection_date} = '{attr_value_date}' WHERE Appeal_ID = {Appeals_ID};"
    elif attr_selection_date != 'None':
        statement = f"UPDATE Appeals SET {attr_selection_date} = '{attr_value_date}' WHERE Appeal_ID = {Appeals_ID};"
    elif attr_selection != 'None':
        statement = f"UPDATE Appeals SET {attr_selection} = '{attr_value}' WHERE Appeal_ID = {Appeals_ID};"
    try: # If it fails, it'd go back to the original page
        exec(statement, cursor) 
        mysql.connection.commit()
        cursor.close()
    except Exception:
        return Update_Appeals()
    return Update_Appeals()

@app.route('/Update_Crime_Charges', methods=["GET", "POST"])
def Update_Crime_Charges():
    return render_template('Officer/Update/Update_Crime_Charges.html')
            
@app.route('/Update_Crime_Charges_Pressed', methods=["POST"])
def Update_Crime_Charges_Pressed():
    Charge_ID = request.form.get("Charge_ID")
    attr_value = request.form.get("attr_value")
    attr_selection = request.form.get("attr_selection")
    attr_value_date = request.form.get("attr_value_date")
    attr_selection_date = request.form.get("attr_selection_date")
    cursor = mysql.connection.cursor()
    
    if attr_selection == "Crime_ID":
        if not (exec(f"SELECT * FROM crime WHERE {attr_selection} = {attr_value}", cursor).empty):
            return Update_Crime_Charges()
    if attr_selection == "Crime_code":
        if not exec(f"SELECT * FROM crime_code WHERE {attr_selection} = {attr_value}", cursor).empty:
            return Update_Crime_Charges()

    if attr_selection != 'None' and attr_selection_date != 'None':
        statement = f"UPDATE Crime_charges SET {attr_selection} = '{attr_value}', {attr_selection_date} = '{attr_value_date}' WHERE Charge_ID = {Charge_ID};"
    elif attr_selection_date != 'None':
        statement = f"UPDATE Crime_charges SET {attr_selection_date} = '{attr_value_date}' WHERE Charge_ID = {Charge_ID};"
    elif attr_selection != 'None':
        statement = f"UPDATE Crime_Charges SET {attr_selection} = '{attr_value}' WHERE Charge_ID = {Charge_ID};"
    try: # If it fails, it'd go back to the original page
        exec(statement, cursor) 
        mysql.connection.commit()
        cursor.close()
    except Exception:
        return Update_Crime_Charges()
    return Update_Crime_Charges()








































@app.route('/criminal', methods = ["GET"])
def criminal(): 
     # Execute raw SQL query to fetch all records from the Criminal table
    sql_query = "SELECT * FROM criminal"
    result = runstatement(sql_query, mysql)
    # Convert the result to a list of dictionaries

    return render_template('/Officer/TablePages/criminal.html', table=Markup(return_table(result)))

@app.route('/crimecharge', methods = ["GET"])
def crimecharge(): 
    
    sql_query = "SELECT * FROM Crime_charges"
    result = runstatement(sql_query, mysql)

    return render_template('/Officer/TablePages/crimecharge.html', table=Markup(return_table(result)))

@app.route('/crime', methods = ["GET"])
def crime(): 
   
    sql_query = "SELECT * FROM Crime"
    result = runstatement(sql_query, mysql)


    return render_template('/Officer/TablePages/crime.html', table=Markup(return_table(result)))

@app.route('/pbO', methods = ["GET"])
def pbO(): 
  
    sql_query = "SELECT * FROM Prob_officer"
    result = runstatement(sql_query, mysql)


    return render_template('/Officer/TablePages/pbO.html', table=Markup(return_table(result)))

@app.route('/appeal', methods = ["GET"])
def appeal(): 

    sql_query = "SELECT * FROM Appeals"
    result = runstatement(sql_query, mysql)
    appeals = [dict(row) for _, row in result.iterrows()]

    return render_template('/Officer/TablePages/appeal.html', table=Markup(return_table(result)))

@app.route('/officer', methods = ["GET"])
def officer(): 

    sql_query = "SELECT * FROM Officer"
    result = runstatement(sql_query, mysql)


    return render_template('/Officer/TablePages/officer.html', table=Markup(return_table(result)))

@app.route('/sentence', methods = ["GET"])
def sentence(): 
    sql_query = "SELECT * FROM Sentences"
    result = runstatement(sql_query, mysql)
    return render_template('/Officer/TablePages/sentence.html', table=Markup(return_table(result)))


@app.route('/crime_code', methods = ["GET"])
def crime_code(): 
    sql_query = "SELECT * FROM crime_code"
    result = runstatement(sql_query, mysql)
    return render_template('/Officer/TablePages/crime_code.html', table=Markup(return_table(result)))

@app.route('/alias', methods = ["GET"])
def alias(): 
    sql_query = "SELECT * FROM alias"
    result = runstatement(sql_query, mysql)
    return render_template('/Officer/TablePages/alias.html', table=Markup(return_table(result)))




















if __name__ == '__main__':
    app.secret_key = 'eh'
    app.run(debug=True, host="0.0.0.0", port=8000)




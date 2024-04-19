from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from helpers import runstatement, simple_hash, return_table, make_search_statement
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
        return redirect(f"/home_{user}_{user_id}") # redirect to home page for that user type
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
    user_type = "Criminal" if criminal_select is None else "Officer"
    id = request.form.get("ID")
    print((user_type))
    # based on which type of user they are our search will change
    token = "criminal_id" if criminal_select is None else "officer_id"
    table = "criminal" if criminal_select is None else "officer"

    # statement to check if they are already in the database
    check_existance_in_database = f"SELECT {token} from {table} WHERE {token}={id}"
    # statement to check if they already have an accoount
    check_existance_in_user_table = f"SELECT id from users WHERE id={id}"
    if (not runstatement(check_existance_in_database, mysql).empty 
        and runstatement(check_existance_in_user_table, mysql).empty):
        # if they are in the db and are not already registered, add them to the user table
        insert_user_statment = f"INSERT INTO users VALUES('{username}','{simple_hash(password)}', '{id}', '{user_type}')"
        runstatement(insert_user_statment, mysql)
    else: # otherwise keep them at the sign up page
        return signup_page()
    
    # if everything works out fine, redirect to login page
    return redirect("/")

@app.route('/home_<user>_<user_id>', methods = ["GET","POST"])
def home(user, user_id):
    if (user == "Officer"):
        return render_template("Officer/officer_home.html") # render officer home page
        
    elif (user == "Criminal"):
        if (request.method == "POST"):
            print(request.form.get("Amount"))
            amount = request.form.get("Amount")
            if (int(amount) < 0):
                return render_template("Criminal/criminal_home.html", message = "lmao what?")
            get_crime_charge_id = f"Select charge_id from crime_charges WHERE crime_id IN (SELECT crime.crime_id from crime, criminal WHERE crime.Criminal_ID = {user_id})"
            crime_charge_id = runstatement(get_crime_charge_id, mysql).loc[0][0]
            pay_fine_statement = f"Select payFine({amount}, {crime_charge_id})"
            df_output = runstatement(pay_fine_statement, mysql)
            amount_left = int(df_output.loc[0][0])
            message = f"Amount Left: {amount_left}"
            if (amount_left < 0):
                message = f"Amount returned: {amount_left}"
            return render_template("Criminal/criminal_home.html", message = message)
        return render_template("Criminal/criminal_home.html", message="") # reder criminal home page

@app.route('/Search_Criminal',  methods = ["GET","POST"])
def Search_Criminal():
    if (request.method == "GET"):
        return render_template('Officer/Search_Criminal.html', extra_rows=Markup(""))
    elif (request.method == "POST"):
        search_statment = make_search_statement("criminal")
        df_output = runstatement(search_statment, mysql)
        
        return render_template('Officer/Search_Criminal.html', extra_rows=Markup(return_table(df_output)))



@app.route('/Search_Alias')
def Search_Alias():
    return render_template('Officer/Search_Alias.html')


@app.route('/Search_Prob_Officer')
def Search_Prob_Officer():
    return render_template('Officer/Search_Prob_Officer.html')

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

# send_file(csv_data,
#                      mimetype='text/csv',
#                      attachment_filename='sample.csv',
#                      as_attachment=True)

@app.route('/Delete_Criminal', methods = ["GET","POST"])
def Delete_Criminal():
    if (request.method == 'POST'):
        id = request.form.get("Criminal_ID")
        statement = f"DELETE from alias, appeals, crime, crime_charges, crime_code, crime_officers, criminal, officer, prob_officer, sentences WHERE criminal.Criminal_ID = {id} "
        
        where = "AND alias.Criminal_ID = criminal.Criminal_ID "
        where += "AND appeals.Crime_ID = Crime.Crime_ID "
        where += "AND crime.Criminal_ID = criminal.Criminal_ID "
        where += "AND crime_charges.Crime_ID = Crime.Crime_ID "
        where += "AND crime_charges.crime_code = crime_code.Crime_code "
        where += "AND crime_officers.Crime_ID = crime.Crime_ID "
        where += "AND crime_officers.Officer_ID = officer.Officer_ID "
        where += "AND criminal.Criminal_ID = sentences.CriminalID "
        where += "AND prob_officer.Prob_ID = sentences.Prob_ID "
        statement += where
        print(statement)
        # print(runstatement(statement, mysql))
        
    return render_template("Delete_Criminal.html")


if __name__ == '__main__':
    app.run(debug=True)

# types of queries
    # one for Select __ where attrr = __
    # one for select __ where attr like "___%"




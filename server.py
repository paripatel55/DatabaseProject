from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from helpers import runstatement, simple_hash, return_table
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
    authenticate_login = f"SELECT user_type from users WHERE username='{username}' AND password='{simple_hash(password)}'"
    df_output = runstatement(authenticate_login, mysql) # get output as dataframe
    if (not df_output.empty): # check if nothing was returned(authentication failed)
        user = df_output.loc[0][0] # get the user type
        return redirect(f"/home_{user}") # redirect to home page for that user type
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
    user_type = "Criminal" if criminal_select else "Officer"
    id = request.form.get("ID")

    # based on which type of user they are our search will change
    token = "criminal_id" if criminal_select else "officer_id"
    table = "criminal" if criminal_select else "officer"

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

@app.route('/home_<user>')
def home(user):
    if (user == "Officer"):
        return render_template("Officer/officer_home.html") # render officer home page
        
    elif (user == "Criminal"):
        ... # reder criminal home page

    return "hi"

@app.route('/Search_Criminal')
def Search_Criminal(extra_rows=""):
    return render_template('Officer/Search_Criminal.html', extra_rows=Markup(extra_rows))

@app.route('/Search_Pressed', methods = ["POST"])
def Search_Pressed():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    filter_attr = request.form.get("items")
    attr_value = request.form.get("attr_value")
    if (filter_attr != "None"):
        search_statment = f"SELECT * from criminal WHERE first = '{first_name}' AND last = '{last_name}' AND {filter_attr}='{attr_value}'"
    else:
        search_statment = f"SELECT * from criminal WHERE first = '{first_name}' AND last = '{last_name}'"
    
    df_output = runstatement(search_statment, mysql)
    if (df_output.empty):
        redirect("/Search_Criminal")
        return Search_Criminal(return_table(df_output))
    else:
        redirect("/Search_Criminal")
        return Search_Criminal(return_table(df_output))

@app.route('/Search_Alias', )
def Search_Alias():
    return render_template('Officer/Search_Alias.html')

@app.route('/Search_Prob_Officer')
def Search_Prob_Officer():
    return render_template('Officer/Search_Prob_Officer.html')


# app.add_url_rule("/login_pressed", view_func=login_pressed)
# app.add_url_rule("/signup_pressed", view_func=signup_pressed)


if __name__ == '__main__':
    app.run(debug=True)

# types of queries
    # one for Select __ where attrr = __
    # one for select __ where attr like "___%"




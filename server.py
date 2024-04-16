from flask import Flask, render_template, request, redirect
import matplotlib

app = Flask(__name__)


@app.route("/") # first page the user will see is login
def login_page():
    return render_template("login.html")

@app.route("/login_pressed", methods = ["POST"])
# route to a page that handles when the login button is pressed
def login_pressed():
# get the username and password. 
    username = request.form.get("username")
    password = request.form.get("password")   
# TODO we need send the database this data and verify it
    # if info is wrong, raise error 
    # Otherwise if everything is correct, redirect to the correct home page for the specific user
    user = "Officer" # something we get back from the database
    return redirect(f"/home_{user}")


@app.route("/signup")
# a page where a new user and register in the database
def signup_page():
    return render_template("signup.html")



@app.route("/signup_pressed", methods = ["POST"])
# # handle when the "submit" button is pressed
def signup_pressed():
# get info
    username = request.form.get("username")
    password = request.form.get("password")   
    officer_select = request.form.get("officer_select")
    criminal_select = request.form.get("criminal_select")
    id = request.form.get("ID")
    ""    
# TODO we need to verify if the id that was inputted is already in the database
    # if they are not, raise error
    # otherwise validate the registering by redirecting to login page
    return redirect("/")

@app.route('/home_<user>')
# 
def home(user):
    if (user == "Officer"):
        return render_template("Officer/officer_home.html") # render officer home page
        
    elif (user == "Criminal"):
        ... # reder criminal home page

    return "hi"

@app.route('/Search_Criminal')
def Search_Criminal():
    return render_template('Officer/Search_Criminal.html')

@app.route('/Search_Alias')
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

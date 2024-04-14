from flask import Flask, render_template, request, redirect

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
    user = ... # something we get back from the database
    return redirect(f"/home_{user}")

@app.route("/signup")
# a page where a new user and register in the database
def signup_page():
    return render_template("signup.html")

@app.route("/signup_pressed", methods = ["POST"])
# handle when the "submit" button is pressed
def signup_pressed():
# get info
    username = request.form.get("username")
    password = request.form.get("password")   
    officer_select = request.form.get("officer_select")
    criminal_select = request.form.get("criminal_select")
    id = request.form.get("ID")
# TODO we need to verify if the id that was inputted is already in the database
    # if they are not, raise error
    # otherwise validate the registering by redirecting to login page
    return redirect("/")


@app.route('/home_<user>')
# 
def home(user):
    if (user == "Officer"):
        ... # render officer home page
        
    elif (user == "Criminal"):
        ... # reder criminal home page

    return "hi"


if __name__ == '__main__':
    app.run(debug=True)
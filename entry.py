from flask import Flask, render_template, request, redirect


def login_pressed(app):
# get the username and password. 
    username = request.form.get("username")
    password = request.form.get("password")   
# TODO we need send the database this data and verify it
    # if info is wrong, raise error 
    # Otherwise if everything is correct, redirect to the correct home page for the specific user
    user = ... # something we get back from the database
    return redirect(f"/home_{user}")

def signup_pressed(app):
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

def sayhi(thing):
    return "hi"
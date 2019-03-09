from app import app
from flask import Flask,render_template
from flask_socketio import SocketIO

socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("student login.html")
    ##If I have time, I will probably include a function for finding the top recipes and also pulling their subscription channels "these are extras for now"
    ##Also maybe favourites
    
@socketio.on("search_database")
def search_database(json, methods=['GET','POST']):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="scrapped"
    )
    return "hi"

@app.route("/myfridge")
def myfridge():
    return render_template("my fridge.html")
##Here is where the function for pulling the info about their fridge comes in "Deluckshan"
##Also the function for advising about if the person is getting enough nutrients "Ashwin"

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/favourites")
def favourites():
    return render_template("favourites.html")
'''
@socketio.on("scan_fridge")
##Here is where the function will go for the google api code "Prabh/Ashwin"

@socketio.on("login")
##Here is where the function for OAuth for logging in using a google account "Ashwin/Prabh"

@app.route("/update")
##This is where the updating database function comes in "Deluckshan"
'''

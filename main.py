
from flask import Flask,render_template
from flask_socketio import SocketIO
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from lxml.html import fromstring
import mysql.connector
import itertools


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
@app.route("/")
def index():
    return render_template("index.html")
    ##If I have time, I will probably include a function for finding the top recipes and also pulling their subscription channels (these are extras for now)
    ##Also maybe favourites
'''
@socketio.on("search_database")
def search_database(json, methods=['GET','POST']):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="scrapped"
    )
@socketio.on("scan_fridge")
##Here is where the function will go for the google api code (Prabh/Ashwin)

@socketio.on("login")
##Here is where the function for OAuth for logging in using a google account (Ashwin/Prabh)

@app.route("/MyFridge")
##Here is where the function for pulling the info about their fridge comes in (Deluckshan)
##Also the function for advising about if the person is getting enough nutrients (Ashwin)

@app.route("/update")
##This is where the updating database function comes in (Deluckshan)
'''
if __name__ == '__main__':
    socketio.run(app, debug=True)

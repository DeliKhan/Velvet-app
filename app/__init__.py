from flask import Flask,render_template

app= Flask(__name__)
#app.config['SECRET KEY'] = 'red velvet'
app.secret_key = "super secret key"

from app import routes

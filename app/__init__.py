from flask import Flask,render_template

app= Flask(__name__)
app.config['SECRET KEY'] = 'red velvet'

from app import routes

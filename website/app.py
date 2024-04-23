import numpy as np 
from flask import Flask,request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
#create flask app
app= Flask(__name__)

#loading the pickle model
model=pickle.load(open("model.pkl","rb"))

@app.route("/")
def home():
    return render_template('index1.html')


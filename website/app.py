import numpy as np 
from flask import Flask,request,jsonify,render_template
import pickle
#create flask app
app= Flask(__name__)

#loading the pickle model
model=pickle.load(open("model.pkl","rb"))

@app.route("/")
def Home():
    return render_template('index1.html')
@app.route("/predict",methods=["POST"])
def predict():
    review=[x for x in request.form.values()]
    prediction=model.predict(review)
    return render_template("index1.html",prediction_text="the liked value is {}".format(prediction))
if (__name__=="__main__"):
    app.run(debug=True)
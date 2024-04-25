import numpy as np 
from flask import Flask,request,jsonify,render_template
import pickle
import numpy as np
import pprint
import time
import csv
import pandas as pd
import json,requests
# Declaring API Keys Use
# Declaring Global Variables Used
places_api_web_service =  'AIzaSyCztZNSls0oSkmLXe3FNjLilCA7xIp4Ork'
geocoding_api = 'AIzaSyA3cUamax65N5NLxuSF4EXuV6DGGMxDNXQ'
def latlong(loc1):
    current_loc = loc1.replace(" ", "+")

    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + current_loc + "&key=" + geocoding_api

    response1 = requests.get(geocode_url)
    data = json.loads(response1.text)

    current_lat = data['results'][0]['geometry']['location']['lat']
    current_long = data['results'][0]['geometry']['location']['lng']
    return current_lat, current_long
#create flask app
app= Flask(__name__)

#loading the pickle model
model=pickle.load(open("model.pkl","rb"))

@app.route("/")
def Home():
    return render_template('index.html')
@app.route("/",methods=["POST"])
def predict():
    friend_location=np.array([x for x in request.form.values()])
    pause = 0.1
    max_api_requests = 150000 
    api_requests_count = 0
    pp = pprint.PrettyPrinter(indent=4)
    # latlng="28.621271,77.061325"
    # radius=5
    radius = 3000
    current_lat=0
    current_long=0
    number_of_users=friend_location.size-1
    typ=friend_location[number_of_users]
    for j in range(number_of_users):
        current_lat1,current_long1=latlong(friend_location[j])
        current_lat+=current_lat1
        current_long+=current_long1
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
    if (api_requests_count < max_api_requests):  
        time.sleep(pause)
        api_requests_count += 1
        reverse_geocode_url = url + str(current_lat/number_of_users) + "," + str(current_long/number_of_users)+ "&radius=" + str(radius) + "&type="+str(typ) + "&key=" + places_api_web_service
        response = requests.get(reverse_geocode_url)
        data = response.json().get("results",{})
    if len(data) > 0:
            resp_address = data
            name = []
            types = []
            rating=[]
            lat=[]
            lng=[]
            rating=[]
            place_id_array=[]
            vicinity=[]
            review=[]
            for i in range (0, len(resp_address)):
                place_idd=resp_address[i]['place_id']
                params = {
                "place_id": place_idd,
                "key": 'AIzaSyCztZNSls0oSkmLXe3FNjLilCA7xIp4Ork',
                "fields": "reviews"  # Request specific fields to minimize data usage
                }
                base_url = "https://maps.googleapis.com/maps/api/place/details/json"
                response = requests.get(base_url, params=params)
                place_details = response.json().get("result", {})

                rat = place_details.get("rating")
                rating.append(rat)

                rev=place_details.get("reviews", [])
                revrat=[]
                for j in range(len(rev)):
                    revrat.append(rev[j]['text'])
                    revrat.append('&&&&&')
                review.append(revrat)
                name.append(str(resp_address[i]['name']))
                types.append (resp_address[i]['types'])
                lat.append(resp_address[i]['geometry']['location']['lat'])
                lng.append (resp_address[i]['geometry']['location']['lng'])
                place_id_array.append(place_idd)
                vicinity.append (resp_address[i]['vicinity'])
    with open('cache_file.csv', 'w',encoding='utf-8') as myfile:
        wr= csv.writer(myfile, quoting=csv.QUOTE_ALL)
        heading = ["name","vicinity", "type",'latitude','longitude','rating','reviews','place_id','Sentiment Ratio']
        wr.writerow(heading)
        for i in range(len(types)):
            wr.writerow([name[i],vicinity[i],types[i],lat[i],lng[i],rating[i],review[i],place_id_array[i]])
    myfile.close()
    write=pd.read_csv("cache_file.csv")
    i=[]
    for item in write['reviews']:    
        listt=item.split('&&&&&')
        count=0
        for j in listt:
            l=model.predict([j])
            count=count+l
        i.append(count/5) 
    write.loc[:,'Sentiment Ratio']=i
    return render_template("index.html",prediction_text="the liked value is {}".format(write))
if (__name__=="__main__"):
    app.run(debug=True)
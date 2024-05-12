import numpy as np 
from flask import Flask,request,jsonify,render_template
from sqlalchemy  import create_engine, ForeignKey,Column,String, Integer, CHAR
from sqlalchemy_utils import ScalarListType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pickle
import numpy as np
import time
import json,requests
from sqlalchemy  import create_engine, ForeignKey,Column,String, String, CHAR,ARRAY,Float
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
Base=declarative_base()
class Person(Base):
    #defining basic structure of table
    __tablename__="Database"
    name        =Column("name",String,primary_key=True)
    vicinity =Column("Vicinity",String ,nullable=True)
    Type         =Column("Type",String ,nullable=True)
    latitude =Column("Latitude",String ,nullable=True)
    longitude=Column("Longitude",String,nullable=True)
    rating    = Column("rating",String ,nullable=True)
    reviews    =Column("reviews",String,nullable=True)
    place_id  =Column("place_id",String,nullable=True)
    sentiment=Column("Sentiment",String,nullable=True)
    #defining the basic structure of a classs
    def __init__(self,name,vicinity,Type,latitude,longitude,rating,reviews,place_id,sentiment):
        self.name=name
        self.vicinity=vicinity
        self.Type=Type
        self.latitude=latitude
        self.longitude=longitude
        self.rating=rating
        self.reviews=reviews
        self.place_id=place_id
        self.sentiment=sentiment
    def __repr__(self): #reprint function 
        return f"({self.name})({self.vicinity})({self.Type})({self.latitude})({self.longitude})({self.rating})({self.reviews})({self.place_id})({self.sentiment})"
engine=create_engine("sqlite:///mydb.db",echo=True)
Base.metadata.create_all(bind=engine)#takes all the class and put them  in seperate tables in a single database
Session = sessionmaker(bind=engine)
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
app.static_folder = 'static'
#loading the pickle model
model=pickle.load(open("model.pkl","rb"))

@app.route("/")
def Home():
    return render_template('index.html')
@app.route("/",methods=["POST"])
def predict():
    friend_location=np.array([x for x in request.form.values()][1:])
    pause = 0.1
    max_api_requests = 150000 
    api_requests_count = 0
    # latlng="28.621271,77.061325"
    # radius=5
    radius = 5000
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
        Sentiment=[]
        for i in range (0, len(resp_address)):
            place_idd=resp_address[i]['place_id']
            params = {
            "place_id": place_idd,
            "key": 'AIzaSyCztZNSls0oSkmLXe3FNjLilCA7xIp4Ork',
            "fields": "reviews,rating"  # Request specific fields to minimize data usage
            }
            base_url = "https://maps.googleapis.com/maps/api/place/details/json"
            response = requests.get(base_url, params=params)
            place_details = response.json().get("result", {})
            rat = place_details.get("rating",None)
            rating.append(rat)
            
            count=0
            rev=place_details.get("reviews", [])
            revrat=[]
            for j in range(len(rev)):
                revrat.append(rev[j]['text'])
                l=model.predict([rev[j]['text']])
                count=count+l
            Sentiment.append(count) 
            review.append(revrat)
            name.append(str(resp_address[i]['name']))
            types.append (resp_address[i]['types'])
            lat.append(resp_address[i]['geometry']['location']['lat'])
            lng.append (resp_address[i]['geometry']['location']['lng'])
            place_id_array.append("https://www.google.com/maps/place/?q=place_id:"+place_idd)
            vicinity.append (resp_address[i]['vicinity'])    
    session = Session()
    try:
        # Delete all existing entries
        session.query(Person).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Failed to clear the table: {e}")

    for j in range(len(resp_address)):
        try:
            person = Person(
                name=str(name[j]),
                Type=str(types[j]),
                rating=str(rating[j]),
                latitude=str(lat[j]),
                longitude=str(lng[j]),
                place_id=str(place_id_array[j]),
                vicinity=str(vicinity[j]),
                reviews=str(review[j]),
                sentiment=str(Sentiment[j])
            )
            session.add(person)
            session.commit()

        except Exception as e:
            session.rollback()  # Roll back the transaction on error
            print(f"Failed to insert data for index {j}: {e}")  # Print or log the error
    query_asc = session.query(Person).order_by(Person.sentiment.desc())
    # Close the session
    return render_template('index.html',allrecords=query_asc)

    
if (__name__=="__main__"):

    app.run(debug=True)
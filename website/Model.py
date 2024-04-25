import json
import os
import csv
import requests
import pprint
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path
import joblib
from joblib import memory
import pickle
# supress warnings
import warnings 
warnings.filterwarnings('ignore')
import seaborn as sns
import matplotlib.pyplot as plt
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score
review_train=pd.read_csv("Restaurant_reviews.csv")
def text_clean_1(text):
    text = text.lower()
    text = re.sub('', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text
cleaned1 = lambda x: text_clean_1(x)
review_train['cleaned_description'] = pd.DataFrame(review_train.Review.apply(cleaned1))

def text_clean2(text):
    text=re.sub('[‘’“”…]', '', text)
    text=re.sub('\n', '', text)
    return text

cleaned2=lambda x: text_clean2(x)
review_train['cleaned_new']=pd.DataFrame(review_train['cleaned_description'].apply(cleaned2))

#NOW OUR DATA IS CLEAN
#Model Training
x=review_train['cleaned_new']
y=review_train['Liked']
x_train, x_test, y_train, y_test=train_test_split(x, y, test_size=0.2, random_state=10)  
tvec = TfidfVectorizer()
clf2 = LogisticRegression(solver = "lbfgs")   
model = Pipeline([('vectorizer',tvec),('classifier',clf2)])
model.fit(x_train, y_train)
predictions = model.predict(x_test)
confusion_matrix(predictions, y_test)
pickle.dump(model, open("model.pkl", "wb"))

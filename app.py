from flask import Flask, render_template, request
from openai import OpenAI
from config import *
import spacy
from utils import Named_Entity_Recognition_Validation,Analyze_Sentiment
from textblob import TextBlob
import re
from collections import defaultdict
from database import  Add_to_Db,Update_Username_if_Dummy


import sqlite3
#Database code
connection = sqlite3.connect('chatbot.db',check_same_thread=False)
cursor = connection.cursor()
table_schema = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        phone_number TEXT
    );
'''
cursor.execute(table_schema)
#Spacy NLP MODEL for NER
nlp_NER = spacy.load("en_core_web_sm")
#Deploying in local using custom html
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    prompts.append({"role": "user","content": message})

    #Name entity recognition and validation fuction will
    # return a defaultdict with all the validated entities

    NER=Named_Entity_Recognition_Validation(nlp_NER,message)
    print("NER",NER)
    #Add to database
    if NER:
        #This function will add new data to the db, and only if the db column is null for a user add the data again
        Add_to_Db(NER,2,cursor,connection)
        if "name" in message:
            if NER["PERSON"]:
                for keyword in keywords:    # kewords are specified in config.py
                    if keyword in message:
                        #when a dummy name to new name  is detected this function will update existing name with new name
                        Update_Username_if_Dummy(2, NER["PERSON"][0],cursor,connection)

    else:
        print("No NER So skipping db")
    SA_Label,SA_Polarity=Analyze_Sentiment(message) # Sentiment Anlaysis 
    print("SA_Label",SA_Label)
    print("SA_Polarity",SA_Polarity)

    # Send the message to OpenAI's API and receive the response
    
    client = OpenAI()# Add openAI Api key inside Openai

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=prompts,
    temperature=openai_config["temperature"],
    max_tokens=openai_config["max_tokens"],
    top_p=openai_config["top_p"],    #openai_config in config.py
    frequency_penalty=openai_config["frequency_penalty"],
    presence_penalty=openai_config["presence_penalty"]
    )
    if response.choices[0].message!=None:
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    else :
        return 'Failed to Generate response!'
    

if __name__=='__main__':
    app.run(debug=True) #App running in debug mode for real time debugging


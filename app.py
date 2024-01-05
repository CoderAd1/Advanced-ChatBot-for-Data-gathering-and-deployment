from flask import Flask, render_template, request
from openai import OpenAI
from config import *
import spacy
from utils import Named_Entity_Recognition_Validation,Analyze_Sentiment,Clean_Input,get_first_words,get_column_as_list
from textblob import TextBlob
import re
from collections import defaultdict
from database import  Add_to_Db,Update_Username_if_Dummy
# import pandas as pd


import sqlite3
#Database code
connection = sqlite3.connect('chatbot.db',check_same_thread=False)
cursor = connection.cursor()
table_schema1='DROP TABLE IF EXISTS users;'
cursor.execute(table_schema1)
table_schema = '''
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        phone_number TEXT
    );
'''
cursor.execute(table_schema)
#Spacy NLP MODEL for NER
nlp_NER = spacy.load("en_core_web_sm")
first_words_list = get_column_as_list("Indian_Names.csv", 1)[1:] # Using a kaggle dataset to get 6k indian names in sorted order so that
#Even if spacy was not able to identify the name entities, we can do a binary search and find the names from this

print("First words are as follows",first_words_list[:10])
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
    print("First words are as follows",first_words_list[:10])
    #prompts.append({"role": "user","content": message})

    #Name entity recognition and validation fuction will
    # return a defaultdict with all the validated entities

    NER=Named_Entity_Recognition_Validation(nlp_NER,message,first_words_list)
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
                        Update_Username_if_Dummy(2, NER["PERSON"],cursor,connection)
                        break

    else:
        print("No NER So skipping db")
    SA_Label,SA_Polarity=Analyze_Sentiment(Clean_Input(message)) # Sentiment Anlaysis 
    print("SA_Label",SA_Label)
    print("SA_Polarity",SA_Polarity)
    message = f"User sentiment: {SA_Label} ({SA_Polarity:.2f})\nUser: {Clean_Input(message)}\nChatBot:"
    print("message is :",message)
    prompts.append({"role": "user","content": message})
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


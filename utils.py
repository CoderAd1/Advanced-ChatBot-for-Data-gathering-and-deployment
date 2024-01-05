import re
from collections import defaultdict
from textblob import TextBlob

def Named_Entity_Recognition_Validation(nlp,user_response,first_words_list):
    # Validate email using a simple regex pattern
    def is_valid_email(email):
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return bool(re.match(email_pattern, email))

    # Validate phone number using a simple regex pattern
    def is_valid_phone_number(phone_number):
        phone_pattern = re.compile(r'^\d{10}$')
        return bool(re.match(phone_pattern, phone_number))

    # Validate age using a simple range check
    def is_valid_age(age):
        return 10 <= age <= 80  

    #Check for email ids since it needs to extracted seperately
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, user_response)
    #Check for phone numbers since it needs to extracted seperately
    phone_pattern = re.compile(r'\b(?:\+\d{1,2}\s?)?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b')
    phone_numbers = re.findall(phone_pattern, user_response)


    # Extract entities using spaCy NER
    doc = nlp(user_response)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    for email in emails:
      entities.append((email,"EMAIL"))
    for phone_number in phone_numbers:
      entities.append((phone_number,"PHONE_NUMBER"))
    #print(entities)

    # Validate and extract specific entities
    # Using Deafault Dict to handle cases where there are more than one entity of the same label
    # If not only the last entity of the corresponding label will be saved
    Validated_Entity=defaultdict(list)
    for entity, label in entities:
        if label == 'PERSON':
            Validated_Entity[label].append(entity.lower())
        elif label == 'EMAIL' and is_valid_email(entity):
            Validated_Entity[label].append(entity)
        elif label == 'PHONE_NUMBER' and is_valid_phone_number(entity):
            Validated_Entity[label].append(entity)
        elif label == 'AGE' and entity.isdigit() and is_valid_age(int(entity)):
            Validated_Entity[label].append(entity)
    lower_input=[word.lower() for word in user_response.split()]
    #if 'PERSON' not in entities:
    if "name" in lower_input:
        for i in lower_input:
            if binary_search(first_words_list,i.lower()):#i.lower() in first_words_list
                Validated_Entity["PERSON"].append(i.lower())
                print("NER Found Using Search: ",i.lower())
    Validated_Entity["PERSON"] = list(set(Validated_Entity["PERSON"]))#Removing duplictes if both spacy and binary search detects same name entities
    return Validated_Entity

def Analyze_Sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)

    # Get the sentiment polarity
    sentiment_polarity = blob.sentiment.polarity

    # Determine the sentiment label based on polarity
    if sentiment_polarity > 0:
        sentiment_label = 'Positive'
    elif sentiment_polarity < 0:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return sentiment_label, sentiment_polarity

def Clean_Input(user_message):
    # Remove any potentially harmful characters or symbols
    cleaned_message = "".join(c for c in user_message if c in ["@",",",".","-"] or c.isalnum() or c.isspace() )
    return cleaned_message

def get_first_words(file_path):
    first_words = []
    try:
        with open(file_path, 'r',encoding="utf8") as file:
            for line in file:
                # Split the line into words and get the first word
                first_word = line.strip().split()[0] if line.strip() else None
                if first_word:
                    first_words.append(first_word)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    return first_words
import csv

def get_column_as_list(file_path, column_index):
    column_values = []
    
    with open(file_path, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        
        for row in reader:
            # Ensure the row has enough columns to avoid index out of range error
            if column_index < len(row):
                column_values.append(row[column_index])
                
    return column_values

def binary_search(sorted_list, target):
    low, high = 0, len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_value = sorted_list[mid]

        if mid_value == target:
            return True  # Found the target, return its index
        elif mid_value < target:
            low = mid + 1  # Target is in the right half
        else:
            high = mid - 1  # Target is in the left half

    return False  # Target is not in the list

# # Example usage:
# file_path = 'your_file.csv'
# column_index = 2  # Replace with the index of the column you want to extract (0-based)

# column_list = get_column_as_list(file_path, 2)
# print(column_list)

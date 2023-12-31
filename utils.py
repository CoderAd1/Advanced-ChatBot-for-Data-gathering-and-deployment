import re
from collections import defaultdict
from textblob import TextBlob

def Named_Entity_Recognition_Validation(nlp,user_response):
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
            Validated_Entity[label].append(entity)
        elif label == 'EMAIL' and is_valid_email(entity):
            Validated_Entity[label].append(entity)
        elif label == 'PHONE_NUMBER' and is_valid_phone_number(entity):
            Validated_Entity[label].append(entity)
        elif label == 'AGE' and entity.isdigit() and is_valid_age(int(entity)):
            Validated_Entity[label].append(entity)
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
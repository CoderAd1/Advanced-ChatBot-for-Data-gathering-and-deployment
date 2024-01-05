# Chatbot using OpenAI API

This is a simple chatbot application built using the OpenAI API and Flask framework. The chatbot leverages the power of OpenAI's GPT-3.5-turbo model to generate responses based on user input.

## Updates
### Cant process finetuning due to OpenAI Trial Account Issue,but code snippets included in ```fine_tune.py``` 
1. Incorporated ```fine_tune.py``` which will create a fine tuned model with the input data(JSON Formatted) present inside ```test_sample1.jsonl```.The more training data going inside ```test_sample1.jsonl``` will make the fine tuned model:
    -  enhance user engagement by initiating conversations with small talk and subtly leading into questions related to personal data.
    - Add variety in conversation direction.
    - Improved actions  while redirecting the conversation when denied or faced with certain responses.
2. Feel free to add more items inside ```test_sample1.jsonl``` as currently i have added only 15 specific cases where the 
    - First 5 are targetinng the actual chatbot target and actual scenarios
    - Next 5 scenarios will add verity to the user conversaion 
    - The last 5 scenarios will counter prompt injection using sentiment analysis for all these cases
        - Unauthorized Access Attempt
        - Malicious Code Injection Attempt
        - Social Engineering Attempt
        - Bias Exploitation Attempt
        - Information Disclosure Attempt
    - For getting a really good model add atleast **100** scenarios into the ```test_sample1.jsonl``` file
3. The feature of Prompt injection is effectively executed using sentiment analysis and Fine tuning scenarios
    - For easier exceution using textblob sentiment polarity(Current code)
    - For more accurate results we can use transformer sentiment-analysis pipeline code included in ```miscellaneous.py```(Can update to pipelines with higher disck space and Ram)
4. Updated the code for overwriting + task 
    - Initally only spacy was used to identify names, but spacy which is an english model fails to identitify indian names like rahul, ahhil etc 
    - Added an extra level of confidence by incorporating a kaggle dataset with processed indian names in sorted order
        - So when a message is send to the charbot and the keywork ```name``` is there in the message the whole message will put through a binary search to find if indian names are in the message 
        - These captured indian names will be then used to Overwrite the Database
        - The overwrite will only happen if the keywords are present in the message ```name``` and  ```["real","dummy","fake","actual","factual" ,"true","wrong","not"]```.
        - Here also we are checking 2 scenarios:
            - If the User is saying only single name in his chat like eg:```"My real name is Aakash"``` , then his previous username will be overwritten by aakash
            - If the User is saying both his real name and dummy name eg1 :```"Aabid is a dummy name ,my real name is Aakash"``` or eg2 :```"my real name is Aakash,not aabid"```
            we will identitify the name which is present in the database and overwrite with the other name
5. Even After all these updates it is not guranteed that our names can be identified by spacy or using binary serach in a dataset
    - Even my name Adwaith is not getting identified by spacy and not in the common ```Indian_Names.csv``` file
    - For this we might have to either expand the ```Indian_Names.csv``` or create a finetued model which can accurately identify indian names

## Getting Started



### Prerequisites

Before running the chatbot, ensure you have the necessary dependencies installed. You can install them using the following:

```bash
pip install Flask openai spacy textblob
```
or
```bash
pip install -r requirements.txt
```
Make sure to also download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```
Running the Application
Add your Chatgpt API key to the python code here:
```Python
client = OpenAI(<yourAPIkey>)
```
or

Add your Chatgpt API key  to the code via Environment variable

Run the following in the cmd prompt, replacing <yourAPIkey> with your API key:
```bash
setx OPENAI_API_KEY “<yourAPIkey>”
```
Before the chatbot, execute the following command to run finetune script:

```bash
python fine_tune.py
```
It will print the model name , which can then be copy pasted into line:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo", # The finetuned model name can be added over here
    messages=prompts,
    temperature=openai_config["temperature"],
    max_tokens=openai_config["max_tokens"],
    top_p=openai_config["top_p"],    #openai_config in config.py
    frequency_penalty=openai_config["frequency_penalty"],
    presence_penalty=openai_config["presence_penalty"]
    )
```
To run the chatbot, execute the following command:

```bash
python app.py
```


Visit http://127.0.0.1:5000/ in your web browser to interact with the chatbot through the provided web interface.
### Database Setup
The chatbot uses SQLite for storing user data. The database is initialized with the following schema:

```sql

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT,
    phone_number TEXT
);
```


## Usage
1.Access the chatbot interface by visiting the root URL (e.g., http://127.0.0.1:5000/).

2.Enter your message in the input field and submit.

3.The chatbot processes your message, performs named entity recognition (NER), sentiment analysis, and updates the database.

4.The chatbot sends the processed conversation to the OpenAI API and displays the generated response.

## Features
* Named Entity Recognition (NER): Identifies and validates entities in user input.

* Sentiment Analysis (SA): Analyzes the sentiment of user input.

* Database Integration: Stores user data in an SQLite database.

* OpenAI Integration: Utilizes the OpenAI GPT-3.5-turbo model for generating chatbot responses.

## Notes
* The code is not full optimized for production as there are multiple print statements inside the code for debugging
* The code is written dynamically with `config.py` containing the configurations and prompts for the Open AI api
* Also the ```database.py``` contains files and functions for SQLite Database
* Then the ```utils.py``` contains the Named Entity Recognition (NER) and Sentiment Analysis (SA) code
* These are called in ```app.py``` for API Excecution and full run

## Advanced Features
* The Chatbot can create and update user data into the Database automatically by analysing Named Entities
* It can overwrite a saved username if the user gave a dummy username and later decides to give correct user name
* It can not only do Named Entity Recognition (NER) but also validate the entities using regular expressions 
* The code also has Sentiment Analysis (SA) implimented which can prevent prompt injection
* We also provide a basic User Interface for seamless testing with the Chatbot
* Use VScode SQLite Viewer to see the Database getting updated in realtime, if running is VScode

![Chatbot Image](templates/image1.png)

## Limitations
* The spacy English language model can right now only process US names, so Indian names wont be processed correctly all  the time(Can be solved by fine tuning)
* ChatGPT Api is used with certain prompting (mentioned in ```config.py```) so the chatbot may behave weirdly(Can be solved by Fine tuning)
* More scenarios have to identified and added to the dummy username update code
* Chatbot replies are slow since print statements are added for verifing work flow(Once its cleaned up, it will be really fast)
* Right now userid is hard code for a single user and single session for testing (while in production can easily update to multiple users and multiple sessions )

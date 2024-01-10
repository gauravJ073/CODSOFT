# Importing modules
import re
from nltk.corpus import wordnet

list_words=['hello','timings', 'deposit', 'withdraw', 'check']
list_syn={}
for word in list_words:
    synonyms=[]
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            # Remove any special characters from synonym strings
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    list_syn[word]=set(synonyms)
# print (list_syn)


# Building dictionary of Intents & Keywords
keywords={}
keywords_dict={}
for key in list_syn.keys():
    keywords[key]=[]
    for synonym in list(list_syn[key]):
        keywords[key].append('.*\\b'+synonym+'\\b.*')

for intent, keys in keywords.items():
    # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
    keywords_dict[intent]=re.compile('|'.join(keys))
# print (keywords_dict)

balance=10000
def hello(balance):
    print('Hello! How can I help you?')
    return balance 

def timings(balance):
    print('We are open from 9AM to 5PM, Monday to Friday. We are closed on weekends and public holidays.')    
    return balance

def check(balance):
    print(f'Balance={balance}')
    print('What more can I help you with?')
    return balance

def withdraw(balance):
    amount=int(input("Enter amount: "))
    balance = balance - amount
    print("money withdrawn")
    print('What more can I help you with?')
    return balance

def deposit(balance):
    amount=int(input("Enter amount: "))
    balance= balance + amount
    print("money deposited")
    print('What more can I help you with?')
    return balance

def unknown(balance):
    print('I dont quite understand. Could you repeat that?')
    return balance



# Building a dictionary of responses
responses={
    'hello':hello,
    'timings':timings,
    'check':check,
    'withdraw':withdraw,
    'deposit':deposit,
    'unknown':unknown,
}


print ("Welcome to MyBank. How may I help you?")
# While loop to run the chatbot indefinetely
while (True):  
    # Takes the user input and converts all characters to lowercase
    
    user_input = input("Enter response")
    user_input=user_input.lower()
    # Defining the Chatbot's exit condition
    if user_input in ['exit','quit']:
        print ("Thank you for visiting.")
        break    
    matched_intent = None
    for intent,pattern in keywords_dict.items():
        
        # print(intent)
        # Using the regular expression search function to look for keywords in user input
        if re.search(pattern, user_input): 
            # if a keyword matches, select the corresponding intent from the keywords_dict dictionary
            matched_intent=intent  
    # The fallback intent is selected by default
    key='unknown' 
    if matched_intent in responses:
        # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
        key = matched_intent
    # The chatbot prints the response that matches the selected intent
    balance=responses[key](balance) 
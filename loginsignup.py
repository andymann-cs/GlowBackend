from PySide6 import QtWidgets, QtGui, QtCore
from better_profanity import profanity
import re
import sys
import hashlib
import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster",
    tls=True,
    tlsAllowInvalidCertificates=True
)
db = client["mood_tracker"]
collection = db["accounts"]

def encrypt(password): ##PLACEHOLDER FOR ACTUAL ENCRYPTION, BOTH LOGIN AND PASSWORD USE THIS
    return password

def verify_login(username, password_decrypted):
    login_successful = False  # Custom signal with username
    password_encrypted = encrypt(password_decrypted)
    user = collection.find_one({"username": username, "password": password_encrypted})
    if user:
        login_successful = True
    return login_successful

#window.login_successful.connect(lambda username: print(f"Logged in as: {username}")) --What is this?

def SignupLogic(name, sex, age, hobbies, username, password, password_repeat): #Bundles all inputs together atm
    signup_successful = False  # Define signal

    def contains_embedded_profanity(text):
        profanity.load_censor_words()
        words = re.findall(r'[a-zA-Z]+', text)  
        for word in words:
            if profanity.contains_profanity(word):
                return True
        return False

    if password != password_repeat:
        return "passwords do not match"
        
    if collection.find_one({"username": username}):  # Fixed checking existing user
        return "username already exists"
        
    if contains_embedded_profanity(username):
        return "username must not contain prohibited words"
        
    if username == "" or password == "":
        return "please fill out all of the required fields"
    
    # Save user to database
    collection.insert_one({
        "name": name,
        "sex": sex, 
        "age": age,
        "hobbies": hobbies,
        "username": username,
        "password": encrypt(password),
    })
    
    signup_successful = True
    return signup_successful

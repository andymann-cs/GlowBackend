#from PySide6 import QtWidgets, QtGui, QtCore
from better_profanity import profanity
import re
import sys
import hashlib
import pymongo

# client = pymongo.MongoClient(
#     "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster",
#     tls=True,
#     tlsAllowInvalidCertificates=True
# )
# db = client["mood_tracker"]
# collection = db["accounts"]

class loginSignup():
    def __init__(self, db):
        self.db = db

    def encrypt(self, password): ##PLACEHOLDER FOR ACTUAL ENCRYPTION, BOTH LOGIN AND PASSWORD USE THIS
        return password

    def verify_login(self, username, password_decrypted):
        login_successful = False  # Custom signal with username
        password_encrypted = self.encrypt(password_decrypted)

        self.collection = self.db["accounts"]
        user = self.collection.find_one({"username": username, "password": password_encrypted})
        if user:
            login_successful = True
        return login_successful

#window.login_successful.connect(lambda username: print(f"Logged in as: {username}")) --What is this?

    def contains_embedded_profanity(self, text):
        profanity.load_censor_words()
        words = re.findall(r'[a-zA-Z]+', text)  
        for word in words:
            if profanity.contains_profanity(word):
                return True
        return False


    def SignupLogic(self, username, password, password_repeat, name, age, sports, hobbies, sex): #Bundles all inputs together atm
        #signup_successful = False  # Define signal

        if password != password_repeat:
            return {"error": "passwords do not match"}
            
        self.collection = self.db["accounts"]
        if self.collection.find_one({"username": username}):  # Fixed checking existing user
            return {"error": "username already exists"}
            
        if self.contains_embedded_profanity(username):
            return {"error": "username must not contain prohibited words"}
            
        if username == "" or password == "":
            return {"error": "please fill out all of the required fields"}
        
        # Save user to database
        self.collection.insert_one({
            "username": username,
            "password": self.encrypt(password),
            "name": name,
            "age": age,
            "exercises": sports,
            "hobbies": hobbies,
            "sex": sex, 
        })
        

        return {"message": "Account created Successfully"}

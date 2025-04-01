from genFakeData import genFakeData
from pymongo import MongoClient 
from bson import ObjectId
import datetime
import random

class DB_CRUD():
    def __init__(self):
        #self.uri = "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"
        #self.uri = "mongodb+srv://user_app:8JSL3N0uHNjSwnmY@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"
        #self.client = MongoClient(self.uri)
        self.client = MongoClient("mongodb+srv://user_app:8JSL3N0uHNjSwnmY@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
        self.db = self.client["mood_tracker"]
        
        #Set collection to moods initially FOR NOW
        #self.collection = self.db["moods"]


    #Consider Validation and error handling

    def getUserID(self, username):
        self.collection = self.db["accounts"]
        try:
            user = self.collection.find_one({"username": username})
            if user:
                return {"user_id": str(user["_id"])}
            else:
                return {"error" : "User does not exist"}
        except Exception as e:
            return{"error" : str(e)}

    def getUsername(self, userID):
        self.collection = self.db["accounts"]
        try:
            username = self.collection.find_one({"_id": ObjectId(userID)})
            if username:
                return {"username" : username["username"]}
            else:
                return {"error" : "User does not exist"}
        except Exception as e:
            return{"error" : str(e)}


    #date as unique?? or id
    def insertMood(self, username, mood, sleep, screen, exercise, alcohol, date):
        self.collection = self.db["moods"]
        username = self.getUserID(username)
        if not username:
            return {"error" : "User Does Not Exist"}
        
        example = {
                "userID": username,
                "mood": mood,
                "alcohol": alcohol,
                "exercise": exercise,
                "screen": screen,
                "sleep": sleep,                
                "date": date
        }
        self.collection.insert_one(example)
        
        return{"may" : "have worked?"}

    def getMoods(self, username):
        self.collection = self.db["moods"]
        mood = self.collection.find({"user_id" : self.getUserID(username)})
        return mood

    #Need to change the time
    # def getLastWeekMoods(self, username):
    #     self.collection = self.db["moods"]
    #     cutoffTime = int(time.time()) - (60*60*24*7)
    #     moods = self.collection.find({"user": username, "date": {"$gte": cutoffTime}})
    #     return list(moods)


    def updateMood(self, username, mood, alcohol, exercise, screen, sleep, date):
        self.collection = self.db["moods"]

        userID = self.getUserID(username)
        if not userID:
            return {"error": "User does not exist"}

        requirement = {"user_id": userID, "date": date}

        changes = {
            "$set": {
                    "mood":mood,
                    "sleep" : sleep,
                    "screen" : screen,
                    "exercise" : exercise,
                    "alcohol" : alcohol
                    }
                }
        self.collection.update_one(requirement, changes)



    def deleteMood(self, userID):
        self.collection = self.db["moods"]
        self.collection.delete_many({"user_id": userID, 
                                   })



    def getMonthlyMood(self, userID, month, year):
        self.collection = self.db["moods"]

        moodData = {}
        start = f"{year}-{month:02d}-01"
        end = f"{year}-{month+1:02d}-01"

        retrievedDocs = self.collection.find({
            "user_id":userID,
            "date": { 
                "$gte" : start,
                "$lt" : end
                }
            }
        )

        for doc in retrievedDocs:
            docMood = doc.get("mood")
            if docMood in moodData:
                moodData[docMood] += 1
            else:
                moodData[docMood] = 1

        return moodData
        

    def deleteUserRecords(self, userID):
        self.collection = self.db["accounts"] 
        docs = self.collection.delete_many({"user_id": userID})

    def getRandomActivity(self, username):
        self.collection = self.db["accounts"]
        doc = self.collection.find_one({"username" : username})
        exerciseList = doc.get("exercises")
        activity = random.randint(0,len(exerciseList)-1)

        return exerciseList[activity]


# uri = "mongodb+srv://user_app:8JSL3N0uHNjSwnmY@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"
# client = MongoClient(uri)
# db = client["mood_tracker"]
# collection = db["accounts"]
# user = collection.find_one({"username": "sammy"})
# if user:
#     print( {"user_id": str(user["_id"])})
# else:
#     print( {"error" : "User does not exist"})

client = MongoClient("mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
db = client["mood_tracker"]
collection = db["accounts"]
result = collection.find_one({"username": "sammy"})
print(result["username"] if result else None)
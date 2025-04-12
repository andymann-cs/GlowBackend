from genFakeData import genFakeData
from pymongo import MongoClient 
from bson import ObjectId
import datetime
import random

class DB_CRUD():
    def __init__(self, db):
        self.factors = ["mood", "alcohol", "sleep", "screen", "exercise"]
        self.moodList = ["angry", "sad", "tired", "happy", "content", "excited", "proud", "stressed", "sick", "unsure"]
        #self.uri = "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"
        #self.uri = "mongodb+srv://user_app:8JSL3N0uHNjSwnmY@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"
        #self.client = MongoClient(self.uri)
        #self.client = MongoClient("mongodb+srv://user_app:8JSL3N0uHNjSwnmY@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
        self.db = db
        
        #Set collection to moods initially FOR NOW
        #self.collection = self.db["moods"]


    #Consider Validation and error handling
    def checkValidFactor(self, testFactor):
        if testFactor in self.factors:
            return True
        else:
            return False
      
    def checkValidMood(self, mood):
        if mood in self.moodList:
            return True
        else:
            return False

    #takes a username, returns corresponding user_id
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

    #takes a user_id, returns corresponding username
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
    def insertMood(self, username, mood, sleep, screen, exercise, alcohol, date, diary):

        self.collection = self.db["moods"]
        userID = self.getUserID(username)["user_id"]
        if not userID:
            return {"error" : "User Does Not Exist"}
        
        mood_entry = {
                "userID": userID,
                "mood": mood,
                "alcohol": alcohol,
                "exercise": exercise,
                "screen": screen,
                "sleep": sleep,                
                "date": date,
                "diary": diary
        }
        self.collection.insert_one(mood_entry)
        
        return{"attempt" : "successful"}

    # def getMoods(self, username):
    #     self.collection = self.db["moods"]
    #     mood = self.collection.find({"user_id" : self.getUserID(username)})
    #     return mood

    #Need to change the time
    # def getLastWeekMoods(self, username):
    #     self.collection = self.db["moods"]
    #     cutoffTime = int(time.time()) - (60*60*24*7)
    #     moods = self.collection.find({"user": username, "date": {"$gte": cutoffTime}})
    #     return list(moods)

    #update an exsiting entry (NEEDS TESTING)
    def updateMood(self, username, mood, alcohol, exercise, screen, sleep, date):
        self.collection = self.db["moods"]

        user_id = self.getUserID(username)["user_id"]
        if not user_id:
            return {"error": "User does not exist"}

        requirement = {"user_id": user_id, "date": date}

        changes = {
            "$set": {
                    "mood":mood,
                    "sleep" : sleep,
                    "screen" : screen,
                    "exercise" : exercise,
                    "alcohol" : alcohol
                    }
                }
        result = self.collection.update_one(requirement, changes)
        if result.matched_count == 0:
            return {"error": "No matching mood entry found to update"}
        return {"message": "Mood updated successfully"}

    #delete every mood entry from the moods collection
    def deleteMood(self, username):
        self.collection = self.db["moods"]
        user_id = self.getUserID(username)["user_id"]
        print(f"Retrieved user_id: {user_id}")
        print(f"Deleting moods with query: {{'user_id': {user_id}}}")
  
        result = self.collection.delete_many({"user_id": user_id})

        username = self.collection.many({"user_id": user_id})
        return username
        if result.deleted_count > 0:
            return {"message": f"Successfully deleted {result.deleted_count} mood entries"}
        else:
            return {"error": "No matching mood entries found to delete"}

    #Grab a list of the specified factor for the whole of a month
    def getMonthlyFactorList(self, username, month, year, factor):
        if not self.checkValidFactor(factor):
            return None
        
        userID = self.getUserID(username)["user_id"]
        if not userID:
            return {"error": "User does not exist"}

        self.collection = self.db["moods"]
        moodDict = {}
        allDocs = []
        start = f"{year}-{month:02d}-01"

        if month == 12:
            end = f"{year+1}-01-01"
        else:
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
            docDate = doc.get("date")
            docMood = doc.get(factor)
            moodDict[docDate] = docMood
        
        for day in range(1, 31+1):
            currentDay = f"{year}-{month:02d}-{day:02d}"

            if currentDay in moodDict:
                allDocs.append(moodDict[currentDay])
            else:
                allDocs.append(None)
        return allDocs
    
    #converts a list of strings to a dictionary of form {"factor": "count"}
    def convertMoodListToChartDict(self, listOfMoods):
        moodData = {}
        for docMood in listOfMoods:
            if docMood in moodData:
                moodData[docMood] += 1
            else:
                moodData[docMood] = 1
        return moodData

    #delete user from accounts 
    def deleteUserRecords(self, username):
        self.collection = self.db["accounts"] 
        self.collection.delete_many({"username": username})

    #returns a random activity from the accounts section
    def getRandomActivity(self, username):
        self.collection = self.db["accounts"]
        doc = self.collection.find_one({"username" : username})
        exerciseList = doc.get("exercises")
        activity = random.randint(0,len(exerciseList)-1)

        return exerciseList[activity]

    #add a custom activity to an account
    def addCustomActivity(self, username, activityName):
        self.collection = self.db["accounts"]
        result = self.collection.update_one(
            {"username": username}, {"addToSet": {"exercises": activityName}}
        )
        if result.matched_count == 0:
            return {"error": "User not found"}
        elif result.modified_count == 0:
            return {"message": "Activity already exists"}
        else:
            return {"message": "Activity added successfully"}

    #check if log exists for a specific person and day
    def hasLoggedMoodToday(self, username, date):
        self.collection = self.db["moods"]
        user_id = self.getUserID(username)["user_id"]
        mood = self.collection.find_one({"user_id": user_id, "date": date})
        return {"logged": bool(mood)}




# uri = "mongodb+srv://user_app:8JSL3N0uHNjSwnmY@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"
# client = MongoClient(uri)
# db = client["mood_tracker"]
# collection = db["accounts"]
# user = collection.find_one({"username": "sammy"})
# if user:
#     print( {"user_id": str(user["_id"])})
# else:
#     print( {"error" : "User does not exist"})

# client = MongoClient("mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
# db = client["mood_tracker"]
# collection = db["accounts"]
# result = collection.find_one({"username": "sammy"})
# print(result["username"] if result else None)
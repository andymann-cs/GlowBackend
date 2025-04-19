from genFakeData import genFakeData
from pymongo import MongoClient 
from bson import ObjectId
from datetime import datetime, timedelta
from collections import Counter
from statistics import mean
import random

class DB_CRUD():
    def __init__(self, db):
        self.factors = ["mood", "alcohol", "sleep", "screen", "exercise", "diary"]
        self.moodList = ["angry", "sad", "tired", "happy", "content", "excited", "proud", "stressed", "sick", "unsure"]
        self.accountDetails = ["firstname", "surname", "sex", "pronouns", "age", "activities", "hobbies"]
        self.accountDetailsHide = ["password"]
        self.db = db

    #####-------------------------------VALID CHECK------------------------#####

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

    def checkValidDetail(self, detail):
        if detail in self.accountDetails:
            return True
        else:
            return False

    def bson_to_dict(self, doc):
        if not doc:
            return {}
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        return doc

    #####------------------------------ACCOUNTS----------------------------#####

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

    def getAccountDetails(self, username, detail=None):
        self.collection = self.db["accounts"]
        try:
            accountDoc = self.collection.find_one({"username": username})
            if not accountDoc:
                return {"error": "User does not exist"}

            if detail:
                if not self.checkValidDetail(detail):
                    return {"error": "Invalid detail"}
                returnedDetail = accountDoc.get(detail)
                if returnedDetail is None:
                    return {"error": "No data for this account detail"}
                return {detail: returnedDetail}
            else:
                accountDoc.pop("password", None)
                accountDoc.pop("_id", None)
                return self.bson_to_dict(accountDoc)
        except Exception as e:
            return {"error": str(e)}
        
    #returns a random activity from the accounts section
    def getRandomActivity(self, username):
        self.collection = self.db["accounts"]
        doc = self.collection.find_one({"username" : username})

        exerciseList = doc.get("exercises")
        activity = random.randint(0,len(exerciseList)-1)
        return exerciseList[activity]

    #returns a random activity from the accounts section
    def getAllActivities(self, username):
        self.collection = self.db["accounts"]
        doc = self.collection.find_one({"username" : username})
        exerciseList = doc.get("exercises")
        return exerciseList

    #add a custom activity to an account
    def addCustomActivity(self, username, activityName):
        self.collection = self.db["accounts"]
        
        account = self.collection.find_one({"username": username})
        if not account:
            return {"error": "User not found"}
        
        if "exercises" not in account:
            self.collection.update_one(
                {"username": username}, {"$set": {"exercises": []}}
        )

        result = self.collection.update_one(
            {"username": username}, {"$addToSet": {"exercises": activityName}}
        )
        if result.modified_count == 0:
            return {"message": "Activity already exists"}
        else:
            return {"message": "Activity added successfully"}

    #add a custom activity to an account
    def addCustomHobby(self, username, hobbyName):
        self.collection = self.db["accounts"]
        
        account = self.collection.find_one({"username": username})
        if not account:
            return {"error": "User not found"}
        
        if "hobbies" not in account:
            self.collection.update_one(
                {"username": username}, {"$set": {"hobbies": []}}
        )

        result = self.collection.update_one(
            {"username": username}, {"$addToSet": {"hobbies": hobbyName}}
        )
        if result.modified_count == 0:
            return {"message": "Activity already exists"}
        else:
            return {"message": "Activity added successfully"}

    #delete user from accounts 
    def deleteUserRecords(self, username):
        self.collection = self.db["accounts"] 
        self.collection.delete_many({"username": username})


    def updateProfile(self, username, detail, value):

        user_id = self.getUserID(username)
        if not user_id:
            return {"error": "User does not exist"}

        if not self.checkValidDetail(detail):
            return{"error": "Invalid account detail to update"}

        user_id = user_id["user_id"]

        # doc = self.collection.find_one({"username" : username, "date": date})
        # if factor not in doc:
        #     self.collection.update_one(
        #         {"username": username, "date": date}, {"$set": {factor: []}}
        # )

        requirement = {"user_id": user_id}
        changes = {"$set": {detail: value}}
        self.collection = self.db["accounts"]

        result = self.collection.update_one(requirement, changes)
        if result.matched_count == 0:
            return {"error": "No matching profile found to update"}
        return {"message": "profile updated successfully"}


#####------------------------------MOODS----------------------------#####

    #date as unique?? or id
    def insertMood(self, username, mood, sleep, screen, exercise, alcohol, date, diary):

        user = self.getUserID(username)
        if not user:
            return {"error" : "User Does Not Exist"}
        
        user_id = user["user_id"]
        mood_entry = {
                "user_id": user_id,
                "mood": mood,
                "alcohol": alcohol,
                "exercise": exercise,
                "screen": screen,
                "sleep": sleep,                
                "date": date,
                "diary": diary
        }

        self.collection = self.db["moods"]
        self.collection.insert_one(mood_entry)
        
        return{"message" : "mood entry added"}

    #NEEDS RENAMING - CHANGES ANY FACTOR
    def updateMood(self, username, factor, value, date):

        user_id = self.getUserID(username)
        if not user_id:
            return {"error": "User does not exist"}

        if not self.checkValidFactor(factor):
            return{"error": "Invalid factor to update"}

        if factor == "mood":
            if not self.checkValidMood(value):
                return{"error": "Invalid mood to update"}

        user_id = user_id["user_id"]

        doc = self.collection.find_one({"username" : username, "date": date})
        if factor not in doc:
            self.collection.update_one(
                {"username": username, "date": date}, {"$set": {factor: []}}
        )

        requirement = {"user_id": user_id, "date": date}
        changes = {"$set": {factor: value}}
        self.collection = self.db["moods"]

        result = self.collection.update_one(requirement, changes)
        if result.matched_count == 0:
            return {"error": "No matching mood entry found to update"}
        return {"message": "Mood updated successfully"}

    def deleteMood(self, username):
        # Get the user_id for the specified username
        user_result = self.getUserID(username)
        if "error" in user_result:
            return {"error": user_result["error"]}
        
        self.collection = self.db["moods"]
        user_id = user_result["user_id"] # Isn't stored as ObjectId for this table

        # Deleting all mood entries for the specified user_id
        result = self.collection.delete_many({"user_id": user_id})

        if result.deleted_count > 0:
            return {"message": f"Successfully deleted {result.deleted_count} mood entries"}
        else:
            return {"error": "No matching mood entries found to delete for user_id: " + user_result["user_id"]}

    #Grab a list of the specified factor for the whole of a month
    def getFactorForXDays(self, username, factor, days=30, end_day=None):
        if not self.checkValidFactor(factor):
            return None
        
        userID = self.getUserID(username)["user_id"]
        if not userID:
            return {"error": "User does not exist"}

        self.collection = self.db["moods"]
        moodDict = {}
        allDocs = []

        if end_day is not None:
            try: 
                end_date_formatted = datetime.strptime(end_day, "%Y-%m-%d")
            except ValueError:
                return {"error": "Invalid end day format. Use YYYY-MM-DD"}
        else:
            end_date_formatted = datetime.now()
            
        start_date = end_date_formatted - timedelta(days=days)
        
        retrievedDocs = self.collection.find({
            "user_id":userID,
            "date": { 
                "$gte" : start_date.strftime("%Y-%m-%d"),
                "$lt" : end_date_formatted.strftime("%Y-%m-%d")
                }
            }
        )

        for doc in retrievedDocs:
            docDate = doc.get("date")
            docMood = doc.get(factor)
            moodDict[docDate] = docMood
        
        for i in range(days):
            currentDay = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            allDocs.append(moodDict.get(currentDay, None))
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

    def getAverageFactorForXDays (self, username, factor, days=30, end_day=None):
        docResult = self.getFactorForXDays(username, factor, days, end_day)

        if factor == "mood" or not self.checkValidFactor(factor):
            return {"error": "invalid factor"}
        else:
            filteredDocResult = [v for v in docResult if v is not None]
        return mean(filteredDocResult)

    def getMostPopularMoodForXDays(self, username, days=30, end_day=None):
        docResult = self.getFactorForXDays(username, "mood", days, end_day)
        filteredDocResult = [v for v in docResult if v is not None]
        countedList = Counter(filteredDocResult)
        return countedList.most_common(1)   

        #check if log exists for a specific person and day
    
    def hasLoggedMoodToday(self, username, date):
        returnedDoc = self.getMoodEntry(username, date)
        return {"logged": bool(returnedDoc)}

    def getMoodEntry(self, username, date):
        user_id = self.getUserID(username)["user_id"]

        self.collection = self.db["moods"]
        moodDoc = self.collection.find_one({"user_id": user_id, "date": date})
        return moodDoc


#####----------------------------EXERCISE-ENTRY----------------------#####
    
    def insertExerciseEntry(self, username, activity, duration, date=None):
        user = self.getUserID(username)
        
        if not user:
            return {"error": "User not found"}
        
        if date is None:
            date = datetime.today().strftime("%Y-%m-%d")

        user_id = user["user_id"]
        exercise_entry = {
                "user_id": user_id,
                "activity": activity,
                "duration": duration,
                "date": date
        }

        self.collection = self.db["exerciseHistory"]
        self.collection.insert_one(exercise_entry)
        
        return{"message" : "exercise entry added"}



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

        #self.uri = "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"
        #self.uri = "mongodb+srv://user_app:8JSL3N0uHNjSwnmY@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"
        #self.client = MongoClient(self.uri)
        #self.client = MongoClient("mongodb+srv://user_app:8JSL3N0uHNjSwnmY@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")

        
        #Set collection to moods initially FOR NOW
        #self.collection = self.db["moods"]
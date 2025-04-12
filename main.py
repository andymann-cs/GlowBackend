## This is the connections between the Backend and the Frontend so they can be called
## When the methods are called they communicate with AWS and FastAPI to get the data from the database
## The data is then returned to the Frontend to be displayed

from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from moods import DB_CRUD
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os


class MoodData(BaseModel):
    mood: str
    sleep: float
    screen: float
    exercise: float
    alcohol: float
    date: str
    diary: Optional[str] = None



#load_dotenv()
#mongo_uri = os.getenv("MONGO_URI")

#Load and establish connection to mongo
client = MongoClient("mongodb+srv://second_admin:hL9l8r6liQROX0Up@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
db = client["mood_tracker"]
app = FastAPI()
db_crud = DB_CRUD(db)

#just a root function - test if fastAPI is responding
@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

#Calls getUserID from moods.py
@app.get("/moods/userID/getUserID/{username}")
async def getUserID(username: str):
    try:
        return db_crud.getUserID(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Calls getUsername from moods.py
@app.get("/moods/username/getUsername/{user_id}")
async def getUsername(user_id: str):
    try:
        return db_crud.getUsername(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

#Calls insertMood from moods.py, takes a body of the form of MoodData
@app.post("/moods/{username}/insert")
async def insertMood(username: str, data: MoodData):
    db_crud.insertMood(username=username, **data)
    return {"message": "Mood inserted successfully"}

#Calls getRandomActivity from moods.py
@app.get("/accounts/{username}/getRandomActivity")
async def getRandomActivity(username: str):
    try:
        return db_crud.getRandomActivity(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Calls addCustomActivity from moods.py, taking the username from the path, and body supplied
@app.post("/accounts/{username}/addActivity")
async def addCustomActivity(username: str, activity: str):
    result = db_crud.addCustomActivity(username, activity)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
    
#Calls getMonthlyFactorList from moods.py taking all parameters from the path
@app.get("/moods/lastThirtyDays/{username}/{factor}")
async def getLastThirtyDaysFactorList(username: str, factor: str, end_day: Optional[str] = Query(default=None, description="Format: YYYY-MM-DD - Default is today")):
    if not db_crud.checkValidFactor(factor):
       raise HTTPException(status_code=400, detail="Invalid factor")
    if end_day is not None:
        try:
            datetime.strptime(end_day, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        
        try:
            return db_crud.getLastThirtyDayFactor(username, factor, end_day)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

#Calls updateMood from moods.py taking username from the path, and mood entry from body provided
@app.put("/moods/{username}/update")
async def updateMood(username: str, date: str, data: MoodData):
    try:
        result = db_crud.updateMood(username=username,
                                    mood=data.mood,
                                    alcohol=data.alcohol,
                                    exercise=data.exercise,
                                    screen=data.screen,
                                    sleep=data.sleep,
                                    date=date
                                )
        
        if "error" in result:
            raise HTTPException(status_code=404, detail="uh oh")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

#Calls deleteAllMoods from moods.py taking the username from the parameter
@app.delete("/moods/{username}/deleteAll")
async def deleteAllMoods(username: str):
    try:
        result = db_crud.deleteMood(username=username)
        return {
            "message": f"All moods for {username} have been deleted.",
            "result": result 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   
    

#Calls deleteUserRecords from moods.py taking the username from the parameter
@app.delete("/accounts/{username}/delete")
async def deleteUser(username: str):
    try:
        db_crud.deleteUserRecords(username=username)
        return {"message": f"User {username} have been deleted!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
#Calls hasLoggedMoodToday from moods.py taking the username and data as parameters from the path
@app.get("/moods/{username}/hasLoggedIn/{date}")
async def hasLoggedIn(username: str, date: str):
    try:
        return db_crud.hasLoggedMoodToday(username, date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
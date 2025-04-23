## This is the connections between the Backend and the Frontend so they can be called
## When the methods are called they communicate with AWS and FastAPI to get the data from the database
## The data is then returned to the Frontend to be displayed

from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, Union, List
from datetime import datetime

from loginsignup import loginSignup
from moods import DB_CRUD
from nhslink import get_nhs_search_urls

import os


class MoodData(BaseModel):
    mood: str
    sleep: float
    screen: float
    exercise: int
    alcohol: float
    date: str
    diary: Optional[str] = None

class MoodUpdate(BaseModel):
    factor: str
    value: Union[str, int, float]

class AccountUpdate(BaseModel):
    detail: str
    value: Union[str, List[str], int]

class ExerciseEntry(BaseModel):
    activity: str
    duration: Union[int, float]
    date: Optional[str] = None

class AccountEntry(BaseModel):
    username: str
    password: str
    password_repeat: str
    name: str
    age: int
    sports: List[str]
    hobbies: List[str]
    sex: str

class LoginEntry(BaseModel):
    username: str
    password: str

#Load and establish connection to mongo
client = MongoClient("mongodb+srv://second_admin:hL9l8r6liQROX0Up@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
db = client["mood_tracker"]
app = FastAPI()

db_crud = DB_CRUD(db)
loginsignup = loginSignup(db)

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
    result = db_crud.insertMood(username, **data.dict())
    return result

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
    return result

#Calls updateMood from moods.py taking username from the path, and mood entry from body provided
@app.put("/moods/{username}/update")
async def updateMoodFactor(username: str, date: str, update: MoodUpdate):
    try:
        result = db_crud.updateMood(username=username,
                                    factor=update.factor,
                                    value=update.value,
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
    
@app.get("/nhs-search")
def nhs_search(keywords: str):
    search_urls = get_nhs_search_urls(keywords)
    return {"search_urls": search_urls}

#Calls getMonthlyFactorList from moods.py taking all parameters from the path
@app.get("/moods/lastXDays/{username}/{factor}/{days}")
async def getFactorForLastXDays(username: str, factor: str, days: int, end_day: Optional[str] = Query(default=None, description="Format: YYYY-MM-DD - Default is today")):
    if not db_crud.checkValidFactor(factor):
       raise HTTPException(status_code=400, detail="Invalid factor")
    
    if end_day is not None:
        try:
            datetime.strptime(end_day, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    try:
        return db_crud.getFactorForXDays(username, factor, days, end_day)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/moods/average/{username}/{factor}/{days}")
async def getAverageFactorForLastXDays(username: str, factor: str, days: int, end_day: Optional[str] = Query(default=None, description="Format: YYYY-MM-DD - Default is today")):
    if not db_crud.checkValidFactor(factor) or factor == "mood":
       raise HTTPException(status_code=400, detail="Invalid factor")
    
    if end_day is not None:
        try:
            datetime.strptime(end_day, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        
    try:
        result = db_crud.getAverageFactorForXDays(username, factor, days, end_day)
        return {"average": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/moods/mostPopularMood/{username}/{days}")
async def getFactorForLastXDays(username: str, days: int, end_day: Optional[str] = Query(default=None, description="Format: YYYY-MM-DD - Default is today")):
    if end_day is not None:
        try:
            datetime.strptime(end_day, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        
    try:
        result = db_crud.getMostPopularMoodForXDays(username, days, end_day)
        if not result:
            return {"message": "No mood data available in this time period"}
        return {"Top mood": result[0][0], "count": result[0][1]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/account/{username}")
async def getAccount(username: str, detail: Optional[str] = Query(default=None, description="Specific account detail to retrieve")):
    try:
        result = db_crud.getAccountDetails(username, detail)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/moods/{username}/getMoodEntry/{date}")
async def getMoodEntry(username: str, date: str):
    try:
        return db_crud.getMoodEntry(username, date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/exercise/{username}/insert")
async def addExerciseEntry(username: str, entry: ExerciseEntry):
    try:
        result = db_crud.insertExerciseEntry(
            username=username,
            activity=entry.activity,
            duration=entry.duration,
            date=entry.date
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/accounts/login")
async def tryLogin(loginData: LoginEntry):
    try:
        result = loginsignup.tryLogin(
            username=loginData.username,
            password_decrypted=loginData.password
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/accounts/signup")
async def trySignup(signupData: AccountEntry):
    try:
        result = loginsignup.trySignUp(
            username=signupData.username,
            password=signupData.password,
            password_repeat=signupData.password_repeat,
            name= signupData.name,
            age= signupData.age,
            sports= signupData.sports,
            hobbies= signupData.hobbies,
            sex= signupData.sex
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/accounts/{username}/addHobby")
async def addCustomHobby(username: str, hobby: str):
    result = db_crud.addCustomHobby(username, hobby)
    return result

@app.put("/accounts/{username}/update")
async def updateProfile(username: str, update: AccountUpdate):
    try:
        result = db_crud.updateProfile(username=username,
                                    detail= update.detail,
                                    value= update.value
                                )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

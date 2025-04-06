## This is the connections between the Backend and the Frontend so they can be called
## When the methods are called they communicate with AWS and FastAPI to get the data from the database
## The data is then returned to the Frontend to be displayed

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from moods import DB_CRUD
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import os


class MoodData(BaseModel):
    mood: str
    sleep: float
    screen: float
    exercise: float
    alcohol: float
    date: str
    diary: Optional[str] = None



load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
print(f"MONGO_URI is: {mongo_uri}")


client = MongoClient("mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
db = client["mood_tracker"]
app = FastAPI()
db_crud = DB_CRUD(db)


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.get("/moods/userID/getUserID/{user_id}")
async def getUserID(user_id: str):
    try:
        return db_crud.getUserID(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/moods/username/getUsername/{username}")
async def getUsername(username: str):
    try:
        return db_crud.getUsername(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@app.post("/moods/{username}/insert")
async def insertMood(username: str, data: MoodData):
    db_crud.insertMood(username=username, **data)
    return {"message": "Mood inserted successfully"}

@app.get("/accounts/{username}/getRandomActivity")
async def getRandomActivity(username: str):
    try:
        return db_crud.getRandomActivity(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/accounts/{username}/addActivity")
async def addCustomActivity(username: str, activity: str):
    result = db_crud.addCustomActivity(username, activity)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
    

@app.get("/moods/monthly/{username}/{month}/{year}/{factor}")
async def getMonthlyFactorList(username: str, month: int, year: int, factor: str):
    if not db_crud.checkValidFactor(factor):
       raise HTTPException(status_code=400, detail="Invalid factor")
    try:
        return db_crud.getMonthlyFactorList(username, month, year, factor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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

@app.delete("/moods/{username}/delete")
async def deleteAllMoods(username: str):
    try:
        db_crud.deleteMood(username=username)
        return {"message": f"All mood entries relating to {username} have been deleted!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@app.delete("/accounts/{username}/delete")
async def deleteUser(username: str):
    try:
        db_crud.deleteUserRecords(username=username)
        return {"message": f"User {username} have been deleted!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@app.get("/moods/{username}/hasLoggedIn/{date}")
async def hasLoggedIn(username: str, date: str):
    try:
        return db_crud.hasLoggedMoodToday(username, date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
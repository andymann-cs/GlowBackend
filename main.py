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

@app.get("/moods/{username}/random_activity")
async def getRandomActivity(username: str):
    try:
        return db_crud.getRandomActivity(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/moods/monthly/{username}/{month}/{year}/{factor}")
async def getMonthlyFactorList(username: str, month: int, year: int, factor: str):
    if not db_crud.checkValidFactor(factor):
       raise HTTPException(status_code=400, detail="Invalid factor")
    try:
        return db_crud.getMonthlyFactorList(username, month, year, factor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
## This is the connections between the Backend and the Frontend so they can be called
## When the methods are called they communicate with AWS and FastAPI to get the data from the database
## The data is then returned to the Frontend to be displayed

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from moods import DB_CRUD
from dotenv import load_dotenv
import os


load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
print("1")
print(mongo_uri)
print("2")

client = MongoClient(mongo_uri)
db = client["mood_tracker"]

app = FastAPI()
db_crud = DB_CRUD(db)


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.get("/moods/userID/getUserID/{user_id}")
async def getUserID(user_id: str):
    try:
        return db.getUserID(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/moods/username/getUsername/{username}")
async def getUsername(username: str):
    try:
        return db.getUsername(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@app.post("/moods/insert")
async def insertMood(data: dict):
    db.insertMood(**data)
    return {"message": "Mood inserted successfully"}

@app.get("/moods/get/{username}")
async def getRandomActivity(username: str):
    try:
        return db.getRandomActivity(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
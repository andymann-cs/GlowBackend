from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from moods import DB_CRUD
from dotenv import load_dotenv
import os


load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
app = FastAPI()
db = DB_CRUD()


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.get("/moods/user/{user_id}")
async def getUserID(user_id: str):
    try:
        return db.getUserID(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/moods/user/{username}")
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
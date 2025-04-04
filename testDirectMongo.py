from pymongo import MongoClient
from moods import DB_CRUD 


MONGODB_URI = "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"  # Local MongoDB server, change if needed
DB_NAME = "mood_tracker"  
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

collection = db["moods"] 

def test_getMonthlyFactorList(username, month, year, factor):
    try:
        dbtest = DB_CRUD(db)
        result = dbtest.convertMoodListToChartDict(dbtest.getMonthlyFactorList(username, month, year, factor))
        
        print(f"Result for {factor} in {year}-{month}:")
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")

# Test the function with some example parameters
username = "Kenya Park" 
month = 2  
year = 2025
factor = "mood"  
test_getMonthlyFactorList(username, month, year, factor)

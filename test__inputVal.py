from pymongo import MongoClient
from moods import DB_CRUD 


MONGODB_URI = "mongodb+srv://second_admin:hL9l8r6liQROX0Up@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster"  # Local MongoDB server, change if needed
DB_NAME = "mood_tracker"  
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db["moods"] 

# def test_getMonthlyFactorList(username, month, year, factor):
#     try:
#         dbtest = DB_CRUD(db)
#         result = dbtest.convertMoodListToChartDict(dbtest.getMonthlyFactorList(username, month, year, factor))
        
#         print(f"Result for {factor} in {year}-{month}:")
#         print(result)
#     except Exception as e:
#         print(f"Error: {str(e)}")

def test_checkValidMood():
        dbtest = DB_CRUD(db)        
        assert dbtest.checkValidMood("happy") == True
        assert dbtest.checkValidMood("angry") == True
        assert dbtest.checkValidMood("sobbing") == False


#Simple Unit test for the method checkValidFactor
def test_checkValidFactor():
        dbtest = DB_CRUD(db)        
        assert dbtest.checkValidFactor("exercise") == True
        assert dbtest.checkValidFactor("calories") == False
        assert dbtest.checkValidFactor("alcohol") == True


def test_checkValidDetai():
        dbtest = DB_CRUD(db)        
        assert dbtest.checkValidDetail("firstname") == True
        assert dbtest.checkValidDetail("location") == False
        assert dbtest.checkValidDetail("age") == True

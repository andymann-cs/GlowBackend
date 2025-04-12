import random
from datetime import datetime, timedelta
from pymongo import MongoClient

#extra users
#"67e37396300f98be0a832ffb","67e373c2300f98be0a832ffc","67e373d7300f98be0a832ffd","67e373ee300f98be0a832ffe","67e37413300f98be0a832fff","67e37442300f98be0a833000","67e37466300f98be0a833001","67e37488300f98be0a833002","67e374a8300f98be0a833003","67e376a2300f98be0a833004","67e376c9300f98be0a833005"

##CURRENTLY DOES A YEAR WORTH
class genFakeData:
    def __init__(self):
        self.users = ["67e183c3c468744e4b235553"]
        self.moods = ["Happy", "Sad", "Stressed", "Tired", "Content", "Excited", "Angry", "Proud", "Unsure", "Sick"]
        self.start = datetime(2025,1,1)
        self.end = datetime(2025,12,31)

        # self.client = MongoClient("mongodb+srv://second_admin:hL9l8r6liQROX0Up@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
        # self.db = self.client["mood_tracker"]
        # self.collection = self.db["moods"]

    def genData(self):
        data = []
        for i in range(0, len(self.users)):
            for day in range ((self.end - self.start).days):
                entryDate = self.start + timedelta(days=day)

                mood = random.choice(self.moods)
                sleep = random.randint(10,100)/10
                screen = random.randint(1,80)/10
                
                alcohol = round((random.random() ** 5) * 1.5, 1)
                if random.random() < 1 / 7:
                    alcohol += round(random.uniform(1, 3), 1)
                elif random.random() < 1 / 30:
                    alcohol = round(random.uniform(7, 15), 1)

                #Lower of 0 and upper of 120. bias of 4.25
                exercise = int((120) * (random.random() **4.25))

                if i == 0 and sleep <= 6:
                    sleepTired = random.randint(1,7)
                    if sleepTired <= 4:
                        mood = "Tired"
                    else:
                        if sleepTired <= 6:
                            mood = "Stressed"

                if i == 1:
                    screen = random.randint(40,140)/10
                    screenStress = random.randint(1,10)
                    if screen >= 8 and screenStress >= 6:
                        mood = "Stressed"
                    else:
                        if screenStress >= 4:
                            mood = "Sad"

                if i == 2 and exercise > 45 :
                    exerciseHappy = random.randint(1,10)
                    if exercise > 100 and exerciseHappy >= 3:
                        mood = "Proud"
                    if exerciseHappy >= 1:
                        mood = "Happy"

                data.append({
                                "user_id": self.users[i],
                                "date": entryDate.strftime("%Y-%m-%d"),
                                "mood": mood,
                                "sleep": round(sleep, 1),
                                "exercise": exercise,
                                "screen": round(screen, 1),
                                "alcohol": round(alcohol, 1)
                                })
        return data
    
#generator = genFakeData()
#test_data = generator.collection.insert_many(generator.genData())
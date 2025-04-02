import httpx
import asyncio

API_URL = "http://16.170.211.11:8000"

async def get_user_mood(username):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_URL}/moods/get/{username}")
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        
async def main():
    result = await get_user_mood("Kenya Park")
    if result:
        print("Data:", result)
    else:
        print("No data returned")

asyncio.run(main())
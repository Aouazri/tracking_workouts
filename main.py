import os
import requests
from datetime import datetime

APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
API_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ['sheety_endpoint']
TOKEN = os.environ['TOKEN']
headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

nlp_parameters = {
    'query': input("Tell me which exercises you did? "),
    'gender': 'male',
    'weight_kg': 70,
    'height_cm': 180,
    'age': 25,
}

response = requests.post(url=API_endpoint, json=nlp_parameters, headers=headers)
result = response.json()
print(result)

# Setting up sheety with the response we get from nutri

# Date and current time formatted
today_date = datetime.now().strftime("%d/%m/%Y")
current_time = datetime.now().strftime("%X")

# sheety input
for exercise in result["exercises"]:
    workout_data = {
        'workout': {
            "date": today_date,
            "time": current_time,
            "exercise": exercise["name"].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }
sheet_headers = {
    'Authorization': f"Bearer {TOKEN}"
}
sheet_response = requests.post(sheety_endpoint, json=workout_data, headers=sheet_headers)
print(sheet_response.text)

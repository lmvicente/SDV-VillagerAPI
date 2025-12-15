from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

""" probably dont need this model since i just want to read the entire json: class Villager(BaseModel):
    name: str
    url: str
    image_url: str
    marriageable: bool """
    

class VillagerBirthdays(BaseModel):
        season: str
        day: int
        villagers: list[str]

@app.get("/villager/{name}")

def get_villager(name: str):
    with open("villagers.json", "r") as f:
        data = json.load(f)
        villagers = data["villagers"]

        for villager_name, villager_data in villagers.items():
            if villager_name.lower() == name.lower():
                return villager_data
        return {"error": "Villager not found"}

@app.get("/date/{season}/{day}")

def get_closest_birthday(season: str, day: int):
    with open("villagers.json", "r") as f:
        data = json.load(f)
        season = season.capitalize()
        birthdays = data["birthdays_by_date"][season]
        closest_birthdays = []
        for birthday, villager_name in birthdays.items():
            if int(birthday) >= day and int(birthday) - day < 5:
                closest_birthdays.append(villager_name + " - " + season + " " + birthday + "(" + str(int(birthday) - day) + " days away)")
        return {"closest_birthdays": closest_birthdays}
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}


def get_live_matches():
    url = f"{BASE_URL}/matches/v1/live"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def get_match_details(match_id):
    url = f"{BASE_URL}/mcenter/v1/{match_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def get_player_stats(player_id):
    url = f"{BASE_URL}/stats/v1/player/{player_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

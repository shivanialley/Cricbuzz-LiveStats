import requests
import os
from dotenv import load_dotenv
from utils.logger import api_logger
import time

# Load environment variables
load_dotenv()

# API Configuration
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")
}


def get_live_matches():
    """
    Fetch live cricket matches from Cricbuzz API
    
    Returns:
        JSON response with live match data
    
    Raises:
        Exception if API call fails
    """
    url = f"{BASE_URL}/matches/v1/live"
    
    try:
        start_time = time.time()
        api_logger.info(f"Fetching live matches from: {url}")
        
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        api_logger.info(f"Live matches fetched successfully in {response_time:.2f}ms")
        
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        api_logger.error(f"HTTP Error fetching live matches: {e}")
        raise Exception(f"API Error: {e}")
    except requests.exceptions.RequestException as e:
        api_logger.error(f"Request Error: {e}")
        raise Exception(f"Network Error: {e}")
    except Exception as e:
        api_logger.error(f"Unexpected error: {e}")
        raise


def get_match_details(match_id):
    """
    Get detailed information about a specific match
    
    Args:
        match_id: ID of the match
    
    Returns:
        JSON response with match details
    """
    url = f"{BASE_URL}/mcenter/v1/{match_id}"
    
    try:
        start_time = time.time()
        api_logger.info(f"Fetching match details for match_id: {match_id}")
        
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        response_time = (time.time() - start_time) * 1000
        api_logger.info(f"Match details fetched in {response_time:.2f}ms")
        
        return response.json()
        
    except Exception as e:
        api_logger.error(f"Error fetching match {match_id}: {e}")
        raise


def get_player_stats(player_id):
    """
    Get statistics for a specific player
    
    Args:
        player_id: ID of the player
    
    Returns:
        JSON response with player statistics
    """
    url = f"{BASE_URL}/stats/v1/player/{player_id}"
    
    try:
        start_time = time.time()
        api_logger.info(f"Fetching player stats for player_id: {player_id}")
        
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        response_time = (time.time() - start_time) * 1000
        api_logger.info(f"Player stats fetched in {response_time:.2f}ms")
        
        return response.json()
        
    except Exception as e:
        api_logger.error(f"Error fetching player {player_id}: {e}")
        raise


def get_recent_matches():
    """
    Get list of recent matches
    
    Returns:
        JSON response with recent matches
    """
    url = f"{BASE_URL}/matches/v1/recent"
    
    try:
        api_logger.info("Fetching recent matches...")
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        api_logger.error(f"Error fetching recent matches: {e}")
        raise
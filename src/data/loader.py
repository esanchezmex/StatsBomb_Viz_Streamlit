"""
Data loading functions for fetching and caching Statsbomb data.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd
import requests
import streamlit as st
from loguru import logger

from config import (CACHE_DIR, COMPETITIONS_URL, EVENTS_URL_TEMPLATE,
                     LINEUPS_URL_TEMPLATE, MATCHES_URL_TEMPLATE, MAX_RETRIES,
                     TIMEOUT)

# Create cache directory if it doesn't exist
CACHE_DIR.mkdir(exist_ok=True)

@st.cache_data(ttl=3600)
def fetch_competitions() -> List[Dict]:
    """
    Fetch available competitions from Statsbomb's open data.
    
    Returns:
        List[Dict]: List of competition dictionaries
    """
    try:
        response = requests.get(COMPETITIONS_URL, timeout=TIMEOUT)
        response.raise_for_status()
        competitions = response.json()
        logger.info(f"Successfully fetched {len(competitions)} competitions")
        return competitions
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching competitions: {e}")
        st.error("Failed to fetch competitions data. Please try again later.")
        return []

@st.cache_data(ttl=3600)
def fetch_matches(competition_id: int, season_id: int) -> List[Dict]:
    """
    Fetch matches for a specific competition and season.
    
    Args:
        competition_id (int): Competition ID
        season_id (int): Season ID
    
    Returns:
        List[Dict]: List of match dictionaries
    """
    url = MATCHES_URL_TEMPLATE.format(
        competition_id=competition_id,
        season_id=season_id
    )
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        matches = response.json()
        logger.info(f"Successfully fetched {len(matches)} matches for competition {competition_id}, season {season_id}")
        return matches
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching matches: {e}")
        st.error("Failed to fetch matches data. Please try again later.")
        return []

@st.cache_data(ttl=3600)
def fetch_events(match_id: int) -> List[Dict]:
    """
    Fetch events for a specific match.
    
    Args:
        match_id (int): Match ID
    
    Returns:
        List[Dict]: List of event dictionaries
    """
    url = EVENTS_URL_TEMPLATE.format(match_id=match_id)
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        events = response.json()
        logger.info(f"Successfully fetched {len(events)} events for match {match_id}")
        return events
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching events: {e}")
        st.error("Failed to fetch events data. Please try again later.")
        return []

@st.cache_data(ttl=3600)
def fetch_lineups(match_id: int) -> List[Dict]:
    """
    Fetch lineups for a specific match.
    
    Args:
        match_id (int): Match ID
    
    Returns:
        List[Dict]: List of lineup dictionaries
    """
    url = LINEUPS_URL_TEMPLATE.format(match_id=match_id)
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        lineups = response.json()
        logger.info(f"Successfully fetched lineups for match {match_id}")
        return lineups
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching lineups: {e}")
        st.error("Failed to fetch lineups data. Please try again later.")
        return []

def save_to_cache(data: Union[List, Dict], filename: str) -> None:
    """
    Save data to cache file.
    
    Args:
        data: Data to cache
        filename (str): Cache filename
    """
    cache_file = CACHE_DIR / filename
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        logger.debug(f"Saved data to cache: {filename}")
    except Exception as e:
        logger.error(f"Error saving to cache: {e}")

def load_from_cache(filename: str) -> Optional[Union[List, Dict]]:
    """
    Load data from cache file.
    
    Args:
        filename (str): Cache filename
    
    Returns:
        Optional[Union[List, Dict]]: Cached data if available
    """
    cache_file = CACHE_DIR / filename
    try:
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                data = json.load(f)
            logger.debug(f"Loaded data from cache: {filename}")
            return data
    except Exception as e:
        logger.error(f"Error loading from cache: {e}")
    return None 
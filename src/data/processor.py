"""
Data processing and validation functions for Statsbomb data.
"""
from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st
from loguru import logger

def validate_competition_data(competitions: List[Dict]) -> List[Dict]:
    """
    Validate competition data and remove invalid entries.
    
    Args:
        competitions (List[Dict]): Raw competition data
    
    Returns:
        List[Dict]: Validated competition data
    """
    valid_competitions = []
    required_fields = {'competition_id', 'competition_name', 'season_id', 'season_name'}
    
    for comp in competitions:
        if all(field in comp for field in required_fields):
            valid_competitions.append(comp)
        else:
            logger.warning(f"Invalid competition data: {comp}")
    
    return valid_competitions

def validate_match_data(matches: List[Dict]) -> List[Dict]:
    """
    Validate match data and remove invalid entries.
    
    Args:
        matches (List[Dict]): Raw match data
    
    Returns:
        List[Dict]: Validated match data
    """
    valid_matches = []
    required_fields = {
        'match_id', 'home_team', 'away_team',
        'home_score', 'away_score', 'match_date'
    }
    
    for match in matches:
        if all(field in match for field in required_fields):
            valid_matches.append(match)
        else:
            logger.warning(f"Invalid match data: {match}")
    
    return valid_matches

def validate_event_data(events: List[Dict]) -> List[Dict]:
    """
    Validate event data and remove invalid entries.
    
    Args:
        events (List[Dict]): Raw event data
    
    Returns:
        List[Dict]: Validated event data
    """
    valid_events = []
    required_fields = {
        'id', 'type', 'minute', 'second',
        'possession', 'play_pattern', 'team',
        'player'
    }
    
    for event in events:
        if all(field in event for field in required_fields):
            valid_events.append(event)
        else:
            logger.warning(f"Invalid event data: {event}")
    
    return valid_events

def process_competitions(competitions: List[Dict]) -> pd.DataFrame:
    """
    Process competition data into a DataFrame.
    
    Args:
        competitions (List[Dict]): Validated competition data
    
    Returns:
        pd.DataFrame: Processed competition data
    """
    df = pd.DataFrame(competitions)
    df = df.sort_values(['competition_name', 'season_name'])
    return df

def process_matches(matches: List[Dict]) -> pd.DataFrame:
    """
    Process match data into a DataFrame.
    
    Args:
        matches (List[Dict]): Validated match data
    
    Returns:
        pd.DataFrame: Processed match data
    """
    df = pd.DataFrame(matches)
    df['match_date'] = pd.to_datetime(df['match_date'])
    df = df.sort_values('match_date')
    return df

def process_events(events: List[Dict]) -> pd.DataFrame:
    """
    Process event data into a DataFrame.
    
    Args:
        events (List[Dict]): Validated event data
    
    Returns:
        pd.DataFrame: Processed event data
    """
    df = pd.DataFrame(events)
    
    # Extract nested data
    df['event_type'] = df['type'].apply(lambda x: x.get('name'))
    df['team_name'] = df['team'].apply(lambda x: x.get('name'))
    df['player_name'] = df['player'].apply(lambda x: x.get('name'))
    
    # Calculate timestamp
    df['timestamp'] = df['minute'] * 60 + df['second']
    
    # Extract shot data
    df['shot'] = df.apply(lambda x: x.get('shot', {}) if x['event_type'] == 'Shot' else {}, axis=1)
    
    return df

def get_team_stats(events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate team statistics from event data.
    
    Args:
        events_df (pd.DataFrame): Processed event data
    
    Returns:
        pd.DataFrame: Team statistics
    """
    stats = events_df.groupby('team_name').agg({
        'id': 'count',
        'event_type': lambda x: x.value_counts().to_dict()
    }).reset_index()
    
    stats.columns = ['team_name', 'total_events', 'event_breakdown']
    return stats

def get_player_stats(events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate player statistics from event data.
    
    Args:
        events_df (pd.DataFrame): Processed event data
    
    Returns:
        pd.DataFrame: Player statistics
    """
    stats = events_df.groupby(['team_name', 'player_name']).agg({
        'id': 'count',
        'event_type': lambda x: x.value_counts().to_dict()
    }).reset_index()
    
    stats.columns = ['team_name', 'player_name', 'total_events', 'event_breakdown']
    return stats 
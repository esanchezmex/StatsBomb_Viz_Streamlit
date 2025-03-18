"""
Tests for data processing functions.
"""
import pandas as pd
import pytest

from src.data.processor import (validate_competition_data, validate_match_data,
                              validate_event_data, process_competitions,
                              process_matches, process_events, get_team_stats,
                              get_player_stats)

# Sample test data
SAMPLE_COMPETITION = {
    'competition_id': 1,
    'competition_name': 'Test League',
    'season_id': 1,
    'season_name': '2021/22'
}

SAMPLE_MATCH = {
    'match_id': 1,
    'home_team': {'home_team_name': 'Team A'},
    'away_team': {'away_team_name': 'Team B'},
    'home_score': 2,
    'away_score': 1,
    'match_date': '2022-01-01'
}

SAMPLE_EVENT = {
    'id': 1,
    'type': {'name': 'Shot'},
    'minute': 10,
    'second': 30,
    'possession': 1,
    'play_pattern': {'name': 'Regular Play'},
    'team': {'name': 'Team A'},
    'player': {'name': 'Player 1'},
    'location': [100, 50]
}

def test_validate_competition_data():
    """Test competition data validation."""
    valid_data = [SAMPLE_COMPETITION]
    invalid_data = [{'competition_id': 1}]  # Missing required fields
    
    assert len(validate_competition_data(valid_data)) == 1
    assert len(validate_competition_data(invalid_data)) == 0

def test_validate_match_data():
    """Test match data validation."""
    valid_data = [SAMPLE_MATCH]
    invalid_data = [{'match_id': 1}]  # Missing required fields
    
    assert len(validate_match_data(valid_data)) == 1
    assert len(validate_match_data(invalid_data)) == 0

def test_validate_event_data():
    """Test event data validation."""
    valid_data = [SAMPLE_EVENT]
    invalid_data = [{'id': 1}]  # Missing required fields
    
    assert len(validate_event_data(valid_data)) == 1
    assert len(validate_event_data(invalid_data)) == 0

def test_process_competitions():
    """Test competition data processing."""
    data = [SAMPLE_COMPETITION]
    df = process_competitions(data)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert 'competition_name' in df.columns
    assert 'season_name' in df.columns

def test_process_matches():
    """Test match data processing."""
    data = [SAMPLE_MATCH]
    df = process_matches(data)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert isinstance(df['match_date'].iloc[0], pd.Timestamp)

def test_process_events():
    """Test event data processing."""
    data = [SAMPLE_EVENT]
    df = process_events(data)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert 'event_type' in df.columns
    assert 'team_name' in df.columns
    assert 'player_name' in df.columns
    assert 'timestamp' in df.columns

def test_get_team_stats():
    """Test team statistics calculation."""
    events_df = process_events([SAMPLE_EVENT])
    stats = get_team_stats(events_df)
    
    assert isinstance(stats, pd.DataFrame)
    assert len(stats) == 1
    assert 'team_name' in stats.columns
    assert 'total_events' in stats.columns
    assert 'event_breakdown' in stats.columns

def test_get_player_stats():
    """Test player statistics calculation."""
    events_df = process_events([SAMPLE_EVENT])
    stats = get_player_stats(events_df)
    
    assert isinstance(stats, pd.DataFrame)
    assert len(stats) == 1
    assert 'team_name' in stats.columns
    assert 'player_name' in stats.columns
    assert 'total_events' in stats.columns
    assert 'event_breakdown' in stats.columns 
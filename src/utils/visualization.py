"""
Visualization utilities for creating interactive plots.
"""
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import PLOT_HEIGHT, PLOT_WIDTH

def create_event_timeline(events_df: pd.DataFrame) -> go.Figure:
    """
    Create an interactive timeline of match events.
    
    Args:
        events_df (pd.DataFrame): Processed event data
    
    Returns:
        go.Figure: Interactive timeline plot
    """
    fig = px.scatter(
        events_df,
        x='timestamp',
        y='event_type',
        color='team_name',
        hover_data=['player_name', 'minute', 'second'],
        title='Match Event Timeline',
        height=PLOT_HEIGHT,
        width=PLOT_WIDTH
    )
    
    fig.update_layout(
        xaxis_title='Match Time (seconds)',
        yaxis_title='Event Type',
        showlegend=True
    )
    
    return fig

def create_team_event_breakdown(team_stats: pd.DataFrame) -> go.Figure:
    """
    Create a breakdown of events by team.
    
    Args:
        team_stats (pd.DataFrame): Team statistics
    
    Returns:
        go.Figure: Interactive bar chart
    """
    # Unpack event breakdown
    event_types = set()
    event_counts = []
    
    for _, row in team_stats.iterrows():
        for event_type, count in row['event_breakdown'].items():
            event_types.add(event_type)
            event_counts.append({
                'team': row['team_name'],
                'event_type': event_type,
                'count': count
            })
    
    events_df = pd.DataFrame(event_counts)
    
    fig = px.bar(
        events_df,
        x='team',
        y='count',
        color='event_type',
        title='Team Event Breakdown',
        height=PLOT_HEIGHT,
        width=PLOT_WIDTH
    )
    
    fig.update_layout(
        xaxis_title='Team',
        yaxis_title='Number of Events',
        barmode='stack'
    )
    
    return fig

def create_player_event_breakdown(player_stats: pd.DataFrame, team_name: str) -> go.Figure:
    """
    Create a breakdown of events by player for a specific team.
    
    Args:
        player_stats (pd.DataFrame): Player statistics
        team_name (str): Team to show players for
    
    Returns:
        go.Figure: Interactive bar chart
    """
    team_players = player_stats[player_stats['team_name'] == team_name]
    
    # Unpack event breakdown
    event_types = set()
    event_counts = []
    
    for _, row in team_players.iterrows():
        for event_type, count in row['event_breakdown'].items():
            event_types.add(event_type)
            event_counts.append({
                'player': row['player_name'],
                'event_type': event_type,
                'count': count
            })
    
    events_df = pd.DataFrame(event_counts)
    
    fig = px.bar(
        events_df,
        x='player',
        y='count',
        color='event_type',
        title=f'{team_name} Player Event Breakdown',
        height=PLOT_HEIGHT,
        width=PLOT_WIDTH
    )
    
    fig.update_layout(
        xaxis_title='Player',
        yaxis_title='Number of Events',
        barmode='stack'
    )
    
    return fig

def create_heatmap(events_df: pd.DataFrame, event_type: Optional[str] = None) -> go.Figure:
    """
    Create a heatmap of event locations on the pitch.
    
    Args:
        events_df (pd.DataFrame): Processed event data
        event_type (Optional[str]): Filter for specific event type
    
    Returns:
        go.Figure: Interactive heatmap
    """
    if event_type:
        events_df = events_df[events_df['event_type'] == event_type]
    
    # Extract location data (assuming standard pitch dimensions)
    locations = events_df['location'].apply(pd.Series)
    locations.columns = ['x', 'y']
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram2d(
        x=locations['x'],
        y=locations['y'],
        colorscale='Viridis',
        nbinsx=20,
        nbinsy=10,
        showscale=True
    ))
    
    # Add pitch markings
    fig.update_layout(
        title=f'Event Heatmap{f" - {event_type}" if event_type else ""}',
        height=PLOT_HEIGHT,
        width=PLOT_WIDTH,
        xaxis_title='Pitch Length',
        yaxis_title='Pitch Width',
        showlegend=False
    )
    
    return fig

def download_plot(fig: go.Figure, filename: str) -> None:
    """
    Save plot to file for downloading.
    
    Args:
        fig (go.Figure): Plotly figure to save
        filename (str): Output filename
    """
    fig.write_html(filename)
    with open(filename, 'rb') as f:
        st.download_button(
            label="Download Plot",
            data=f,
            file_name=filename,
            mime='text/html'
        ) 
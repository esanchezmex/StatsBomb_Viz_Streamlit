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

def create_player_performance_radar(events_df: pd.DataFrame, player_names: List[str]) -> go.Figure:
    """
    Create a radar chart showing various performance metrics for selected players.
    
    Args:
        events_df (pd.DataFrame): Processed event data
        player_names (List[str]): Names of the players to analyze
    
    Returns:
        go.Figure: Interactive radar chart
    """
    if not player_names:
        # Return empty figure if no players selected
        fig = go.Figure()
        fig.add_annotation(
            text="No players selected",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color='white')
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    # Define neon colors for different players
    neon_colors = [
        ('rgb(0, 200, 255)', 'rgba(0, 200, 255, 0.1)'),    # Neon blue
        ('rgb(255, 50, 50)', 'rgba(255, 50, 50, 0.1)'),    # Neon red
        ('rgb(0, 255, 100)', 'rgba(0, 255, 100, 0.1)'),    # Neon green
        ('rgb(255, 150, 0)', 'rgba(255, 150, 0, 0.1)'),    # Neon orange
        ('rgb(200, 100, 255)', 'rgba(200, 100, 255, 0.1)') # Neon purple
    ]
    
    fig = go.Figure()
    max_value = 0
    
    # Calculate metrics for each player
    for idx, player_name in enumerate(player_names):
        # Filter events for the player
        player_events = events_df[events_df['player_name'] == player_name].copy()
        
        if len(player_events) == 0:
            continue
            
        # Calculate various performance metrics
        total_events = len(player_events)
        metrics = {}
        
        # Passing metrics
        passes = player_events[player_events['event_type'] == 'Pass']
        metrics['Passes'] = len(passes)
        
        # Shot metrics
        shots = player_events[player_events['event_type'] == 'Shot']
        metrics['Shots'] = len(shots)
        
        # Dribble metrics
        dribbles = player_events[player_events['event_type'] == 'Dribble']
        metrics['Dribbles'] = len(dribbles)
        
        # Pressure metrics
        pressure = player_events[player_events['event_type'] == 'Pressure']
        metrics['Pressure Actions'] = len(pressure)
        
        # Ball Recovery metrics
        recoveries = player_events[player_events['event_type'] == 'Ball Recovery']
        metrics['Ball Recoveries'] = len(recoveries)
        
        # Normalize metrics to percentage of total events
        for key in metrics:
            metrics[key] = (metrics[key] / total_events) * 100 if total_events > 0 else 0
        
        # Update max value for scaling
        max_value = max(max_value, max(metrics.values()))
        
        # Get color for this player
        line_color, fill_color = neon_colors[idx % len(neon_colors)]
        
        # Create radar plot for this player
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=player_name,
            line=dict(
                color=line_color,
                width=3
            ),
            fillcolor=fill_color
        ))
    
    # Add faint background grid with reduced opacity
    fig.add_trace(go.Scatterpolar(
        r=[max_value * 1.1] * (len(categories) + 1),
        theta=categories + [categories[0]],
        fill=None,
        mode='lines',
        line=dict(color='rgba(255, 255, 255, 0.1)', width=1),
        showlegend=False
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_value * 1.1],
                color='white',  # White text
                tickfont=dict(size=10),
                ticksuffix='%',  # Add percentage symbol
                gridcolor='rgba(255, 255, 255, 0.1)',  # Faint grid
                linecolor='rgba(255, 255, 255, 0.3)'   # Slightly visible axis line
            ),
            angularaxis=dict(
                color='white',  # White text
                gridcolor='rgba(255, 255, 255, 0.1)',  # Faint grid
                linecolor='rgba(255, 255, 255, 0.3)'   # Slightly visible axis line
            ),
            bgcolor='rgba(0,0,0,0)'  # Transparent background
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent background
        title=dict(
            text='Player Performance Comparison',
            font=dict(color='white', size=20)
        ),
        height=PLOT_HEIGHT,
        width=PLOT_WIDTH
    )
    
    return fig 
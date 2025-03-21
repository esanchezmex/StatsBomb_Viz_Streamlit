"""
Main Streamlit application for football analytics dashboard.
"""
import os
from pathlib import Path

import streamlit as st
from loguru import logger

from data.loader import (fetch_competitions, fetch_events, fetch_lineups,
                        fetch_matches)
from data.processor import (get_player_stats, get_team_stats, process_competitions,
                          process_events, process_matches, validate_competition_data,
                          validate_event_data, validate_match_data)
from utils.visualization import (create_event_timeline,
                               create_player_event_breakdown,
                               create_team_event_breakdown, create_heatmap,
                               download_plot)

# Configure logger
logger.add("app.log", rotation="500 MB")

# Set page config
st.set_page_config(
    page_title="StatsBomb Free Data Visualizer",
    page_icon="⚽",
    layout="wide"
)

# Initialize session state
if 'competition_id' not in st.session_state:
    st.session_state.competition_id = None
if 'season_id' not in st.session_state:
    st.session_state.season_id = None
if 'match_id' not in st.session_state:
    st.session_state.match_id = None
if 'team_name' not in st.session_state:
    st.session_state.team_name = None
if 'player_name' not in st.session_state:
    st.session_state.player_name = None

# App title and description
st.title("⚽ StatsBomb Free Data Visualizer")
st.markdown("""
This app will help you to visualize StatsBomb's free data, 
but also understand the structure of the free data like what competitions, 
seasons and matches are available, 
as well as what type of event data like passes, shots, and more. 

You can also visualize the data for a specific match. 

Select a competition, season, and match to explore the data. 

*NOTE*: More graph options will be added soon. 
This app is still under development and some features might not work as expected.
""")

# Sidebar filters
st.sidebar.header("Filters")

# Load and validate competition data
with st.spinner("Loading competitions..."):
    competitions = fetch_competitions()
    valid_competitions = validate_competition_data(competitions)
    competitions_df = process_competitions(valid_competitions)

# Competition selector
competition_season = st.sidebar.selectbox(
    "Select Competition & Season",
    options=competitions_df.apply(
        lambda x: f"{x['competition_name']} - {x['season_name']}", axis=1
    ).unique(),
    key="competition_season"
)

if competition_season:
    selected_comp = competitions_df[
        competitions_df.apply(
            lambda x: f"{x['competition_name']} - {x['season_name']}" == competition_season,
            axis=1
        )
    ].iloc[0]
    
    st.session_state.competition_id = selected_comp['competition_id']
    st.session_state.season_id = selected_comp['season_id']
    
    # Load and validate match data
    with st.spinner("Loading matches..."):
        matches = fetch_matches(
            st.session_state.competition_id,
            st.session_state.season_id
        )
        valid_matches = validate_match_data(matches)
        matches_df = process_matches(valid_matches)
    
    # Match selector
    match_label = st.sidebar.selectbox(
        "Select Match",
        options=matches_df.apply(
            lambda x: f"{x['home_team']['home_team_name']} {x['home_score']} - {x['away_score']} {x['away_team']['away_team_name']}",
            axis=1
        ).unique(),
        key="match"
    )
    
    if match_label:
        selected_match = matches_df[
            matches_df.apply(
                lambda x: f"{x['home_team']['home_team_name']} {x['home_score']} - {x['away_score']} {x['away_team']['away_team_name']}" == match_label,
                axis=1
            )
        ].iloc[0]
        
        st.session_state.match_id = selected_match['match_id']
        
        # Load and validate event data
        with st.spinner("Loading match events..."):
            events = fetch_events(st.session_state.match_id)
            valid_events = validate_event_data(events)
            events_df = process_events(valid_events)
            
            # Calculate statistics
            team_stats = get_team_stats(events_df)
            player_stats = get_player_stats(events_df)
        
        # Team selector
        st.session_state.team_name = st.sidebar.selectbox(
            "Select Team",
            options=team_stats['team_name'].unique(),
            key="team"
        )
        
        if st.session_state.team_name:
            # Player selector
            team_players = player_stats[
                player_stats['team_name'] == st.session_state.team_name
            ]
            st.session_state.player_name = st.sidebar.selectbox(
                "Select Player",
                options=team_players['player_name'].unique(),
                key="player"
            )
        
        # Event type selector
        event_type = st.sidebar.selectbox(
            "Select Event Type",
            options=['All'] + list(events_df['event_type'].unique()),
            key="event_type"
        )
        
        # Main content area
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Match Timeline")
            timeline_fig = create_event_timeline(events_df)
            st.plotly_chart(timeline_fig, use_container_width=True)
            
            if st.button("Download Timeline"):
                download_plot(timeline_fig, "timeline.html")
        
        with col2:
            st.subheader("Team Event Breakdown")
            team_breakdown_fig = create_team_event_breakdown(team_stats)
            st.plotly_chart(team_breakdown_fig, use_container_width=True)
            
            if st.button("Download Team Breakdown"):
                download_plot(team_breakdown_fig, "team_breakdown.html")
        
        if st.session_state.team_name:
            st.subheader(f"Player Event Breakdown - {st.session_state.team_name}")
            player_breakdown_fig = create_player_event_breakdown(
                player_stats,
                st.session_state.team_name
            )
            st.plotly_chart(player_breakdown_fig, use_container_width=True)
            
            if st.button("Download Player Breakdown"):
                download_plot(player_breakdown_fig, "player_breakdown.html")
        
        st.subheader("Event Heatmap")
        selected_event_type = None if event_type == 'All' else event_type
        heatmap_fig = create_heatmap(events_df, selected_event_type)
        st.plotly_chart(heatmap_fig, use_container_width=True)
        
        if st.button("Download Heatmap"):
            download_plot(heatmap_fig, "heatmap.html") 
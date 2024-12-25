import streamlit as st
import pandas as pd

# Load the CSV file based on input type (hitters or pitchers)
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

# App starts here
st.title("Board Baseball Lineup Created")

# File paths for hitter and pitcher stats
hitters_file = 'hitters_stats.csv'
pitchers_file = 'pitchers_stats.csv'

# Load hitter and pitcher data
hitters_data = load_data(hitters_file)
pitchers_data = load_data(pitchers_file)

# Extract player names and seasons for the dropdowns
hitters_names = sorted(hitters_data['Name'].unique())  # Updated column name
pitchers_names = sorted(pitchers_data['Name'].unique())  # Updated column name
seasons = sorted(hitters_data['Year'].unique())  # Assuming 'Year' is common for both datasets

# Positions for hitters and pitchers
positions_hitter = ['1B', '2B', '3B', 'SS', 'C', 'LF', 'CF', 'RF', 'DH']
positions_pitcher = ['SP', 'RP', 'CL']

# Create input fields for hitters
st.header("Hitting Lineup")
hitting_lineup = []
for i in range(1, 10):
    col1, col2, col3 = st.columns(3)
    with col1:
        player = st.selectbox(f"Player {i} (Hitter)", hitters_names, key=f"hitter_{i}_player")
    with col2:
        season = st.selectbox(f"Year for Player {i}", seasons, key=f"hitter_{i}_season")
    with col3:
        position = st.selectbox(f"Position for Player {i}", positions_hitter, key=f"hitter_{i}_position")
    hitting_lineup.append({"Player": player, "Year": season, "Position": position})

# Create input fields for pitchers
st.header("Pitching Lineup")
pitching_lineup = []
for i in range(1, 6):
    col1, col2, col3 = st.columns(3)
    with col1:
        player = st.selectbox(f"Player {i} (Pitcher)", pitchers_names, key=f"pitcher_{i}_player")
    with col2:
        season = st.selectbox(f"Year for Player {i}", seasons, key=f"pitcher_{i}_season")
    with col3:
        position = st.selectbox(f"Role for Player {i}", positions_pitcher, key=f"pitcher_{i}_position")
    pitching_lineup.append({"Player": player, "Year": season, "Position": position})

# Button to generate the lineup
if st.button("Generate Lineup"):
    st.subheader("Your Lineup")

    # Display hitting lineup in a compact table
    st.write("### Hitting Lineup")
    hitter_stats = []
    for i, hitter in enumerate(hitting_lineup, 1):
        player_stats = hitters_data[
            (hitters_data['Name'] == hitter['Player']) & (hitters_data['Year'] == hitter['Year'])
        ]
        hitter_stats.append({
            'Player': hitter['Player'],
            'Position': hitter['Position'],
            'BA': player_stats['BA'].values[0],  # Show key stats like BA, HR, RBI
            'HR': player_stats['HR'].values[0],
            'RBI': player_stats['RBI'].values[0]
        })
    
    # Display in a table format (compact)
    st.table(hitter_stats)

    # Display pitching lineup in a compact table
    st.write("### Pitching Lineup")
    pitcher_stats = []
    for i, pitcher in enumerate(pitching_lineup, 1):
        player_stats = pitchers_data[
            (pitchers_data['Name'] == pitcher['Player']) & (pitchers_data['Year'] == pitcher['Year'])
        ]
        pitcher_stats.append({
            'Player': pitcher['Player'],
            'Position': pitcher['Position'],
            'W': player_stats['W'].values[0],  # Show key stats like W, ERA, SO
            'ERA': player_stats['ERA'].values[0],
            'SO': player_stats['SO'].values[0]
        })

    # Display in a table format (compact)
    st.table(pitcher_stats)

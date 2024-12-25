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
    st.subheader(f"Player {i} (Hitter)")
    
    # Input fields stacked vertically
    player = st.selectbox(f"Select Player {i}", hitters_names, key=f"hitter_{i}_player")
    season = st.selectbox(f"Select Year for Player {i}", seasons, key=f"hitter_{i}_season")
    position = st.selectbox(f"Select Position for Player {i}", positions_hitter, key=f"hitter_{i}_position")
    
    hitting_lineup.append({"Player": player, "Year": season, "Position": position})

# Create input fields for pitchers
st.header("Pitching Lineup")
pitching_lineup = []
for i in range(1, 6):
    st.subheader(f"Player {i} (Pitcher)")
    
    # Input fields stacked vertically
    player = st.selectbox(f"Select Player {i}", pitchers_names, key=f"pitcher_{i}_player")
    season = st.selectbox(f"Select Year for Player {i}", seasons, key=f"pitcher_{i}_season")
    position = st.selectbox(f"Select Role for Player {i}", positions_pitcher, key=f"pitcher_{i}_position")
    
    pitching_lineup.append({"Player": player, "Year": season, "Position": position})

# Button to generate the lineup
if st.button("Generate Lineup"):
    st.subheader("Your Lineup")

    # Display hitting lineup in a simple table format
    st.write("### Hitting Lineup")
    hitter_stats = []
    for i, hitter in enumerate(hitting_lineup, 1):
        player_stats = hitters_data[
            (hitters_data['Name'] == hitter['Player']) & (hitters_data['Year'] == hitter['Year'])
        ]
        
        # Collect stats for the player
        stats = {
            'Index': i,  # Added index starting from 1
            'Player': hitter['Player'],
            'Year': hitter['Year'],  # Added Year to the stats
            'Position': hitter['Position'],
        }

        if 'BA' in player_stats.columns:
            stats['

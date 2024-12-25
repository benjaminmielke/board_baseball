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
hitters_names = sorted(hitters_data['Player Name'].unique())
pitchers_names = sorted(pitchers_data['Player Name'].unique())
seasons = sorted(hitters_data['Season'].unique())  # Assuming seasons are common

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
    hitting_lineup.append({"Player": player, "Season": season, "Position": position})

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
    pitching_lineup.append({"Player": player, "Season": season, "Position": position})

# Button to generate the lineup
if st.button("Generate Lineup"):
    st.subheader("Your Lineup")

    # Create and display hitting lineup
    st.write("### Hitting Lineup")
    for i, hitter in enumerate(hitting_lineup, 1):
        player_stats = hitters_data[
            (hitters_data['Player Name'] == hitter['Player']) & (hitters_data['Season'] == hitter['Season'])
        ]
        st.write(f"{i}. {hitter['Player']} ({hitter['Position']} - {hitter['Season']})")
        st.dataframe(player_stats)

    # Create and display pitching lineup
    st.write("### Pitching Lineup")
    for i, pitcher in enumerate(pitching_lineup, 1):
        player_stats = pitchers_data[
            (pitchers_data['Player Name'] == pitcher['Player']) & (pitchers_data['Season'] == pitcher['Season'])
        ]
        st.write(f"{i}. {pitcher['Player']} ({pitcher['Position']} - {pitcher['Season']})")
        st.dataframe(player_stats)

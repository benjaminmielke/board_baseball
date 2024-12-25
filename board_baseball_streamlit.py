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
    # Use columns for layout
    col1, col2, col3 = st.columns([1, 1, 1])  # Distribute columns equally
    
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
    # Use columns for layout
    col1, col2, col3 = st.columns([1, 1, 1])  # Distribute columns equally
    
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

    # Display hitting lineup in the default Streamlit table
    st.write("### Hitting Lineup")
    hitter_stats = []
    for i, hitter in enumerate(hitting_lineup, 1):
        player_stats = hitters_data[
            (hitters_data['Name'] == hitter['Player']) & (hitters_data['Year'] == hitter['Year'])
        ]
        
        # Check the available columns and adjust accordingly
        stats = {
            'Index': i,  # Added index starting from 1
            'Player': hitter['Player'],
            'Year': hitter['Year'],  # Added Year to the stats
            'Position': hitter['Position'],
        }

        if 'BA' in player_stats.columns:
            stats['BA'] = player_stats['BA'].values[0]
        if 'HR' in player_stats.columns:
            stats['HR'] = player_stats['HR'].values[0]
        if 'H' in player_stats.columns:
            stats['H'] = player_stats['H'].values[0]

        hitter_stats.append(stats)

    # Create a DataFrame for easier formatting and display
    hitter_df = pd.DataFrame(hitter_stats)

    # Display the table using Streamlit's built-in table function
    st.table(hitter_df)

    # Display pitching lineup in the default Streamlit table
    st.write("### Pitching Lineup")
    pitcher_stats = []
    for i, pitcher in enumerate(pitching_lineup, 1):
        player_stats = pitchers_data[
            (pitchers_data['Name'] == pitcher['Player']) & (pitchers_data['Year'] == pitcher['Year'])
        ]
        
        # Check the available columns and adjust accordingly
        stats = {
            'Index': i,  # Added index starting from 1
            'Player': pitcher['Player'],
            'Year': pitcher['Year'],  # Added Year to the stats
            'Position': pitcher['Position'],
        }

        if 'W' in player_stats.columns:
            stats['W'] = player_stats['W'].values[0]
        if 'ERA' in player_stats.columns:
            stats['ERA'] = player_stats['ERA'].values[0]
        if 'SO' in player_stats.columns:
            stats['SO'] = player_stats['SO'].values[0]

        pitcher_stats.append(stats)

    # Create a DataFrame for easier formatting and display
    pitcher_df = pd.DataFrame(pitcher_stats)

    # Display the table using Streamlit's built-in table function
    st.table(pitcher_df)

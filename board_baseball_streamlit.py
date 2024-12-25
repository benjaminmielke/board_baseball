import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file based on input type (hitters or pitchers)
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to save DataFrame as an image
def save_dataframe_as_image(df, image_path):
    fig, ax = plt.subplots(figsize=(12, 4))  # Specify the size of the figure
    ax.axis('tight')
    ax.axis('off')
    
    # Render the dataframe as a table
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colColours=["#f5f5f5"]*len(df.columns))

    # Save the figure as an image file
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0.05)

# App starts here
st.title("Board Baseball Lineup Created")

# Add an input field for the team name
team_name = st.text_input("Enter your Team Name", "")

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
    # Custom colored header for hitting lineup (yellow)
    st.markdown(f"<h4 style='color: yellow;'>Hitter {i}</h4>", unsafe_allow_html=True)
    
    # Input fields stacked vertically
    player = st.selectbox(f"Select Player for Hitter {i}", hitters_names, key=f"hitter_{i}_player")
    season = st.selectbox(f"Select Year for Hitter {i}", seasons, key=f"hitter_{i}_season")
    position = st.selectbox(f"Select Position for Hitter {i}", positions_hitter, key=f"hitter_{i}_position")
    
    hitting_lineup.append({"Player": player, "Year": season, "Position": position})

# Create input fields for pitchers
st.header("Pitching Rotation")
pitching_lineup = []
for i in range(1, 6):
    # Custom colored header for pitching lineup (green)
    st.markdown(f"<h4 style='color: green;'>Pitcher {i}</h4>", unsafe_allow_html=True)
    
    # Input fields stacked vertically
    player = st.selectbox(f"Select Player for Pitcher {i}", pitchers_names, key=f"pitcher_{i}_player")
    season = st.selectbox(f"Select Year for Pitcher {i}", seasons, key=f"pitcher_{i}_season")
    position = st.selectbox(f"Select Role for Pitcher {i}", positions_pitcher, key=f"pitcher_{i}_position")
    
    pitching_lineup.append({"Player": player, "Year": season, "Position": position})

# Button to generate the lineup
if st.button("Generate Lineup"):
    st.subheader("Your Lineup")

    # Display team name if provided
    if team_name:
        st.write(f"### Team: {team_name}")
    else:
        st.write("### Team: [No team name provided]")

    # Prepare Hitting Lineup
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
            stats['BA'] = player_stats['BA'].values[0]
        if 'HR' in player_stats.columns:
            stats['HR'] = player_stats['HR'].values[0]
        if 'H' in player_stats.columns:
            stats['H'] = player_stats['H'].values[0]

        hitter_stats.append(stats)

    # Create a DataFrame for hitting lineup
    hitter_df = pd.DataFrame(hitter_stats)
    st.table(hitter_df)

    # Prepare Pitching Rotation
    pitcher_stats = []
    for i, pitcher in enumerate(pitching_lineup, 1):
        player_stats = pitchers_data[
            (pitchers_data['Name'] == pitcher['Player']) & (pitchers_data['Year'] == pitcher['Year'])
        ]
        
        # Collect stats for the player
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

    # Create a DataFrame for pitching rotation
    pitcher_df = pd.DataFrame(pitcher_stats)
    st.table(pitcher_df)

    # Save both lineups as images
    save_dataframe_as_image(hitter_df, "hitting_lineup.png")
    save_dataframe_as_image(pitcher_df, "pitching_rotation.png")

    st.write("### Lineups saved as images!")

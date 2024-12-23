import streamlit as st
import pandas as pd
from pybaseball import playerid_lookup, batting_stats, pitching_stats
import time

# Function to fetch players based on their type (Hitter or Pitcher)
def get_players_by_type(player_type):
    # Fetch batting and pitching stats for a range of years
    all_batting = batting_stats(2020)  # Example: Batting data from 2020
    all_pitching = pitching_stats(2020)  # Example: Pitching data from 2020
    
    if player_type == "Hitter":
        players = all_batting['playerID'].unique()  # Hitter IDs
    elif player_type == "Pitcher":
        players = all_pitching['playerID'].unique()  # Pitcher IDs
    else:
        players = []
    
    # Get player names for those IDs
    player_names = []
    for player_id in players:
        try:
            player_data = playerid_lookup(player_id)
            if not player_data.empty:
                player_names.append(player_data['name_full'].iloc[0])
        except:
            continue
    
    return sorted(player_names)

# Function to get the player's stats for the selected year
def get_player_stats(player_name, player_type, year):
    # Search for the player by name using playerid_lookup
    player_data = playerid_lookup(player_name)

    # If no player found
    if player_data.empty:
        st.error(f"No player found with the name: {player_name}")
        return pd.DataFrame()  # Return an empty DataFrame
    
    # Retrieve player ID (player's unique ID in the database)
    player_id = player_data['key_bbref'].iloc[0]
    st.write(f"Player found: {player_name} (BBREF ID: {player_id})")

    # Fetch batting stats for the specific year (if available)
    try:
        batting = batting_stats(year)
    except Exception as e:
        st.error(f"Error fetching batting stats for {year}: {e}")
        return pd.DataFrame()
    
    # Fetch pitching stats for the specific year (if available)
    try:
        pitching = pitching_stats(year)
    except Exception as e:
        st.error(f"Error fetching pitching stats for {year}: {e}")
        return pd.DataFrame()

    # Filter data for the specific player
    player_batting_stats = batting[batting['playerID'] == player_id]
    player_pitching_stats = pitching[pitching['playerID'] == player_id]

    # Create the final DataFrame
    stats = pd.DataFrame()

    if player_type == "Hitter" and not player_batting_stats.empty:
        player_batting_stats = player_batting_stats[['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA']]
        player_batting_stats['player_type'] = 'Hitter'
        stats = pd.concat([stats, player_batting_stats], ignore_index=True)
    
    if player_type == "Pitcher" and not player_pitching_stats.empty:
        player_pitching_stats = player_pitching_stats[['playerID', 'G', 'IP', 'SO', 'BB', 'ERA']]
        player_pitching_stats['player_type'] = 'Pitcher'
        stats = pd.concat([stats, player_pitching_stats], ignore_index=True)

    # Check if no stats are found and inform the user
    if stats.empty:
        st.write(f"No data available for {player_name} in {year}. This may be due to missing or incomplete stats.")
    
    return stats

def main():
    # Streamlit user interface
    st.title("Baseball Player Stats Viewer")

    # Select whether the player is a hitter or pitcher
    player_type = st.selectbox("Select Player Type", ["Hitter", "Pitcher"])

    # Get the list of players based on the selected type
    players = get_players_by_type(player_type)

    # Dropdown for selecting a player
    player_name = st.selectbox("Select Player", players)

    # Year selection
    year = st.number_input("Select Year", min_value=1985, max_value=2023, step=1)

    if st.button("Get Player Stats"):
        if player_name:
            # Fetch player stats for the selected year and player type
            player_stats_df = get_player_stats(player_name, player_type, year)

            # Display player stats if available
            if not player_stats_df.empty:
                st.write(f"Stats for {player_name} ({player_type}) in {year}")
                st.dataframe(player_stats_df)
            else:
                st.write(f"No data available for {player_name} in {year}.")
        else:
            st.error("Please select a player's name.")

if __name__ == "__main__":
    main()

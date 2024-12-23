import streamlit as st
import pandas as pd
from pybaseball import playerid_lookup, batting_stats, pitching_stats

# Function to fetch players based on their type (Hitter or Pitcher) and available years
def get_players_and_years(player_type):
    players = []
    years = set()  # To store unique years for the selected player type

    # Fetch stats for a range of years from 1985 to 2023
    try:
        for year in range(1985, 2024):
            if player_type == "Hitter":
                batting = batting_stats(year)
                # Check available columns in batting stats
                st.write(f"Batting stats columns for {year}: {batting.columns}")
                if 'playerID' in batting.columns:
                    players += batting['playerID'].unique().tolist()
                    years.update(batting['year'].unique().tolist())
                else:
                    st.write(f"Warning: 'playerID' not found in batting stats for {year}. Available columns: {batting.columns}")
            elif player_type == "Pitcher":
                pitching = pitching_stats(year)
                # Check available columns in pitching stats
                st.write(f"Pitching stats columns for {year}: {pitching.columns}")
                if 'playerID' in pitching.columns:
                    players += pitching['playerID'].unique().tolist()
                    years.update(pitching['year'].unique().tolist())
                else:
                    st.write(f"Warning: 'playerID' not found in pitching stats for {year}. Available columns: {pitching.columns}")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    
    # Remove duplicates
    players = list(set(players))
    years = sorted(list(years))

    # Get player names for those IDs
    player_names = []
    for player_id in players:
        try:
            player_data = playerid_lookup(player_id)
            if not player_data.empty:
                player_names.append(player_data['name_full'].iloc[0])
        except:
            continue
    
    return sorted(player_names), years

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
        if player_type == "Hitter":
            batting = batting_stats(year)
            # Check if 'playerID' exists
            if 'playerID' in batting.columns:
                player_batting_stats = batting[batting['playerID'] == player_id]
                player_batting_stats = player_batting_stats[['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA']]
                player_batting_stats['player_type'] = 'Hitter'
                return player_batting_stats
            else:
                st.error(f"'playerID' column not found in batting stats for {year}. Available columns: {batting.columns}")
                return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching batting stats for {year}: {e}")

    # Fetch pitching stats for the specific year (if available)
    try:
        if player_type == "Pitcher":
            pitching = pitching_stats(year)
            # Check if 'playerID' exists
            if 'playerID' in pitching.columns:
                player_pitching_stats = pitching[pitching['playerID'] == player_id]
                player_pitching_stats = player_pitching_stats[['playerID', 'G', 'IP', 'SO', 'BB', 'ERA']]
                player_pitching_stats['player_type'] = 'Pitcher'
                return player_pitching_stats
            else:
                st.error(f"'playerID' column not found in pitching stats for {year}. Available columns: {pitching.columns}")
                return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching pitching stats for {year}: {e}")

    return pd.DataFrame()  # Return empty DataFrame if no data found

def main():
    # Streamlit user interface
    st.title("Baseball Player Stats Viewer")

    # Select whether the player is a hitter or pitcher
    player_type = st.selectbox("Select Player Type", ["Hitter", "Pitcher"])

    # Get the list of players and years based on the selected type
    players, years = get_players_and_years(player_type)

    if not players:
        st.write("No players found for the selected type.")
        return

    # Dropdown for selecting a player
    player_name = st.selectbox("Select Player", players)

    # Dropdown for selecting a year based on the player selected
    year = st.selectbox("Select Year", years)

    # Button to fetch and display player stats for the selected year
    if st.button("Get Player Stats"):
        if player_name and year:
            # Fetch player stats for the selected year and player type
            player_stats_df = get_player_stats(player_name, player_type, year)

            # Display player stats if available
            if not player_stats_df.empty:
                st.write(f"Stats for {player_name} ({player_type}) in {year}")
                st.dataframe(player_stats_df)
            else:
                st.write(f"No data available for {player_name} in {year}.")
        else:
            st.error("Please select a player's name and a year.")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from pybaseball import playerid_lookup, batting_stats, pitching_stats

# Function to fetch all players and years from 2000 onwards
def get_players_and_years():
    players = []
    years = set()

    try:
        # Fetch stats for a range of years from 2000 to 2023
        for year in range(2000, 2024):
            # Fetch batting stats for the year
            batting = batting_stats(year)
            # Fetch pitching stats for the year
            pitching = pitching_stats(year)

            # Inspect columns to understand the data structure
            if batting is not None and 'playerID' in batting.columns:
                players += batting['playerID'].unique().tolist()
                years.update(batting['year'].unique().tolist())  # Check if 'year' exists
            else:
                st.warning(f"No 'playerID' column found in batting stats for {year}. Columns: {batting.columns if batting is not None else 'None'}")

            if pitching is not None and 'playerID' in pitching.columns:
                players += pitching['playerID'].unique().tolist()
                years.update(pitching['year'].unique().tolist())  # Check if 'year' exists
            else:
                st.warning(f"No 'playerID' column found in pitching stats for {year}. Columns: {pitching.columns if pitching is not None else 'None'}")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

    # Remove duplicates and sort
    players = list(set(players))
    years = sorted(list(years))

    # Get player names based on playerIDs
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
def get_player_stats(player_name, year):
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
        if batting is not None and 'playerID' in batting.columns:
            player_batting_stats = batting[batting['playerID'] == player_id]
            if not player_batting_stats.empty:
                player_batting_stats = player_batting_stats[['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA']]
                player_batting_stats['player_type'] = 'Hitter'
                return player_batting_stats
    except Exception as e:
        st.error(f"Error fetching batting stats for {year}: {e}")

    # Fetch pitching stats for the specific year (if available)
    try:
        pitching = pitching_stats(year)
        if pitching is not None and 'playerID' in pitching.columns:
            player_pitching_stats = pitching[pitching['playerID'] == player_id]
            if not player_pitching_stats.empty:
                player_pitching_stats = player_pitching_stats[['playerID', 'G', 'IP', 'SO', 'BB', 'ERA']]
                player_pitching_stats['player_type'] = 'Pitcher'
                return player_pitching_stats
    except Exception as e:
        st.error(f"Error fetching pitching stats for {year}: {e}")

    return pd.DataFrame()  # Return empty DataFrame if no data found

def main():
    # Streamlit user interface
    st.title("Baseball Player Stats Viewer")

    # Get the list of players and years based on the selected type
    players, years = get_players_and_years()

    if not players:
        st.write("No players found for the selected range.")
        return

    # Dropdown for selecting a player
    player_name = st.selectbox("Select Player", players)

    # Dropdown for selecting a year based on the player selected
    year = st.selectbox("Select Year", years)

    # Button to fetch and display player stats for the selected year
    if st.button("Get Player Stats"):
        if player_name and year:
            # Fetch player stats for the selected year
            player_stats_df = get_player_stats(player_name, year)

            # Display player stats if available
            if not player_stats_df.empty:
                st.write(f"Stats for {player_name} in {year}")
                st.dataframe(player_stats_df)
            else:
                st.write(f"No data available for {player_name} in {year}.")
        else:
            st.error("Please select a player's name and a year.")

if __name__ == "__main__":
    main()

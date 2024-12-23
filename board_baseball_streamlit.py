import streamlit as st
import pandas as pd
from pybaseball import player_search, batting_stats, pitching_stats
import time

def get_player_stats(player_name, year):
    # Search for the player by name
    player_data = player_search(player_name)

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

    if not player_batting_stats.empty:
        player_batting_stats = player_batting_stats[['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA']]
        player_batting_stats['player_type'] = 'Hitter'
        stats = pd.concat([stats, player_batting_stats], ignore_index=True)
    
    if not player_pitching_stats.empty:
        player_pitching_stats = player_pitching_stats[['playerID', 'G', 'IP', 'SO', 'BB', 'ERA']]
        player_pitching_stats['player_type'] = 'Pitcher'
        stats = pd.concat([stats, player_pitching_stats], ignore_index=True)

    return stats

def main():
    # Streamlit user interface
    st.title("Baseball Player Stats Viewer")

    # Player name input
    player_name = st.text_input("Enter Player's Name", "")

    # Year selection
    year = st.number_input("Select Year", min_value=1985, max_value=2023, step=1)

    if st.button("Get Player Stats"):
        if player_name:
            # Fetch player stats for the selected year
            player_stats_df = get_player_stats(player_name, year)

            # Display player stats if available
            if not player_stats_df.empty:
                st.write(f"Stats for {player_name} in {year}")
                st.dataframe(player_stats_df)
            else:
                st.write(f"No data available for {player_name} in {year}.")
        else:
            st.error("Please enter a player's name.")

if __name__ == "__main__":
    main()

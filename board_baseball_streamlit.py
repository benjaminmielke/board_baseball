import streamlit as st
import pandas as pd
from pybaseball import batting_stats, pitching_stats, playerid_lookup
from pybaseball.playerid_lookup import playerid_lookup

# Function to fetch player stats for the years 2021 to 2024
def get_player_stats():
    all_stats = pd.DataFrame()

    # Lookup player ID data from Baseball-Reference (bbref)
    players = playerid_lookup()

    # Filter out players we want to focus on (batters and pitchers)
    player_ids = players['playerID']

    # Fetch stats for a specific range of years (2021 to 2024)
    for year in range(2021, 2025):  # Adjusted year range to 2021-2024
        try:
            # Fetch batting stats for the given year
            batting = batting_stats(year)
            # Fetch pitching stats for the given year
            pitching = pitching_stats(year)

            # If we have valid data for batting stats
            if batting is not None:
                # Filter data based on playerID from the lookup
                batting = batting[batting['playerID'].isin(player_ids)]

                if 'playerID' in batting.columns:
                    batting['year'] = year
                    batting_columns = ['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA']
                else:
                    st.warning(f"No 'playerID' column found in batting stats for {year}.")
                    continue  # Skip to next year if no valid identifier is found

                # Filter available columns in batting
                available_batting_columns = [col for col in batting_columns if col in batting.columns]
                all_stats = pd.concat([all_stats, batting[available_batting_columns + ['year']]])

            # If we have valid data for pitching stats
            if pitching is not None:
                # Filter data based on playerID from the lookup
                pitching = pitching[pitching['playerID'].isin(player_ids)]

                if 'playerID' in pitching.columns:
                    pitching['year'] = year
                    pitching_columns = ['playerID', 'G', 'IP', 'SO', 'BB', 'ERA']
                else:
                    st.warning(f"No 'playerID' column found in pitching stats for {year}.")
                    continue  # Skip to next year if no valid identifier is found

                # Filter available columns in pitching
                available_pitching_columns = [col for col in pitching_columns if col in pitching.columns]
                all_stats = pd.concat([all_stats, pitching[available_pitching_columns + ['year']]])

        except Exception as e:
            st.error(f"Error fetching stats for {year}: {e}")
    
    # Convert 'year' column from float to int
    if 'year' in all_stats.columns:
        all_stats['year'] = all_stats['year'].astype(int)

    return all_stats

def main():
    # Streamlit user interface
    st.title("Baseball Player Stats Viewer")

    # Fetch and display the player stats for years 2021-2024
    all_stats_df = get_player_stats()

    if not all_stats_df.empty:
        # Display the number of rows in the dataframe
        num_rows = all_stats_df.shape[0]
        st.write(f"Number of rows in the dataset: {num_rows}")
        
        # Display the dataframe itself
        st.write("Player Stats from 2021 to 2024:")
        st.dataframe(all_stats_df)
    else:
        st.write("No stats available for the selected years.")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from pybaseball import batting_stats, pitching_stats

# Function to fetch player stats for the years 2021 to 2024
def get_player_stats():
    all_stats = pd.DataFrame()

    # Fetch stats for a specific range of years (2021 to 2024)
    for year in range(2021, 2025):  # Adjusted year range to 2021-2024
        try:
            # Fetch batting stats for the given year
            batting = batting_stats(year)
            # Fetch pitching stats for the given year
            pitching = pitching_stats(year)

            # If we have valid data for batting stats
            if batting is not None and 'playerID' in batting.columns:
                # Adjust the year column to 'Season' and filter for desired columns
                batting['Season'] = year
                batting_filtered = batting[['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA', 'Season']]
                all_stats = pd.concat([all_stats, batting_filtered])

            # If we have valid data for pitching stats
            if pitching is not None and 'playerID' in pitching.columns:
                # Adjust the year column to 'Season' and filter for desired columns
                pitching['Season'] = year
                pitching_filtered = pitching[['playerID', 'G', 'IP', 'SO', 'BB', 'ERA', 'Season']]
                all_stats = pd.concat([all_stats, pitching_filtered])

        except Exception as e:
            st.error(f"Error fetching stats for {year}: {e}")
    
    # Convert 'Season' column from float to int
    if 'Season' in all_stats.columns:
        all_stats['Season'] = all_stats['Season'].astype(int)

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
        
        # Display the first few rows of the final dataframe
        st.write("First few rows of the dataset:")
        st.dataframe(all_stats_df.head())  # Display only the first few rows of the final dataframe
    else:
        st.write("No stats available for the selected years.")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from pybaseball import playerid_lookup, batting_stats, pitching_stats

# Function to fetch all years and stats from 2000 to 2023
def get_players_and_years():
    years = set()

    try:
        # Fetch stats for a range of years from 2000 to 2023
        for year in range(2000, 2024):
            # Fetch batting stats for the year
            batting = batting_stats(year)
            # Fetch pitching stats for the year
            pitching = pitching_stats(year)

            # Check if 'year' column exists and update years set
            if batting is not None and 'year' in batting.columns:
                years.update(batting['year'].unique().tolist())
            if pitching is not None and 'Season' in pitching.columns:
                years.update(pitching['Season'].unique().tolist())  # 'Season' column for year
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")

    # Return sorted years
    return sorted(list(years))

# Function to fetch the top 10 player stats for all years
def get_top_10_player_stats(years):
    all_stats = pd.DataFrame()

    # Fetch stats for a range of years from 2000 to 2023
    for year in range(2000, 2024):
        try:
            # Fetch batting stats for the year
            batting = batting_stats(year)
            # Fetch pitching stats for the year
            pitching = pitching_stats(year)

            # If we have valid data for batting stats
            if batting is not None and 'playerID' in batting.columns:
                batting['year'] = year
                all_stats = pd.concat([all_stats, batting[['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA', 'year']]])

            # If we have valid data for pitching stats
            if pitching is not None:
                # The correct column for player names might be 'Name' for the pitching stats
                if 'Name' in pitching.columns:
                    pitching['year'] = year
                    pitching = pitching[['Name', 'G', 'IP', 'SO', 'BB', 'ERA', 'year']]
                    pitching['playerID'] = pitching['Name']  # Use 'Name' as 'playerID'
                    all_stats = pd.concat([all_stats, pitching[['playerID', 'G', 'IP', 'SO', 'BB', 'ERA', 'year']]])

        except Exception as e:
            st.error(f"Error fetching stats for {year}: {e}")
    
    # Show top 10 rows of the combined stats
    top_10_stats = all_stats.head(10)

    return top_10_stats

def main():
    # Streamlit user interface
    st.title("Baseball Player Stats Viewer")

    # Get the available years from 2000 to 2023
    years = get_players_and_years()

    if not years:
        st.write("No data found for the selected range.")
        return

    # Fetch and display the top 10 player stats
    top_10_stats_df = get_top_10_player_stats(years)

    if not top_10_stats_df.empty:
        st.write("Top 10 Player Stats:")
        st.dataframe(top_10_stats_df)
    else:
        st.write("No stats available for the selected years.")

if __name__ == "__main__":
    main()

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

    return years

# Function to fetch stats for the top 10 players and display them
def get_top_10_player_stats(years):
    all_stats = pd.DataFrame()

    # Fetch stats for a range of years from 2000 to 2023
    for year in range(2000, 2024):
        try:
            batting = batting_stats(year)
            pitching = pitching_stats(year)

            # If we have valid data for both batting and pitching stats
            if batting is not None and 'playerID' in batting.columns:
                batting['year'] = year
                all_stats = pd.concat([all_stats, batting[['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA', 'year']]])

            if pitching is not None and 'playerID' in pitching.columns:
                pitching['year'] = year
                all_stats = pd.concat([all_stats, pitching[['playerID', 'G', 'IP', 'SO', 'BB', 'ERA', 'year']]])

        except Exception as e:
            st.error(f"Error fetching stats for {year}: {e}")
    
    # Show top 10 rows of the data
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

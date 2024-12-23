import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to fetch player stats from Baseball Reference
def fetch_stats(year):
    # URL to Baseball Reference stats page for each year
    url_batting = f"https://www.baseball-reference.com/leagues/MLB/{year}-standard-batting.shtml"
    url_pitching = f"https://www.baseball-reference.com/leagues/MLB/{year}-standard-pitching.shtml"

    try:
        # Fetching batting stats
        response_batting = requests.get(url_batting)
        soup_batting = BeautifulSoup(response_batting.text, 'html.parser')

        # Fetching the batting table
        batting_table = soup_batting.find('table', {'class': 'stats_table'})

        # Parse the table into a DataFrame
        batting_df = pd.read_html(str(batting_table))[0]

        # Debug: Show columns for the batting DataFrame
        st.write(f"Columns in Batting DataFrame for {year}:")
        st.write(batting_df.columns)

        # Filter columns and clean up the data (we will need to adjust this based on actual columns)
        if 'Rk' in batting_df.columns:
            batting_df = batting_df[['Rk', 'Player', 'Age', 'G', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA']]
            batting_df['Season'] = year
            batting_df = batting_df.rename(columns={"Player": "playerID", "BA": "batting_average"})
            batting_df['playerID'] = batting_df['playerID'].str.strip()  # Clean up player names
        else:
            batting_df = pd.DataFrame()

        # Fetching pitching stats
        response_pitching = requests.get(url_pitching)
        soup_pitching = BeautifulSoup(response_pitching.text, 'html.parser')

        # Fetching the pitching table
        pitching_table = soup_pitching.find('table', {'class': 'stats_table'})

        # Parse the table into a DataFrame
        pitching_df = pd.read_html(str(pitching_table))[0]

        # Debug: Show columns for the pitching DataFrame
        st.write(f"Columns in Pitching DataFrame for {year}:")
        st.write(pitching_df.columns)

        # Filter columns and clean up the data (we will need to adjust this based on actual columns)
        if 'Rk' in pitching_df.columns:
            pitching_df = pitching_df[['Rk', 'Player', 'Age', 'G', 'IP', 'SO', 'BB', 'ERA']]
            pitching_df['Season'] = year
            pitching_df = pitching_df.rename(columns={"Player": "playerID", "ERA": "earned_run_avg"})
            pitching_df['playerID'] = pitching_df['playerID'].str.strip()  # Clean up player names
        else:
            pitching_df = pd.DataFrame()

        # Combine both DataFrames
        combined_df = pd.concat([batting_df[['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'batting_average', 'Season']],
                                 pitching_df[['playerID', 'G', 'IP', 'SO', 'BB', 'earned_run_avg', 'Season']]], ignore_index=True)

        return combined_df

    except Exception as e:
        st.error(f"Error fetching stats for {year}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Function to fetch all player stats for the years 2021 to 2024
def get_player_stats():
    all_stats = pd.DataFrame()

    # Fetch stats for a specific range of years (2021 to 2024)
    for year in range(2021, 2025):  # Adjusted year range to 2021-2024
        stats_df = fetch_stats(year)
        if not stats_df.empty:
            all_stats = pd.concat([all_stats, stats_df], ignore_index=True)

    # Clean up the final DataFrame (if needed)
    all_stats = all_stats.dropna(subset=['playerID'])  # Drop rows where playerID is missing

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

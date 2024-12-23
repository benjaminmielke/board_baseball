import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to fetch batting stats for a given year
def get_batting_stats(year):
    url = f'https://www.baseball-reference.com/leagues/MLB/{year}-standard-batting.shtml'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table that contains player stats
            table = soup.find('table', {'class': 'stats_table'})
            if table:
                df = pd.read_html(str(table))[0]  # Convert HTML table to DataFrame
                df['year'] = year  # Add the year column
                return df[['Rk', 'Player', 'Age', 'G', 'PA', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA', 'year']]
            else:
                st.error(f"No stats found for batting in {year}")
                return pd.DataFrame()
        else:
            st.error(f"Failed to fetch data for batting stats for {year}. Status code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching batting stats for {year}: {e}")
        return pd.DataFrame()

# Function to fetch pitching stats for a given year
def get_pitching_stats(year):
    url = f'https://www.baseball-reference.com/leagues/MLB/{year}-standard-pitching.shtml'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table that contains pitcher stats
            table = soup.find('table', {'class': 'stats_table'})
            if table:
                df = pd.read_html(str(table))[0]  # Convert HTML table to DataFrame
                df['year'] = year  # Add the year column
                return df[['Rk', 'Player', 'Age', 'G', 'GS', 'IP', 'W', 'L', 'SV', 'ERA', 'WHIP', 'BB', 'SO', 'year']]
            else:
                st.error(f"No stats found for pitching in {year}")
                return pd.DataFrame()
        else:
            st.error(f"Failed to fetch data for pitching stats for {year}. Status code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching pitching stats for {year}: {e}")
        return pd.DataFrame()

# Function to combine batting and pitching stats for all years (2021-2024)
def get_all_stats():
    all_stats = pd.DataFrame()

    # Loop through the years 2021 to 2024
    for year in range(2021, 2025):
        st.write(f"Fetching stats for {year}...")

        # Fetch batting stats
        batting_df = get_batting_stats(year)
        if not batting_df.empty:
            all_stats = pd.concat([all_stats, batting_df], ignore_index=True)

        # Fetch pitching stats
        pitching_df = get_pitching_stats(year)
        if not pitching_df.empty:
            all_stats = pd.concat([all_stats, pitching_df], ignore_index=True)

    return all_stats

def main():
    # Streamlit user interface
    st.title("Baseball Player Stats Viewer (Scraped from Baseball Reference)")

    # Fetch and display the player stats for years 2021-2024
    all_stats_df = get_all_stats()

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

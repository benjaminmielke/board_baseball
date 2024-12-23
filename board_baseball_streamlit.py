import streamlit as st
import pandas as pd
from pybaseball import batting_stats, pitching_stats

# Function to fetch all years from 2000 onwards
def get_years():
    years = set()

    try:
        # Fetch stats for a range of years from 2000 to 2023
        for year in range(2000, 2024):
            # Fetch batting stats for the year
            batting = batting_stats(year)
            # Fetch pitching stats for the year
            pitching = pitching_stats(year)

            # Check columns for batting stats
            if batting is not None:
                # Update years based on available data
                years.update(batting['Season'].unique().tolist())

            # Check columns for pitching stats
            if pitching is not None:
                # Update years based on available data
                years.update(pitching['Season'].unique().tolist())

    except Exception as e:
        st.error(f"Error fetching data: {e}")

    # Return years in sorted order
    return sorted(list(years))

# Function to fetch player stats for all years (2000 - 2023)
def get_player_stats():
    all_stats = pd.DataFrame()

    # Fetch stats for a range of years from 2000 to 2023
    for year in range(2000, 2024):
        try:
            # Fetch batting stats
            batting = batting_stats(year)
            # Fetch pitching stats
            pitching = pitching_stats(year)

            # If we have valid data for batting stats
            if batting is not None:
                if 'IDfg' in batting.columns:  # Use 'IDfg' for recent years
                    batting['year'] = year
                    batting_columns = ['IDfg', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA']
                elif 'playerID' in batting.columns:  # Use 'playerID' for older years
                    batting['year'] = year
                    batting_columns = ['playerID', 'H', '2B', '3B', 'HR', 'BB', 'SB', 'BA']
                else:
                    st.warning(f"No 'IDfg' or 'playerID' column found in batting stats for {year}.")
                    continue  # Skip to next year if no valid identifier is found

                # Filter available columns in batting
                available_batting_columns = [col for col in batting_columns if col in batting.columns]
                all_stats = pd.concat([all_stats, batting[available_batting_columns + ['year']]])

            # If we have valid data for pitching stats
            if pitching is not None:
                if 'IDfg' in pitching.columns:  # Use 'IDfg' for recent years
                    pitching['year'] = year
                    pitching_columns = ['IDfg', 'G', 'IP', 'SO', 'BB', 'ERA']
                elif 'playerID' in pitching.columns:  # Use 'playerID' for older years
                    pitching['year'] = year
                    pitching_columns = ['playerID', 'G', 'IP', 'SO', 'BB', 'ERA']
                else:
                    st.warning(f"No 'IDfg' or 'playerID' column found in pitching stats for {year}.")
                    continue  # Skip to next year if no valid identifier is found

                # Filter available columns in pitching
                available_pitching_columns = [col for col in pitching_columns if col in pitching.columns]
                pitching = pitching.rename(columns={'IDfg': 'playerID'})  # Rename to match with batting stats
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

    # Get the available years from 2000 to 2023
    years = get_years()

    if not years:
        st.write("No data found for the selected range.")
        return

    # Fetch and display the player stats for all years (2000 - 2023)
    all_stats_df = get_player_stats()

    if not all_stats_df.empty:
        # Display the number of rows in the dataframe
        num_rows = all_stats_df.shape[0]
        st.write(f"Number of rows in the dataset: {num_rows}")
        
        # Display the dataframe itself
        st.write("Player Stats from 2000 to 2023:")
        st.dataframe(all_stats_df)
    else:
        st.write("No stats available for the selected years.")

if __name__ == "__main__":
    main()

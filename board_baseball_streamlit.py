import streamlit as st
import pandas as pd
import math
from PIL import Image, ImageDraw, ImageFont
import io

# Set page config to use a narrow layout
st.set_page_config(layout="wide")

# Inject custom CSS for mobile layout and prevent stacking
st.markdown("""
    <style>
    /* Ensure block container doesn't take up too much space on mobile */
    .block-container {
        max-width: 100% !important;  /* Allow container to stretch to full width */
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    /* Make the column layout more flexible with flexbox */
    .css-1v0mbdj {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: space-between !important;  /* Add space between columns */
    }

    /* Specifically for small screen sizes (mobile), ensure columns fit well */
    @media screen and (max-width: 600px) {
        .css-1v0mbdj {
            flex-direction: row !important;  /* Ensure columns stay in one row */
            width: 100% !important;
        }
        
        .css-1aumxhk {
            width: 33% !important;  /* Limit the width of each column on mobile */
        }
        
        /* Adjust input fields and selectors */
        .css-1y4ud5 {
            padding: 8px 0;
        }

        .css-1axtv6d {
            font-size: 14px;
        }
        
        /* Adjusting select box sizes on mobile */
        select {
            font-size: 14px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sample data loading function
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Metrics calculation functions
def calculate_hitter_metrics(hitter_name, hitter_position, hitter_year, H, Double, Triple, HR, BB_H, SB, AVG):
    H = pd.to_numeric(H, errors='coerce')
    Double = pd.to_numeric(Double, errors='coerce')
    Triple = pd.to_numeric(Triple, errors='coerce')
    HR = pd.to_numeric(HR, errors='coerce')
    BB_H = pd.to_numeric(BB_H, errors='coerce')
    SB = pd.to_numeric(SB, errors='coerce')
    AVG = pd.to_numeric(AVG, errors='coerce')

    H = H if pd.notna(H) else 0
    Double = Double if pd.notna(Double) else 0
    Triple = Triple if pd.notna(Triple) else 0
    HR = HR if pd.notna(HR) else 0
    BB_H = BB_H if pd.notna(BB_H) else 0
    SB = SB if pd.notna(SB) else 0
    AVG = AVG if pd.notna(AVG) else 0

    hitter_boost = math.floor(AVG * 100)

    if H != 0:
        hitter_dice_row = math.floor(((Double + Triple + HR) / H) * 10)
    else:
        hitter_dice_row = 0

    if (H + BB_H) != 0:
        stealing = math.floor((SB / (H + BB_H)) * 100)
    else:
        stealing = 0

    stealing = "Yes" if stealing >= 5 else "No"

    return {
        'Hitter Boost': hitter_boost,
        'Dice Row': hitter_dice_row,
        'Stealing': stealing,
    }

# App starts here
st.title("Board Baseball Lineup Created")

# Input fields for team name and file paths
team_name = st.text_input("Enter your Team Name", "")

# Load hitter and pitcher data
hitters_file = 'hitters_stats.csv'
pitchers_file = 'pitchers_stats.csv'

hitters_data = load_data(hitters_file)
pitchers_data = load_data(pitchers_file)

# Extract player names for the dropdowns
hitters_names = sorted(hitters_data['Name'].unique())
pitchers_names = sorted(pitchers_data['Name'].unique())

# Define player positions
positions_hitter = ['1B', '2B', '3B', 'SS', 'C', 'LF', 'CF', 'RF', 'DH']
positions_pitcher = ['SP', 'RP', 'CL']

# Input for the hitting lineup
st.header("Hitting Lineup")
hitting_lineup = []
for i in range(1, 10):
    # Custom header
    st.markdown(f"<h4 style='color: lightblue;'>Hitter {i}</h4>", unsafe_allow_html=True)
    
    # Create flexible columns
    col1, col2, col3 = st.columns([2, 1, 1])  # Adjusted column width for mobile responsiveness
    
    # Player selection for hitting
    with col1:
        player = st.selectbox(f"Select Player for Hitter {i}", [" "] + hitters_names, key=f"hitter_{i}_player")
    
    # Year selection for hitting
    with col2:
        if player:
            available_years = sorted(hitters_data[hitters_data['Name'] == player]['Year'].unique())
            season = st.selectbox(f"Select Year for Hitter {i}", [" "] + available_years, key=f"hitter_{i}_season")
        else:
            season = st.selectbox(f"Select Year for Hitter {i}", [" "], key=f"hitter_{i}_season")
    
    # Position selection for hitting
    with col3:
        position = st.selectbox(f"Select Position for Hitter {i}", [" "] + positions_hitter, key=f"hitter_{i}_position")
    
    hitting_lineup.append({"Player": player, "Year": season, "Position": position})

# Input for the pitching lineup
st.header("Pitching Rotation")
pitching_lineup = []
for i in range(1, 6):
    # Custom header
    st.markdown(f"<h4 style='color: lightblue;'>Pitcher {i}</h4>", unsafe_allow_html=True)
    
    # Create flexible columns
    col1, col2, col3 = st.columns([2, 1, 1])  # Adjusted column width for mobile responsiveness
    
    # Player selection for pitching
    with col1:
        player = st.selectbox(f"Select Player for Pitcher {i}", [" "] + pitchers_names, key=f"pitcher_{i}_player")
    
    # Year selection for pitching
    with col2:
        if player:
            available_years = sorted(pitchers_data[pitchers_data['Name'] == player]['Year'].unique())
            season = st.selectbox(f"Select Year for Pitcher {i}", [" "] + available_years, key=f"pitcher_{i}_season")
        else:
            season = st.selectbox(f"Select Year for Pitcher {i}", [" "], key=f"pitcher_{i}_season")
    
    # Position selection for pitching
    with col3:
        position = st.selectbox(f"Select Role for Pitcher {i}", [" "] + positions_pitcher, key=f"pitcher_{i}_position")
    
    pitching_lineup.append({"Player": player, "Year": season, "Position": position})

# Generate lineup
if st.button("Generate Lineup"):
    st.subheader("Your Lineup")
    
    if team_name:
        st.write(f"### Team: {team_name}")
    else:
        st.write("### Team: [No team name provided]")

    # Display hitting lineup
    st.write("### Hitting Lineup")
    hitter_stats = []
    for i, hitter in enumerate(hitting_lineup, 1):
        player_stats = hitters_data[
            (hitters_data['Name'] == hitter['Player']) & (hitters_data['Year'] == hitter['Year'])
        ]
        
        if not player_stats.empty:
            metrics = calculate_hitter_metrics(
                hitter['Player'],
                hitter['Position'],
                hitter['Year'],
                player_stats['H'].values[0],
                player_stats['2B'].values[0],
                player_stats['3B'].values[0],
                player_stats['HR'].values[0],
                player_stats['BB'].values[0],
                player_stats['SB'].values[0],
                player_stats['BA'].values[0]
            )
            stats = {
                'Index': i,
                'Player': hitter['Player'],
                'Year': hitter['Year'],
                'Position': hitter['Position'],
                'Hitter Boost': metrics['Hitter Boost'],
                'Dice Row': metrics['Dice Row'],
                'Stealing': metrics['Stealing'],
            }
            hitter_stats.append(stats)
    
    hitter_df = pd.DataFrame(hitter_stats)
    st.table(hitter_df)

    # Display pitching lineup
    st.write("### Pitching Rotation")
    pitcher_stats = []
    for i, pitcher in enumerate(pitching_lineup, 1):
        player_stats = pitchers_data[
            (pitchers_data['Name'] == pitcher['Player']) & (pitchers_data['Year'] == pitcher['Year'])
        ]
        
        if not player_stats.empty:
            metrics = calculate_pitcher_metrics(
                pitcher['Player'],
                pitcher['Position'],
                pitcher['Year'],
                player_stats['ERA'].values[0],
                player_stats['G'].values[0],
                player_stats['IP'].values[0],
                player_stats['SO'].values[0],
                player_stats['BB'].values[0]
            )
            stats = {
                'Index': i,
                'Player': pitcher['Player'],
                'Year': pitcher['Year'],
                'Position': pitcher['Position'],
                'Pitcher Decrease': metrics['Pitcher Decrease'],
                'Dice Row': metrics['Dice Row'],
                'Endurance': metrics['Endurance'],
            }
            pitcher_stats.append(stats)
    
    pitcher_df = pd.DataFrame(pitcher_stats)
    st.table(pitcher_df)

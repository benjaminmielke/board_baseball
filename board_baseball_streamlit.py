import streamlit as st
import pandas as pd
import math
from PIL import Image, ImageDraw, ImageFont
import io

# Load the CSV file based on input type (hitters or pitchers)
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

# Hitter Metrics Calculation
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

# Pitcher Metrics Calculation
def calculate_pitcher_metrics(pitcher_name, pitcher_position, pitcher_year, ERA, G, IP, SO, BB_P):
    ERA = pd.to_numeric(ERA, errors='coerce')
    G = pd.to_numeric(G, errors='coerce')
    IP = pd.to_numeric(IP, errors='coerce')
    SO = pd.to_numeric(SO, errors='coerce')
    BB_P = pd.to_numeric(BB_P, errors='coerce')

    ERA = ERA if pd.notna(ERA) else 0
    G = G if pd.notna(G) else 0
    IP = IP if pd.notna(IP) else 0
    SO = SO if pd.notna(SO) else 0
    BB_P = BB_P if pd.notna(BB_P) else 0

    pitcher_decrease = -(math.floor(ERA * 10)) + 20

    pitcher_dice_row = math.floor(SO / BB_P) if BB_P != 0 else 0

    endurance = math.ceil(IP / G) if G != 0 else 0

    return {
        'Pitcher Decrease': pitcher_decrease,
        'Dice Row': pitcher_dice_row,
        'Endurance': endurance,
    }

# Function to convert dataframe to image
def dataframe_to_image(df):
    # Create a white canvas
    img_width = 1000
    img_height = 50 + len(df) * 40  # Height adjusts based on the number of rows
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Load font (default font in case the system does not have arial)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()
    
    # Define column names and column widths
    columns = df.columns
    x_pos = 10
    y_pos = 10
    
    # Draw column headers
    for col in columns:
        draw.text((x_pos, y_pos), col, font=font, fill=(0, 0, 0))
        x_pos += 180  # Space between columns
    
    # Draw row values
    y_pos = 40  # Start drawing rows after headers
    for idx, row in df.iterrows():
        x_pos = 10
        for val in row:
            draw.text((x_pos, y_pos), str(val), font=font, fill=(0, 0, 0))
            x_pos += 180  # Space between columns
        y_pos += 40  # Move to the next row
    
    return img

# Function to save the image as a PNG file
def save_image(img):
    # Save the image to a BytesIO object (in-memory file)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)  # Reset pointer to the beginning of the image data
    
    return img_bytes

# App starts here
st.title("Board Baseball Lineup Created")

# Add an input field for the team name, starting with an empty string
team_name = st.text_input("Enter your Team Name", "")

# File paths for hitter and pitcher stats
hitters_file = 'hitters_stats.csv'
pitchers_file = 'pitchers_stats.csv'

# Load hitter and pitcher data
hitters_data = load_data(hitters_file)
pitchers_data = load_data(pitchers_file)

# Extract player names and seasons for the dropdowns
hitters_names = sorted(hitters_data['Name'].unique())  # Updated column name
pitchers_names = sorted(pitchers_data['Name'].unique())  # Updated column name
seasons = sorted(hitters_data['Year'].unique())  # Assuming 'Year' is common for both datasets

# Positions for hitters and pitchers
positions_hitter = ['1B', '2B', '3B', 'SS', 'C', 'LF', 'CF', 'RF', 'DH']
positions_pitcher = ['SP', 'RP', 'CL']

# Create input fields for hitters, all starting as blank (None)
st.header("Hitting Lineup")
hitting_lineup = []
for i in range(1, 10):
    # Custom colored header for hitting lineup (yellow)
    st.markdown(f"<h4 style='color: yellow;'>Hitter {i}</h4>", unsafe_allow_html=True)
    
    # Input fields stacked vertically, starting as blank
    player = st.selectbox(f"Select Player for Hitter {i}", [None] + hitters_names, key=f"hitter_{i}_player")
    season = st.selectbox(f"Select Year for Hitter {i}", [None] + seasons, key=f"hitter_{i}_season")
    position = st.selectbox(f"Select Position for Hitter {i}", [None] + positions_hitter, key=f"hitter_{i}_position")
    
    hitting_lineup.append({"Player": player, "Year": season, "Position": position})

# Create input fields for pitchers, all starting as blank (None)
st.header("Pitching Rotation")
pitching_lineup = []
for i in range(1, 6):
    # Custom colored header for pitching lineup (green)
    st.markdown(f"<h4 style='color: green;'>Pitcher {i}</h4>", unsafe_allow_html=True)
    
    # Input fields stacked vertically, starting as blank
    player = st.selectbox(f"Select Player for Pitcher {i}", [None] + pitchers_names, key=f"pitcher_{i}_player")
    season = st.selectbox(f"Select Year for Pitcher {i}", [None] + seasons, key=f"pitcher_{i}_season")
    position = st.selectbox(f"Select Role for Pitcher {i}", [None] + positions_pitcher, key=f"pitcher_{i}_position")
    
    pitching_lineup.append({"Player": player, "Year": season, "Position": position})

# Button to generate the lineup
if st.button("Generate Lineup"):
    st.subheader("Your Lineup")

    # Display team name if provided
    if team_name:
        st.write(f"### Team: {team_name}")
    else:
        st.write("### Team: [No team name provided]")

    # Display hitting lineup in a simple table format
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
                player_stats['H'].values

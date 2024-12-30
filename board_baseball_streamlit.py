import streamlit as st
import pandas as pd
import math
from PIL import Image, ImageDraw, ImageFont
import io
import random

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
def dataframe_to_image(df, header_text):
    img_width = 1300
    img_height = 80 + len(df) * 40
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    columns = df.columns
    x_pos = 10
    y_pos = 10
    draw.text((x_pos, y_pos), header_text, font=font, fill=(0, 0, 0))
    y_pos += 30
    for col in columns:
        draw.text((x_pos, y_pos), col, font=font, fill=(0, 0, 0))
        x_pos += 180
    y_pos += 30
    for idx, row in df.iterrows():
        x_pos = 10
        for val in row:
            draw.text((x_pos, y_pos), str(val), font=font, fill=(0, 0, 0))
            x_pos += 180
        y_pos += 40
    return img

# Function to save the image as a PNG file
def save_image(img):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

# App starts here
st.set_page_config(page_title="Board Baseball", page_icon="⚾", layout="wide")

# Custom CSS for baseball theme
st.markdown("""
    <style>
        body {
            background-image: url('https://www.hdwallpapers.in/download/baseball_field_grass_sports_field-2560x1600.jpg');
            background-size: cover;
            color: white;
        }
        h1, h2, h3, h4 {
            font-family: 'Press Start 2P', cursive;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .stSelectbox>div>div>div>input {
            background-color: #f4f4f4;
            border-radius: 5px;
        }
        .stTextInput>div>div>input {
            background-color: #f4f4f4;
            border-radius: 5px;
        }
        .stTable {
            font-family: 'Courier New', Courier, monospace;
            border: 1px solid #ffffff;
            margin-top: 20px;
        }
        .stTable th {
            background-color: rgba(255, 255, 255, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("⚾ Board Baseball ⚾")

# Add an input field for the team name
team_name = st.text_input("Enter your Team Name", "")

# File paths for hitter and pitcher stats
hitters_file = 'hitters_stats.csv'
pitchers_file = 'pitchers_stats.csv'

# Load hitter and pitcher data
hitters_data = load_data(hitters_file)
pitchers_data = load_data(pitchers_file)

# Extract player names and seasons for the dropdowns
hitters_names = sorted(hitters_data['Name'].unique())
pitchers_names = sorted(pitchers_data['Name'].unique())

# Positions for hitters and pitchers
positions_hitter = ['1B', '2B', '3B', 'SS', 'C', 'LF', 'CF', 'RF', 'DH']
positions_pitcher = ['SP', 'RP', 'CL']

# Add a button to generate random lineup
if st.button("Randomize Players"):
    for i in range(1, 10):
        hitter = random.choice(hitters_names)
        season = random.choice(sorted(hitters_data[hitters_data['Name'] == hitter]['Year'].unique()))
        position = random.choice(positions_hitter)
        st.session_state[f"hitter_{i}_player"] = hitter
        st.session_state[f"hitter_{i}_season"] = season
        st.session_state[f"hitter_{i}_position"] = position
    
    for i in range(1, 6):
        pitcher = random.choice(pitchers_names)
        season = random.choice(sorted(pitchers_data[pitchers_data['Name'] == pitcher]['Year'].unique()))
        position = random.choice(positions_pitcher)
        st.session_state[f"pitcher_{i}_player"] = pitcher
        st.session_state[f"pitcher_{i}_season"] = season
        st.session_state[f"pitcher_{i}_position"] = position

# Create hitting lineup and pitching rotation as before (refer to the initial code for this)
# For brevity, I won't repeat the entire code again here, but ensure you use the same process.

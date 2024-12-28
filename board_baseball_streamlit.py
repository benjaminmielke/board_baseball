import streamlit as st
import pandas as pd
import math
from PIL import Image, ImageDraw, ImageFont
import io

# Cache function to load the data
@st.cache_data
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
    # Create a white canvas
    img_width = 1300
    img_height = 80 + len(df) * 40  # Height adjusts based on the number of rows
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Load font (default font in case the system does not have arial)
    font = ImageFont.load_default()
    
    # Define column names and column widths
    columns = df.columns
    x_pos = 10
    y_pos = 10
    
    # Draw the header text
    draw.text((x_pos, y_pos), header_text, font=font, fill=(0, 0, 0))
    y_pos += 30  # Move down after header text
    
    # Draw column headers
    for col in columns:
        draw.text((x_pos, y_pos), col, font=font, fill=(0, 0, 0))
        x_pos += 180  # Space between columns
    
    # Draw row values
    y_pos += 30  # Move down after column headers
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

# Step 1: Team name input field
if 'team_name' not in st.session_state:
    st.session_state.team_name = ""

team_name = st.text_input("Enter your Team Name", value=st.session_state.team_name)

if team_name:
    st.session_state.team_name = team_name
    st.session_state.step = 1  # Move to step 1 after team name is entered

# Step 2: Show hitting lineup
if 'step' not in st.session_state:
    st.session_state.step = 0

# If the team name is set, proceed to the hitting lineup section
if st.session_state.step == 1:
    st.header("Hitting Lineup")

    # Step 2: Hitter 1 selection
    hitting_lineup = []
    if 'hitter_1' not in st.session_state:
        st.session_state.hitter_1 = {}
    hitter_1 = st.session_state.hitter_1

    st.markdown("<h4 style='color: yellow;'>Hitter 1</h4>", unsafe_allow_html=True)
    player_1 = st.selectbox("Select Player for Hitter 1", [" "] + hitters_names, key="hitter_1_player")
    
    if player_1:
        available_years_1 = sorted(hitters_data[hitters_data['Name'] == player_1]['Year'].unique())
        season_1 = st.selectbox(f"Select Year for Hitter 1", [" "] + available_years_1, key="hitter_1_year")
    else:
        season_1 = st.selectbox(f"Select Year for Hitter 1", [" "], key="hitter_1_year")

    position_1 = st.selectbox(f"Select Position for Hitter 1", [" "] + positions_hitter, key="hitter_1_position")
    
    if player_1 and season_1 and position_1:
        hitting_lineup.append({"Player": player_1, "Year": season_1, "Position": position_1})
        st.session_state.step = 2  # Move to next step once player 1 is filled

# Step 3: Show additional players (Hitter 2, Hitter 3, etc.)
if st.session_state.step == 2:
    # Hitter 2
    st.markdown("<h4 style='color: yellow;'>Hitter 2</h4>", unsafe_allow_html=True)
    player_2 = st.selectbox("Select Player for Hitter 2", [" "] + hitters_names, key="hitter_2_player")
    if player_2:
        available_years_2 = sorted(hitters_data[hitters_data['Name'] == player_2]['Year'].unique())
        season_2 = st.selectbox(f"Select Year for Hitter 2", [" "] + available_years_2, key="hitter_2_year")
    else:
        season_2 = st.selectbox(f"Select Year for Hitter 2", [" "], key="hitter_2_year")

    position_2 = st.selectbox(f"Select Position for Hitter 2", [" "] + positions_hitter, key="hitter_2_position")

    if player_2 and season_2 and position_2:
        hitting_lineup.append({"Player": player_2, "Year": season_2, "Position": position_2})
        st.session_state.step = 3  # Move to next step

# Repeat similar pattern for Hitter 3, Hitter 4, etc.

# Pitcher Selection and Further steps
# Once hitting lineup is fully completed, we move to pitching steps

if st.session_state.step == 5:
    st.markdown("<h4 style='color: yellow;'>Pitcher 1</h4>", unsafe_allow_html=True)
    pitcher_1 = st.selectbox("Select Player for Pitcher 1", [" "] + pitchers_names, key="pitcher_1_player")
    
    if pitcher_1:
        available_years_1 = sorted(pitchers_data[pitchers_data['Name'] == pitcher_1]['Year'].unique())
        season_1 = st.selectbox(f"Select Year for Pitcher 1", [" "] + available_years_1, key="pitcher_1_year")
    else:
        season_1 = st.selectbox(f"Select Year for Pitcher 1", [" "], key="pitcher_1_year")

    position_1 = st.selectbox(f"Select Position for Pitcher 1", [" "] + positions_pitcher, key="pitcher_1_position")

    # Continue to build the pitcher lineup step by step as needed


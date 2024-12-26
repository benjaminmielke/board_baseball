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
def dataframe_to_image(df, header_text):
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

# Positions for hitters and pitchers
positions_hitter = ['1B', '2B', '3B', 'SS', 'C', 'LF', 'CF', 'RF', 'DH']
positions_pitcher = ['SP', 'RP', 'CL']

# Create input fields for hitters, all starting as blank (empty string)
st.header("Hitting Lineup")
hitting_lineup = []
for i in range(1, 10):
    # Custom colored header for hitting lineup (yellow)
    st.markdown(f"<h4 style='color: yellow;'>Hitter {i}</h4>", unsafe_allow_html=True)
    
    # Select Player for Hitter
    player = st.selectbox(f"Select Player for Hitter {i}", [" "] + hitters_names, key=f"hitter_{i}_player")
    
    # Dynamically filter available years for selected player
    if player:
        available_years = sorted(hitters_data[hitters_data['Name'] == player]['Year'].unique())
        season = st.selectbox(f"Select Year for Hitter {i}", [" "] + available_years, key=f"hitter_{i}_season")
    else:
        season = st.selectbox(f"Select Year for Hitter {i}", [" "], key=f"hitter_{i}_season")
    
    position = st.selectbox(f"Select Position for Hitter {i}", [" "] + positions_hitter, key=f"hitter_{i}_position")
    
    hitting_lineup.append({"Player": player, "Year": season, "Position": position})

# Create input fields for pitchers, all starting as blank (empty string)
st.header("Pitching Rotation")
pitching_lineup = []
for i in range(1, 6):
    # Custom colored header for pitching lineup (green)
    st.markdown(f"<h4 style='color: green;'>Pitcher {i}</h4>", unsafe_allow_html=True)
    
    # Select Player for Pitcher
    player = st.selectbox(f"Select Player for Pitcher {i}", [" "] + pitchers_names, key=f"pitcher_{i}_player")
    
    # Dynamically filter available years for selected player
    if player:
        available_years = sorted(pitchers_data[pitchers_data['Name'] == player]['Year'].unique())
        season = st.selectbox(f"Select Year for Pitcher {i}", [" "] + available_years, key=f"pitcher_{i}_season")
    else:
        season = st.selectbox(f"Select Year for Pitcher {i}", [" "], key=f"pitcher_{i}_season")
    
    position = st.selectbox(f"Select Role for Pitcher {i}", [" "] + positions_pitcher, key=f"pitcher_{i}_position")
    
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

    for hitter in hitting_lineup:
        if hitter['Player'] and hitter['Year'] and hitter['Position']:
            hitter_data = hitters_data[(hitters_data['Name'] == hitter['Player']) & 
                                       (hitters_data['Year'] == hitter['Year'])]

            if not hitter_data.empty:
                # Calculate metrics for this hitter
                metrics = calculate_hitter_metrics(
                    hitter['Player'], 
                    hitter['Position'], 
                    hitter['Year'], 
                    *hitter_data[['H', '2B', '3B', 'HR', 'BB_H', 'SB', 'AVG']].iloc[0]
                )
                hitter_stats.append({
                    'Player': hitter['Player'],
                    'Position': hitter['Position'],
                    'Year': hitter['Year'],
                    'Hitter Boost': metrics['Hitter Boost'],
                    'Dice Row': metrics['Dice Row'],
                    'Stealing': metrics['Stealing'],
                })

    # Display pitcher lineup in a simple table format
    st.write("### Pitching Rotation")
    pitcher_stats = []

    for pitcher in pitching_lineup:
        if pitcher['Player'] and pitcher['Year'] and pitcher['Position']:
            pitcher_data = pitchers_data[(pitchers_data['Name'] == pitcher['Player']) & 
                                         (pitchers_data['Year'] == pitcher['Year'])]

            if not pitcher_data.empty:
                # Calculate metrics for this pitcher
                metrics = calculate_pitcher_metrics(
                    pitcher['Player'], 
                    pitcher['Position'], 
                    pitcher['Year'], 
                    *pitcher_data[['ERA', 'G', 'IP', 'SO', 'BB_P']].iloc[0]
                )
                pitcher_stats.append({
                    'Player': pitcher['Player'],
                    'Position': pitcher['Position'],
                    'Year': pitcher['Year'],
                    'Pitcher Decrease': metrics['Pitcher Decrease'],
                    'Dice Row': metrics['Dice Row'],
                    'Endurance': metrics['Endurance'],
                })

    # Create DataFrame from stats
    hitter_df = pd.DataFrame(hitter_stats)
    pitcher_df = pd.DataFrame(pitcher_stats)

    # Combine both DataFrames
    full_df = pd.concat([hitter_df, pitcher_df], ignore_index=True)

    # Convert DataFrame to image
    img = dataframe_to_image(full_df, "Baseball Lineup")

    # Display the image in the app
    st.image(img)

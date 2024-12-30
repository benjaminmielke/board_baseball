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
st.set_page_config(page_title="Board Baseball 🎲", page_icon="⚾", layout="wide")

# Custom CSS for baseball theme and button styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rock+Salt&display=swap');
        
        body {
            background-image: url('https://cdn.pixabay.com/photo/2021/07/09/07/47/baseball-6402182_960_720.jpg');
            background-size: cover;
            color: white;
            font-family: 'Press Start 2P', cursive;
            background-position: center center;
            background-attachment: fixed;
            padding: 0;
            margin: 0;
        }
        h1, h2, h3, h4 {
            font-family: 'Press Start 2P', cursive;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
        }
        .stButton>button {
            background: linear-gradient(145deg, #28A745, #34D058); /* Green gradient */
            color: white;
            border: 2px solid #fff;
            padding: 12px 24px;
            font-size: 18px;
            cursor: pointer;
            border-radius: 8px;
            box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.3), -4px -4px 8px rgba(255, 255, 255, 0.2);
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(145deg, #34D058, #28A745); /* Inverted green gradient */
            transform: translateY(-2px);
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
        }
        .stSelectbox>div>div>div>input, .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            padding: 10px;
        }
        .stTable {
            font-family: 'Courier New', Courier, monospace;
            background-color: rgba(0, 0, 0, 0.5);
            border: 1px solid white;
            margin-top: 20px;
            border-radius: 10px;
        }
        .stTable th {
            background-color: rgba(255, 255, 255, 0.2);
            color: yellow;
        }
        .stTable td {
            text-align: center;
            color: white;
        }
        .stTable th, .stTable td {
            padding: 15px;
        }
        .stTable td {
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stHeader {
            color: #1E40AF; /* Blue Header Color for Pitchers */
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("⚾ Board Baseball 🎲")

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
positions_hitter = ['C', '1B', '2B', '3B', 'SS', 'OF', 'DH']
positions_pitcher = ['SP', 'RP']

# Hitting lineup section
st.header("Hitting Lineup")
hitting_lineup = []
for i in range(1, 10):
    st.markdown(f"<h4 style='color: #FF001D;'>Hitter {i}</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 1])  # Player selector takes more space

    with col1:
        player = st.selectbox(f"Player Name", [" "] + hitters_names, key=f"hitter_{i}_player")
    
    with col2:
        if player:
            available_years = sorted(hitters_data[hitters_data['Name'] == player]['Year'].unique())
            season = st.selectbox(f"Year", [" "] + available_years, key=f"hitter_{i}_season")
        else:
            season = st.selectbox(f"Year", [" "], key=f"hitter_{i}_season")
    
    with col3:
        position = st.selectbox(f"Position", [" "] + positions_hitter, key=f"hitter_{i}_position")
    
    hitting_lineup.append({"Player": player, "Year": season, "Position": position})

# Pitching rotation section
st.header("Pitching Rotation")
pitching_lineup = []
for i in range(1, 6):
    st.markdown(f"<h4 style='color: #0080FF;'>Pitcher {i}</h4>", unsafe_allow_html=True)  # Blue for pitchers
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        player = st.selectbox(f"Player Name", [" "] + pitchers_names, key=f"pitcher_{i}_player")
    
    with col2:
        if player:
            available_years = sorted(pitchers_data[pitchers_data['Name'] == player]['Year'].unique())
            season = st.selectbox(f"Year", [" "] + available_years, key=f"pitcher_{i}_season")
        else:
            season = st.selectbox(f"Year", [" "], key=f"pitcher_{i}_season")
    
    with col3:
        position = st.selectbox(f"Position", [" "] + positions_pitcher, key=f"pitcher_{i}_position")
    
    pitching_lineup.append({"Player": player, "Year": season, "Position": position})

# Button to generate lineup
if st.button("Generate Lineup"):
    st.subheader("Your Lineup")

    if team_name:
        st.write(f"### Team: {team_name}")
    else:
        st.write("### Team: [No team name provided]")

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
        else:
            stats = {
                'Index': i,
                'Player': hitter['Player'],
                'Year': hitter['Year'],
                'Position': hitter['Position'],
                'Hitter Boost': 'N/A',
                'Dice Row': 'N/A',
                'Stealing': 'N/A',
            }
            hitter_stats.append(stats)

    hitter_df = pd.DataFrame(hitter_stats)
    st.table(hitter_df)

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
        else:
            stats = {
                'Index': i,
                'Player': pitcher['Player'],
                'Year': pitcher['Year'],
                'Position': pitcher['Position'],
                'Pitcher Decrease': 'N/A',
                'Dice Row': 'N/A',
                'Endurance': 'N/A',
            }
            pitcher_stats.append(stats)

    pitcher_df = pd.DataFrame(pitcher_stats)
    st.table(pitcher_df)

    # Create PNG output for hitting and pitching lineups combined
    img_hitter = dataframe_to_image(hitter_df, f"{team_name} - Hitting Lineup")
    img_pitcher = dataframe_to_image(pitcher_df, f"{team_name} - Pitching Rotation")
    
    # Combine both images into one
    total_height = img_hitter.height + img_pitcher.height
    combined_img = Image.new('RGB', (img_hitter.width, total_height), color=(255, 255, 255))
    combined_img.paste(img_hitter, (0, 0))
    combined_img.paste(img_pitcher, (0, img_hitter.height))
    
    # Save the combined image as PNG
    img_bytes = save_image(combined_img)

    # Provide download button for the combined PNG
    st.download_button(
        label="Download Combined Lineup as PNG",
        data=img_bytes,
        file_name=f"{team_name}_combined_lineup.png" if team_name else "combined_lineup.png",
        mime="image/png"
    )

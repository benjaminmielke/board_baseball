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

# Function to convert dataframe to image with larger text
def dataframe_to_image(df, header_text):
    # Create a white canvas
    img_width = 1300
    img_height = 80 + len(df) * 60  # Height adjusts based on the number of rows and larger font
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Load a larger font (use a TTF file for a better font)
    try:
        font = ImageFont.truetype("arial.ttf", 28)  # Large font for the table and header
    except IOError:
        font = ImageFont.load_default()  # Fallback in case the font isn't found
    
    # Define column names and column widths
    columns = df.columns
    x_pos = 10
    y_pos = 10
    
    # Draw the header text with larger font size
    draw.text((x_pos, y_pos), header_text, font=font, fill=(0, 0, 0))
    y_pos += 50  # Move down after header text to give space for the header
    
    # Draw column headers with larger font size
    for col in columns:
        draw.text((x_pos, y_pos), col, font=font, fill=(0, 0, 0))
        x_pos += 220  # Space between columns
    
    # Draw row values with larger font size
    y_pos += 40  # Move down after column headers
    for idx, row in df.iterrows():
        x_pos = 10
        for val in row:
            draw.text((x_pos, y_pos), str(val), font=font, fill=(0, 0, 0))
            x_pos += 220  # Space between columns
        y_pos += 60  # Move to the next row with more vertical spacing
    
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
        @import url('https://fonts.googleapis.com/css2?family=Squada+One&display=swap');
        
        body {
            background-image: url('https://img.freepik.com/free-vector/gradient-softball-background_23-2150742153.jpg');
            background-size: cover;
            color: white;
            font-family: 'Squada One';
            background-position: center center;
            background-attachment: fixed;
            padding: 0;
            margin: 0;
        }
        h1, h2, h3, h4 {
            font-family: 'Squada One', cursive;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
        }
        .center-title {
            text-align: center;
            font-size: 38px;
            color: #EED9DC; /* Orange color for the title */
            text-shadow: 2px 2px 4px rgba(143, 192, 235, .5);
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

# Title with custom CSS for centering
st.markdown('<h1 class="center-title">⚾ Board Baseball 🎲</h1>', unsafe_allow_html=True)

# The rest of your code remains unchanged...

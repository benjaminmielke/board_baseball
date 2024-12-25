import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# Function to convert dataframe to image
def dataframe_to_image(df):
    # Create a white canvas
    img_width = 800
    img_height = 50 + len(df) * 30  # Height adjusts based on the number of rows
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Load font (default font in case the system does not have arial)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()
    
    # Define column names
    columns = df.columns
    x_pos = 10
    y_pos = 10
    
    # Draw column headers
    for col in columns:
        draw.text((x_pos, y_pos), col, font=font, fill=(0, 0, 0))
        x_pos += 140  # Space between columns
    
    # Draw row values
    y_pos = 40  # Start drawing rows after headers
    for idx, row in df.iterrows():
        x_pos = 10
        for val in row:
            draw.text((x_pos, y_pos), str(val), font=font, fill=(0, 0, 0))
            x_pos += 140  # Space between columns
        y_pos += 30  # Move to the next row
    
    return img

# Function to save the image as a PNG file
def save_image(img):
    # Save the image to a BytesIO object (in-memory file)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)  # Reset pointer to the beginning of the image data
    
    return img_bytes

# Example DataFrame (replace with your actual lineup DataFrame)
def generate_sample_lineup():
    # Sample data for hitters and pitchers (replace with actual lineup data)
    data = {
        "Index": [1, 2, 3],
        "Player": ["Player 1", "Player 2", "Player 3"],
        "Year": [2023, 2023, 2023],
        "Position": ["1B", "2B", "SS"],
        "BA": [0.300, 0.280, 0.270],
        "HR": [10, 15, 8],
        "H": [150, 120, 100]
    }
    
    df = pd.DataFrame(data)
    return df

# Streamlit app
st.title("Board Baseball Lineup")

# Sample hitting lineup DataFrame (use actual data from your app)
hitting_lineup_df = generate_sample_lineup()

# Display hitting lineup as table
st.write("### Hitting Lineup")
st.dataframe(hitting_lineup_df)

# Convert dataframe to image
img = dataframe_to_image(hitting_lineup_df)

# Show the image
st.image(img, caption="Generated Lineup", use_column_width=True)

# Save the image as a PNG file
img_bytes = save_image(img)

# Provide the image for download
st.download_button(
    label="Download Lineup as PNG",
    data=img_bytes,
    file_name="board_baseball_lineup.png",
    mime="image/png"
)

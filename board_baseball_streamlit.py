import random

# Function to generate random hitting lineup
def generate_random_hitting_lineup():
    # Select 9 random hitters from the available hitter names
    random_hitters = random.sample(hitters_names, 9)
    
    # Assign a random position from the positions_hitter list for each hitter
    random_hitting_lineup = []
    for i, player in enumerate(random_hitters, 1):
        position = random.choice(positions_hitter)
        random_hitting_lineup.append({"Player": player, "Year": " ", "Position": position})
    
    return random_hitting_lineup

# Function to generate random pitching rotation
def generate_random_pitching_rotation():
    # Select 5 random pitchers from the available pitcher names
    random_pitchers = random.sample(pitchers_names, 5)
    
    # Assign a random position from the positions_pitcher list for each pitcher
    random_pitching_rotation = []
    for i, player in enumerate(random_pitchers, 1):
        position = random.choice(positions_pitcher)
        random_pitching_rotation.append({"Player": player, "Year": " ", "Position": position})
    
    return random_pitching_rotation

# Add a button to generate a random lineup at the top of the app
random_button = st.button("Generate Random Lineup")

if random_button:
    # Generate random hitting lineup and pitching rotation when the button is clicked
    hitting_lineup = generate_random_hitting_lineup()
    pitching_lineup = generate_random_pitching_rotation()

# App starts here
st.title("Board Baseball")  # Updated title

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
for i, hitter in enumerate(hitting_lineup, 1):
    # Custom colored header for hitting lineup (yellow)
    st.markdown(f"<h4 style='color: yellow;'>Hitter {i}</h4>", unsafe_allow_html=True)
    
    # Create 3 columns for Player, Year, Position
    col1, col2, col3 = st.columns([3, 1, 1])  # Player selector takes more space

    # Select Player for Hitter
    with col1:
        player = st.selectbox(f"Player Name", [" "] + hitters_names, key=f"hitter_{i}_player", index=hitters_names.index(hitter['Player']) if hitter['Player'] in hitters_names else 0)
    
    # Dynamically filter available years for selected player
    with col2:
        if player:
            available_years = sorted(hitters_data[hitters_data['Name'] == player]['Year'].unique())
            season = st.selectbox(f"Year", [" "] + available_years, key=f"hitter_{i}_season")
        else:
            season = st.selectbox(f"Year", [" "], key=f"hitter_{i}_season")
    
    # Select Position for Hitter
    with col3:
        position = st.selectbox(f"Position", [" "] + positions_hitter, key=f"hitter_{i}_position", index=positions_hitter.index(hitter['Position']) if hitter['Position'] in positions_hitter else 0)

# Create input fields for pitchers, all starting as blank (empty string)
st.header("Pitching Rotation")
for i, pitcher in enumerate(pitching_lineup, 1):
    # Custom colored header for pitching lineup (green)
    st.markdown(f"<h4 style='color: green;'>Pitcher {i}</h4>", unsafe_allow_html=True)
    
    # Create 3 columns for Player, Year, Position
    col1, col2, col3 = st.columns([3, 1, 1])  # Player selector takes more space

    # Select Player for Pitcher
    with col1:
        player = st.selectbox(f"Player Name", [" "] + pitchers_names, key=f"pitcher_{i}_player", index=pitchers_names.index(pitcher['Player']) if pitcher['Player'] in pitchers_names else 0)
    
    # Dynamically filter available years for selected player
    with col2:
        if player:
            available_years = sorted(pitchers_data[pitchers_data['Name'] == player]['Year'].unique())
            season = st.selectbox(f"Year", [" "] + available_years, key=f"pitcher_{i}_season")
        else:
            season = st.selectbox(f"Year", [" "], key=f"pitcher_{i}_season")
    
    # Select Position for Pitcher
    with col3:
        position = st.selectbox(f"Position", [" "] + positions_pitcher, key=f"pitcher_{i}_position", index=positions_pitcher.index(pitcher['Position']) if pitcher['Position'] in positions_pitcher else 0)

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

    # Display the table using Streamlit's built-in table function
    st.table(hitter_df)

    # Display pitching lineup in a simple table format
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

    # Display the table using Streamlit's built-in table function
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

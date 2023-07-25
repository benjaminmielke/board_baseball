import streamlit as st
import pandas as pd
import math

# Function to calculate Hitter metricspip
def calculate_hitter_metrics(hitter_name, hitter_position, hitter_year, H, Double, Triple, HR, BB_H, SB, AVG):
    hitter_boost = math.floor(float(AVG) * 100)
    hitter_dice_row = math.floor(((int(Double) + int(Triple) + int(HR)) / int(H)) * 10)
    stealing = math.floor((int(SB) / (int(H) + int(BB_H))) * 100)
    if stealing >= 5:
        stealing = "Yes"
    else:
        stealing = "No"

    return f":green[- **{hitter_year} {hitter_name}**[{hitter_position}]]: --- *Hitter Boost* **(:green[{hitter_boost}])**---*Hitter Dice Row* **(:green[{hitter_dice_row}])**---*Stealing* **(:green[{stealing}])**"

# Function to calculate Pitcher metrics
def calculate_pitcher_metrics(pitcher_name, pitcher_position, pitcher_year, ERA, G, IP, SO, BB_P):
    pitcher_decrease = math.floor(float(ERA) * 10) + 10
    pitcher_dice_row = math.floor(int(SO) / int(BB_P))
    endurance = math.ceil(int(IP) / int(G))

    return f":blue[- **{pitcher_year} {pitcher_name}**[{pitcher_position}]]:--- *Pitcher Decrease* **(:blue[{pitcher_decrease}])**---*Pitcher Dice Row* **(:blue[{pitcher_dice_row}])**---*Endurance* **(:blue[{endurance}])**"

# Function to save results to CSV file
def save_to_csv(results, filename):
    df = pd.DataFrame(results, columns=["Results"])
    df.to_csv(filename, index=False)

# Main Streamlit app
def main():

    result = ""
    st.set_page_config(layout="wide")  # Optimize layout for phone screens

    st.title("Board Baseball Calculator")
    
    
    with st.container():
        st.header(f":green[Enter Hitter]")
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([1, 1, 1, 1 , 1, 1, 1, 1, 1, 1])
        with col1:
            hitter_name = st.text_input("**Hitter Name**")
        with col2:
            hitter_position = st.text_input("**Hitter Position**")
        with col3:
            hitter_year = st.text_input("**Hitter Year**")
        with col4:
            H = st.number_input("**H**", value="")
        with col5:
            Double = st.number_input("**2B**", value="")
        with col6:
            Triple = st.number_input("**3B**", value="")
        with col7:
            HR = st.number_input("**HR**", value="")
        with col8:
            BB_H = st.number_input("**Hitter BB**", value="")
        with col9:
            SB = st.number_input("**SB**", value="")
        with col10:
            AVG = st.number_input("**AVG**", value="")
    with st.container():
        col1, col2 = st.columns([1,10])
        with col1:
            if st.button(f":green[Calculate Hitter Metrics]"):
                result = calculate_hitter_metrics(hitter_name, hitter_position, hitter_year, H, Double, Triple, HR, BB_H, SB, AVG)
                with col2:
                    st.write(result)
        

    with st.container():
        st.header(f":blue[Enter Pitcher]")
        col1, col2, col3, col4, col5, col6, col7, col8   = st.columns([ 1, 1, 1, 1 , 1, 1, 1, 1])
        with col1:
            pitcher_name = st.text_input("**Pitcher Name**")
        with col2:
            pitcher_position = st.text_input("**Pitcher Position**")
        with col3:
            pitcher_year = st.text_input("**Pitcher Year**")
        with col4:
            ERA = st.number_input("**ERA**", value="")
        with col5:
            G = st.number_input("**G**", value="")
        with col6:
            IP = st.number_input("**IP**", value="")
        with col7:
            SO = st.number_input("**SO**", value="")
        with col8:
            BB_P = st.number_input("**Pitcher BB**", value="")
    with st.container():
        col1, col2 = st.columns([1,10])
        with col1:
            if st.button(f":blue[Calculate Pitcher Metrics]"):
                result = calculate_pitcher_metrics(pitcher_name, pitcher_position, pitcher_year, ERA, G, IP, SO, BB_P)
                with col2:
                    st.write(result)
        
        

        

        



    st.write("")
    st.write("")
    st.write("")


    # Update the session state with new results
    if result:
        st.session_state.results.append(result)
    if st.session_state.get("results") is None:
        st.session_state.results = []

    # Display the list of results
    with st.container():
        col1, col2 = st.columns([1,10])
        with col1:
            st.write("## Lineup")
        with col2:
            if st.button(f":red[Clear Lineup]"):
                st.session_state.results = []
                st.success("Results cleared successfully!")

            
    all_results = st.session_state.get("results", [])
    for result in all_results:
        st.write(result)
    

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import math
import datetime

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
    pitcher_decrease = -(math.floor(float(ERA) * 10)) + 20
    pitcher_dice_row = math.floor(int(SO) / int(BB_P))
    endurance = math.ceil(int(IP) / int(G))

    return f":blue[- **{pitcher_year} {pitcher_name}**[{pitcher_position}]]:--- *Pitcher Decrease* **(:blue[{pitcher_decrease}])**---*Pitcher Dice Row* **(:blue[{pitcher_dice_row}])**---*Endurance* **(:blue[{endurance}])**"

# Function to save results to CSV file
def save_to_csv(results, filename):
    df = pd.DataFrame(results, columns=["Results"])
    df.to_csv(filename, index=False)

def clear_hitter_text():
        st.session_state["hitter_name_key"] = ""
        #st.session_state["hitter_position_key"] = ""
        #st.session_state["hitter_year_key"] = ""
        st.session_state["H_key"] = ""
        st.session_state["Double_key"] = ""
        st.session_state["Triple_key"] = ""
        st.session_state["HR_key"] = ""
        st.session_state["BB_key"] = ""
        st.session_state["SB_key"] = ""
        st.session_state["AVG_key"] = 0.00

def clear_pitcher_text():
        st.session_state["pitcher_name_key"] = ""
        #st.session_state["hitter_position_key"] = ""
        #st.session_state["hitter_year_key"] = ""
        st.session_state["G_key"] = ""
        st.session_state["IP_key"] = ""
        st.session_state["SO_key"] = ""
        st.session_state["BB_P_key"] = ""
        st.session_state["ERA_key"] = 0.00

# Main Streamlit app
def main():

    result = ""

    st.set_page_config(layout="wide")  # Optimize layout for phone screens
    st.title("Board Baseball Calculator")
    
    
    with st.container():
        st.header(f":green[Enter Hitter]")
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([1, 1, 1, 1 , 1, 1, 1, 1, 1, 1])
        with col1:
            hitter_name = st.text_input("**Hitter Name**", key="hitter_name_key")
        with col2:
            options = ["C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position = st.selectbox("**Hitter Position**", options, key="hitter_position_key")
        with col3:
            options = list(range(1900, datetime.datetime.now().year + 1))
            hitter_year = st.selectbox("**Hitter Year**", options, key="hitter_year_key")
        with col4:
            H = st.text_input("**H**", value="", key="H_key")
        with col5:
            Double = st.text_input("**2B**", value="", key="Double_key")
        with col6:
            Triple = st.text_input("**3B**", value="", key="Triple_key")
        with col7:
            HR = st.text_input("**HR**", value="", key="HR_key")
        with col8:
            BB_H = st.text_input("**Hitter BB**", value="", key="BB_key")
        with col9:
            SB = st.text_input("**SB**", value="", key="SB_key")
        with col10:
            AVG = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key")
    with st.container():
        col0, col1, col2 = st.columns([1,1,10])
        with col0:
            st.button(f":red[Clear Hitter Inputs]", on_click=clear_hitter_text)
        with col1:
            if st.button(f":green[Calculate Hitter Metrics]"):
                result = calculate_hitter_metrics(hitter_name, hitter_position, hitter_year, H, Double, Triple, HR, BB_H, SB, AVG)
                with col2:
                    st.write(result)
        

    with st.container():
        st.header(f":blue[Enter Pitcher]")
        col1, col2, col3, col4, col5, col6, col7, col8   = st.columns([ 1, 1, 1, 1 , 1, 1, 1, 1])
        with col1:
            pitcher_name = st.text_input("**Pitcher Name**", key="pitcher_name_key")
        with col2:
            options = ["SP", "RP", "P"]
            pitcher_position = st.selectbox("**Pitcher Position**", options, key="pitcher_position_key")
        with col3:
            options = list(range(1900, datetime.datetime.now().year + 1))
            pitcher_year = st.selectbox("**Pitcher Year**", options, key="pitcher_year_key")
        with col4:
            G = st.text_input("**G**", value="", key="G_key")
        with col5:
            IP = st.text_input("**IP**", value="", key="IP_key")
        with col6:
            SO = st.text_input("**SO**", value="", key="SO_key")
        with col7:
            BB_P = st.text_input("**Pitcher BB**", value="", key="BB_P_key")
        with col8:
            ERA = st.number_input("**ERA**", min_value=0.00, max_value=10.00, key="ERA_key")
    with st.container():
        col0, col1, col2 = st.columns([1,1,10])
        with col0:
            st.button(f":red[Clear Pitcher Inputs]", on_click=clear_pitcher_text)
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

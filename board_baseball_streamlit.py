import streamlit as st
import pandas as pd
import math
import datetime

# Function to calculate Hitter metricspip
def calculate_hitter_metrics_lineup(order, hitter_position, hitter_name, hitter_year, H, Double, Triple, HR, BB_H, SB, AVG):
    hitter_boost = "+"+str(math.floor(float(AVG) * 100))
    hitter_dice_row = math.floor(((int(Double) + int(Triple) + int(HR)) / int(H)) * 10)
    if hitter_dice_row >= 5:
        hitter_dice_row = "Row 5"
    else:
        hitter_dice_row = "Row " + str(hitter_dice_row)
    stealing = math.floor((int(SB) / (int(H) + int(BB_H))) * 100)
    if stealing >= 5:
        stealing = "Yes"
    else:
        stealing = "No"

    return pd.DataFrame({'Order': str(order), 'Position': hitter_position, 'Player': hitter_name, 'Card Year': hitter_year, 'Hitter Boost/Pitcher Decrease': hitter_boost, 'Hitter/Pitcher Dice Row': hitter_dice_row, 'Stealing/Endurance': stealing}, index=[0])

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
    endurance = math.ceil(float(IP) / int(G))

    return f":blue[- **{pitcher_year} {pitcher_name}**[{pitcher_position}]]:--- *Pitcher Decrease* **(:blue[{pitcher_decrease}])**---*Pitcher Dice Row* **(:blue[{pitcher_dice_row}])**---*Endurance* **(:blue[{endurance}])**"

def calculate_pitcher_metrics_lineup(order, pitcher_position, pitcher_name, pitcher_year, ERA, G, IP, SO, BB_P):
    pitcher_decrease = str(-(math.floor(float(ERA) * 10)) + 20)
    pitcher_dice_row = math.floor(int(SO) / int(BB_P))
    if pitcher_dice_row >= 5:
        pitcher_dice_row = "Row 5"
    else:
        pitcher_dice_row = "Row " + str(pitcher_dice_row)
    endurance = str(math.ceil(float(IP) / int(G))) + " Innings"

    return pd.DataFrame({'Order': str(order), 'Position': pitcher_position, 'Player': pitcher_name, 'Card Year': pitcher_year, 'Hitter Boost/Pitcher Decrease': pitcher_decrease, 'Hitter/Pitcher Dice Row': pitcher_dice_row, 'Stealing/Endurance': endurance}, index=[0])

# Function to save results to CSV file
def save_to_csv(results, filename):
    df = pd.DataFrame(results, columns=["Results"])
    df.to_csv(filename, index=False)

def clear_hitter_text():
    st.session_state[f"hitter_name_key"] = " "
    st.session_state[f"hitter_position_key"] = ""
    st.session_state[f"hitter_year_key"] = " "
def clear_hitter_1():
    st.session_state[f"hitter_name_key1"] = " "
    st.session_state[f"hitter_position_key1"] = ""
    st.session_state[f"hitter_year_key1"] = " "
def clear_hitter_2():
    st.session_state[f"hitter_name_key2"] = " "
    st.session_state[f"hitter_position_key2"] = ""
    st.session_state[f"hitter_year_key2"] = " "
def clear_hitter_3():
    st.session_state[f"hitter_name_key3"] = " "
    st.session_state[f"hitter_position_key3"] = ""
    st.session_state[f"hitter_year_key3"] = " "
def clear_hitter_4():
    st.session_state[f"hitter_name_key4"] = " "
    st.session_state[f"hitter_position_key4"] = ""
    st.session_state[f"hitter_year_key4"] = " "
def clear_hitter_5():
    st.session_state[f"hitter_name_key5"] = " "
    st.session_state[f"hitter_position_key5"] = ""
    st.session_state[f"hitter_year_key5"] = " "
def clear_hitter_6():
    st.session_state[f"hitter_name_key6"] = " "
    st.session_state[f"hitter_position_key6"] = ""
    st.session_state[f"hitter_year_key6"] = " "
def clear_hitter_7():
    st.session_state[f"hitter_name_key7"] = " "
    st.session_state[f"hitter_position_key7"] = ""
    st.session_state[f"hitter_year_key7"] = " "
def clear_hitter_8():
    st.session_state[f"hitter_name_key8"] = " "
    st.session_state[f"hitter_position_key8"] = ""
    st.session_state[f"hitter_year_key8"] = " "
def clear_hitter_9():
    st.session_state[f"hitter_name_key9"] = " "
    st.session_state[f"hitter_position_key9"] = ""
    st.session_state[f"hitter_year_key9"] = " "

def clear_pitcher_text():
    st.session_state["pitcher_name_key"] = " "
    st.session_state["pitcher_position_key"] = ""
    st.session_state["pitcher_year_key"] = " "
def clear_pitcher_1():
    st.session_state[f"pitcher_name_key1"] = " "
    st.session_state[f"pitcher_year_key1"] = " "
def clear_pitcher_2():
    st.session_state[f"hpitcher_name_key2"] = " "
    st.session_state[f"pitcher_year_key2"] = " "
def clear_pitcher_3():
    st.session_state[f"pitcher_name_key3"] = " "
    st.session_state[f"pitcher_year_key3"] = " "
def clear_pitcher_4():
    st.session_state[f"pitcher_name_key4"] = " "
    st.session_state[f"pitcher_year_key4"] = " "
def clear_pitcher_5():
    st.session_state[f"pitcher_name_key5"] = " "
    st.session_state[f"pitcher_year_key5"] = " "

def read_pitcher_csv():
    df = pd.read_csv("pitchers_stats.csv") 
    pitcher_names = df["Name"].unique().tolist()
    pitcher_years = df["Year"].unique().tolist()
    return pitcher_names, pitcher_years

def read_hitter_csv():
    df = pd.read_csv("hitters_stats.csv")  
    hitter_names = df["Name"].unique().tolist()
    hitter_years = df["Year"].unique().tolist()
    return hitter_names, hitter_years

def get_hitter_stats(hitter_name, hitter_year):
    df = pd.read_csv("hitters_stats.csv")  
    stats = df[(df["Name"] == hitter_name) & (df["Year"] == hitter_year)].iloc[0]
    return stats

def get_pitcher_stats(pitcher_name, pitcher_year):
    df = pd.read_csv("pitchers_stats.csv")  
    stats = df[(df["Name"] == pitcher_name) & (df["Year"] == pitcher_year)].iloc[0]
    return stats

# Function to populate hitter input values based on the selected name and year
def populate_hitter_input_values(hitter_name, hitter_year, key):
    if hitter_name and hitter_year:
        if key == 100:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key"] = str(stats["H"])
            st.session_state["Double_key"] = str(stats["2B"])
            st.session_state["Triple_key"] = str(stats["3B"])
            st.session_state["HR_key"] = str(stats["HR"])
            st.session_state["BB_key"] = str(stats["BB"])
            st.session_state["SB_key"] = str(stats["SB"])
            st.session_state["AVG_key"] = stats["BA"]
        if key == 0:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key"] = str(stats["H"])
            st.session_state["Double_key"] = str(stats["2B"])
            st.session_state["Triple_key"] = str(stats["3B"])
            st.session_state["HR_key"] = str(stats["HR"])
            st.session_state["BB_key"] = str(stats["BB"])
            st.session_state["SB_key"] = str(stats["SB"])
            st.session_state["AVG_key"] = stats["BA"]
        if key == 1:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key1"] = str(stats["H"])
            st.session_state["Double_key1"] = str(stats["2B"])
            st.session_state["Triple_key1"] = str(stats["3B"])
            st.session_state["HR_key1"] = str(stats["HR"])
            st.session_state["BB_key1"] = str(stats["BB"])
            st.session_state["SB_key1"] = str(stats["SB"])
            st.session_state["AVG_key1"] = stats["BA"]
        if key == 2:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key2"] = str(stats["H"])
            st.session_state["Double_key2"] = str(stats["2B"])
            st.session_state["Triple_key2"] = str(stats["3B"])
            st.session_state["HR_key2"] = str(stats["HR"])
            st.session_state["BB_key2"] = str(stats["BB"])
            st.session_state["SB_key2"] = str(stats["SB"])
            st.session_state["AVG_key2"] = stats["BA"]
        if key == 3:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key3"] = str(stats["H"])
            st.session_state["Double_key3"] = str(stats["2B"])
            st.session_state["Triple_key3"] = str(stats["3B"])
            st.session_state["HR_key3"] = str(stats["HR"])
            st.session_state["BB_key3"] = str(stats["BB"])
            st.session_state["SB_key3"] = str(stats["SB"])
            st.session_state["AVG_key3"] = stats["BA"]
        if key == 4:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key4"] = str(stats["H"])
            st.session_state["Double_key4"] = str(stats["2B"])
            st.session_state["Triple_key4"] = str(stats["3B"])
            st.session_state["HR_key4"] = str(stats["HR"])
            st.session_state["BB_key4"] = str(stats["BB"])
            st.session_state["SB_key4"] = str(stats["SB"])
            st.session_state["AVG_key4"] = stats["BA"]
        if key == 5:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key5"] = str(stats["H"])
            st.session_state["Double_key5"] = str(stats["2B"])
            st.session_state["Triple_key5"] = str(stats["3B"])
            st.session_state["HR_key5"] = str(stats["HR"])
            st.session_state["BB_key5"] = str(stats["BB"])
            st.session_state["SB_key5"] = str(stats["SB"])
            st.session_state["AVG_key5"] = stats["BA"]
        if key == 6:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key6"] = str(stats["H"])
            st.session_state["Double_key6"] = str(stats["2B"])
            st.session_state["Triple_key6"] = str(stats["3B"])
            st.session_state["HR_key6"] = str(stats["HR"])
            st.session_state["BB_key6"] = str(stats["BB"])
            st.session_state["SB_key6"] = str(stats["SB"])
            st.session_state["AVG_key6"] = stats["BA"]
        if key == 7:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key7"] = str(stats["H"])
            st.session_state["Double_key7"] = str(stats["2B"])
            st.session_state["Triple_key7"] = str(stats["3B"])
            st.session_state["HR_key7"] = str(stats["HR"])
            st.session_state["BB_key7"] = str(stats["BB"])
            st.session_state["SB_key7"] = str(stats["SB"])
            st.session_state["AVG_key7"] = stats["BA"]
        if key == 8:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key8"] = str(stats["H"])
            st.session_state["Double_key8"] = str(stats["2B"])
            st.session_state["Triple_key8"] = str(stats["3B"])
            st.session_state["HR_key8"] = str(stats["HR"])
            st.session_state["BB_key8"] = str(stats["BB"])
            st.session_state["SB_key8"] = str(stats["SB"])
            st.session_state["AVG_key8"] = stats["BA"]
        if key == 9:
            stats = get_hitter_stats(hitter_name, hitter_year)
            st.session_state["H_key9"] = str(stats["H"])
            st.session_state["Double_key9"] = str(stats["2B"])
            st.session_state["Triple_key9"] = str(stats["3B"])
            st.session_state["HR_key9"] = str(stats["HR"])
            st.session_state["BB_key9"] = str(stats["BB"])
            st.session_state["SB_key9"] = str(stats["SB"])
            st.session_state["AVG_key9"] = stats["BA"]


# Function to populate hitter input values based on the selected name and year
def populate_pitcher_input_values(pitcher_name, pitcher_year, key):
    if pitcher_name and pitcher_year:
        if key == 100:
            stats = get_pitcher_stats(" ", " ")
            st.session_state["G_key"] = str(stats["G"])
            st.session_state["IP_key"] (stats["IP"])
            st.session_state["SO_key"] = str(stats["SO"])
            st.session_state["BB_P_key"] = str(stats["BB"])
            st.session_state["ERA_key"] = stats["ERA"]
        if key == 0:
            stats = get_pitcher_stats(pitcher_name, pitcher_year)
            st.session_state["G_key"] = str(stats["G"])
            st.session_state["IP_key"] = (stats["IP"])
            st.session_state["SO_key"] = str(stats["SO"])
            st.session_state["BB_P_key"] = str(stats["BB"])
            st.session_state["ERA_key"] = (stats["ERA"])
        if key == 1:
            stats = get_pitcher_stats(pitcher_name, pitcher_year)
            st.session_state["G_key1"] = str(stats["G"])
            st.session_state["IP_key1"] = (stats["IP"])
            st.session_state["SO_key1"] = str(stats["SO"])
            st.session_state["BB_P_key1"] = str(stats["BB"])
            st.session_state["ERA_key1"] = (stats["ERA"])
        if key == 2:
            stats = get_pitcher_stats(pitcher_name, pitcher_year)
            st.session_state["G_key2"] = str(stats["G"])
            st.session_state["IP_key2"] = (stats["IP"])
            st.session_state["SO_key2"] = str(stats["SO"])
            st.session_state["BB_P_key2"] = str(stats["BB"])
            st.session_state["ERA_key2"] = (stats["ERA"])
        if key == 3:
            stats = get_pitcher_stats(pitcher_name, pitcher_year)
            st.session_state["G_key3"] = str(stats["G"])
            st.session_state["IP_key3"] = (stats["IP"])
            st.session_state["SO_key3"] = str(stats["SO"])
            st.session_state["BB_P_key3"] = str(stats["BB"])
            st.session_state["ERA_key3"] = (stats["ERA"])
        if key == 4:
            stats = get_pitcher_stats(pitcher_name, pitcher_year)
            st.session_state["G_key4"] = str(stats["G"])
            st.session_state["IP_key4"] = (stats["IP"])
            st.session_state["SO_key4"] = str(stats["SO"])
            st.session_state["BB_P_key4"] = str(stats["BB"])
            st.session_state["ERA_key4"] = (stats["ERA"])
        if key == 5:
            stats = get_pitcher_stats(pitcher_name, pitcher_year)
            st.session_state["G_key5"] = str(stats["G"])
            st.session_state["IP_key5"] = (stats["IP"])
            st.session_state["SO_key5"] = str(stats["SO"])
            st.session_state["BB_P_key5"] = str(stats["BB"])
            st.session_state["ERA_key5"] = (stats["ERA"])
        


# Main Streamlit app
def main():

    result = ""

    st.set_page_config(layout="wide")  # Optimize layout for phone screens
    st.title("Board Baseball Calculator")
    
    # Read the CSV file and extract pitcher_name and pitcher_year options
    pitcher_names, pitcher_years = read_pitcher_csv()
    hitter_names, hitter_years = read_hitter_csv()
    


        
   ##-------1------------
    with st.container():
        st.header(f":orange[Create Whole Lineup]")
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write(f"## :green[1]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_1, key='xh1')
        with col1:
            hitter_name_1 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key1")
        with col2:
            hitter_year_1 = st.selectbox(":green[**Hitter Year**]", hitter_years, key="hitter_year_key1")
        with col3:
            options = ["", "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_1 = st.selectbox(":green[**Hitter Position**]", options, key="hitter_position_key1")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_1, hitter_year_1, 1)
        with col4:
            H_1 = st.text_input("**H**", value="", key="H_key1")
        with col5:
            Double_1 = st.text_input("**2B**", value="", key="Double_key1")
        with col6:
            Triple_1 = st.text_input("**3B**", value="", key="Triple_key1")
        with col7:
            HR_1 = st.text_input("**HR**", value="", key="HR_key1")
        with col8:
            BB_H_1 = st.text_input("**Hitter BB**", value="", key="BB_key1")
        with col9:
            SB_1 = st.text_input("**SB**", value="", key="SB_key1")
        with col10:
            AVG_1 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key1")

    ##------2------------
    with st.container():
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write("## :green[2]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_2, key='xh2')
        with col1:
            hitter_name_2 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key2")
        with col2:
            hitter_year_2 = st.selectbox(f":green[**Hitter Year**]", hitter_years, key="hitter_year_key2")
        with col3:
            options = ['', "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_2 = st.selectbox(f":green[**Hitter Position**]", options, key="hitter_position_key2")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_2, hitter_year_2, 2)
        with col4:
            H_2 = st.text_input("**H**", value="", key="H_key2")
        with col5:
            Double_2 = st.text_input("**2B**", value="", key="Double_key2")
        with col6:
            Triple_2 = st.text_input("**3B**", value="", key="Triple_key2")
        with col7:
            HR_2 = st.text_input("**HR**", value="", key="HR_key2")
        with col8:
            BB_H_2 = st.text_input("**Hitter BB**", value="", key="BB_key2")
        with col9:
            SB_2 = st.text_input("**SB**", value="", key="SB_key2")
        with col10:
            AVG_2 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key2")

    ##-------3------------
    with st.container():
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write("## :green[1]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_3, key='xh3')
        with col1:
            hitter_name_3 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key3")
        with col2:
            hitter_year_3 = st.selectbox(f":green[**Hitter Year**]", hitter_years, key="hitter_year_key3")
        with col3:
            options = ['', "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_3 = st.selectbox(f":green[**Hitter Position**]", options, key="hitter_position_key3")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_3, hitter_year_3, 3)
        with col4:
            H_3 = st.text_input("**H**", value="", key="H_key3")
        with col5:
            Double_3 = st.text_input("**2B**", value="", key="Double_key3")
        with col6:
            Triple_3 = st.text_input("**3B**", value="", key="Triple_key3")
        with col7:
            HR_3 = st.text_input("**HR**", value="", key="HR_key3")
        with col8:
            BB_H_3 = st.text_input("**Hitter BB**", value="", key="BB_key3")
        with col9:
            SB_3 = st.text_input("**SB**", value="", key="SB_key3")
        with col10:
            AVG_3 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key3")

    ##-------4------------
    with st.container():
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write("## :green[4]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_4, key='xh4')
        with col1:
            hitter_name_4 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key4")
        with col2:
            hitter_year_4 = st.selectbox(f":green[**Hitter Year**]", hitter_years, key="hitter_year_key4")
        with col3:
            options = ['', "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_4 = st.selectbox(f":green[**Hitter Position**]", options, key="hitter_position_key4")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_4, hitter_year_4, 4)
        with col4:
            H_4 = st.text_input("**H**", value="", key="H_key4")
        with col5:
            Double_4 = st.text_input("**2B**", value="", key="Double_key4")
        with col6:
            Triple_4 = st.text_input("**3B**", value="", key="Triple_key4")
        with col7:
            HR_4 = st.text_input("**HR**", value="", key="HR_key4")
        with col8:
            BB_H_4 = st.text_input("**Hitter BB**", value="", key="BB_key4")
        with col9:
            SB_4 = st.text_input("**SB**", value="", key="SB_key4")
        with col10:
            AVG_4 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key4")

    ##-------5------------
    with st.container():
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write("## :green[5]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_5, key='xh5')
        with col1:
            hitter_name_5 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key5")
        with col2:
            hitter_year_5 = st.selectbox(f":green[**Hitter Year**]", hitter_years, key="hitter_year_key5")
        with col3:
            options = ['', "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_5 = st.selectbox(f":green[**Hitter Position**]", options, key="hitter_position_key5")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_5, hitter_year_5, 5)
        with col4:
            H_5 = st.text_input("**H**", value="", key="H_key5")
        with col5:
            Double_5 = st.text_input("**2B**", value="", key="Double_key5")
        with col6:
            Triple_5 = st.text_input("**3B**", value="", key="Triple_key5")
        with col7:
            HR_5 = st.text_input("**HR**", value="", key="HR_key5")
        with col8:
            BB_H_5 = st.text_input("**Hitter BB**", value="", key="BB_key5")
        with col9:
            SB_5 = st.text_input("**SB**", value="", key="SB_key5")
        with col10:
            AVG_5 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key5")

    ##-------6------------
    with st.container():
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write("## :green[6]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_6, key='xh6')
        with col1:
            hitter_name_6 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key6")
        with col2:
            hitter_year_6 = st.selectbox(f":green[**Hitter Year**]", hitter_years, key="hitter_year_key6")
        with col3:
            options = ['', "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_6 = st.selectbox(f":green[**Hitter Position**]", options, key="hitter_position_key6")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_6, hitter_year_6, 6)
        with col4:
            H_6 = st.text_input("**H**", value="", key="H_key6")
        with col5:
            Double_6 = st.text_input("**2B**", value="", key="Double_key6")
        with col6:
            Triple_6 = st.text_input("**3B**", value="", key="Triple_key6")
        with col7:
            HR_6 = st.text_input("**HR**", value="", key="HR_key6")
        with col8:
            BB_H_6 = st.text_input("**Hitter BB**", value="", key="BB_key6")
        with col9:
            SB_6 = st.text_input("**SB**", value="", key="SB_key6")
        with col10:
            AVG_6 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key6")

    ##-------7------------
    with st.container():
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write("## :green[7]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_7, key='xh7')
        with col1:
            hitter_name_7 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key7")
        with col2:
            hitter_year_7 = st.selectbox(f":green[**Hitter Year**]", hitter_years, key="hitter_year_key7")
        with col3:
            options = ['', "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_7 = st.selectbox(f":green[**Hitter Position**]", options, key="hitter_position_key7")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_7, hitter_year_7, 7)
        with col4:
            H_7 = st.text_input("**H**", value="", key="H_key7")
        with col5:
            Double_7 = st.text_input("**2B**", value="", key="Double_key7")
        with col6:
            Triple_7 = st.text_input("**3B**", value="", key="Triple_key7")
        with col7:
            HR_7 = st.text_input("**HR**", value="", key="HR_key7")
        with col8:
            BB_H_7 = st.text_input("**Hitter BB**", value="", key="BB_key7")
        with col9:
            SB_7 = st.text_input("**SB**", value="", key="SB_key7")
        with col10:
            AVG_7 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key7")

    ##-------8------------
    with st.container():
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write("## :green[8]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_8, key='xh8')
        with col1:
            hitter_name_8 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key8")
        with col2:
            hitter_year_8 = st.selectbox(f":green[**Hitter Year**]", hitter_years, key="hitter_year_key8")
        with col3:
            options = ['', "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_8 = st.selectbox(f":green[**Hitter Position**]", options, key="hitter_position_key8")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_8, hitter_year_8, 8)
        with col4:
            H_8 = st.text_input("**H**", value="", key="H_key8")
        with col5:
            Double_8 = st.text_input("**2B**", value="", key="Double_key8")
        with col6:
            Triple_8 = st.text_input("**3B**", value="", key="Triple_key8")
        with col7:
            HR_8 = st.text_input("**HR**", value="", key="HR_key8")
        with col8:
            BB_H_8 = st.text_input("**Hitter BB**", value="", key="BB_key8")
        with col9:
            SB_8 = st.text_input("**SB**", value="", key="SB_key8")
        with col10:
            AVG_8 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key8")

    ##-------9------------
    with st.container():
        col0,colb1,col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns([.25, .3, 2, 1.2, 1.2, 1 , 1, 1, 1, 1, 1, 1])
        with col0:
            st.write("## :green[9]")
        with colb1:
            st.button(f":red[X]", on_click=clear_hitter_9, key='xh9')
        with col1:
            hitter_name_9 = st.selectbox(f":green[**Hitter Name**]", hitter_names, key="hitter_name_key9")
        with col2:
            hitter_year_9 = st.selectbox(f":green[**Hitter Year**]", hitter_years, key="hitter_year_key9")
        with col3:
            options = ['', "C", "1B", "2B", "3B", "SS", "OF", "DH"]
            hitter_position_9 = st.selectbox(f":green[**Hitter Position**]", options, key="hitter_position_key9")
        # Populate the hitter input fields when the user selects a name and year
        populate_hitter_input_values(hitter_name_9, hitter_year_9, 9)
        with col4:
            H_9 = st.text_input("**H**", value="", key="H_key9")
        with col5:
            Double_9 = st.text_input("**2B**", value="", key="Double_key9")
        with col6:
            Triple_9 = st.text_input("**3B**", value="", key="Triple_key9")
        with col7:
            HR_9 = st.text_input("**HR**", value="", key="HR_key9")
        with col8:
            BB_H_9 = st.text_input("**Hitter BB**", value="", key="BB_key9")
        with col9:
            SB_9 = st.text_input("**SB**", value="", key="SB_key9")
        with col10:
            AVG_9 = st.number_input("**AVG**", min_value=.000, max_value=.500, key="AVG_key9")

    ##-----SP-------------
    with st.container():
        col0, colb1, col1, col2, col3, col4, col5, col6, col7, col8   = st.columns([ .25,.2, 1.4, .9, .9, 1 , 1, 1, 1, 1])
        with col0:
            st.write("## :blue[SP]")
        with colb1:
            st.button(f":red[X]", on_click=clear_pitcher_1, key='xp1')
        with col1:
            pitcher_name_1 = st.selectbox(f":blue[**Pitcher Name**]", pitcher_names, key="pitcher_name_key1")
        with col2:
            pitcher_year_1 = st.selectbox(f":blue[**Pitcher Year**]", pitcher_years, key="pitcher_year_key1")
        with col3:
            options = ["SP"]
            pitcher_position_1 = st.selectbox(f":blue[**Pitcher Position**]", options, key="pitcher_position_key1")
        # Populate the hitter input fields when the user selects a name and year
        populate_pitcher_input_values(pitcher_name_1, pitcher_year_1, 1)
        with col4:
            G_1 = st.text_input("**G**", value="", key="G_key1")
        with col5:
            IP_1 = st.text_input("**IP**", value="", key="IP_key1")
        with col6:
            SO_1 = st.text_input("**SO**", value="", key="SO_key1")
        with col7:
            BB_P_1 = st.text_input("**Pitcher BB**", value="", key="BB_P_key1")
        with col8:
            ERA_1 = st.number_input("**ERA**", min_value=0.00, max_value=10.00, key="ERA_key1")

    ##-----P2-------------
    with st.container():
        col0, colb1, col1, col2, col3, col4, col5, col6, col7, col8   = st.columns([ .25,.2, 1.4, .9, .9, 1 , 1, 1, 1, 1])
        with col0:
            st.write("## :blue[P]")
        with colb1:
            st.button(f":red[X]", on_click=clear_pitcher_2, key='xp2')
        with col1:
            pitcher_name_2 = st.selectbox(f":blue[**Pitcher Name**]", pitcher_names, key="pitcher_name_key2")
        with col2:
            pitcher_year_2 = st.selectbox(f":blue[**Pitcher Year**]", pitcher_years, key="pitcher_year_key2")
        with col3:
            options = ["P"]
            pitcher_position_2 = st.selectbox(f":blue[**Pitcher Position**]", options, key="pitcher_position_key2")
        # Populate the hitter input fields when the user selects a name and year
        populate_pitcher_input_values(pitcher_name_2, pitcher_year_2, 2)
        with col4:
            G_2 = st.text_input("**G**", value="", key="G_key2")
        with col5:
            IP_2 = st.text_input("**IP**", value="", key="IP_key2")
        with col6:
            SO_2 = st.text_input("**SO**", value="", key="SO_key2")
        with col7:
            BB_P_2 = st.text_input("**Pitcher BB**", value="", key="BB_P_key2")
        with col8:
            ERA_2 = st.number_input("**ERA**", min_value=0.00, max_value=10.00, key="ERA_key2")

    ##-----P3-------------
    with st.container():
        col0, colb1, col1, col2, col3, col4, col5, col6, col7, col8   = st.columns([ .25,.2, 1.4, .9, .9, 1 , 1, 1, 1, 1])
        with col0:
            st.write("## :blue[P]")
        with colb1:
            st.button(f":red[X]", on_click=clear_pitcher_3, key='xp3')
        with col1:
            pitcher_name_3 = st.selectbox(f":blue[**Pitcher Name**]", pitcher_names, key="pitcher_name_key3")
        with col2:
            pitcher_year_3 = st.selectbox(f":blue[**Pitcher Year**]", pitcher_years, key="pitcher_year_key3")
        with col3:
            options = ["P"]
            pitcher_position_3 = st.selectbox(f":blue[**Pitcher Position**]", options, key="pitcher_position_key3")
        # Populate the hitter input fields when the user selects a name and year
        populate_pitcher_input_values(pitcher_name_3, pitcher_year_3, 3)
        with col4:
            G_3 = st.text_input("**G**", value="", key="G_key3")
        with col5:
            IP_3 = st.text_input("**IP**", value="", key="IP_key3")
        with col6:
            SO_3 = st.text_input("**SO**", value="", key="SO_key3")
        with col7:
            BB_P_3 = st.text_input("**Pitcher BB**", value="", key="BB_P_key3")
        with col8:
            ERA_3 = st.number_input("**ERA**", min_value=0.00, max_value=10.00, key="ERA_key3")


    ##-----P4-------------
    with st.container():
        col0, colb1, col1, col2, col3, col4, col5, col6, col7, col8   = st.columns([ .25,.2, 1.4, .9, .9, 1 , 1, 1, 1, 1])
        with col0:
            st.write("## :blue[SP]")
        with colb1:
            st.button(f":red[X]", on_click=clear_pitcher_4, key='xp4')
        with col1:
            pitcher_name_4 = st.selectbox(f":blue[**Pitcher Name**]", pitcher_names, key="pitcher_name_key4")
        with col2:
            pitcher_year_4 = st.selectbox(f":blue[**Pitcher Year**]", pitcher_years, key="pitcher_year_key4")
        with col3:
            options = ["P"]
            pitcher_position_4 = st.selectbox(f":blue[**Pitcher Position**]", options, key="pitcher_position_key4")
        # Populate the hitter input fields when the user selects a name and year
        populate_pitcher_input_values(pitcher_name_4, pitcher_year_4, 4)
        with col4:
            G_4 = st.text_input("**G**", value="", key="G_key4")
        with col5:
            IP_4 = st.text_input("**IP**", value="", key="IP_key4")
        with col6:
            SO_4 = st.text_input("**SO**", value="", key="SO_key4")
        with col7:
            BB_P_4 = st.text_input("**Pitcher BB**", value="", key="BB_P_key4")
        with col8:
            ERA_4 = st.number_input("**ERA**", min_value=0.00, max_value=10.00, key="ERA_key4")

     ##-----P5-------------
    with st.container():
        col0, colb1, col1, col2, col3, col4, col5, col6, col7, col8   = st.columns([ .25,.2, 1.4, .9, .9, 1 , 1, 1, 1, 1])
        with col0:
            st.write("## :blue[P]")
        with colb1:
            st.button(f":red[X]", on_click=clear_pitcher_5, key='xp5')
        with col1:
            pitcher_name_5 = st.selectbox(f":blue[**Pitcher Name**]", pitcher_names, key="pitcher_name_key5")
        with col2:
            pitcher_year_5 = st.selectbox(f":blue[**Pitcher Year**]", pitcher_years, key="pitcher_year_key5")
        with col3:
            options = ["P"]
            pitcher_position_5 = st.selectbox(f":blue[**Pitcher Position**]", options, key="pitcher_position_key5")
        # Populate the hitter input fields when the user selects a name and year
        populate_pitcher_input_values(pitcher_name_5, pitcher_year_5, 5)
        with col4:
            G_5 = st.text_input("**G**", value="", key="G_key5")
        with col5:
            IP_5 = st.text_input("**IP**", value="", key="IP_key5")
        with col6:
            SO_5 = st.text_input("**SO**", value="", key="SO_key5")
        with col7:
            BB_P_5 = st.text_input("**Pitcher BB**", value="", key="BB_P_key5")
        with col8:
            ERA_5 = st.number_input("**ERA**", min_value=0.00, max_value=10.00, key="ERA_key5")

    if st.button("Create Lineup!!"):
        
        df_lineup = pd.concat([
        calculate_hitter_metrics_lineup(1, hitter_position_1, hitter_name_1, hitter_year_1, H_1, Double_1, Triple_1, HR_1, BB_H_1, SB_1, AVG_1),
        calculate_hitter_metrics_lineup(2, hitter_position_2, hitter_name_2, hitter_year_2, H_2, Double_2, Triple_2, HR_2, BB_H_2, SB_2, AVG_2),
        calculate_hitter_metrics_lineup(3, hitter_position_3, hitter_name_3, hitter_year_3, H_2, Double_3, Triple_3, HR_3, BB_H_3, SB_3, AVG_3),
        calculate_hitter_metrics_lineup(4, hitter_position_4, hitter_name_4, hitter_year_4, H_2, Double_4, Triple_4, HR_4, BB_H_4, SB_4, AVG_4),
        calculate_hitter_metrics_lineup(5, hitter_position_5, hitter_name_5, hitter_year_5, H_2, Double_5, Triple_5, HR_5, BB_H_5, SB_5, AVG_5),
        calculate_hitter_metrics_lineup(6, hitter_position_6, hitter_name_6, hitter_year_6, H_2, Double_6, Triple_6, HR_6, BB_H_6, SB_6, AVG_6),
        calculate_hitter_metrics_lineup(7, hitter_position_7, hitter_name_7, hitter_year_7, H_2, Double_7, Triple_7, HR_7, BB_H_7, SB_7, AVG_7),
        calculate_hitter_metrics_lineup(8, hitter_position_8, hitter_name_8, hitter_year_8, H_2, Double_8, Triple_8, HR_8, BB_H_8, SB_8, AVG_8),
        calculate_hitter_metrics_lineup(9, hitter_position_9, hitter_name_9, hitter_year_9, H_2, Double_9, Triple_9, HR_9, BB_H_9, SB_9, AVG_9),
        calculate_pitcher_metrics_lineup("P1", pitcher_position_1, pitcher_name_1, pitcher_year_1, ERA_1, G_1, IP_1, SO_1, BB_P_1),
        calculate_pitcher_metrics_lineup("P2", pitcher_position_2, pitcher_name_2, pitcher_year_2, ERA_2, G_2, IP_2, SO_2, BB_P_2),
        calculate_pitcher_metrics_lineup("P3", pitcher_position_3, pitcher_name_3, pitcher_year_3, ERA_3, G_3, IP_3, SO_3, BB_P_3),
        calculate_pitcher_metrics_lineup("P4", pitcher_position_4, pitcher_name_4, pitcher_year_4, ERA_4, G_4, IP_4, SO_4, BB_P_4),
        calculate_pitcher_metrics_lineup("P5", pitcher_position_5, pitcher_name_5, pitcher_year_5, ERA_5, G_5, IP_5, SO_5, BB_P_5)

        ])
        df_lineup.set_index("Order", inplace=True)

        st.dataframe(df_lineup.style.set_properties(**{'background-color': 'black',
                           'color': 'lawngreen',
                           'border-color': 'white'}))
        csv = df_lineup.to_csv(index=False).encode('utf-8')
        st.download_button(
        "Download Lineup to File!!!",
        csv,
        "lineup.csv",
        "text/csv",
        key='download-csv'
        )

    

    st.write("")
    st.write("")
    st.write("")


    # Update the session state with new results
    if result:
        st.session_state.results.append(result)
    if st.session_state.get("results") is None:
        st.session_state.results = []

            
    all_results = st.session_state.get("results", [])
    for result in all_results:
        st.write(result)

if __name__ == "__main__":
    main()

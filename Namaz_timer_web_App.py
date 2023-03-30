import requests
import streamlit as st
from datetime import datetime, timedelta

def get_prayer_time_data(namaz, latitude, longitude, date):
    url = f"http://api.aladhan.com/v1/timings/{date}?latitude={latitude}&longitude={longitude}&method=2"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        timings = data['data']['timings']
        return timings[namaz.capitalize()]
    else:
        return None

def main():
    st.set_page_config(page_title="Namaz Timings", page_icon=":pray:", layout="wide")
    st.title("Namaz Timings")

    # Get user inputs
    namaz = st.selectbox("Select Namaz", ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"])
    print(namaz)
    location = st.text_input("Enter Location (City, Country)", "Karachi, Pakistan")
    date = st.date_input("Select Date", datetime.now())

    # Get latitude and longitude from location
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
        response = requests.get(url)
        data = response.json()[0]
        latitude = data["lat"]
        longitude = data["lon"]
    except:
        st.write("Error: Could not find location. Please enter a valid location.")
        return

    # Get prayer time data
    prayer_time = get_prayer_time_data(namaz.lower(), latitude, longitude, date.strftime("%Y-%m-%d"))
    if prayer_time is None:
        st.write("Error: Could not get prayer time data. Please try again later.")
        return

    # Display prayer time data
    st.write(f"Location: {location.title()}")
    st.write(f"Date: {date.strftime('%Y-%m-%d')}")
    st.write(f"{namaz.title()} Time: {prayer_time}")
    
    # Add colors to the interface
    st.markdown("""
        <style>
            body {
                color: #212121;
                background-color: #fafafa;
            }
            .stButton button {
                background-color: #2196f3;
                border: 2px solid #2196f3;
                border-radius: 5px;
                color: #ffffff;
                font-weight: bold;
            }
            .stTextInput input {
                border: 2px solid #2196f3;
                border-radius: 5px;
                padding: 8px;
            }
            .stSelectbox select {
                border: 2px solid #2196f3;
                border-radius: 5px;
                padding: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

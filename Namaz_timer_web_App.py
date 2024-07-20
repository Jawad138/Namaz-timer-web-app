import requests
import streamlit as st
from datetime import datetime

OPENCAGE_API_KEY = "79c3a88590d74a01ac579a0dc13e4d08"

def get_prayer_time_data(namaz, latitude, longitude, date):
    url = f"http://api.aladhan.com/v1/timings/{date}?latitude={latitude}&longitude={longitude}&method=2"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        timings = data['data']['timings']
        return timings[namaz.capitalize()]
    else:
        return None

def get_coordinates(city, country):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city},{country}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()['results']
        if results:
            location = results[0]['geometry']
            return location['lat'], location['lng']
    return None, None

def main():
    st.set_page_config(page_title="Namaz Timings", page_icon=":pray:", layout="wide")
    st.title("Namaz Timings")

    namaz = st.selectbox("Select Namaz", ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"])
    
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("Enter City", "Lahore")
    with col2:
        country = st.text_input("Enter Country", "Pakistan")
    
    date = st.date_input("Select Date", datetime.now())

    if st.button("Get Prayer Time"):
        latitude, longitude = get_coordinates(city, country)
        
        if latitude is None or longitude is None:
            st.error(f"Could not find coordinates for {city}, {country}. Please check the spelling and try again.")
        else:
            prayer_time = get_prayer_time_data(namaz.lower(), latitude, longitude, date.strftime("%Y-%m-%d"))
            
            if prayer_time is None:
                st.error("Error: Could not get prayer time data. Please try again later.")
            else:
                st.success(f"Location: {city}, {country}")
                st.success(f"Coordinates: {latitude:.4f}, {longitude:.4f}")
                st.success(f"Date: {date.strftime('%Y-%m-%d')}")
                st.success(f"{namaz.title()} Time: {prayer_time}")

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

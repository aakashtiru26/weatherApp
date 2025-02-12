import requests
import pandas as pd
import streamlit as st

st.title('A Seven-Day Weather Forecast App')

# API key
key = "9fc0683698a9450faa051106afb89aa2"  # Your Weatherbit API key

@st.cache_resource
def weather_forecast(city, state, country, api_key):
    base_url = "https://api.weatherbit.io/v2.0/forecast/daily"
    params = {
        'city': city,
        'state': state,
        'country': country,
        'key': api_key,
        'days': 7  # Number of days for the forecast
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        st.error("Failed to fetch data. Check your inputs.")
        return None

left, right = st.columns(2)
city = left.text_input('Enter City')
state = right.text_input('Enter State (optional)')
country = st.text_input('Enter Country')
op = st.selectbox('Select Display Format', ['DataFrame', 'BarChart', 'LineChart'])

# Fetch forecast data on button click
if st.button('Fetch'):
    forecast = weather_forecast(city, state, country, key)
    if forecast:
        dates = []
        temps = []
        precips = []
        weather_desc = []
        wind_speeds = []

        for day in forecast:
            dates.append(day['datetime'])
            temps.append(day['temp'])
            precips.append(day['precip'])
            weather_desc.append(day['weather']['description'])
            wind_speeds.append(day['wind_spd'])

        df = pd.DataFrame({
            'Date': dates,
            'Temperature (°C)': temps,
            'Precipitation (mm)': precips,
            'Wind Speed (m/s)': wind_speeds,
            'Weather': weather_desc
        })

        if op == 'DataFrame':
            st.dataframe(df)
        elif op == 'BarChart':
            st.bar_chart(df['Temperature (°C)'])
        else:
            st.line_chart(df['Temperature (°C)'])
    else:
        st.warning("No forecast data available. Please check your inputs.")

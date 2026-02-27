import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="National Farm Analysis", page_icon="📊")

st.title("📊 5-Day National Weather Analysis")
st.markdown("Select your region to get localized treatment safety forecasts across India.")

# --- 1. COMPREHENSIVE LOCATION DATA ---
# This structure ensures a clean "State -> District" selection flow.
india_data = {
    "Bihar": {
        "Bhagalpur": {"lat": 25.2425, "lon": 87.0145},
        "Patna": {"lat": 25.5941, "lon": 85.1376},
        "Gaya": {"lat": 24.7914, "lon": 85.0002},
        "Muzaffarpur": {"lat": 26.1209, "lon": 85.3647},
        "Purnia": {"lat": 25.7771, "lon": 87.4753}
    },
    "Uttar Pradesh": {
        "Lucknow": {"lat": 26.8467, "lon": 80.9462},
        "Varanasi": {"lat": 25.3176, "lon": 82.9739},
        "Kanpur": {"lat": 26.4499, "lon": 80.3319},
        "Prayagraj": {"lat": 25.4358, "lon": 81.8463}
    },
    "Maharashtra": {
        "Mumbai": {"lat": 19.0760, "lon": 72.8777},
        "Pune": {"lat": 18.5204, "lon": 73.8567},
        "Nagpur": {"lat": 21.1458, "lon": 79.0882}
    },
    "West Bengal": {
        "Kolkata": {"lat": 22.5726, "lon": 88.3639},
        "Siliguri": {"lat": 26.7271, "lon": 88.3953}
    },
    "Punjab": {
        "Amritsar": {"lat": 31.6340, "lon": 74.8723},
        "Ludhiana": {"lat": 30.9010, "lon": 75.8573}
    }
}

# --- 2. DYNAMIC UI FOR FARMERS ---
col1, col2 = st.columns(2)

with col1:
    selected_state = st.selectbox("🌍 Select State:", list(india_data.keys()))

with col2:
    # This filters the district list instantly based on the selected state
    districts_in_state = list(india_data[selected_state].keys())
    selected_district = st.selectbox("🏙️ Select District:", districts_in_state)

# --- 3. WEATHER PREDICTION LOGIC ---
if st.button("Predict 5-Day Spraying Conditions"):
    coords = india_data[selected_state][selected_district]
    
    try:
        # Fetching data from Open-Meteo (No API Key Required)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&daily=temperature_2m_max,precipitation_probability_max&timezone=auto"
        response = requests.get(url).json()

        if "daily" in response:
            st.subheader(f"🌦️ 5-Day Forecast for {selected_district}, {selected_state}")
            
            daily = response["daily"]
            forecast_list = []
            
            for i in range(5):
                date = daily["time"][i]
                temp = daily["temperature_2m_max"][i]
                rain_prob = daily["precipitation_probability_max"][i]
                
                # Treatment Logic: Avoid chemicals if rain is likely
                advice = "✅ Safe to Spray" if rain_prob <= 40 else "❌ High Rain Risk"
                forecast_list.append([date, f"{temp}°C", f"{rain_prob}%", advice])

            df = pd.DataFrame(forecast_list, columns=["Date", "Max Temp", "Rain Chance", "Action Advice"])
            # Using 'stretch' to keep the presentation professional
            st.table(df)
            st.success("Analysis complete. Review the 'Action Advice' before applying treatments.")
        else:
            st.error("Could not fetch data. Please try again.")

    except Exception as e:
        st.error(f"Network error: {e}")

# --- 4. DATA HISTORY ---
st.divider()
st.subheader("📋 Disease Scan History")
if os.path.exists("history_log.csv"):
    history_df = pd.read_csv("history_log.csv")
    # Clean UI for the dashboard
    st.dataframe(history_df.tail(10), width="stretch")
else:
    st.info("No scan history recorded. Go to the main page to scan a crop leaf!")

# Sidebar info
st.sidebar.markdown(f"**Developer:** Anuj Soni  \n**IIIT Bhagalpur**")
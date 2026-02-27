import streamlit as st

st.set_page_config(page_title="National Farmer Support", page_icon="📍")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("IN Farmer Support & Govt. Portals")
st.markdown("Select your region to find nearest support centers and official government schemes.")

# --- 1. STATE & DISTRICT MAPPING (Expandable) ---
# I have added major districts for key states. You can add more easily.
location_data = {
    "Bihar": ["Bhagalpur", "Patna", "Gaya", "Muzaffarpur", "Purnia", "Darbhanga", "Araria"],
    "Uttar Pradesh": ["Lucknow", "Varanasi", "Kanpur", "Agra", "Meerut", "Prayagraj"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "West Bengal": ["Kolkata", "Howrah", "Darjeeling", "Hooghly", "Siliguri"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Karnal"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner"]
}

# --- 2. OFFICIAL PORTAL MAPPING ---
state_portals = {
    "Bihar": "https://dbtagriculture.bihar.gov.in/",
    "Uttar Pradesh": "http://upagriculture.com/",
    "Punjab": "https://agri.punjab.gov.in/",
    "Maharashtra": "https://krishi.maharashtra.gov.in/",
    "West Bengal": "https://matirkatha.gov.in/",
    "Haryana": "https://agriharyana.gov.in/",
    "Rajasthan": "https://agriculture.rajasthan.gov.in/"
}

# --- 3. DYNAMIC SELECTION UI ---
col1, col2 = st.columns(2)

with col1:
    # Farmer selects the State first
    selected_state = st.selectbox("🌍 Select State:", list(location_data.keys()))

with col2:
    # District list updates automatically based on the State choice
    available_districts = location_data.get(selected_state, [])
    selected_district = st.selectbox("🏙️ Select District:", available_districts)

if st.button("🔍 Find Nearest Agriculture Office"):
    st.divider()
    
    # --- 4. DYNAMIC NAVIGATION LOGIC (Database-Free) ---
    # Creates a direct Google Maps search query
    office_query = f"District Agriculture Office {selected_district} {selected_state}"
    maps_link = f"https://www.google.com/maps/search/{office_query.replace(' ', '+')}"
    
    st.subheader(f"📍 Results for {selected_district}, {selected_state}")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("🏢 **Office Location**")
        st.write("Click below to find the exact location, photos, and contact info on Google Maps.")
        st.link_button("📍 Open in Google Maps", maps_link)
        
    with col_b:
        st.success(f"📜 **{selected_state} Schemes**")
        st.write(f"Apply for subsidies and insurance on the official {selected_state} portal.")
        st.link_button("🔗 Visit Govt. Portal", state_portals.get(selected_state, "#"))

    # --- 5. EMERGENCY CONTACTS ---
    st.markdown("---")
    st.subheader("📞 Emergency Farmer Helplines")
    st.warning("""
    * **Kisan Call Center:** 1800-180-1551 (Toll-Free, 24/7)
    * **PM-Kisan Help:** 011-24300606
    * **Note:** If the AI diagnosis seems unclear, visit your local Krishi Vigyan Kendra (KVK) with a leaf sample.
    """)

# --- SIDEBAR BRANDING ---
st.sidebar.title("👨‍🔬 Developer Info")
st.sidebar.markdown(f"""
**Anuj Soni** IIIT Bhagalpur  
""")
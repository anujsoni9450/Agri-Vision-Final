import streamlit as st
import os

st.set_page_config(page_title="Market & Pesticides", page_icon="🛒")

st.title("🛒 Market & Pesticide Locator")
st.markdown("Find the right treatments and locate verified dealers across India.")

# --- 1. PESTICIDE SEARCH ENGINE ---
st.subheader("💊 Search for Treatment")
user_query = st.text_input("Enter Disease Name (e.g., Rice Blast):")

if user_query:
    search_term = user_query.replace(" ", "+")
    st.write(f"**Quick Links for {user_query}:**")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🔎 Buy on Amazon India", f"https://www.amazon.in/s?k={search_term}+pesticide")
    with col2:
        st.link_button("🏗️ Buy on Moglix", f"https://www.moglix.com/search?q={search_term}")

st.divider()

# --- 2. DYNAMIC STORE LOCATOR ---
st.subheader("🏢 Locate Nearest Store")

# State & District Data for Manual Selection
india_location_data = {
    "Bihar": ["Bhagalpur", "Patna", "Gaya", "Muzaffarpur", "Purnia"],
    "Uttar Pradesh": ["Lucknow", "Varanasi", "Kanpur", "Agra", "Meerut"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"]
}

# Choice: Current Location vs Manual Selection
search_method = st.radio(
    "How do you want to find stores?",
    ["Use My Current Location", "Choose State & District"],
    horizontal=True
)

store_type = st.selectbox("I am looking for:", ["Pesticide Dealer", "Beej Bhandar (Seeds)", "Fertilizer Shop"])

if search_method == "Use My Current Location":
    if st.button(f"Find {store_type}s Near Me"):
        # This triggers a Google Maps search around the user's current GPS location
        near_me_url = f"https://www.google.com/maps/search/{store_type.replace(' ', '+')}+near+me"
        st.success(f"Opening Google Maps to find {store_type}s around you...")
        st.link_button("📍 View Near Me on Maps", near_me_url)

else:
    # Manual Selection Logic
    c1, c2 = st.columns(2)
    with c1:
        s_state = st.selectbox("Select State:", list(india_location_data.keys()))
    with c2:
        districts = india_location_data.get(s_state, [])
        s_district = st.selectbox("Select District:", districts)
    
    if st.button(f"Find in {s_district}"):
        search_query = f"{store_type} in {s_district} {s_state}".replace(" ", "+")
        manual_url = f"https://www.google.com/maps/search/{search_query}"
        st.link_button(f"📍 View {store_type}s in {s_district}", manual_url)

# Sidebar info
st.sidebar.markdown(f"""
**Developer:** Anuj Soni
""")
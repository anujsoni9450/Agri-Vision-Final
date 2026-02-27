import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="App Feedback", page_icon="📝")

st.title("📝 Agri-Vision Feedback Form")
st.markdown("Your feedback helps us improve the AI accuracy for farmers across India.")

# --- FEEDBACK FORM ---
with st.form("feedback_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    user_type = st.selectbox("I am a:", ["Farmer", "Agriculture Expert", "Student", "Other"])
    
    # Rating scale
    rating = st.slider("How accurate was the disease detection?", 1, 5, 3)
    
    # Detailed comments
    comments = st.text_area("Any suggestions or missing diseases?")
    
    # Submit Button
    submit_button = st.form_submit_button("Submit Feedback")

if submit_button:
    if name and comments:
        # Create a small dictionary of the data
        feedback_data = {
            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Name": [name],
            "Type": [user_type],
            "Rating": [rating],
            "Comments": [comments]
        }
        
        # Display a success message
        st.success(f"Thank you, {name}! Your feedback has been recorded.")
        
        # Pro-Tip: Saving to a local CSV (Database-free)
        df = pd.DataFrame(feedback_data)
        df.to_csv("feedback_log.csv", mode='a', index=False, header=not os.path.exists("feedback_log.csv"))
        
        st.info("Technical Note: This feedback is being saved to 'feedback_log.csv' in your project folder.")
    else:
        st.error("Please fill in your name and comments before submitting.")

# Sidebar info
st.sidebar.title("👨‍🔬 Developer")
st.sidebar.write("Anuj Soni, IIIT Bhagalpur")
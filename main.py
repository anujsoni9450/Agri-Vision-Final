import streamlit as st
import torch
import os
import base64
import pandas as pd
from datetime import datetime
from PIL import Image
from torchvision import transforms
from transformers import ViTForImageClassification
from openai import OpenAI
from gtts import gTTS
from youtubesearchpython import VideosSearch
from dotenv import load_dotenv

# --- PAGE CONFIG ---
st.set_page_config(page_title="Agri-Vision AI", page_icon="🌱", layout="centered")

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# --- CONFIGURATION ---
current_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(current_dir, "crop_final_model")
client = OpenAI(api_key=OPENAI_KEY)

# --- 1. LOAD MODEL (Cached for speed) ---
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model folder not found at: {MODEL_PATH}")
        return None
    model = ViTForImageClassification.from_pretrained(MODEL_PATH, local_files_only=True)
    model.eval()
    return model

model = load_model()

# --- 2. PREPROCESSING ---
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]) 
])

# --- 3. HELPER FUNCTIONS ---
def get_voice_html(file_path):
    """Encodes audio to base64 for seamless playback in Streamlit."""
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio controls src="data:audio/mp3;base64,{b64}">'

def get_yt_recommendations(disease_name, language):
    """Fetches real-time YouTube videos and thumbnails in the selected language."""
    st.markdown("---")
    st.subheader(f"📺 {language} Video Guides for {disease_name}")
    
    query = f"{disease_name} treatment for farmers in {language}"
    
    try:
        search = VideosSearch(query, limit=2)
        results = search.result()['result']

        if results:
            col1, col2 = st.columns(2)
            with col1:
                st.image(results[0]['thumbnails'][0]['url'], width="stretch")
                st.markdown(f"**{results[0]['title'][:45]}...**")
                st.link_button(f"Watch in {language}", results[0]['link'])

            if len(results) > 1:
                with col2:
                    st.image(results[1]['thumbnails'][0]['url'], width="stretch")
                    st.markdown(f"**{results[1]['title'][:45]}...**")
                    st.link_button(f"Watch in {language}", results[1]['link'])
        else:
            st.info(f"No specific {language} videos found.")
    except Exception as e:
        st.error(f"Thumbnail loading failed. Error: {e}")

# --- DASHBOARD UI ---
st.title("🌱 Agri-Vision AI")
st.markdown("### Multilingual Disease Detection & Expert Advice")

uploaded_file = st.file_uploader("Upload a crop leaf photo...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None and model is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", width="stretch")
    
    # --- Step 1: Detection ---
    with st.spinner("Analyzing Leaf Architecture..."):
        pixel_values = preprocess(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(pixel_values)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, prediction_idx = torch.max(probabilities, dim=-1)
            disease_name = model.config.id2label[prediction_idx.item()]
    
    st.metric(label="Prediction Confidence", value=f"{confidence.item()*100:.2f}%")
    st.success(f"Detected: **{disease_name}**")

    # --- NEW FEATURE: SAVE TO HISTORY ---
    history_file = "history_log.csv"
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Disease": disease_name,
        "Confidence": f"{confidence.item()*100:.2f}%"
    }
    df_new = pd.DataFrame([new_entry])
    df_new.to_csv(history_file, mode='a', index=False, header=not os.path.exists(history_file))

    # --- Step 2: Language Selection ---
    languages = {
        "Hindi": "hi", "English": "en", "Bengali": "bn", "Telugu": "te", 
        "Marathi": "mr", "Tamil": "ta", "Gujarati": "gu", "Urdu": "ur", 
        "Kannada": "kn", "Odia": "or", "Malayalam": "ml", "Punjabi": "pa",
        "Assamese": "as", "Maithili": "mai"
    }
    
    lang_choice = st.selectbox("Select Language for Advice:", list(languages.keys()))
    
    if st.button("Get Expert Advice & Videos"):
        if not OPENAI_KEY:
            st.error("API Key missing! Check your .env or Secrets.")
        else:
            with st.spinner(f"Consulting AI in {lang_choice}..."):
                prompt = f"Professional agricultural treatment for {disease_name} in {lang_choice}. Limit to 60 words."
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                advice_text = response.choices[0].message.content
                st.info(advice_text)

                tts_lang = languages.get(lang_choice, "en")
                try:
                    tts = gTTS(text=advice_text, lang=tts_lang)
                    tts.save("response.mp3")
                    st.markdown(get_voice_html("response.mp3"), unsafe_allow_html=True)
                except Exception as e:
                    st.error("Voice output failed.")

            # --- Step 3: Dynamic YouTube Recommendations ---
            get_yt_recommendations(disease_name, lang_choice)

            # --- NEW FEATURE: EXPERT SUPPORT (WHATSAPP) ---
            st.markdown("---")
            st.subheader("🆘 Need a Second Opinion?")
            whatsapp_msg = f"Hello Expert, my crop was identified as {disease_name} by Agri-Vision AI. Can you verify this?"
            whatsapp_url = f"https://wa.me/91XXXXXXXXXX?text={whatsapp_msg.replace(' ', '%20')}"
            st.link_button("📲 Chat with an Expert on WhatsApp", whatsapp_url)

# --- SIDEBAR ---
st.sidebar.title("👨‍🔬 Project Details")
st.sidebar.markdown(f"""
**Developer:** Anuj Soni  
---
**Technical Stack:**
* **Vision:** Vision Transformer (ViT)
* **LLM:** GPT-4o Mini
* **Voice:** gTTS API
* **History:** Local CSV Storage
""")
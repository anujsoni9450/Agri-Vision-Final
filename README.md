🌱 Agri-Vision AI: Multilingual Crop Disease Diagnostics
Overview
Agri-Vision AI is a deep learning-powered platform designed to empower Indian farmers with instant crop disease detection and expert treatment advice. By bridging the gap between Computer Vision and Large Language Models, the system identifies leaf diseases and provides localized advice in 14 regional languages through both text and voice interfaces.

🚀 Key Features
Disease Detection: Uses a fine-tuned Vision Transformer (ViT) model to classify leaf images from the "New Plant Diseases Dataset".

Multilingual Support: Expert treatment plans generated in 14 major Indian languages including Hindi, Bengali, Telugu, Punjabi, and Maithili.

Voice Advice: Integrated gTTS (Google Text-to-Speech) engine to read out treatment plans for better accessibility.

Real-time Confidence: Displays a confidence metric for every prediction, alerting users if a crop is potentially out-of-distribution (like Cabbage in a Tomato-trained model).

🛠️ Tech Stack
Deep Learning: PyTorch, Torchvision, Transformers (Hugging Face).

Architecture: ViT-Base (Vision Transformer) fine-tuned for agricultural diagnostics.

LLM Interface: OpenAI GPT-4o Mini for generating context-aware treatment advice.

Voice Engine: Google Text-to-Speech (gTTS).

Framework: Streamlit for the web dashboard.

💻 Local Installation
To run this project on your local machine:

Clone the repository:

Bash
pip install -r requirements.txt
Set up Environment Variables:
Create a .env file and add your OpenAI API Key:

Plaintext
OPENAI_API_KEY="your_api_key_here"
Run the app:

Bash
streamlit run main.py
📂 Project Structure
Plaintext
├── crop_final_model/   # Fine-tuned ViT weights and config
├── main.py             # Streamlit dashboard and logic
├── requirements.txt    # Required Python libraries
├── .env                # Private API keys (not for upload)
└── README.md           # Project documentation
👨‍💻 Developer Information
Name: Anuj Soni

Institution: IIIT Bhagalpur

Department: Electronics and Communication Engineering (ECE)

⚖️ License
This project is licensed under the MIT License.

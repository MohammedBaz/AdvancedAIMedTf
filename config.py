# config.py

import streamlit as st

# Access the API key from Streamlit secrets
API_KEY = st.secrets["GeminiKey"]

# Database settings
DATABASE_NAME = "taif_medical.db"

# Gemini model settings
MODEL_NAME = "gemini-pro"

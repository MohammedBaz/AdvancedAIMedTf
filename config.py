# config.py

import streamlit as st

# Access the API key from Streamlit secrets
API_KEY = st.secrets["API_KEY"]

# Database settings
DATABASE_NAME = "taif_medical.db"

# Gemini model settings
MODEL_NAME = "gemini-pro"

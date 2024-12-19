import streamlit as st

# Access the API key from Streamlit secrets
API_KEY = st.secrets["GeminiKey"]

# Database settings
DATABASE_NAME = "taif_medical.db"

# Gemini model settings
MODEL_NAME = "gemini-pro"

# Import from the correct location
from utils.database import execute_query
from model import get_gemini_response, extract_sql_query, extract_contextualization

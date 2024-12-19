# imports.py

import streamlit as st
import sqlite3
import pandas as pd
import random
from tabulate import tabulate
import google.generativeai as genai

# Access the API key from Streamlit secrets
API_KEY = st.secrets["GeminiKey"]

# Configure Genai Key
genai.configure(api_key=API_KEY)

# Database settings
DATABASE_NAME = "taif_medical.db"

# Gemini model settings
MODEL_NAME = "gemini-pro"

# Import from the correct location
from utils.database import execute_query
# Only import get_gemini_response from model.py
from model import get_gemini_response 

# config.py

import streamlit as st
import sqlite3
import pandas as pd
import random
from tabulate import tabulate
import google.generativeai as genai
from utils.database import execute_query
from model import get_gemini_response, extract_sql_query, extract_contextualization
import config

# Access the API key from Streamlit secrets
API_KEY = st.secrets["GeminiKey"]

# Database settings
DATABASE_NAME = "taif_medical.db"

# Gemini model settings
MODEL_NAME = "gemini-pro"

# config.py

import streamlit as st
import sqlite3
import pandas as pd
import random
from tabulate import tabulate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import google.generativeai as genai
import streamlit as st
# Access the API key from Streamlit secrets
API_KEY = st.secrets["GeminiKey"]

# Database settings
DATABASE_NAME = "taif_medical.db"

# Gemini model settings
MODEL_NAME = "gemini-pro"

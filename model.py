# model.py

import google.generativeai as genai
import sqlite3
import pandas as pd
import imports  # Import the imports module

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query, retrieving information from the Taif medical institutions database, and providing  answers based on the retrieved data.

    You should respond conversationally to greetings or general inquiries, but provide data-driven answers to specific questions about the Taif medical institutions.

    The database has three tables:
    * MedicalInstitutions: Name, Type, District, Beds, Speciality
    * WaitingTimes: Hospital, WaitingTime
    * KPIs: Hospital, OccupancyRate, PatientSatisfaction

    Instructions:

- If the user asks a question about the Taif medical institutions, ALWAYS generate a SQL query to retrieve the relevant information from the database.
- Ensure that the generated SQL query uses the correct table and column names from the database schema (MedicalInstitutions, WaitingTimes, KPIs).
- The SQL query should be specific enough to answer the user's question accurately.

    Please provide ONLY the answer to the question as your output.
    """
]

def extract_sql_query(response):
    # Assuming the SQL query is enclosed in backticks
    start = response.find("`") + 1
    end = response.find("`", start)
    return response[start:end]

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel(imports.MODEL_NAME)
    response = model.generate_content([prompt[0], question])
    
    # Return the response from Gemini directly
    return response.text

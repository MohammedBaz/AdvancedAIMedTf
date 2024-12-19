# model.py

import google.generativeai as genai
import sqlite3
import pandas as pd
import imports

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query, retrieving information from the Taif medical institutions database, and providing answers based on the retrieved data.

    The database has three tables:
    * MedicalInstitutions: Name, Type, District, Beds, Speciality
    * WaitingTimes: Hospital, WaitingTime
    * KPIs: Hospital, OccupancyRate, PatientSatisfaction

    Instructions:

    - If the user asks a specific question about the Taif medical institutions that can be answered using the data in the tables, generate a SQL query to retrieve the necessary information from the database, execute the query, and provide ONLY the answer based on the query results.
    - If the user asks a question that is not related to the Taif medical institutions or cannot be answered using the data, provide a message indicating that the question is not applicable.

    Please provide ONLY the answer to the question as your output.
    """
]

def execute_query(query):
    conn = sqlite3.connect(imports.DATABASE_NAME)
    cur = conn.cursor()
    try:
        cur.execute(query)
        result = cur.fetchone()  # Get the first result
        return result[0] if result else "No data found."
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return "Error executing SQL query."
    finally:
        conn.close()

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel(imports.MODEL_NAME)
    response = model.generate_content([prompt[0], question])
    return response.text

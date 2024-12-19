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

    - If the user greets you or asks a general question (e.g., "Hello," "How are you?"), respond in a friendly and professional manner.
    - If the user asks a specific question about the Taif medical institutions that can be answered using the data in the tables, generate a SQL query to retrieve the necessary information from the database, execute the query, and provide ONLY the answer based on the query results.
    - If the user asks a question that is not related to the Taif medical institutions or cannot be answered using the data, provide a message indicating that the question is not applicable or suggest alternative resources if available.

    Please provide ONLY the answer to the question as your output.
    """
]

def execute_query(query):
    conn = sqlite3.connect(imports.DATABASE_NAME)  # Access DATABASE_NAME from imports
    cur = conn.cursor()
    try:
        cur.execute(query)
        results = cur.fetchall()
        # Get column names from cursor description
        col_names = [desc[0] for desc in cur.description]
        # Convert to DataFrame for easier handling
        df = pd.DataFrame(results, columns=col_names)
        return df
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None
    finally:
        conn.close()

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel(imports.MODEL_NAME)
    response = model.generate_content([prompt[0], question])
    
    # Return the response from Gemini directly
    return response.text

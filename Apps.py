
import sqlite3
import pandas as pd
import random
from tabulate import tabulate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import google.generativeai as genai

# Configure Genai Key
genai.configure(api_key='YOUR_API_KEY')  # Replace with your actual Gemini Pro API key

# --- Database Generation ---

# Define the number of random entries to create
num_entries = 30  # Adjust as needed
# Generate random data for medical institutions in Taif
data = {
    'Name': [],
    'Type': [],
    'District': [],
    'Beds': [],
    'Speciality': []
}

# Ensure all lists have the same length (num_entries)
data['Name'] = [f'{random.choice(["Taif", "Al Hada", "Ash Shafa"])} {random.choice(["Clinic", "Hospital", "Medical Center"])} {i}' for i in range(1, num_entries + 1)]
data['Type'] = [random.choice(['Hospital', 'Clinic', 'Pharmacy', 'Lab']) for _ in range(num_entries)]
data['District'] = [random.choice(['Al Hawiyah', 'Al Khalidiyah', 'Al Faisaliyah', 'Al Qumariyah', 'An Nur']) for _ in range(num_entries)]

# Calculate 'Beds' based on 'Type', ensuring the same length
data['Beds'] = [random.randint(10, 200) if 'Hospital' in t else None for t in data['Type']]

data['Speciality'] = [random.choice(['General Medicine', 'Pediatrics', 'Dental', 'ENT', 'Dermatology', 'Ophthalmology']) for _ in range(num_entries)]

# Create a DataFrame from the random data for medical institutions
medical_df = pd.DataFrame(data)

# Generate random data for waiting times
waiting_times_data = {
    'Hospital': medical_df[medical_df['Type'] == 'Hospital']['Name'].sample(frac=0.8, replace=True).tolist(),  # 80% of hospitals have waiting time data
    'WaitingTime': [random.randint(5, 20) for _ in range(int(num_entries * 0.8))]  # Waiting time in minutes
}

# Create a DataFrame from the random data for waiting times
waiting_times_df = pd.DataFrame(waiting_times_data)

# Generate random data for KPIs
kpi_data = {
    'Hospital': medical_df[medical_df['Type'] == 'Hospital']['Name'].tolist(),
    'OccupancyRate': [random.uniform(0.6, 0.9) for _ in range(medical_df[medical_df['Type'] == 'Hospital'].shape[0])],
    'PatientSatisfaction': [random.uniform(0.7, 0.95) for _ in range(medical_df[medical_df['Type'] == 'Hospital'].shape[0])]
}

# Create a DataFrame from the random data for KPIs
kpi_df = pd.DataFrame(kpi_data)

# Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect("taif_medical.db")

# Create tables and load the data (replace if the tables exist)
medical_df.to_sql('MedicalInstitutions', conn, if_exists='replace', index=False)
waiting_times_df.to_sql('WaitingTimes', conn, if_exists='replace', index=False)
kpi_df.to_sql('KPIs', conn, if_exists='replace', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Taif medical database created and populated with random data.")

# --- Gemini Model ---

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query, retrieving information from the Taif medical institutions database, and providing contextualized responses that highlight the role of AI in healthcare.

    The database has three tables:
    * MedicalInstitutions: Name, Type, District, Beds, Speciality
    * WaitingTimes: Hospital, WaitingTime
    * KPIs: Hospital, OccupancyRate, PatientSatisfaction

    When answering questions, consider the following:

    * Saudi Vision 2030 Goals:
        - Improve public health through preventative care and healthy lifestyle promotion.
        - Enhance healthcare services by increasing access to quality care and promoting innovation.
        - Develop a skilled workforce by training and retaining healthcare professionals.
        - Promote private sector participation in the healthcare sector.
        - Utilize technology to improve healthcare delivery and access.

    * The Role of AI in Healthcare:
        - AI can help analyze patient data to identify trends and predict health risks.
        - AI can assist in diagnosis by analyzing medical images and patient records.
        - AI can personalize treatment plans and monitor patient progress.
        - AI can automate administrative tasks and improve operational efficiency.
        - AI can enhance patient engagement through chatbots and virtual assistants.

    * Provide Examples:
        - When discussing preventative care, mention AI-powered apps that promote healthy habits.
        - When discussing improved access to care, mention AI-powered telemedicine platforms.
        - When discussing workforce development, mention AI-powered training and simulation tools.

    Example:

    Question: What is the average waiting time in hospital X?

    Answer:

    SQL query: `SELECT AVG(WaitingTime) FROM WaitingTimes WHERE Hospital = 'X';`

    Context: The average waiting time in hospital X is 10 minutes. This is higher than the 2024 target of 5 minutes. To achieve the 2030 goal of 2 minutes, the hospital could consider AI-powered solutions for optimizing patient flow, such as appointment scheduling systems that predict patient arrival times and allocate resources accordingly.

    Please provide the SQL query and the contextualized response as your output.
    """
]

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# --- Interface ---

import streamlit as st

# Function to execute SQL query and return results as DataFrame
def execute_query(query):
    conn = sqlite3.connect("taif_medical.db")
    try:
        # Split multiple SQL statements
        for stmt in query.split(";"):
            if stmt.strip():  # Execute only if the statement is not empty
                cur = conn.cursor()
                cur.execute(stmt)
                results = cur.fetchall()
                # Get column names from cursor description
                col_names = [desc[0] for desc in cur.description]
                # Display results in a table
                if results:
                  print(tabulate(results, headers=col_names, tablefmt="fancy_grid"))  # Use col_names here
                else:
                  print("No results found.")
    except Exception as e:
        print(f"Error executing SQL query: {e}")
    finally:
        conn.close()

# Streamlit app
st.title("NL2SQL with Gemini Pro and Contextualization")

# User input
user_question = st.text_input("Enter your question:")

if user_question:
    try:
        response = get_gemini_response(user_question, prompt)

        # You'll need to implement these functions to extract the SQL and context
        # sql_query = extract_sql_query(response)
        # contextualized_response = extract_contextualization(response)

        # For now, let's just display the raw response
        st.write(response)

        # Execute the query (if you have extracted the SQL query)
        # execute_query(sql_query)

    except Exception as e:
        st.write(f"Error: {e}")

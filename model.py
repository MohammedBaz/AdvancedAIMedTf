# model.py
import model
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

    Example 1:

    Question: What is the average waiting time in hospital X?

    Answer:
    
    10 minutes


    Example 2:

    Question: dsf 

    Answer:

    This question is not applicable to the Taif medical institutions database.


    Please provide ONLY the answer to the question as your output.
    """
]

def execute_query(query):
    conn = sqlite3.connect(DATABASE_NAME)
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
    model = genai.GenerativeModel(import.MODEL_NAME)
    response = model.generate_content([prompt[0], question])

    # Access the 'text' attribute of the response
    response_text = response.text 

    # Assuming the SQL query is enclosed in backticks
    start = response_text.find("`") + 1  # Use response_text here
    end = response_text.find("`", start)  # Use response_text here
    sql_query = response_text[start:end]  # Use response_text here

    # Execute the query and get the result
    result_df = execute_query(sql_query)

    # Check if the question is irrelevant
    if "This question cannot be answered using the Taif medical institutions database" in response:
        return response.strip()
    
    # Return the result from the database
    if result_df is not None:
        # Assuming the result is a single value, you might need to adjust this based on your query
        answer = result_df.iloc[0, 0] if not result_df.empty else "No data found."
        return str(answer)
    else:
        return "Error executing SQL query."

from imports import *

# Streamlit app
st.title("DDS for THC")

# User input
user_question = st.text_input("Enter your question:")

if user_question:
    try:
        response = get_gemini_response(user_question, prompt)  # Access prompt from model.py

        # You'll need to implement these functions to extract the SQL and context
        sql_query = extract_sql_query(response)
        contextualized_response = extract_contextualization(response)

        st.write("Generated SQL query:", sql_query)

        # Execute the query (if you have extracted the SQL query)
        execute_query(sql_query)

        if contextualized_response:
            st.write(contextualized_response)

    except Exception as e:
        st.write(f"Error: {e}")

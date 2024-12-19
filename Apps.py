# app.py

import model

from imports import *
st.title("DDS for XHC")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# Get user input
if prompt := st.chat_input("Enter your question:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Generate response using Gemini Pro
        response = get_gemini_response(prompt, model.prompt)  # Access prompt from model

        # Extract SQL query and contextualization
        sql_query = extract_sql_query(response)
        contextualized_response = extract_contextualization(response)

        # Execute the query
        execute_query(sql_query)

        # Display the generated SQL query and contextualized response
        with st.chat_message("assistant"):
            st.markdown(f"Generated SQL query:\n```sql\n{sql_query}\n```")
            if contextualized_response:
                st.markdown(contextualized_response)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": f"Generated SQL query:\n```sql\n{sql_query}\n```\n\n{contextualized_response}"})

    except Exception as e:
        with st.chat_message("assistant"):
            st.markdown(f"Error: {e}")
    




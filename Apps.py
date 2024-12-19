# app.py

from imports import *
import model

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Enter your question:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Generate response using Gemini Pro
        response = get_gemini_response(prompt, model.prompt)

        # Extract SQL query and contextualization
        sql_query = extract_sql_query(response)
        contextualized_response = extract_contextualization(response)

        # Check if the question is irrelevant
        if "This question cannot be answered using the Taif medical institutions database" in contextualized_response:
            with st.chat_message("assistant"):
                # Display the full response for irrelevant questions
                st.markdown(contextualized_response)  
        else:
            # Execute the query
            execute_query(sql_query)

            # Display the generated SQL query and contextualized response
            with st.chat_message("assistant"):
                if sql_query:
                    st.markdown(f"Generated SQL query:\n```sql\n{sql_query}\n```")
                if contextualized_response:
                    st.markdown(contextualized_response)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": contextualized_response})

    except Exception as e:
        with st.chat_message("assistant"):
            st.markdown(f"Error: {e}")

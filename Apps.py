# app.py

from imports import *
import model

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get user input
if prompt := st.chat_input(""):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Generate response using the model
        response = get_gemini_response(prompt, model.prompt)

        # Check if the question is irrelevant
        if "This question cannot be answered using the Taif medical institutions database" in response:
            # Display the full response for irrelevant questions
            st.session_state.messages.append({"role": "assistant", "content": response})  
        else:
            # Extract the SQL query
            sql_query = model.extract_sql_query(response)

            # Execute the query and get the results
            results = execute_query(sql_query)  

            # Format the results
            formatted_results = format_results(results)

            # Add assistant message to chat history (formatted results only)
            st.session_state.messages.append({"role": "assistant", "content": formatted_results})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Display chat messages from history
for i, message in enumerate(st.session_state.messages):
    with st.container(key=f"{message['role']}_{i}"):
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Add styling for the chat
st.markdown(
    """
    <style>
    [data-testid="stChatMessage"][data-role="user"] .stChatMessageBox {
        background-color: #f0f0f0;
        border-radius: 10px 10px 10px 0px;
    }
    [data-testid="stChatMessage"][data-role="assistant"] .stChatMessageBox {
        background-color: #eaf7ff;
        border-radius: 10px 10px 0px 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

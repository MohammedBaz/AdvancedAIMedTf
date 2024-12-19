from imports import *
import model

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Generate response using Gemini Pro
        response = get_gemini_response(prompt, model.prompt)

        # Extract SQL query and contextualization
        sql_query = extract_sql_query(response)
        contextualized_response = extract_contextualization(response)

        # Check if the question is irrelevant
        if "This question cannot be answered using the Taif medical institutions database" in contextualized_response:
            st.session_state.messages.append({"role": "assistant", "content": contextualized_response})
        else:
            # Execute the query
            execute_query(sql_query)

            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Generated SQL query:\n```sql\n{sql_query}\n```\n\n{contextualized_response}"
            })
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Display chat messages from history
for i, message in enumerate(st.session_state.messages):
    with st.container(key=f"{message['role']}_{i}"):
        alignment_class = "assistant-message" if message["role"] == "assistant" else "user-message"
        with st.chat_message(message["role"]):
            st.write(message["content"], unsafe_allow_html=True)

# Add styling for chat alignment
st.markdown(
    """
    <style>
    [data-testid="stChatMessage"] {
        flex-direction: row; /* Default for user */
    }
    [data-testid="stChatMessage.user-message"] {
        flex-direction: row-reverse; /* User message on the left */
        text-align: left;
    }
    [data-testid="stChatMessage.assistant-message"] {
        flex-direction: row; /* Assistant message on the right */
        text-align: right;
    }
    [data-testid="stChatMessage"] .stChatMessageBox {
        max-width: 80%; /* Adjust box width for better alignment */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

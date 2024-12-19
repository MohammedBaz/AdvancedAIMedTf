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
    alignment_class = "user-message" if message["role"] == "user" else "assistant-message"
    with st.container(key=f"{message['role']}_{i}"):
        with st.chat_message(message["role"]):
            st.markdown(f"<div class='{alignment_class}'>{message['content']}</div>", unsafe_allow_html=True)

# Add styling for chat alignment
st.markdown(
    """
    <style>
    /* User messages aligned to the left */
    .user-message {
        text-align: left;
        background-color: #f1f1f1;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }

    /* Assistant messages aligned to the right */
    .assistant-message {
        text-align: right;
        background-color: #d9edf7;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }

    /* Make sure the chat bubbles look nice */
    [data-testid="stChatMessage"] {
        max-width: 80%;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

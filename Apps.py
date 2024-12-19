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

        # Extract only the contextualized response (no SQL query)
        contextualized_response = extract_contextualization(response)

        # Check if the question is irrelevant
        if "This question cannot be answered using the Taif medical institutions database" in contextualized_response:
            st.session_state.messages.append({"role": "assistant", "content": contextualized_response})
        else:
            # Add only the meaningful response to chat history
            st.session_state.messages.append({"role": "assistant", "content": contextualized_response})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Display chat messages from history
for i, message in enumerate(st.session_state.messages):
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    with st.container(key=f"{message['role']}_{i}"):
        with st.chat_message(message["role"]):
            st.markdown(f"<div class='{role_class}'>{message['content']}</div>", unsafe_allow_html=True)

# Add styling for chat alignment and colors
st.markdown(
    """
    <style>
    /* Shared styles for all messages */
    [data-testid="stChatMessage"] {
        max-width: 80%;
        margin: auto;
    }

    /* User messages (question) styling */
    .user-message {
        text-align: left;
        background-color: #fdebd0; /* Light orange for user */
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }

    /* Assistant messages (response) styling */
    .assistant-message {
        text-align: left;
        background-color: #d6eaf8; /* Light blue for assistant */
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

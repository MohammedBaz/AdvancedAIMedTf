from imports import *
import model

# Function to extract the contextualized response from the full response
def extract_contextualized_response(full_response):
    if "Contextualized response:" in full_response:
        return full_response.split("Contextualized response:")[1].strip()
    return full_response.strip()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get user input
if prompt := st.chat_input("Ask a question about Taif medical institutions"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Generate response using the model
        response = get_gemini_response(prompt, model.prompt)

        # Extract only the contextualized response (no SQL query)
        contextualized_response = extract_contextualized_response(response)

        # Check if the question is irrelevant
        if "This question cannot be answered using the Taif medical institutions database" in contextualized_response:
            # Display the response for irrelevant questions
            st.session_state.messages.append({"role": "assistant", "content": contextualized_response})
        else:
            # Add contextualized assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": contextualized_response})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Display chat messages from history
for i, message in enumerate(st.session_state.messages):
    with st.container(key=f"{message['role']}_{i}"):
        # Display messages with roles (user/assistant)
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

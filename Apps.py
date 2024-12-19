# app.py

import model  # Import the model module here
from imports import *

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get user input
if prompt := st.chat_input(""):
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Generate response using the model
        response = get_gemini_response(prompt, model.prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    with st.container(key=f"{message['role']}_{i}"):
        with st.chat_message(message["role"]):
            st.write(message["content"])

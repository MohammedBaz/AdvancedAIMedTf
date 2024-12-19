# app.py

from imports import *
import model  # Import the model module

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create columns for chat input and file uploader
col1, col2 = st.columns([3, 1])  # Adjust column ratios as needed

# Chat input in the first column
with col1:
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

with col2:
    st.markdown(
        """
        <style>
        .stFileUploader > label {
            display: none;
        }
        .stFileUploader > div > button {
            background-color: #4CAF50; /* Green */
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        </style>
        <input type="file" id="fileUploader">
        <button>Upload Image</button>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.session_state.get("fileUploader", None)

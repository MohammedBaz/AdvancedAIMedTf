import google.generativeai as genai


# Configure Genai Key
genai.configure(api_key=config.API_KEY)

# Define Your Prompt
prompt = [
    """
    ... (your prompt definition) ...
    """
]

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel(config.MODEL_NAME)
    response = model.generate_content([prompt[0], question])
    return response.text

def extract_sql_query(response):
    # Assuming the SQL query is enclosed in backticks
    start = response.find("`") + 1
    end = response.find("`", start)
    return response[start:end]

def extract_contextualization(response):
    # Assuming the context comes after the SQL query
    start = response.find("`", response.find("`") + 1) + 1  # Find the second backtick
    return response[start:].strip()

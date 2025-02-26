from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AzureOpenAI
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Azure OpenAI configuration
AZURE_OPENAI_API_KEY = "#####"
AZURE_OPENAI_DEPLOYMENT_ID = "###"
AZURE_ENDPOINT = "#####"

# Instantiate the AzureOpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version="###",
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_ID
)

app = Flask(__name__)
CORS(app)

def dax_to_sql(user_message: str) -> str:
    """Converts a DAX query to SQL."""
    system_message = """You are an expert with more than 20 years of experence in translating DAX queries into optimized SQL queries.
                        If the input is not a valid DAX query, politely inform the user.
                        You only provide the translated query nothing else"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_ID,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Convert this DAX query to SQL: {user_message}"}
        ],
        max_tokens=1000,
        temperature=0,
        top_p=0.95
    )
    
    return response.choices[0].message.content.strip()

def sql_to_dax(user_message: str) -> str:
    """Converts an SQL query to DAX."""
    system_message = """You are an expert with more than 20 years of experence in translating SQL queries into optimized DAX queries.
                        If the input is not a valid SQL query, politely inform the user.
                        You only provide the translated query nothing else"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_ID,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Convert this SQL query to DAX: {user_message}"}
        ],
        max_tokens=1000,
        temperature=0,
        top_p=0.95
    )

    return response.choices[0].message.content.strip()

def explain_queries(original_query: str, translated_query: str, conversion_type: str) -> str:
    """Compares the original and translated queries and provides an explanation."""
    system_message = f"""You are an expert in query translation. Explain the transformation
                         from {conversion_type}, highlighting key differences and explain about the translated query"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_ID,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Original Query: {original_query}\nTranslated Query: {translated_query}"}
        ],
        max_tokens=10000,
        temperature=0,
        top_p=0.95
    )

    return response.choices[0].message.content.strip()

@app.route("/translate", methods=["POST"])
def translate():
    """Receives a query and translates it based on the requested language."""
    data = request.get_json()
    user_message = data.get("query", "")
    target_language = data.get("target_language", "").lower()

    if not user_message or target_language not in ["sql", "dax"]:
        return jsonify({"error": "Invalid input. Provide a query and specify 'sql' or 'dax'."}), 400

    if target_language == "sql":
        translated_query = dax_to_sql(user_message)
        conversion_type = "DAX to SQL"
    else:
        translated_query = sql_to_dax(user_message)
        conversion_type = "SQL to DAX"

    explanation = explain_queries(user_message, translated_query, conversion_type)

    return jsonify({
        "original_query": user_message,
        "translated_query": translated_query,
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(debug=True)

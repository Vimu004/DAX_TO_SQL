import re
import logging
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any
 
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
 
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import openai
 
# Load environment variables from a .env file (if available)
load_dotenv()
 
# Configure logging
logging.basicConfig(level=logging.INFO)
 
# Azure OpenAI configuration
AZURE_OPENAI_API_KEY = "9tCIKRFHYXumPEAMEPUWEcGmSwEAUBMILlx4CN5BPhGnnsNK0EmVJQQJ99BBACfhMk5XJ3w3AAABACOGhWbS"
AZURE_OPENAI_DEPLOYMENT_ID = "gpt-4o"
AZURE_ENDPOINT = "https://haycarb.openai.azure.com/"
 
# Azure Search configuration
SEARCH_INDEX_NAME = "haycarb-index"
SEARCH_API_KEY = "FgDHX6OW2boALgCkuQeTCkzZ5DRuPahNHKcAqzyfMUAzSeC87V7U"
SEARCH_ENDPOINT = "https://haycarb-search.search.windows.net"
ANNUAL_INDEX_NAME = "haycarb-annual-index"
 
openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_ENDPOINT
openai.api_version = "2023-03-15-preview"
 
annual_prompt = (
    "You are an AI assistant specialized in providing detailed answers based on annual report of haycarb. "
    "Ensure that your responses are comprehensive, accurate, and cite relevant information from the reports."
)
 
app = Flask(__name__)
CORS(app)
 
def process_message(user_message: str) -> str:
    """
    Sends the user message along with the system prompt to Azure OpenAI and includes
    additional parameters for Azure Search integration.
    """
    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_DEPLOYMENT_ID,
        messages=[
            {"role": "system", "content": annual_prompt},
            {"role": "user", "content": f"Current Question: {user_message}"}
        ],
        max_tokens=4096,
        temperature=0,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "endpoint": SEARCH_ENDPOINT,
                    "index_name": ANNUAL_INDEX_NAME,
                    "semantic_configuration": "haycarb-annual-index-semantic-configuration",
                    "query_type": "vector_semantic_hybrid",
                    "fields_mapping": {
                        "content_fields_separator": "\n",
                        "content_fields": None,
                        "filepath_field": None,
                        "title_field": "title",
                        "url_field": None,
                        "vector_fields": ["text_vector"],
                    },
                    "in_scope": True,
                    "role_information": annual_prompt,
                    "filter": None,
                    "strictness": 3,
                    "top_n_documents": 5,
                    "authentication": {
                        "type": "api_key",
                        "key": SEARCH_API_KEY
                    },
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": "text-embedding-ada-002"
                    }
                }
            }]
        }
    )
    return response["choices"][0]["message"]["content"].strip()
 
@app.route("/chat", methods=["POST"])
def chat() -> Any:
    data = request.get_json()
    user_message = data.get("message", "")
 
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
 
    processed_message = user_message.upper()
    logging.info("User Message: %s", processed_message)
 
    response_text = process_message(processed_message)
    return jsonify({"response": response_text})
 
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
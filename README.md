# DAX to SQL Chatbot

## Overview
DAX to SQL is a Python-based chatbot designed to assist data science and AI engineers in translating DAX queries to SQL and vice versa. This tool is particularly useful for migration projects where understanding and converting between these query languages is essential. The chatbot also provides a comparison feature to explain the generated SQL or DAX queries, helping users build more complex queries by combining different elements.

## Features
- **DAX to SQL Translation**: Convert DAX queries into SQL queries.
- **SQL to DAX Translation**: Convert SQL queries into DAX queries.
- **Query Comparison**: Compare generated queries with input queries for better understanding and learning.
- **Interactive Frontend**: Streamlit-based frontend for an interactive user experience.

## Prerequisites
- Python 3.x
- Virtual Environment (venv)

## Installation
## Create a Virtual Environment
Create an isolated environment to manage project dependencies.

```bash
python3 -m venv venv
```

## Activate the Virtual Environment

### On Windows:
```bash
venv\Scripts\activate
```

### On macOS and Linux:
```bash
source venv/bin/activate
```

## Install Dependencies
Install the required packages using pip and the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Run the Application
Start the application using:

```bash
python app.py
```
## Run the Frontend:
Open another terminal and run:
```bash
 streamlit run s_app.py
```

## Access the Chatbot:
Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).

## Configuration
To use Azure OpenAI services, you need to configure the following settings in the code:
```bash
 # Azure OpenAI configuration
 AZURE_OPENAI_API_KEY = "your_api_key"
 AZURE_OPENAI_DEPLOYMENT_ID = "your_deployment_id"
 AZURE_ENDPOINT = "your_endpoint_url"
```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.














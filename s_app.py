import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Query Translator", layout="wide")

# Custom CSS for dark theme and styling
st.markdown("""
    <style>
    /* Dark theme */
    body {
        color: #ffffff;
        background-color: #1e1e1e;
    }
    .stTextArea textarea {
        font-family: monospace;
        font-size: 16px;
        background-color: #262631;
        color: #ffffff;
        border: 1px solid #444;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px;
        border: none;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .result-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #262631;
        margin-top: 10px;
        font-family: monospace;
        font-size: 16px;
        color: #ffffff;
        border: 1px solid #444;
    }
    .stCode {
        background-color: #262631;
        color: #ffffff;
        border-radius: 5px;
        padding: 10px;
        border: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("Query Translator")
st.markdown("Translate your queries between **SQL** and **DAX** effortlessly!")

# Layout: Split into columns
col1, col2 = st.columns(2)

# Left column: Input query and language selection
with col1:
    st.subheader("Input Query")
    query = st.text_area("Enter your query here:", height=200, placeholder="e.g., SELECT * FROM table")

    st.subheader("Target Language")
    target_language = st.selectbox("Choose the language to translate into:", ["SQL", "DAX"])

    if st.button("Translate"):
        if not query:
            st.error("Please enter a query to translate.")
        else:
            # Prepare the payload for the API
            payload = {
                "query": query,
                "target_language": target_language.lower()
            }

            # Make a POST request to the translation endpoint
            try:
                response = requests.post("endpoint/translate", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.translated_query = result.get("translated_query", "")
                    st.session_state.explanation = result.get("explanation", "")
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the translation service: {e}")

# Right column: Display translated query and explanation
with col2:
    if "translated_query" in st.session_state:
        st.subheader("Translated Query")
        st.code(st.session_state.translated_query, language="sql")

    if "explanation" in st.session_state:
        st.subheader("Explanation")
        st.markdown(f'<div class="result-box">{st.session_state.explanation}</div>', unsafe_allow_html=True)
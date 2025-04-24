import os
import json
import streamlit as st
from openai import AzureOpenAI

# Load the JSON file containing product data
with open('data/CAG.json', 'r') as f:
    data = json.load(f)

# Azure OpenAI setup
endpoint = "https://team12hacker03.openai.azure.com/"
model_name = "o3-mini"
deployment = "o3-mini"

subscription_key = "94AyvW2opL0U247mxRKMto6l9m6o6hNmtUxJZFfrVJJc1saq1lDEJQQJ99BDACmepeSXJ3w3AAABACOGzGsW"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# System prompt setup


# Function to process user input and call the OpenAI API
def process_input(user_input, product):

    system_prompt = f"You are a banking assistant. Answer the user's query using only the following information. Responses should be be max 50 words. Text should be displayed in a digestable format using a title and bulleted lists, not just one big block. Use a friendly and professional tone. Information: {data[product]}"

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_input,
            }
        ],
        max_completion_tokens=10000,
        model=deployment
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("Banking Assistant - Choose your product and ask a question")

# User input to select a product (or use a specific question)
user_input = st.text_input("Ask a question about a product or service:")

if user_input:
    # Call the model and show the result
    response = process_input(user_input)
    st.write("Response from the assistant:")
    st.write(response)

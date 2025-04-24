import os
from openai import AzureOpenAI
import json

# Load the JSON file
with open("data/CAG.json", "r") as f:
    data = json.load(f)

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


system_prompt = f"You are a banking assistant. Answer the user's query using only the following information: {data['cashback']}"


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from local HTML


def process_input(user_input, system_prompt):

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_input,
            },
        ],
        max_completion_tokens=100000,
        model=deployment,
    )

    response.choices[0].message.content

    return response.choices[0].message.content


@app.route("/process", methods=["POST"])
def process():
    data = request.json
    user_input = data.get("input")
    result = process_input(user_input)
    return jsonify({"output": result})


if __name__ == "__main__":
    app.run(debug=True)

import os
from openai import AzureOpenAI

# Azure OpenAI API configuration
endpoint = "https://team12hacker03.openai.azure.com/"
model_name = "o3-mini"
deployment = "o3-mini"
subscription_key = "94AyvW2opL0U247mxRKMto6l9m6o6hNmtUxJZFfrVJJc1saq1lDEJQQJ99BDACmepeSXJ3w3AAABACOGzGsW"
api_version = "2024-12-01-preview"

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint, api_key=subscription_key, api_version=api_version
)


# Function to generate text using the Azure OpenAI model
def generate_text(prompt):
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract and return the generated text
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating text: {str(e)}"


# Example usage
if __name__ == "__main__":
    prompt = "Write a short poem about artificial intelligence."
    result = generate_text(prompt)
    print("\nPrompt:", prompt)
    print("\nGenerated text:")
    print(result)

    # You can add more examples here
    prompt2 = "Explain quantum computing in simple terms."
    result2 = generate_text(prompt2)
    print("\nPrompt:", prompt2)
    print("\nGenerated text:")
    print(result2)

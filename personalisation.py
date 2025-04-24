import json
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

# Sample bank products
bank_products = [
    {
        "product_id": "savings_plus",
        "name": "Premium Savings Account",
        "interest_rate": 3.5,
        "min_balance": 5000,
        "monthly_fee": 0,
        "benefits": ["High interest rate", "No monthly fees with minimum balance", "Mobile banking"],
        "suitable_for": ["High-balance savers", "Long-term financial goals"]
    },
    {
        "product_id": "first_time_mortgage",
        "name": "First-Time Homebuyer Mortgage",
        "interest_rate": 4.1,
        "down_payment": 10,
        "term_years": 30,
        "benefits": ["Lower down payment requirement", "Competitive rates", "First-time buyer assistance program"],
        "suitable_for": ["First-time homebuyers", "Good credit history"]
    },
    {
        "product_id": "retirement_fund",
        "name": "Retirement Investment Portfolio",
        "annual_fee": 0.3,
        "min_investment": 10000,
        "benefits": ["Tax advantages", "Diversified investment options", "Retirement planning assistance"],
        "suitable_for": ["Pre-retirement planning", "Long-term wealth preservation"]
    },
    {
        "product_id": "student_loan_refi",
        "name": "Student Loan Refinancing",
        "interest_rate": 3.75,
        "min_credit_score": 680,
        "benefits": ["Lower interest rate", "Flexible repayment terms", "No origination fees"],
        "suitable_for": ["Young professionals with student debt", "Good credit history"]
    },
    {
        "product_id": "education_savings",
        "name": "Education Savings Plan",
        "annual_fee": 0.15,
        "tax_advantages": "Yes",
        "benefits": ["Tax-advantaged growth", "Flexible withdrawals for education expenses", "Gift contribution options"],
        "suitable_for": ["Parents saving for children's education", "Long-term education planning"]
    },
    {
        "product_id": "premium_credit",
        "name": "Premium Rewards Credit Card",
        "annual_fee": 95,
        "rewards_rate": "2-5%",
        "benefits": ["Premium travel rewards", "Purchase protection", "Concierge service"],
        "suitable_for": ["Frequent travelers", "High-income individuals", "Regular credit card users"]
    }
]

def load_customer_profiles(file_path="data/customer_profiles.json"):
    """Load customer profiles from JSON file"""
    try:
        with open(file_path, 'r') as file:
            profiles = json.load(file)
        return profiles
    except Exception as e:
        print(f"Error loading customer profiles: {str(e)}")
        return []

def generate_personalized_recommendations(customer_profile, products):
    """Generate personalized product recommendations using Azure OpenAI"""
    
    # Create a prompt that explains the customer profile and available products
    prompt = f"""
    As a financial advisor, recommend the most suitable banking products for this customer:

    CUSTOMER PROFILE:
    Name: {customer_profile['name']}
    Age: {customer_profile['age']}
    Annual Income: ${customer_profile['annual_income']}
    Credit Score: {customer_profile['credit_score']}
    Account Balance: ${customer_profile['account_balance']}
    Total Debt: ${customer_profile['total_debt']}
    Life Situation: {customer_profile['life_situation']}

    AVAILABLE PRODUCTS:
    {json.dumps(products, indent=2)}

    Please provide:
    1. The top 3 most suitable products for this customer in priority order
    2. For each product, explain why it's a good fit based on their profile
    3. Suggest a personalized marketing message that would resonate with this customer
    
    Use British English. Format your response as JSON with the following structure:
    {{
        "top_recommendations": [
            {{
                "product_id": "...",
                "product_name": "...",
                "reasoning": "...",
                "personalized_message": "..."
            }},
            ...
        ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model=deployment,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a financial advisor specialized in matching banking products to customer needs. Provide thoughtful, personalized recommendations."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract and parse the generated recommendations
        recommendations_json = response.choices[0].message.content
        recommendations = json.loads(recommendations_json)
        return recommendations
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return {"error": str(e)}

def format_recommendations_for_display(recommendations, customer_name):
    """Format recommendations for display to customer"""
    
    if "error" in recommendations:
        return f"Sorry, we encountered an error generating recommendations for {customer_name}: {recommendations['error']}"
    
    result = f"Personalized Recommendations for {customer_name}:\n"
    result += "=" * 50 + "\n\n"
    
    for i, rec in enumerate(recommendations.get("top_recommendations", []), 1):
        result += f"{i}. {rec.get('product_name', 'Unknown Product')}\n"
        result += f"   Why it's right for you: {rec.get('reasoning', '')}\n"
        result += f"   {rec.get('personalized_message', '')}\n\n"
    
    return result

def main():
    # Load customer profiles
    profiles = load_customer_profiles()
    
    if not profiles:
        print("No customer profiles found. Please check the file path.")
        return
    
    # Process each customer profile
    for profile in profiles:
        print(f"\nProcessing recommendations for {profile['name']}...")
        recommendations = generate_personalized_recommendations(profile, bank_products)
        
        # Format and display recommendations
        formatted_recommendations = format_recommendations_for_display(recommendations, profile['name'])
        print(formatted_recommendations)
        
        # Optionally save recommendations to file
        with open(f"recommendations_{profile['profile_id']}.txt", "w") as f:
            f.write(formatted_recommendations)
        
        print(f"Recommendations for {profile['name']} saved to recommendations_{profile['profile_id']}.txt")

if __name__ == "__main__":
    main()
import streamlit as st
import json
import random
from openai import AzureOpenAI

# --- Load Data and Configuration ---
def load_data():
    # Load product data
    with open('data/CAG.json', 'r') as f:
        product_data = json.load(f)
    
    # Load customer profiles
    with open('data/customer_profiles.json', 'r') as f:
        customer_profiles = json.load(f)
    
    return product_data, customer_profiles

# --- Azure OpenAI Setup ---
def get_openai_client():
    endpoint = "https://team12hacker03.openai.azure.com/"
    subscription_key = "94AyvW2opL0U247mxRKMto6l9m6o6hNmtUxJZFfrVJJc1saq1lDEJQQJ99BDACmepeSXJ3w3AAABACOGzGsW"
    api_version = "2024-12-01-preview"
    
    return AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

# --- Personalization Functions ---
def generate_product_ranking(customer_profile, product_data):
    """Rank products based on customer profile using Azure OpenAI"""
    client = get_openai_client()
    
    # Create a prompt that explains the customer profile and available products
    prompt = f"""
    As a financial advisor, rank the following banking products for this customer:

    CUSTOMER PROFILE:
    Name: {customer_profile['name']}
    Age: {customer_profile['age']}
    Annual Income: £{customer_profile['annual_income']}
    Credit Score: {customer_profile['credit_score']}
    Account Balance: £{customer_profile['account_balance']}
    Total Debt: £{customer_profile['total_debt']}
    Life Situation: {customer_profile['life_situation']}

    AVAILABLE PRODUCTS:
    1. club-lloyds: A premium current account with lifestyle benefits
    2. ready-made-investments: Investment portfolios managed by experts
    3. mortgage: Home loan products including first-time buyer options
    4. savings-plan: Savings accounts with competitive interest rates and cashback

    For each product, rate its suitability for this customer on a scale of 1-10.
    Provide a brief explanation (max 30 words) of why the product is or isn't suitable.
    
    Format your response as JSON with the following structure:
    {{
        "rankings": [
            {{
                "product_id": "...",
                "score": 0-10,
                "explanation": "..."
            }},
            ...
        ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="o3-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a financial advisor specialized in matching banking products to customer needs."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract and parse the generated recommendations
        rankings_json = response.choices[0].message.content
        rankings = json.loads(rankings_json)
        
        # Sort by score in descending order
        rankings["rankings"].sort(key=lambda x: x["score"], reverse=True)
        
        return rankings
    except Exception as e:
        print(f"Error generating rankings: {str(e)}")
        
        # Fallback to a simple ranking if API fails
        return {
            "rankings": [
                {"product_id": "club-lloyds", "score": 7, "explanation": "Good all-around product with lifestyle benefits."},
                {"product_id": "ready-made-investments", "score": 6, "explanation": "Suitable for long-term financial goals."},
                {"product_id": "mortgage", "score": 5, "explanation": "Depends on housing needs."},
                {"product_id": "savings-plan", "score": 8, "explanation": "Everyone benefits from saving more."}
            ]
        }

def get_product_details(product_id, product_full_data):
    """Extract product details in a structured format"""
    product_text = product_full_data.get(product_id, "")
    
    # Use a simplified mapping for demo purposes
    product_info = {
        "club-lloyds": {
            "name": "Club Lloyds",
            "short_description": "For variable credit interest, no debit card fees abroad and great perks",
            "image": "💳",
        },
        "ready-made-investments": {
            "name": "Ready-Made Investments",
            "short_description": "Investments built and managed by our experts",
            "image": "📈",
        },
        "mortgage": {
            "name": "Mortgages",
            "short_description": "Find the right mortgage for your needs",
            "image": "🏡",
        },
        "savings-plan": {
            "name": "Cashback & Savings",
            "short_description": "Get up to 15% cashback on your everyday spending",
            "image": "💰",
        },
    }
    
    return product_info.get(product_id, {"name": product_id, "short_description": "Learn more", "image": "📋"})

def get_product_explanation(customer_profile, product_id, product_data, explanation=None):
    """Generate a personalized explanation for why this product is recommended"""
    client = get_openai_client()
    
    if explanation:
        return explanation
    
    # If no explanation provided, generate one
    prompt = f"""
    Create a personalized explanation for why the '{product_id}' product is recommended for this customer:
    
    CUSTOMER PROFILE:
    Name: {customer_profile['name']}
    Age: {customer_profile['age']}
    Annual Income: £{customer_profile['annual_income']}
    Life Situation: {customer_profile['life_situation']}
    
    Keep it brief (max 40 words) and highlight specific benefits relevant to their situation.
    """
    
    try:
        response = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a financial advisor providing brief, personalized product recommendations."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating explanation: {str(e)}")
        return "This product aligns with your financial goals and situation."

# --- Generate Product Q&A ---
def process_product_query(query, product_id, product_data):
    """Process user queries about products using Azure OpenAI"""
    client = get_openai_client()
    
    product_info = product_data.get(product_id, "No information available")
    
    system_prompt = f"""
    You are a banking assistant. Answer the user's query using only the following information. 
    Responses should be max 50 words. Text should be displayed in a digestable format using a title and bulleted lists,
    not just one big block. Use a friendly and professional tone.
    
    Information: {product_info}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model="o3-mini",
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        return "I'm sorry, I couldn't process that query. Please try again."

# --- Main Application ---
def main():
    st.set_page_config(page_title="LBG Perks", layout="centered")
    
    # Load data
    product_data, customer_profiles = load_data()
    
    # Session state initialization
    if "selected_profile" not in st.session_state:
        st.session_state.selected_profile = None
    if "rankings" not in st.session_state:
        st.session_state.rankings = None
    if "viewed" not in st.session_state:
        st.session_state.viewed = set()
    
    # Sidebar for profile selection
    with st.sidebar:
        st.title("👤 Choose Your Profile")
        
        profile_options = {p["profile_id"]: f"{p['name']}, {p['age']} - {p['life_situation'].split('.')[0]}" 
                          for p in customer_profiles}
        
        selected_id = st.selectbox("Select a customer profile:", 
                                  options=list(profile_options.keys()),
                                  format_func=lambda x: profile_options[x])
        
        # Get the full profile
        selected_profile = next((p for p in customer_profiles if p["profile_id"] == selected_id), None)
        st.session_state.selected_profile = selected_profile
        
        if st.button("Generate Recommendations"):
            rankings = generate_product_ranking(selected_profile, product_data)
            st.session_state.rankings = rankings
            st.rerun()
    
    # Get query params for product detail view
    query_params = st.query_params
    selected_product_id = query_params.get("product")
    
    # Main content
    if selected_product_id:
        # Product Detail View
        product_details = get_product_details(selected_product_id, product_data)
        
        st.header(f"{product_details['image']} {product_details['name']}")
        
        # Mark this product as viewed
        st.session_state.viewed.add(selected_product_id)
        
        # Show personalized recommendation reason if available
        if st.session_state.rankings:
            product_ranking = next((r for r in st.session_state.rankings["rankings"] 
                                  if r["product_id"] == selected_product_id), None)
            
            if product_ranking:
                st.info(f"**Why we recommended this for you:** {product_ranking['explanation']}")
        
        # Tabs for different product information
        tab1, tab2 = st.tabs(["Product Details", "Ask a Question"])
        
        with tab1:
            st.markdown("### Product Information")
            
            # Extract first few paragraphs for a summary
            product_text = product_data.get(selected_product_id, "No information available")
            summary = product_text.split(".", 3)[:3]
            summary = ". ".join(summary) + "."
            
            st.write(summary)
            
            with st.expander("View Full Details"):
                st.write(product_text)
        
        with tab2:
            st.markdown("### Have a Question?")
            question = st.text_input("Ask about this product:")
            
            if question:
                answer = process_product_query(question, selected_product_id, product_data)
                st.write(answer)
        
        if st.button("⬅️ Back to recommendations"):
            st.query_params.clear()
            st.rerun()
            
    else:
        # Main recommendation view
        st.title("💼 Your Personalized LBG Products")
        
        if st.session_state.selected_profile:
            st.markdown(f"### 👋 Welcome, {st.session_state.selected_profile['name']}")
            
            if not st.session_state.rankings:
                st.info("Click 'Generate Recommendations' in the sidebar to get personalized product suggestions.")
            else:
                st.success(f"Here are your personalized product recommendations:")
                
                # Display ranked products as cards
                for rank, product in enumerate(st.session_state.rankings["rankings"]):
                    product_id = product["product_id"]
                    product_details = get_product_details(product_id, product_data)
                    is_viewed = product_id in st.session_state.viewed
                    
                    # Create a visual indicator of personalization score
                    score = product["score"]
                    score_display = "🟢" * int(score/2) + "⚪" * (5-int(score/2))
                    
                    # Create a card-like display with colored background based on rank
                    card_bg = "#e8f5e9" if rank == 0 else "#f9f9f9"
                    card_border = "2px solid #4CAF50" if rank == 0 else "1px solid #ddd"
                    
                    st.markdown(f"""
                    <a href="?product={product_id}" style="text-decoration: none; color: inherit;">
                        <div style="border: {card_border}; border-radius: 10px; padding: 16px; margin-bottom: 16px; background-color: {card_bg};">
                            <h3 style="margin-top:0;">
                                {product_details['image']} {product_details['name']} 
                                {"✅" if is_viewed else ""}
                            </h3>
                            <p><b>Match score:</b> {score_display} ({score}/10)</p>
                            <p style="margin-bottom:4px;">{product_details['short_description']}</p>
                            <p><b>Why it's for you:</b> {product['explanation']}</p>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                
                # Stats about viewed products
                if st.session_state.viewed:
                    st.info(f"You've viewed {len(st.session_state.viewed)} of {len(st.session_state.rankings['rankings'])} recommended products.")
        else:
            st.info("Please select a customer profile from the sidebar to get started.")

if __name__ == "__main__":
    main()
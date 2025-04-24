import streamlit as st
import random
import json
from app import process_input
from openai import AzureOpenAI

# --- Load Data ---
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

# --- Personalization Function ---
def generate_product_ranking(customer_profile, available_products):
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
    {', '.join([p['id'] for p in available_products])}

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
                {"product_id": p["id"], "score": random.randint(5, 9), 
                 "explanation": "This product might be suitable for your needs."} 
                for p in available_products
            ]
        }

# --- Session State ---
if "viewed" not in st.session_state:
    st.session_state.viewed = set()
if "ratings" not in st.session_state:
    st.session_state.ratings = {}
if "reviews" not in st.session_state:
    st.session_state.reviews = {}
if "show_reviews" not in st.session_state:
    st.session_state.show_reviews = {}
if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = None
if "rankings" not in st.session_state:
    st.session_state.rankings = None

# --- Product Data ---
def load_products():
    return [
        {
            "id": "mortgage",
            "name": "Mortgage",
            "description": "Great for home buyers",
            "public_info": "Our award-winning mortgage service offers competitive interest rates and flexible repayment options.",
            "colleague_benefit": "As an LBG colleague, you get **1.5% fixed interest** and **zero down payment**."
        },
        {
            "id": "club-lloyds",
            "name": "Club Lloyds",
            "description": "Enjoy perks with Club Lloyds banking",
            "public_info": "Club Lloyds offers lifestyle rewards, cashback, and fee-free overdrafts.",
            "colleague_benefit": "Colleagues get **double cashback offers** and **priority customer service**."
        },
        {
            "id": "savings-plan",
            "name": "Savings Plan",
            "description": "Ideal for saving more",
            "public_info": "A smart savings product with auto deposits and interest bonuses.",
            "colleague_benefit": "LBG matches your savings by **5% every month**, up to £100."
        },
        {
            "id": "ready-made-investments",
            "name": "Ready-Made Investments",
            "description": "Expert-managed investments to match your goals",
            "public_info": "Let experts manage your money with flexible options based on your risk profile. Start from just £50/month.",
            "colleague_benefit": "As a colleague, enjoy a **simplified onboarding journey** and **discounted investment management fees**."
        }
    ]

# --- Dummy Reviews ---
dummy_reviews = {
    "mortgage": [
        ("Emma", "Helped me buy my first home with peace of mind."),
        ("Jack", "Super flexible options. Recommended."),
    ],
    "club-lloyds": [
        ("Liam", "Love the double cashback – it's a no brainer."),
        ("Sophie", "Very useful for travel perks."),
    ],
    "savings-plan": [
        ("James", "The employer match makes saving easy."),
        ("Olivia", "I've saved more in 6 months than I expected!"),
    ],
    "ready-made-investments": [
        ("Mark", "Great way to invest without stress."),
        ("Amelia", "The expert management is worth it."),
    ]
}

# --- Stats Generator ---
def get_product_stats(product_id):
    random.seed(product_id)
    return {
        "rating": round(random.uniform(3.8, 4.9), 1),
        "votes": random.randint(80, 500)
    }

# --- Draw Clickable Stars ---
def draw_star_rating(product_id):
    current_rating = st.session_state.ratings.get(product_id, 0)
    cols = st.columns(5)
    for i in range(1, 6):
        star = "⭐" if i <= current_rating else "☆"
        if cols[i - 1].button(star, key=f"star_{product_id}_{i}"):
            st.session_state.ratings[product_id] = i
            st.rerun()

# --- Setup ---
st.set_page_config(page_title="Your LBG Perks", layout="centered")
query_params = st.query_params
selected_product_id = query_params.get("product")

# Load data
all_products = load_products()
product_data, customer_profiles = load_data()

# --- Sidebar for customer profile selection ---
with st.sidebar:
    st.title("👤 Customer Profile")
    
    profile_options = {p["profile_id"]: f"{p['name']}, {p['age']} - {p['life_situation'].split('.')[0]}" 
                      for p in customer_profiles}
    
    selected_id = st.selectbox("Select a profile:", 
                              options=list(profile_options.keys()),
                              format_func=lambda x: profile_options[x])
    
    # Get the full profile
    selected_profile = next((p for p in customer_profiles if p["profile_id"] == selected_id), None)
    st.session_state.selected_profile = selected_profile
    
    # Generate recommendations when profile changes or button is clicked
    if st.button("Update Recommendations") or (selected_profile and selected_profile != st.session_state.get("last_profile")):
        st.session_state.rankings = generate_product_ranking(selected_profile, all_products)
        st.session_state["last_profile"] = selected_profile

# --- Product Detail View ---
if selected_product_id:
    product = next((p for p in all_products if p["id"] == selected_product_id), None)
    if product:
        st.session_state.viewed.add(product["id"])

        st.header(product["name"])
        st.markdown("### 🌍 What this product is")
        st.write(product["public_info"])

        st.markdown("### 💼 What this means for colleagues")
        st.markdown(product["colleague_benefit"])
        
        # Show personalized recommendation reason if available
        if st.session_state.rankings:
            product_ranking = next((r for r in st.session_state.rankings["rankings"] 
                                 if r["product_id"] == selected_product_id), None)
            
            if product_ranking:
                st.info(f"**Why this might be good for {st.session_state.selected_profile['name']}:** {product_ranking['explanation']}")

        # Assistant
        st.markdown("### 🤖 Ask the assistant")
        question = st.text_input("Ask a question about this product")
        if question:
            response = process_input(question, product['id'])
            st.write("Response from the assistant:")
            st.write(response)

        # Ratings
        stats = get_product_stats(product["id"])
        user_rating = st.session_state.ratings.get(product["id"])

        if user_rating:
            updated_votes = stats["votes"] + 1
            updated_rating = round((stats["rating"] * stats["votes"] + user_rating) / updated_votes, 1)
        else:
            updated_votes = stats["votes"]
            updated_rating = stats["rating"]

        st.markdown(f"**⭐ {updated_rating} / 5** from **{updated_votes}** colleagues")
        st.markdown("### ⭐ Rate this product")
        draw_star_rating(product["id"])

        # Reviews
        if product["id"] not in st.session_state.reviews:
            st.session_state.reviews[product["id"]] = dummy_reviews.get(product["id"], [])
        if product["id"] not in st.session_state.show_reviews:
            st.session_state.show_reviews[product["id"]] = True

        st.markdown("### 📝 Leave a Review")
        review = st.text_area("Write your review", key=f"review_input_{product['id']}")
        
        col1, col2 = st.columns([1, 3])
        user_name = st.session_state.selected_profile['name'] if st.session_state.selected_profile else "User"
        
        with col1:
            if st.button("Submit Review", key=f"submit_review_{product['id']}"):
                if review.strip():
                    st.session_state.reviews[product["id"]].append((user_name, review.strip()))
                    st.success("Thanks for your review!")
                    st.session_state.show_reviews[product["id"]] = True
                else:
                    st.warning("Please write something before submitting.")

        # Toggle review visibility
        toggle = st.checkbox("💬 Show reviews", value=st.session_state.show_reviews[product["id"]],
                             key=f"toggle_reviews_{product['id']}")
        st.session_state.show_reviews[product["id"]] = toggle

        if toggle:
            st.markdown("**💬 What others are saying:**")
            for i, (reviewer, text) in enumerate(st.session_state.reviews[product["id"]]):
                col1, col2 = st.columns([0.85, 0.15])
                with col1:
                    st.markdown(f"> **{reviewer}**: {text}")
                if reviewer == user_name:
                    with col2:
                        if st.button("❌", key=f"del_{product['id']}_{i}"):
                            st.session_state.reviews[product["id"]].pop(i)
                            st.rerun()

        if st.button("⬅️ Back to all perks"):
            st.query_params.clear()
            st.rerun()

# --- Main Page ---
else:
    # Default user name if no profile selected yet
    user_name = st.session_state.selected_profile['name'] if st.session_state.selected_profile else "there"
    
    st.markdown(f"### 👋 Welcome, {user_name}")
    st.info(f"🧭 You've viewed **{len(st.session_state.viewed)}** product(s) so far.")
    
    # Show profile-specific message if profile is selected
    if st.session_state.selected_profile:
        profile = st.session_state.selected_profile
        st.success(f"Showing personalized recommendations for {profile['name']}, {profile['age']} - {profile['life_situation'].split('.')[0]}")
    
    # If we have rankings, use them to sort products, otherwise use the original order
    if st.session_state.rankings:
        # Create a mapping of product_id to score
        scores = {r["product_id"]: r["score"] for r in st.session_state.rankings["rankings"]}
        
        # Sort products by their scores
        sorted_products = sorted(
            all_products, 
            key=lambda p: scores.get(p["id"], 0), 
            reverse=True
        )
    else:
        sorted_products = all_products
    
    # Display products
    for product in sorted_products:
        stats = get_product_stats(product["id"])
        link = f"/?product={product['id']}"
        
        # Get personalization score and explanation if available
        score_display = ""
        explanation = ""
        
        if st.session_state.rankings:
            product_ranking = next((r for r in st.session_state.rankings["rankings"] 
                                 if r["product_id"] == product["id"]), None)
            if product_ranking:
                score = product_ranking["score"]
                explanation = product_ranking["explanation"]
                # Visual score representation
                score_display = "🟢" * int(score/2) + "⚪" * (5-int(score/2))

        # Determine card styling based on ranking
        if st.session_state.rankings:
            top_product = st.session_state.rankings["rankings"][0]["product_id"] == product["id"]
            card_bg = "#e8f5e9" if top_product else "#f9f9f9"
            card_border = "2px solid #005a30" if top_product else "1px solid #ccc"
        else:
            card_bg = "#f9f9f9"
            card_border = "1px solid #ccc"
            
        # Create a card with additional personalization information
        st.markdown(f"""
        <a href="{link}" style="text-decoration: none; color: inherit;">
            <div style="border: {card_border}; border-radius: 10px; padding: 16px; margin-bottom: 16px; background-color: {card_bg};">
                <h4 style="color:#005a30;">{product['name']} {"✅" if product["id"] in st.session_state.viewed else ""}</h4>
                <p style="margin:0;color:#444;">{product['description']}</p>
                <p style="margin:4px 0 0 0;"><strong>⭐ {stats['rating']} / 5</strong> from {stats['votes']} votes</p>
                {f'<p style="margin-top:8px;"><strong>Match for {user_name}:</strong> {score_display}</p>' if score_display else ''}
                {f'<p style="margin-top:4px;color:#444;"><em>Why: {explanation}</em></p>' if explanation else ''}
            </div>
        </a>
        """, unsafe_allow_html=True)
import streamlit as st
import random

# --- Simulated user info ---
user_name = "Alex"
user_segment = "Family Planner"

# --- Segment Mapping ---
segment_map = {
    "Young Ambitious": ["club-card", "savings-plan"],
    "Family Planner": ["mortgage", "savings-plan", "club-card"],
    "Lifestyle Seeker": ["club-card"]
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
            "id": "club-card",
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
        }
    ]

# --- Dummy Reviews ---
dummy_reviews = {
    "mortgage": [
        ("Emma", "Helped me buy my first home with peace of mind."),
        ("Jack", "Super flexible options. Recommended."),
    ],
    "club-card": [
        ("Liam", "Love the double cashback – it's a no brainer."),
        ("Sophie", "Very useful for travel perks."),
    ],
    "savings-plan": [
        ("James", "The employer match makes saving easy."),
        ("Olivia", "I've saved more in 6 months than I expected!"),
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

all_products = load_products()

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

        # Assistant
        st.markdown("### 🤖 Ask the assistant")
        question = st.text_input("Ask a question about this product")
        if question:
            st.info(f"Assistant: Thanks for your question — we’ll get back to you shortly!")

        # Reviews
        if product["id"] not in st.session_state.reviews:
            st.session_state.reviews[product["id"]] = dummy_reviews.get(product["id"], [])
        if product["id"] not in st.session_state.show_reviews:
            st.session_state.show_reviews[product["id"]] = True

        st.markdown("### 📝 Leave a Review")
        review = st.text_area("Write your review", key=f"review_input_{product['id']}")
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
    st.markdown(f"### 👋 Welcome, {user_name}")
    st.info(f"🧭 You’ve viewed **{len(st.session_state.viewed)}** product(s) so far.")
    matched = [p for p in all_products if p["id"] in segment_map[user_segment]]

    for product in matched:
        stats = get_product_stats(product["id"])
        link = f"/?product={product['id']}"

        st.markdown(f"""
        <a href="{link}" style="text-decoration: none;">
            <div style="border: 1px solid #ccc; border-radius: 10px; padding: 16px; margin-bottom: 16px; background-color: #f9f9f9;">
                <h4 style="color:#005a30;">{product['name']}</h4>
                <p style="margin:0;color:#444;">{product['description']}</p>
                <p style="margin:4px 0 0 0;"><strong>⭐ {stats['rating']} / 5</strong> from {stats['votes']} votes</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

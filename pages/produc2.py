import streamlit as st
import random

# --- Product Data ---
def load_products():
    return [
        {"id": "mortgage", "name": "Mortgage", "description": "Great for home buyers"},
        {"id": "club-card", "name": "Club Card", "description": "Perfect for lifestyle perks"},
        {"id": "savings-plan", "name": "Savings Plan", "description": "Ideal for saving more"}
    ]

# --- Assign Segment Based on Onboarding ---
def assign_segment(age, goal):
    if age in ["18-24", "25-34"] and goal == "Enjoy lifestyle perks":
        return "Young Ambitious"
    elif goal == "Buy a home":
        return "Family Planner"
    else:
        return "Lifestyle Seeker"

# --- Simulate Ratings and Popularity ---
def get_product_stats(product_id):
    random.seed(product_id)  # ensures consistent ratings across sessions
    return {
        "rating": round(random.uniform(3.8, 4.9), 1),
        "votes": random.randint(80, 500),
        "popularity": round(random.uniform(0.5, 1.0), 2)
    }

# --- App Setup ---
st.set_page_config(page_title="Colleague Perks", layout="wide")
st.title("💼 Financial Perks for Colleagues")

# --- Step Management ---
if "stage" not in st.session_state:
    st.session_state.stage = "onboarding"

# --- Onboarding Screen ---
if st.session_state.stage == "onboarding":
    st.header("🧬 Help us personalise your experience")
    
    age = st.selectbox("Your age group", ["18-24", "25-34", "35-50", "50+"])
    goal = st.radio("Primary financial goal?", ["Save more", "Buy a home", "Enjoy lifestyle perks"])
    
    if st.button("Show My Perks"):
        st.session_state.age = age
        st.session_state.goal = goal
        st.session_state.segment = assign_segment(age, goal)
        st.session_state.stage = "results"
        st.rerun()

# --- Results Screen ---
elif st.session_state.stage == "results":
    st.success(f"🎯 Based on your profile, you're a **{st.session_state.segment}**")
    st.write("Here are some perks that match your needs:")

    # Load and filter products
    all_products = load_products()
    segment_map = {
        "Young Ambitious": ["club-card", "savings-plan"],
        "Family Planner": ["mortgage", "savings-plan"],
        "Lifestyle Seeker": ["club-card"]
    }

    matched_products = [p for p in all_products if p["id"] in segment_map[st.session_state.segment]]
    cols = st.columns(len(matched_products))

    for i, product in enumerate(matched_products):
        with cols[i]:
            stats = get_product_stats(product["id"])
            st.markdown(f"""
                <div style='background-color:#e8f5e9;padding:20px;border-radius:12px;margin-bottom:15px;'>
                    <h4>{product['name']}</h4>
                    <p style='font-size:14px;'>{product['description']}</p>
                    <p>⭐ {stats['rating']} / 5 from {stats['votes']} votes</p>
                    <p>📈 Popularity Score:</p>
                </div>
            """, unsafe_allow_html=True)
            st.progress(stats["popularity"])

    # Back or Share
    st.markdown("---")
    if st.button("🔁 Start Again"):
        st.session_state.stage = "onboarding"
        st.rerun()
    
    st.markdown("🔗 [Share this app](https://your-streamlit-app-url) with a colleague!")


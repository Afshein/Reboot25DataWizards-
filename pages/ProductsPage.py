import streamlit as st
import json

# Load product data
def load_products():
    return [
        {"id": "mortgage", "name": "Mortgage", "description": "Special rates for employees."},
        {"id": "club-card", "name": "Club Card", "description": "Earn points on all purchases."},
        {"id": "savings-plan", "name": "Savings Plan", "description": "5% employer match on savings."}
    ]

# App config
st.set_page_config(page_title="Colleague Perks")
st.title("💼 Financial Perks for Colleagues")

<<<<<<< HEAD
# Sidebar filter
with st.sidebar:
    st.header("Find what suits you 🔍")
    wants_home = st.checkbox("🏡 I'm planning to buy a home")
    wants_rewards = st.checkbox("🎁 I want perks on spending")
    wants_savings = st.checkbox("💰 I want to grow my savings")


# Layout: 3 columns for card-style buttons
all_products = load_products()
# Filter logic
products = [
    p for p in all_products
    if (wants_home and p['id'] == 'mortgage') or
       (wants_rewards and p['id'] == 'club-card') or
       (wants_savings and p['id'] == 'savings-plan') or
       (not any([wants_home, wants_rewards, wants_savings]))
]

cols = st.columns(3)

for index, product in enumerate(products):
    with cols[index % 3]:
        st.markdown(f"""
            <div style='background-color:#d4edda;padding:20px;border-radius:12px;margin-bottom:15px;'>
                <h4>{product['name']}</h4>
                <p style='font-size:14px;'>{product['description']}</p>
                <form action="?product={product['id']}" method="get">
                    <input type="submit" value="View" style="background-color:#28a745;border:none;padding:8px 16px;color:white;border-radius:6px;">
                </form>
            </div>
        """, unsafe_allow_html=True)
        
        
st.markdown("---")
st.subheader("📢 Share your experience")

story = st.text_area("What do you love about a product? Share a tip!")
if st.button("Submit your story"):
    st.success("Thanks for sharing your experience! 🙌")

st.markdown("🔗 Want to tell a colleague about this? [Copy & share this link](https://your-streamlit-app-url)")
if len(products) >= 3:
    st.success("🏅 Perk Explorer: You viewed 3 or more perks today!")
=======

products = load_products()


for product in products:
    # Just for demo purposes – simulate a rating (1 to 5)
    rating = product.get("rating", 4)  # or random.randint(1, 5)

    stars = "⭐" * rating + "☆" * (5 - rating)  # Optional: filled + empty stars

    st.markdown(f"""
        <form action="" method="get" style="margin:0;">
            <input type="hidden" name="product" value="{product['id']}"/>
            <button type="submit" style="
                display: flex;
                align-items: center;
                background-color:#006a4d;
                border:none;
                padding:20px;
                border-radius:12px;
                margin-bottom:15px;
                width:100%;
                text-align:left;
                cursor:pointer;
            ">
                <div style="margin-right:20px; font-size:18px; min-width:80px;">
                    {stars}
                </div>
                <div style="flex-grow:1; text-align:left;">
                    <h4 style="margin:0;">{product['name']}</h4>
                    <p style='font-size:14px;margin:8px 0 0;'>{product['description']}</p>
                </div>
            </button>
        </form>
    """, unsafe_allow_html=True)

>>>>>>> f7ddbedf87b573ffe50bad9dcc07cb212ed6b3f2


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



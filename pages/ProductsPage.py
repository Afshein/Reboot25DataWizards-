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
st.set_page_config(page_title="Colleague Perks", layout="wide")
st.title("💼 Financial Perks for Colleagues")

# Layout: 3 columns for card-style buttons
products = load_products()
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

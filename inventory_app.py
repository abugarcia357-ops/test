import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Product Inventory Analysis System",
    layout="wide"
)

st.title("Online Store Product Inventory Analysis System")

if "inventory_data" not in st.session_state:
    st.session_state["inventory_data"] = []

st.header("Product Entry Form")

with st.form("inventory_form"):
    product_name = st.text_input("Product Name")
    product_category = st.selectbox(
        "Product Category",
        ["Electronics", "Clothing", "Accessories"]
    )
    stock_quantity_str = st.text_input("Stock Quantity")
    
    submit_button = st.form_submit_button("Process Inventory")

if submit_button:
    validation_passed = True
    
    if not product_name.strip():
        st.error("Error: Product Name cannot be empty.")
        validation_passed = False

    try:
        stock_quantity = int(stock_quantity_str)
        if stock_quantity < 0:
            st.error("Error: Stock Quantity cannot be negative.")
            validation_passed = False
    except ValueError:
        st.error("Error: Stock Quantity must be a valid integer.")
        validation_passed = False

    if validation_passed:
        st.success(f"Successfully processed: {product_name} | Category: {product_category} | Quantity: {stock_quantity}")
        
        st.session_state["inventory_data"].append({
            "Product Name": product_name.strip(),
            "Category": product_category,
            "Quantity": stock_quantity
        })

st.divider()
st.header("Inventory Analysis and Reports")

if len(st.session_state["inventory_data"]) > 0:
    current_data = st.session_state["inventory_data"]
else:
    
    current_data = [
        {"Product Name": "Laptop", "Category": "Electronics", "Quantity": 30},
        {"Product Name": "T-Shirt", "Category": "Clothing", "Quantity": 15},
        {"Product Name": "Watch", "Category": "Accessories", "Quantity": 8},
        {"Product Name": "Headphones", "Category": "Electronics", "Quantity": 25}
    ]

quantities = [item["Quantity"] for item in current_data]
quantities_array = np.array(quantities)

st.subheader("NumPy Stock Analysis")
total_stock = np.sum(quantities_array)
min_stock = np.min(quantities_array)
below_20_count = np.sum(quantities_array < 20)

col1, col2, col3 = st.columns(3)
col1.metric("Total Stock Quantity", total_stock)
col2.metric("Minimum Stock Quantity", min_stock)
col3.metric("Stock Below 20 Units", below_20_count)

st.subheader("Inventory Status Report")

df = pd.DataFrame(current_data)

def classify_stock(qty):
    if qty >= 20:
        return "Sufficient"
    elif 1 <= qty <= 19:
        return "Low Stock"
    else:
        return "Out of Stock"

df["Stock Status"] = df["Quantity"].apply(classify_stock)

st.write("Complete Inventory DataFrame:")
st.dataframe(df, use_container_width=True)

st.subheader("Filtered Products (Stock Quantity < 20)")
low_stock_df = df[df["Quantity"] < 20]
if not low_stock_df.empty:
    st.dataframe(low_stock_df, use_container_width=True)
else:
    st.write("No products currently have stock below 20 units.")

st.subheader("Category-Based Analysis")

grouped_df = df.groupby("Category")["Quantity"].sum().reset_index()
grouped_df.rename(columns={"Quantity": "Total Stock Quantity"}, inplace=True)

st.write("Grouped Inventory Data by Category:")
st.dataframe(grouped_df, use_container_width=True)

st.subheader("Total Stock Quantity by Category (Chart)")
chart_data = grouped_df.set_index("Category")
st.bar_chart(chart_data)
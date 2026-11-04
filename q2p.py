
# File Name: inventory_app.py

import streamlit as st
import numpy as np
import pandas as pd

# QUESTION 2(a) - STREAMLIT INTERFACE

st.title("Online Store Product Inventory Analysis System")

if "products" not in st.session_state:
    st.session_state.products = []

product_name = st.text_input("Enter Product Name")

category = st.selectbox(
    "Select Product Category",
    ["Electronics", "Clothing", "Accessories"]
)

quantity_input = st.text_input("Enter Stock Quantity")

# QUESTION 2(b) - EXCEPTION HANDLING

if st.button("Process Inventory"):
    try:
        if product_name.strip() == "":
            raise ValueError("Product name cannot be empty.")

        quantity = int(quantity_input)

        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        product = {
            "Product Name": product_name.strip(),
            "Category": category,
            "Quantity": quantity
        }

        st.session_state.products.append(product)
        st.success("Product added successfully!")

    except ValueError as e:
        st.error(f"Invalid input: {e}")

if len(st.session_state.products) > 0:

    # QUESTION 2(d) - PANDAS DATAFRAME

    df = pd.DataFrame(st.session_state.products)

    def classify_stock(quantity):
        if quantity >= 20:
            return "Sufficient"
        elif quantity >= 1:
            return "Low Stock"
        else:
            return "Out of Stock"

    df["Stock Status"] = df["Quantity"].apply(classify_stock)

    st.subheader("Product Inventory Data")
    st.dataframe(df)

    # QUESTION 2(c) - NUMPY ANALYSIS

    stock_quantities = np.array(df["Quantity"])

    total_stock = np.sum(stock_quantities)
    minimum_stock = np.min(stock_quantities)
    low_stock_count = np.sum(stock_quantities < 20)

    st.subheader("NumPy Inventory Analysis")
    st.write("Total Stock:", int(total_stock))
    st.write("Minimum Stock:", int(minimum_stock))
    st.write("Products Below 20 Units:", int(low_stock_count))

    # QUESTION 2(d) - FILTERING

    low_stock_df = df[df["Quantity"] < 20]

    st.subheader("Products Below 20 Units")
    st.dataframe(low_stock_df)

    # QUESTION 2(e) - GROUPING

    category_summary = (
        df.groupby("Category")["Quantity"]
        .sum()
        .reset_index()
    )

    st.subheader("Total Stock by Category")
    st.dataframe(category_summary)

    # QUESTION 2(e) - VISUALIZATION

    st.subheader("Inventory Bar Chart")
    st.bar_chart(
        category_summary.set_index("Category")["Quantity"]
    )

else:
    st.info("Please enter a product to begin inventory analysis.")

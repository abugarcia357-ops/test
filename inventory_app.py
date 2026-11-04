import numpy as np
import pandas as pd
import streamlit as st


CATEGORIES = ["Electronics", "Clothing", "Accessories"]


def get_stock_status(quantity):
	if quantity >= 20:
		return "Sufficient"
	if quantity >= 1:
		return "Low Stock"
	return "Out of Stock"


st.set_page_config(page_title="Product Inventory Analysis", page_icon="📦")
st.title("Online Store Product Inventory Analysis System")
st.write("Add products to manage inventory and review stock levels.")

if "products" not in st.session_state:
	st.session_state["products"] = []

with st.form("product_entry", clear_on_submit=True):
	product_name = st.text_input("Product Name")
	product_category = st.selectbox("Product Category", CATEGORIES)
	stock_quantity = st.text_input("Stock Quantity", placeholder="Enter a whole number")
	submitted = st.form_submit_button("Process Inventory")

if submitted:
	if not product_name.strip():
		st.error("Product Name cannot be empty.")
	else:
		try:
			quantity = int(stock_quantity.strip())
			if quantity < 0:
				st.error("Stock Quantity cannot be negative.")
			else:
				product = {
					"Product Name": product_name.strip(),
					"Category": product_category,
					"Quantity": quantity,
				}
				st.session_state["products"].append(product)
				st.success("Product information entered successfully.")
				st.write("Added product:", product)
		except (ValueError, AttributeError):
			st.error("Enter a valid whole number for Stock Quantity.")

if st.session_state["products"]:
	st.subheader("Inventory Analysis")
	inventory = pd.DataFrame(st.session_state["products"])
	inventory["Stock Status"] = inventory["Quantity"].apply(get_stock_status)

	quantities = inventory["Quantity"].to_numpy(dtype=int)
	col1, col2, col3 = st.columns(3)
	col1.metric("Total Stock Quantity", int(np.sum(quantities)))
	col2.metric("Minimum Stock Quantity", int(np.min(quantities)))
	col3.metric("Products Below 20 Units", int(np.count_nonzero(quantities < 20)))

	st.subheader("Complete Product Inventory")
	st.dataframe(inventory, use_container_width=True, hide_index=True)

	st.subheader("Products Below 20 Units")
	low_stock = inventory[ inventory["Quantity"] < 20 ]
	if low_stock.empty:
		st.info("There are no products below 20 units.")
	else:
		st.dataframe(low_stock, use_container_width=True, hide_index=True)

	st.subheader("Inventory by Category")
	category_totals = (
		inventory.groupby("Category")["Quantity"]
		.sum()
		.reindex(CATEGORIES, fill_value=0)
		.rename("Total Stock Quantity")
	)
	st.dataframe(category_totals, use_container_width=True)
	st.bar_chart(category_totals)
else:
	st.info("No products have been added yet. Enter a product to see inventory reports.")

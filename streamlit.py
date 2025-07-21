import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

BACKEND_URL = "http://127.0.0.1:5000"

st.title("Delivery Prediction App")

page = st.sidebar.radio("📂 Select Page", ["Dataset Preview", "Predict Delivery"])

# Dataset Preview
if page == "Dataset Preview":
    st.subheader("Dataset Preview")
    try:
        response = requests.get(f"{BACKEND_URL}/data")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            st.dataframe(df)

            st.markdown("---")
            st.info("👈 Klik menu **Predict Delivery** di sidebar untuk masuk ke halaman prediksi.")
        else:
            st.error(f"Failed to load data. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

# Predict Delivery
elif page == "Predict Delivery":
    st.subheader("Predict Delivery Time")

    # Load dataset untuk mengambil nilai unik sebagai opsi selectbox
    try:
        response = requests.get(f"{BACKEND_URL}/data")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            # Ambil opsi unik
            market_options = sorted(df["market_id"].dropna().unique())
            store_id_options = sorted(df["store_id"].dropna().unique())
            category_options = sorted(df["store_primary_category"].dropna().unique())
            order_protocol_options = sorted(df["order_protocol"].dropna().unique())
        else:
            st.error("Gagal memuat data untuk select options.")
            market_options = [1.0]
            store_id_options = ["store_x"]
            category_options = ["Unknown"]
            order_protocol_options = [1.0]
    except Exception as e:
        st.error(f"Error loading select options: {e}")
        market_options = [1.0]
        store_id_options = ["store_x"]
        category_options = ["Unknown"]
        order_protocol_options = [1.0]

    with st.form("prediction_form"):
        market_id = st.selectbox("Market ID", market_options)
        created_at = st.text_input("Created At (YYYY-MM-DD HH:MM:SS)", "2025-07-10 10:00:00")
        actual_delivery_time = st.text_input("Actual Delivery Time", "2025-07-10 11:00:00")
        store_id = st.selectbox("Store ID", store_id_options)
        store_primary_category = st.selectbox("Store Category", category_options)
        order_protocol = st.selectbox("Order Protocol", order_protocol_options)

        total_items = st.number_input("Total Items", min_value=1)
        subtotal = st.number_input("Subtotal", min_value=0.0)
        num_distinct_items = st.number_input("Distinct Items", min_value=1)
        min_item_price = st.number_input("Min Item Price", min_value=0.0)
        max_item_price = st.number_input("Max Item Price", min_value=0.0)
        total_onshift_partners = st.number_input("Onshift Partners", min_value=0)
        total_busy_partners = st.number_input("Busy Partners", min_value=0)
        total_outstanding_orders = st.number_input("Outstanding Orders", min_value=0)

        submit = st.form_submit_button("Predict")

    if submit:
        input_data = {
            "market_id": market_id,
            "created_at": created_at,
            "actual_delivery_time": actual_delivery_time,
            "store_id": store_id,
            "store_primary_category": store_primary_category,
            "order_protocol": order_protocol,
            "total_items": total_items,
            "subtotal": subtotal,
            "num_distinct_items": num_distinct_items,
            "min_item_price": min_item_price,
            "max_item_price": max_item_price,
            "total_onshift_partners": total_onshift_partners,
            "total_busy_partners": total_busy_partners,
            "total_outstanding_orders": total_outstanding_orders
        }

        try:
            prediction_response = requests.post(f"{BACKEND_URL}/predict", json=input_data)
            if prediction_response.status_code == 200:
                result = prediction_response.json()
                st.success(f"Predicted delivery duration: **{result['prediction']:.2f} minutes**")
            else:
                st.error(f"Prediction failed: {prediction_response.json().get('error')}")
        except Exception as e:
            st.error(f"Error: {e}")

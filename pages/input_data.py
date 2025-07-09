import streamlit as st
import requests
from datetime import datetime

API_URL = "http://192.168.100.173:8888"

st.set_page_config(page_title="Input Data Form", layout="wide")

st.title("Food Delivery - Input Data Form")
st.markdown("Use the form below to submit a new delivery record.")

with st.form("data_form"):
    st.header("Delivery Timing")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        market_id = st.number_input("Market ID", value=1.0)
    with col2:
        created_at = st.date_input("Created Date")
    with col3:
        created_time = st.time_input("Created Time")
    with col4:
        actual_date = st.date_input("Delivery Date")
    
    col5, col6 = st.columns(2)
    with col5:
        actual_time = st.time_input("Delivery Time")

    st.header("Store Information")
    col7, col8 = st.columns(2)
    with col7:
        store_id = st.text_input("Store ID")
    with col8:
        category = st.text_input("Primary Category")

    st.header("Order Details")
    col9, col10, col11 = st.columns(3)
    with col9:
        order_protocol = st.number_input("Order Protocol", value=1)
        total_items = st.number_input("Total Items", value=1)
        subtotal = st.number_input("Subtotal", value=0.0)
    with col10:
        num_distinct = st.number_input("Distinct Items", value=1)
        min_price = st.number_input("Min Item Price", value=0.0)
        max_price = st.number_input("Max Item Price", value=0.0)
    with col11:
        total_onshift = st.number_input("Onshift Partners", value=0)
        total_busy = st.number_input("Busy Partners", value=0)
        total_outstanding = st.number_input("Outstanding Orders", value=0)

    submit = st.form_submit_button("Submit")

    if submit:
        payload = {
            "market_id": market_id,
            "created_at": datetime.combine(created_at, created_time).isoformat(),
            "actual_delivery_time": datetime.combine(actual_date, actual_time).isoformat(),
            "store_id": store_id,
            "store_primary_category": category,
            "order_protocol": order_protocol,
            "total_items": total_items,
            "subtotal": subtotal,
            "num_distinct_items": num_distinct,
            "min_item_price": min_price,
            "max_item_price": max_price,
            "total_onshift_partners": total_onshift,
            "total_busy_partners": total_busy,
            "total_outstanding_orders": total_outstanding,
        }

        try:
            res = requests.post(f"{API_URL}/api/insert", json=payload)
            if res.status_code == 200:
                st.success("Data saved successfully.")
            else:
                st.error(f"Failed to save data (status code: {res.status_code}).")
        except Exception as e:
            st.error(f"Error: {e}")

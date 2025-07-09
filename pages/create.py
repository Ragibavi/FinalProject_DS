import streamlit as st
import requests
from datetime import datetime

API_URL = "http://192.168.100.173:8888"

st.set_page_config(page_title="📥 Input Data", layout="centered")
st.title("📥 Form Input Data")

with st.form("data_form"):
    market_id = st.number_input("Market ID", value=1.0)
    created_at = st.date_input("Created Date")
    created_time = st.time_input("Created Time")
    actual_date = st.date_input("Actual Delivery Date")
    actual_time = st.time_input("Actual Delivery Time")

    store_id = st.text_input("Store ID")
    category = st.text_input("Store Primary Category")

    order_protocol = st.number_input("Order Protocol", value=1)
    total_items = st.number_input("Total Items", value=1)
    subtotal = st.number_input("Subtotal", value=0.0)
    num_distinct = st.number_input("Distinct Items", value=1)
    min_price = st.number_input("Min Item Price", value=0.0)
    max_price = st.number_input("Max Item Price", value=0.0)
    total_onshift = st.number_input("Total Onshift Partners", value=0)
    total_busy = st.number_input("Total Busy Partners", value=0)
    total_outstanding = st.number_input("Outstanding Orders", value=0)

    submit = st.form_submit_button("💾 Simpan")

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
                st.success("✅ Data berhasil disimpan!")
            else:
                st.error(f"❌ Gagal menyimpan data. ({res.status_code})")
        except Exception as e:
            st.error(f"❌ Error: {e}")

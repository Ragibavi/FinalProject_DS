import streamlit as st
import requests
import pandas as pd
import altair as alt

API_URL = "http://192.168.100.173:8888"

st.set_page_config(page_title="Food Delivery Data Viewer", layout="wide")
st.title("Stored Data Viewer")


def clean_dataframe(data):
    df = pd.DataFrame(data)

    numeric_columns = [
        "market_id", "order_protocol", "total_items", "subtotal",
        "num_distinct_items", "min_item_price", "max_item_price",
        "total_onshift_partners", "total_busy_partners", "total_outstanding_orders"
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

    string_columns = ["store_id", "store_primary_category"]
    for col in string_columns:
        df[col] = df.get(col, "N/A").fillna("N/A")

    return df


try:
    res = requests.get(f"{API_URL}/api/data")
    if res.status_code == 200:
        data = res.json()
        if data:
            df = clean_dataframe(data)

            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            if 'actual_delivery_time' in df.columns:
                df['actual_delivery_time'] = pd.to_datetime(df['actual_delivery_time'], errors='coerce')

            # Date range filter
            if not df['created_at'].isnull().all():
                min_date = df['created_at'].min().date()
                max_date = df['created_at'].max().date()

                start_date, end_date = st.date_input(
                    "Filter by Created Date Range:",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )

                df = df[
                    (df['created_at'].dt.date >= start_date) &
                    (df['created_at'].dt.date <= end_date)
                ]

            # Search filter
            search_query = st.text_input("Search by Store ID, Category, or Market ID")
            if search_query:
                df = df[
                    df["store_id"].astype(str).str.contains(search_query, case=False, na=False) |
                    df["store_primary_category"].astype(str).str.contains(search_query, case=False, na=False) |
                    df["market_id"].astype(str).str.contains(search_query, case=False, na=False)
                ]

            st.write(f"Total records: {len(df)}")
            st.dataframe(df, use_container_width=True)

            # Visualization Section
            st.markdown("---")
            st.subheader("Data Visualization")

            # Bar Chart: Total Orders by Store
            st.markdown("Total Orders per Store")
            orders_per_store = df.groupby("store_id").size().reset_index(name="total_orders")
            bar_chart = alt.Chart(orders_per_store).mark_bar().encode(
                x=alt.X("store_id:N", sort="-y", title="Store ID"),
                y=alt.Y("total_orders:Q", title="Total Orders"),
                tooltip=["store_id", "total_orders"]
            ).properties(width=700, height=400)
            st.altair_chart(bar_chart, use_container_width=True)

            # Bar Chart: Average Subtotal by Category
            st.markdown("Average Subtotal per Store Category")
            avg_subtotal = df.groupby("store_primary_category")["subtotal"].mean().reset_index()
            avg_chart = alt.Chart(avg_subtotal).mark_bar(color="#4c78a8").encode(
                x=alt.X("store_primary_category:N", sort="-y", title="Store Category"),
                y=alt.Y("subtotal:Q", title="Average Subtotal"),
                tooltip=["store_primary_category", "subtotal"]
            ).properties(width=700, height=400)
            st.altair_chart(avg_chart, use_container_width=True)

            # Line Chart: Onshift vs Busy Partners Over Time
            st.markdown("Partner Count Over Time (Onshift vs Busy)")
            daily_partners = df.dropna(subset=["created_at"]).copy()
            daily_partners["created_at"] = pd.to_datetime(daily_partners["created_at"])
            grouped = daily_partners.groupby(daily_partners["created_at"].dt.date)[
                ["total_onshift_partners", "total_busy_partners"]
            ].sum().reset_index().rename(columns={"created_at": "date"})

            melted = grouped.melt("date", var_name="Partner Type", value_name="Count")

            line_chart = alt.Chart(melted).mark_line(point=True).encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("Count:Q", title="Number of Partners"),
                color="Partner Type:N",
                tooltip=["date", "Partner Type", "Count"]
            ).properties(width=800, height=400)

            st.altair_chart(line_chart, use_container_width=True)

        else:
            st.info("No data available.")
    else:
        st.warning(f"Failed to fetch data from the API. Status code: {res.status_code}")
except Exception as e:
    st.error(f"Error fetching data: {e}")

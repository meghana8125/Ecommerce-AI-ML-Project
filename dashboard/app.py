import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="E-Commerce Customer Intelligence",
    page_icon="🛒",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")


def model_file(filename):
    return os.path.join(MODELS_DIR, filename)


def load_csv(filename):
    path = model_file(filename)
    if not os.path.isfile(path):
        st.error(f"Missing file: {path}")
        st.stop()
    return pd.read_csv(path)


@st.cache_data
def load_data():
    monthly_revenue = load_csv("monthly_revenue.csv")
    monthly_orders = load_csv("monthly_orders.csv")
    monthly_aov = load_csv("monthly_aov.csv")
    customer_rfm = load_csv("customer_rfm.csv")
    # Your actual saved filename is customer_segments.csv
    customer_segments = load_csv("customer_segments.csv")
    recommendations = load_csv("product_recommendations.csv")
    return (
        monthly_revenue,
        monthly_orders,
        monthly_aov,
        customer_rfm,
        customer_segments,
        recommendations
    )


try:
    (
        monthly_revenue,
        monthly_orders,
        monthly_aov,
        customer_rfm,
        customer_segments,
        recommendations
    ) = load_data()
except Exception as e:
    st.error("Unable to load the saved project data.")
    st.exception(e)
    st.stop()


for df in (monthly_revenue, monthly_orders, monthly_aov):
    if "Month" in df.columns:
        df["Month"] = pd.to_datetime(df["Month"], errors="coerce")


st.title("🛒 E-Commerce Customer Intelligence Dashboard")
st.markdown(
    "### AI/ML-powered analysis of sales, customer behavior, segmentation and product recommendations"
)
st.divider()

total_revenue = monthly_revenue["Revenue"].sum()
total_orders = monthly_orders["Orders"].sum()
total_customers = (
    customer_rfm["Customer ID"].nunique()
    if "Customer ID" in customer_rfm.columns
    else len(customer_rfm)
)

recommendation_product_count = (
    recommendations["Recommended Product"].nunique()
    if "Recommended Product" in recommendations.columns
    else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Revenue", f"£{total_revenue:,.2f}")
with col2:
    st.metric("Total Orders", f"{total_orders:,.0f}")
with col3:
    st.metric("Customers", f"{total_customers:,}")
with col4:
    st.metric("Recommendation Products", f"{recommendation_product_count:,}")

st.divider()

st.subheader("📈 Sales Performance")
col1, col2 = st.columns(2)

with col1:
    st.write("### Monthly Revenue")
    revenue_chart = monthly_revenue.dropna(subset=["Month", "Revenue"]).copy()
    revenue_chart = revenue_chart.set_index("Month")
    st.line_chart(revenue_chart["Revenue"])

with col2:
    st.write("### Monthly Orders")
    orders_chart = monthly_orders.dropna(subset=["Month", "Orders"]).copy()
    orders_chart = orders_chart.set_index("Month")
    st.line_chart(orders_chart["Orders"])

st.subheader("💰 Monthly Average Order Value")
aov_chart = monthly_aov.dropna(
    subset=["Month", "Average_Order_Value"]
).copy()
aov_chart = aov_chart.set_index("Month")
st.line_chart(aov_chart["Average_Order_Value"])

st.divider()

st.subheader("👥 Customer Segmentation")

if "Segment" in customer_segments.columns:
    st.bar_chart(customer_segments["Segment"].value_counts())

    required = ["Customer ID", "Recency", "Frequency", "Monetary"]
    if all(c in customer_segments.columns for c in required):
        segment_summary = (
            customer_segments.groupby("Segment")
            .agg(
                Customers=("Customer ID", "count"),
                Average_Recency=("Recency", "mean"),
                Average_Frequency=("Frequency", "mean"),
                Average_Monetary=("Monetary", "mean")
            )
            .reset_index()
        )
        segment_summary["Average_Recency"] = segment_summary["Average_Recency"].round(2)
        segment_summary["Average_Frequency"] = segment_summary["Average_Frequency"].round(2)
        segment_summary["Average_Monetary"] = segment_summary["Average_Monetary"].round(2)
        st.dataframe(segment_summary, use_container_width=True, hide_index=True)
else:
    st.warning("The Segment column was not found in customer_segments.csv.")

st.divider()

st.subheader("🛍️ Product Recommendation System")
st.write(
    "Products frequently purchased together are recommended using co-purchase analysis."
)

expected = ["Input Product", "Recommended Product", "Co-purchase Count"]
if all(c in recommendations.columns for c in expected):
    input_products = recommendations["Input Product"].dropna().unique().tolist()

    if input_products:
        selected_product = st.selectbox("Select a product", input_products)
        filtered = recommendations[
            recommendations["Input Product"] == selected_product
        ].copy()

        filtered = filtered.rename(
            columns={"Co-purchase Count": "Times Purchased Together"}
        )

        st.dataframe(filtered, use_container_width=True, hide_index=True)
    else:
        st.info("No recommendation products are available.")
else:
    st.warning("The recommendation CSV does not contain the expected columns.")

st.divider()

st.subheader("📊 Customer RFM Summary")

if all(c in customer_rfm.columns for c in ["Recency", "Frequency", "Monetary"]):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Average Recency", f"{customer_rfm['Recency'].mean():.1f} days")
    with col2:
        st.metric("Average Frequency", f"{customer_rfm['Frequency'].mean():.1f} orders")
    with col3:
        st.metric(
            "Average Monetary Value",
            f"£{customer_rfm['Monetary'].mean():,.2f}"
        )
else:
    st.warning("RFM columns were not found in customer_rfm.csv.")

st.divider()

st.subheader("🤖 Machine Learning Components")
st.markdown(
    """
- **K-Means Clustering:** Customer segmentation using RFM features.
- **Random Forest Regression:** Customer spending prediction using Recency and Frequency.
- **Co-purchase Recommendation:** Product recommendations based on products purchased together.
"""
)

st.divider()
st.caption(
    "E-Commerce Customer Intelligence | Python • Pandas • Scikit-learn • Streamlit"
)

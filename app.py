import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Sales & Customer Behavior Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv")

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    return df

df = load_data()

# ==========================
# TITLE
# ==========================

st.title("📊 Sales & Customer Behavior Analytics Dashboard")
st.markdown("E-Commerce Dataset")

# ==========================
# SIDEBAR FILTERS
# ==========================

st.sidebar.header("Filters")

state_filter = st.sidebar.multiselect(
    "Select State",
    options=sorted(df["customer_state"].dropna().unique())
)

payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    options=sorted(df["payment_type"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["product_category_name"].dropna().unique())
)

filtered_df = df.copy()

if state_filter:
    filtered_df = filtered_df[
        filtered_df["customer_state"].isin(state_filter)
    ]

if payment_filter:
    filtered_df = filtered_df[
        filtered_df["payment_type"].isin(payment_filter)
    ]

if category_filter:
    filtered_df = filtered_df[
        filtered_df["product_category_name"].isin(category_filter)
    ]

# ==========================
# KPI CARDS
# ==========================

total_revenue = filtered_df["Revenue"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["order_id"].nunique()

total_customers = filtered_df["customer_unique_id"].nunique()

avg_delivery = filtered_df["delivery_days"].mean()

repeat_rate = (
    filtered_df.groupby("customer_unique_id")
    .size()
    .gt(1)
    .mean()
    * 100
)

col1, col2, col3 = st.columns(3)

col1.metric(
    " Total Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    " Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    " Total Orders",
    f"{total_orders:,}"
)

col4, col5, col6 = st.columns(3)

col4.metric(
    " Total Customers",
    f"{total_customers:,}"
)

col5.metric(
    " Avg Delivery Days",
    f"{avg_delivery:.1f}"
)

col6.metric(
    " Repeat Customer Rate",
    f"{repeat_rate:.2f}%"
)

st.markdown("---")

# ==========================
# MONTHLY SALES TREND
# ==========================

st.subheader("📅 Monthly Revenue Trend")

monthly_sales = (
    filtered_df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

month_order = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig = px.bar(
    monthly_sales,
    x="Month",
    y="Revenue",
    title="Monthly Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# TOP CATEGORIES
# ==========================

st.subheader(" Top Product Categories")

top_categories = (
    filtered_df.groupby(
        "product_category_name"
    )["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_categories,
    x="product_category_name",
    y="Revenue",
    title="Top 10 Categories by Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# PAYMENT METHODS
# ==========================

st.subheader(" Payment Method Distribution")

payment_data = (
    filtered_df["payment_type"]
    .value_counts()
    .reset_index()
)

payment_data.columns = [
    "Payment Method",
    "Count"
]

fig = px.pie(
    payment_data,
    names="Payment Method",
    values="Count",
    title="Payment Methods"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# REVENUE BY STATE
# ==========================

st.subheader(" Revenue by State")

state_sales = (
    filtered_df.groupby(
        "customer_state"
    )["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    state_sales,
    x="customer_state",
    y="Revenue",
    title="Top States by Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# CUSTOMER LIFETIME VALUE
# ==========================

st.subheader(" Top Customers by CLV")

clv = (
    filtered_df.groupby(
        "customer_unique_id"
    )["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    clv,
    x="customer_unique_id",
    y="Revenue",
    title="Top 10 Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# DELIVERY TIME ANALYSIS
# ==========================

st.subheader(" Delivery Time Analysis")

fig = px.histogram(
    filtered_df,
    x="delivery_days",
    nbins=30,
    title="Delivery Days Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# DATA TABLE
# ==========================

st.subheader(" Dataset Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)

# ==========================
# DOWNLOAD BUTTON
# ==========================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Interactive Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("Cleaned_Auto_Sales.csv")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("📊 Interactive Sales Dashboard")
st.markdown("Analyze sales performance using interactive charts and filters.")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🔍 Filters")

# Product Line Filter
product_line = st.sidebar.selectbox(
    "Select Product Line",
    ["All"] + list(df["PRODUCTLINE"].unique())
)

# Country Filter
country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + list(df["COUNTRY"].unique())
)

# Deal Size Filter
deal_size = st.sidebar.selectbox(
    "Select Deal Size",
    ["All"] + list(df["DEALSIZE"].unique())
)

# Year Filter
year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(list(df["YEAR"].unique()))
)

# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------
filtered_df = df.copy()

if product_line != "All":
    filtered_df = filtered_df[
        filtered_df["PRODUCTLINE"] == product_line
    ]

if country != "All":
    filtered_df = filtered_df[
        filtered_df["COUNTRY"] == country
    ]

if deal_size != "All":
    filtered_df = filtered_df[
        filtered_df["DEALSIZE"] == deal_size
    ]

if year != "All":
    filtered_df = filtered_df[
        filtered_df["YEAR"] == year
    ]

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------
total_sales = filtered_df["SALES"].sum()
average_sales = filtered_df["SALES"].mean()
total_orders = filtered_df["ORDERNUMBER"].nunique()
total_customers = filtered_df["CUSTOMERNAME"].nunique()

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "📈 Average Sales",
    f"${average_sales:,.2f}"
)

col3.metric(
    "🧾 Total Orders",
    total_orders
)

col4.metric(
    "👥 Total Customers",
    total_customers
)

st.markdown("---")

# ---------------------------------------------------
# CHART 1 — SALES BY PRODUCT LINE
# ---------------------------------------------------
sales_product = filtered_df.groupby(
    "PRODUCTLINE"
)["SALES"].sum().reset_index()

fig1 = px.bar(
    sales_product,
    x="PRODUCTLINE",
    y="SALES",
    color="PRODUCTLINE",
    title="Sales by Product Line"
)

# ---------------------------------------------------
# CHART 2 — SALES BY COUNTRY
# ---------------------------------------------------
sales_country = filtered_df.groupby(
    "COUNTRY"
)["SALES"].sum().reset_index()

fig2 = px.pie(
    sales_country,
    names="COUNTRY",
    values="SALES",
    title="Sales Distribution by Country"
)

# ---------------------------------------------------
# DISPLAY FIRST ROW CHARTS
# ---------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# CHART 3 — MONTHLY SALES TREND
# ---------------------------------------------------
monthly_sales = filtered_df.groupby(
    "MONTH"
)["SALES"].sum().reset_index()

fig3 = px.line(
    monthly_sales,
    x="MONTH",
    y="SALES",
    markers=True,
    title="Monthly Sales Trend"
)

# ---------------------------------------------------
# CHART 4 — QUANTITY VS SALES
# ---------------------------------------------------
fig4 = px.scatter(
    filtered_df,
    x="QUANTITYORDERED",
    y="SALES",
    color="PRODUCTLINE",
    size="SALES",
    hover_data=["CUSTOMERNAME"],
    title="Quantity Ordered vs Sales"
)

# ---------------------------------------------------
# DISPLAY SECOND ROW CHARTS
# ---------------------------------------------------
col7, col8 = st.columns(2)

with col7:
    st.plotly_chart(fig3, use_container_width=True)

with col8:
    st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# CHART 5 — DEAL SIZE DISTRIBUTION
# ---------------------------------------------------
st.subheader("📊 Deal Size Distribution")

fig5 = px.histogram(
    filtered_df,
    x="DEALSIZE",
    color="DEALSIZE",
    title="Deal Size Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------
st.subheader("📄 Filtered Dataset")

st.dataframe(filtered_df)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.markdown(
    "✅ Dashboard Created Using Streamlit & Plotly"
)
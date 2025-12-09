 # app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide", initial_sidebar_state="expanded")

# ---------- Helpers ----------
@st.cache_data
def load_data(path="data/sales.csv"):
    df = pd.read_csv(path, parse_dates=["Order Date"], dayfirst=False, encoding='utf-8')
    # Basic cleaning & safe defaults
    df = df.drop_duplicates().copy()
    # Standardize column names (optional - handle common variants)
    df.columns = [c.strip() for c in df.columns]
    # Ensure expected columns exist - minimal safe handling
    for col in ["Sales","Profit","Quantity","Discount"]:
        if col not in df.columns:
            df[col] = 0
    # numeric casts
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0)
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(1).replace(0,1).astype(int)
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce").fillna(0)
    # Dates
    if df["Order Date"].dtype != "datetime64[ns]":
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    # Feature engineering
    df["Year"] = df["Order Date"].dt.year.fillna(0).astype(int)
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["UnitPrice"] = df["Sales"] / df["Quantity"]
    df["PriceAfterDiscount"] = df["UnitPrice"] * (1 - df["Discount"])
    df["ProfitMargin"] = df.apply(lambda r: (r["Profit"] / r["Sales"]) if r["Sales"] != 0 else 0, axis=1)
    # Fill missing categorical cols if any
    for c in ["Region","Category","Customer ID","Customer Name"]:
        if c not in df.columns:
            df[c] = "Unknown"
        df[c] = df[c].fillna("Unknown")
    return df

def format_currency(x):
    try:
        return f"₹{int(x):,}"
    except:
        return f"₹{x}"

def to_csv_bytes(df_in):
    return df_in.to_csv(index=False).encode("utf-8")

# ---------- Load data ----------
DATA_PATH = "data/Superstore.csv"    
df = load_data(DATA_PATH)

# ---------- Sidebar Filters ----------
st.sidebar.header("Filters")
years = ["All"] + sorted(df["Year"].unique().tolist(), reverse=True)
sel_year = st.sidebar.selectbox("Year", years, index=0)

regions = ["All"] + sorted(df["Region"].unique().tolist())
sel_region = st.sidebar.selectbox("Region", regions, index=0)

categories = ["All"] + sorted(df["Category"].unique().tolist())
sel_category = st.sidebar.multiselect("Category (multi)", options=categories, default=["All"])

search_customer = st.sidebar.text_input("Search Customer ID / Name (optional)")

# Apply filters
data = df.copy()
if sel_year != "All":
    data = data[data["Year"] == int(sel_year)]
if sel_region != "All":
    data = data[data["Region"] == sel_region]
if sel_category and "All" not in sel_category:
    data = data[data["Category"].isin(sel_category)]
if search_customer:
    q = search_customer.strip().lower()
    data = data[data["Customer ID"].astype(str).str.lower().str.contains(q) | data["Customer Name"].str.lower().str.contains(q)]

# ---------- KPIs ----------
total_revenue = data["Sales"].sum()
total_profit = data["Profit"].sum()
orders = data["Order ID"].nunique() if "Order ID" in data.columns else len(data)
aov = (total_revenue / orders) if orders != 0 else 0
repeat_customers_pct = (data.groupby("Customer ID").size().gt(1).mean() * 100)

st.title("📊 Sales Performance Dashboard (Plotly)")
st.markdown("Interactive dashboard built with Pandas, NumPy, Plotly & Streamlit. Use filters on the left.")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", format_currency(total_revenue))
k2.metric("Total Profit", format_currency(total_profit))
k3.metric("Orders", f"{orders:,}")
k4.metric("Avg Order Value", format_currency(aov))

st.markdown("---")

# ---------- Charts Row 1 ----------
c1, c2 = st.columns((2,1))

# Monthly revenue trend - ensure continuous months
with c1:
    st.subheader("Monthly Revenue Trend")
    monthly = data.groupby("Month")["Sales"].sum().reset_index().sort_values("Month")
    # fill missing months between min and max
    if not monthly.empty:
        all_months = pd.date_range(start=monthly["Month"].min(), end=monthly["Month"].max(), freq="MS")
        monthly = monthly.set_index("Month").reindex(all_months, fill_value=0).rename_axis("Month").reset_index()
    fig_month = px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly Revenue")
    fig_month.update_traces(line=dict(width=3))
    fig_month.update_layout(hovermode="x unified", margin=dict(t=40,l=20,r=20,b=20))
    st.plotly_chart(fig_month, use_container_width=True)

with c2:
    st.subheader("Category & Region Snapshot")
    cat_df = data.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    if cat_df.shape[0] > 0:
        fig_cat = px.bar(cat_df.head(10), x="Sales", y="Category", orientation="h", title="Top Categories (by revenue)", text="Sales")
        fig_cat.update_layout(margin=dict(t=30,l=10,r=10,b=10), yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)
    region_df = data.groupby("Region")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    if region_df.shape[0] > 0:
        fig_reg = px.pie(region_df, names="Region", values="Sales", title="Revenue by Region")
        fig_reg.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_reg, use_container_width=True)

st.markdown("---")

# ---------- Charts Row 2 ----------
c3, c4 = st.columns((1,1))
with c3:
    st.subheader("Top 10 Products (by Sales)")
    prod = data.groupby("Product Name")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(10)
    if not prod.empty:
        fig_prod = px.bar(prod, x="Sales", y="Product Name", orientation="h", text="Sales", title="Top Products")
        fig_prod.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=30,l=10,r=10,b=10))
        st.plotly_chart(fig_prod, use_container_width=True)
with c4:
    st.subheader("Top 10 Customers (by Sales)")
    top_cust = data.groupby(["Customer ID","Customer Name"])["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(10)
    if not top_cust.empty:
        fig_cust = px.bar(top_cust, x="Sales", y="Customer Name", orientation="h", text="Sales", title="Top Customers")
        fig_cust.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=30,l=10,r=10,b=10))
        st.plotly_chart(fig_cust, use_container_width=True)

st.markdown("---")

# ---------- Insights / small analysis ----------
st.subheader("Quick Insights")
insights = []
if total_revenue > 0:
    top_cat = cat_df.iloc[0]["Category"] if not cat_df.empty else "N/A"
    top_reg = region_df.iloc[0]["Region"] if not region_df.empty else "N/A"
    insights.append(f"• Top category by revenue: **{top_cat}**")
    insights.append(f"• Top region by revenue: **{top_reg}**")
    insights.append(f"• Repeat customers: **{repeat_customers_pct:.1f}%** of customers made >1 order")
else:
    insights.append("No sales data for selected filters.")
for line in insights:
    st.markdown(line)

st.markdown("---")

# ---------- Data preview and download ----------
st.subheader("Data Preview")
with st.expander("Show data table (first 300 rows)"):
    st.dataframe(data.head(300))

st.download_button("⬇️ Download filtered CSV", data=to_csv_bytes(data), file_name="sales_filtered.csv", mime="text/csv")

st.markdown("Made with ❤️ — Pandas, NumPy, Plotly & Streamlit.")

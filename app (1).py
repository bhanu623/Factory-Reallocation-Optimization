
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Nassau Dashboard",
    layout="wide"
)

# Title
st.title("Factory Reallocation & Shipping Optimization Dashboard")

# Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

# Create Lead Time
df['Lead_Time'] = (
    df['Ship Date'] - df['Order Date']
).dt.days

# Sidebar filters
st.sidebar.title("Filters")

region = st.sidebar.radio(
    "Select Region",
    df['Region'].unique()
)

ship_mode = st.sidebar.radio(
    "Select Ship Mode",
    df['Ship Mode'].unique()
)

# Filter dataset
filtered_df = df[
    (df['Region'] == region) &
    (df['Ship Mode'] == ship_mode)
]

# Filtered dataset
st.subheader("Filtered Dataset")

st.text(
    filtered_df.head(10).to_string()
)

# Key metrics
st.subheader("Key Metrics")

total_sales = round(
    filtered_df['Sales'].sum(),
    2
)

total_profit = round(
    filtered_df['Gross Profit'].sum(),
    2
)

avg_lead = round(
    filtered_df['Lead_Time'].mean(),
    2
)

st.write(f"Total Sales: {total_sales}")
st.write(f"Total Profit: {total_profit}")
st.write(f"Average Lead Time: {avg_lead}")

# Sales by division
st.subheader("Sales by Division")

division_sales = filtered_df.groupby(
    'Division'
)['Sales'].sum()

st.text(
    division_sales.to_string()
)

# Lead time summary
st.subheader("Lead Time Distribution")

min_lead = filtered_df['Lead_Time'].min()
max_lead = filtered_df['Lead_Time'].max()

st.write(f"Minimum Lead Time: {min_lead}")
st.write(f"Maximum Lead Time: {max_lead}")
st.write(f"Average Lead Time: {avg_lead}")

# Recommendation system
st.subheader("Factory Recommendation System")

filtered_df['Recommendation'] = filtered_df[
    'Lead_Time'
].apply(
    lambda x:
    "Recommend Faster Factory"
    if x > 5
    else "Current Factory is Good"
)

recommendation_table = filtered_df[
    ['Product Name',
     'Lead_Time',
     'Recommendation']
].head(10)

st.text(
    recommendation_table.to_string()
)

# Footer
st.success(
    "Dashboard Running Successfully"
)

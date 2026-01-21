import streamlit as st
import pandas as pd

# This tells the website to look professional
st.set_page_config(page_title="AI Strategic Observatory", layout="wide")

# 1. THE DATA ENGINE
# This part reads the file you uploaded
@st.cache_data
def load_data():
    # MAKE SURE THIS NAME MATCHES YOUR FILE EXACTLY
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name'])
    # MIT Risk Scan logic
    df['Privacy_Risk'] = df['Short Description'].str.contains('privacy|data|security', case=False, na=False)
    return df

df = load_data()

# 2. THE DASHBOARD
st.title("🔭 AI Strategic Intelligence Observatory")

# Show the metrics
st.metric("Total AI Tools Scanned", f"{len(df):,}")

# Show the main chart
st.subheader("Top 10 Market Sectors")
st.bar_chart(df['Category'].value_counts().head(10))

# Show the Data Table
st.subheader("Risk Audit Log")
st.dataframe(df[['Name', 'Category', 'Privacy_Risk']].head(20))

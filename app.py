import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config - Using a standard "Management" layout
st.set_page_config(page_title="AI Strategic Intelligence", layout="wide")

# CSS to make it look like a high-end SaaS product
st.markdown("""
    <style>
    .stApp { background-color: #f9fbfd; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e6e9ef; }
    .card { background: white; padding: 20px; border-radius: 8px; border: 1px solid #e6e9ef; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_clean_data():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).fillna("Unclassified")
    # Simplify Categories to keep it clean
    df['Category'] = df['Category'].str.title()
    # Create a "Strategic Risk Score"
    df['Risk_Score'] = df['Short Description'].str.contains('data|privacy|tracking', case=False).map({True: "🔴 High", False: "🟢 Low"})
    return df

df = load_clean_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🔭 GovIntel")
st.sidebar.markdown("---")
selected_sector = st.sidebar.selectbox("1. Filter by Sector", ["All Sectors"] + sorted(df['Category'].unique().tolist()))
search_name = st.sidebar.text_input("2. Search Tool Name", "")

# Filter Logic
filtered_df = df if selected_sector == "All Sectors" else df[df['Category'] == selected_sector]
if search_name:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]

# --- MAIN DASHBOARD ---
st.title("Strategic AI Observatory")
st.markdown(f"Currently auditing **{len(filtered_df):,}** tools within the **{selected_sector}** ecosystem.")

# 1. THE PULSE (Metrics)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Tool Volume", f"{len(filtered_df):,}")
with col2:
    high_risk_count = len(filtered_df[filtered_df['Risk_Score'] == "🔴 High"])
    st.metric("High-Risk Entities", high_risk_count, delta_color="inverse")
with col3:
    st.metric("Sector Diversity", filtered_df['Category'].nunique() if selected_sector == "All Sectors" else "Single Sector")

st.markdown("---")

# 2. THE LANDSCAPE (Visuals)
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Market Distribution")
    # A simple, horizontal bar chart is the easiest to read
    top_cats = filtered_df['Category'].value_counts().head(10).reset_index()
    fig = px.bar(top_cats, x='count', y='Category', orientation='h', 
                 color_discrete_sequence=['#1f77b4'], template="plotly_white")
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Risk Breakdown")
    risk_pie = px.pie(filtered_df, names='Risk_Score', hole=0.7, 
                      color='Risk_Score', color_discrete_map={"🔴 High":"#ff4b4b", "🟢 Low":"#1f77b4"})
    st.plotly_chart(risk_pie, use_container_width=True)

# 3. THE DOSSIER (Individual Records)
st.markdown("---")
st.subheader("Individual Intelligence Records")
st.dataframe(filtered_df[['Name', 'Category', 'Risk_Score', 'Short Description']].sort_values('Risk_Score', ascending=False), 
             use_container_width=True, hide_index=True)

# 4. EXPORT BUTTON (The "Pro" Feature)
st.download_button("Export Intelligence Report (CSV)", 
                   filtered_df.to_csv(index=False), 
                   "ai_intelligence_report.csv", 
                   "text/csv")

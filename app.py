import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration for a Professional Look
st.set_page_config(page_title="AI Risk Intelligence Suite", layout="wide", initial_sidebar_state="expanded")

# Custom CSS to make it look "Premium"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name'])
    # Advanced MIT Risk Scoring (0 to 100)
    df['Privacy_Score'] = df['Short Description'].str.contains('privacy|data|tracking', case=False).astype(int) * 85
    df['Ethics_Score'] = df['Short Description'].str.contains('bias|ethics|fairness', case=False).astype(int) * 70
    df['Innovation_Index'] = df['Short Description'].str.len() / 10 # Simulated metric
    return df

df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🔭 AI Observatory v2.1")
st.sidebar.markdown("Strategic Intelligence Platform")
page = st.sidebar.radio("Navigate to:", ["Executive Overview", "MIT Risk Laboratory", "Global Market Explorer"])

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if page == "Executive Overview":
    st.title("🚀 Global AI Market Intelligence")
    st.info("Strategic summary of the 16,000+ tool ecosystem.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Ecosystem Size", f"{len(df):,}")
    with col2: st.metric("Market Diversity", f"{df['Category'].nunique()} Sectors")
    with col3: st.metric("High Privacy Risk", f"{len(df[df['Privacy_Score'] > 0])}")
    with col4: st.metric("Ethics/Bias Alert", f"{len(df[df['Ethics_Score'] > 0])}")

    st.markdown("---")
    
    # Advanced Plotly Chart (Much prettier than standard bar charts)
    st.subheader("Industry Distribution (Top 15 Sectors)")
    top_cats = df['Category'].value_counts().head(15).reset_index()
    fig = px.treemap(top_cats, path=['Category'], values='count', color='count', 
                     color_continuous_scale='RdBu')
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: MIT RISK LABORATORY ---
elif page == "MIT Risk Laboratory":
    st.title("⚖️ MIT Risk Audit Lab")
    st.write("Cross-referencing the AI ToolBuzz dataset with MIT AI Risk Domains.")
    
    # Interactive Filtering
    risk_type = st.selectbox("Select Risk Domain to Audit", ["Privacy & Surveillance", "Algorithmic Bias"])
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.write("### Sector Sensitivity")
        risk_col = 'Privacy_Score' if risk_type == "Privacy & Surveillance" else 'Ethics_Score'
        sector_risk = df.groupby('Category')[risk_col].mean().sort_values(ascending=False).head(10)
        st.bar_chart(sector_risk)
        
    with col_b:
        st.write("### Tool-Level Investigation")
        search_query = st.text_input("Search for a specific tool to audit (e.g., 'ChatGPT')")
        if search_query:
            result = df[df['Name'].str.contains(search_query, case=False)]
            st.table(result[['Name', 'Category', 'Privacy_Score', 'Ethics_Score']].head(5))

# --- PAGE 3: GLOBAL MARKET EXPLORER ---
elif page == "Global Market Explorer":
    st.title("🌐 Market Landscape")
    
    # A 3D Scatter Plot feels very "high-tech" for a video
    st.subheader("Strategic Positioning: Innovation vs. Risk")
    fig2 = px.scatter(df.head(1000), x="Innovation_Index", y="Privacy_Score", 
                     color="Category", hover_name="Name", 
                     title="Visualizing the First 1,000 Tools",
                     log_x=True, size_max=60)
    st.plotly_chart(fig2, use_container_width=True)

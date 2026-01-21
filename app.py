import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="AI Risk Intelligence Suite", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Load the data
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name'])
    
    # CRITICAL FIX: Fill empty descriptions with text so the math doesn't break
    df['Short Description'] = df['Short Description'].fillna('No description available')
    
    # MIT Risk Scoring - Using a safer method for 16k rows
    df['Privacy_Score'] = df['Short Description'].str.contains('privacy|data|tracking|security', case=False, na=False).astype(int) * 85
    df['Ethics_Score'] = df['Short Description'].str.contains('bias|ethics|fairness|discrimination', case=False, na=False).astype(int) * 70
    
    # Create a simulated Innovation Index for visualization
    df['Innovation_Index'] = df['Short Description'].apply(len) / 10
    return df

# Initialize Data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("🔭 Intelligence Suite")
page = st.sidebar.radio("Navigate to:", ["Executive Overview", "MIT Risk Laboratory", "Market Explorer"])

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if page == "Executive Overview":
    st.title("🚀 Global AI Market Intelligence")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Ecosystem", f"{len(df):,}")
    m2.metric("Market Sectors", df['Category'].nunique())
    m3.metric("Privacy Flags", len(df[df['Privacy_Score'] > 0]))
    m4.metric("Ethics Flags", len(df[df['Ethics_Score'] > 0]))

    st.markdown("---")
    
    st.subheader("Industry Sector Dominance")
    top_cats = df['Category'].value_counts().head(15).reset_index()
    top_cats.columns = ['Sector', 'Count']
    
    # Treemap is much more "premium" looking for a video demo
    fig = px.treemap(top_cats, path=['Sector'], values='Count', 
                     color='Count', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: MIT RISK LABORATORY ---
elif page == "MIT Risk Laboratory":
    st.title("⚖️ MIT Risk Audit Lab")
    
    tab1, tab2 = st.tabs(["Sector Analysis", "Tool-Level Search"])
    
    with tab1:
        st.write("### Average Risk by Category")
        risk_chart = df.groupby('Category')[['Privacy_Score', 'Ethics_Score']].mean().sort_values('Privacy_Score', ascending=False).head(10)
        st.bar_chart(risk_chart)
        
    with tab2:
        search = st.text_input("Enter Tool Name (e.g., 'Copy.ai')")
        if search:
            results = df[df['Name'].str.contains(search, case=False, na=False)]
            st.dataframe(results[['Name', 'Category', 'Privacy_Score', 'Ethics_Score']])

# --- PAGE 3: MARKET EXPLORER ---
elif page == "Market Explorer":
    st.title("🌐 Strategic Landscape")
    
    # 3D-style scatter plot for high-end visualization
    fig_scatter = px.scatter(df.head(2000), 
                            x="Innovation_Index", 
                            y="Privacy_Score", 
                            color="Category",
                            size="Innovation_Index",
                            hover_name="Name",
                            title="Visualizing Innovation vs. Privacy Risk (Sample: 2000 Tools)")
    st.plotly_chart(fig_scatter, use_container_width=True)
with st.expander("💼 Strategic Consultant View"):
    st.write("### Sector Recommendation")
    high_risk_sectors = df.groupby('Category')['Privacy_Score'].mean().nlargest(3).index.tolist()
    st.warning(f"ADVISORY: The sectors {', '.join(high_risk_sectors)} show elevated Risk Profiles. Procurement should require SOC2 compliance before deployment.")
    
    st.write("### Opportunity Map")
    low_density_sectors = df['Category'].value_counts().nsmallest(5).index.tolist()
    st.success(f"STRATEGY: Minimal competition detected in {', '.join(low_density_sectors)}. Ideal for R&D investment.")

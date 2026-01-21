import streamlit as st
import pandas as pd
import plotly.express as px

# 1. THE ARCHITECTURE: Professional UI
st.set_page_config(page_title="GovIntel: AI Strategic Observatory", layout="wide")

# Custom CSS for a "Security Operations Center" Look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00d4ff; font-family: 'Courier New', monospace; }
    .report-card { 
        background-color: #1a1c24; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).fillna("N/A")
    # MIT Risk Heuristics
    df['Privacy_Flag'] = df['Short Description'].str.contains('data|privacy|tracking|secure', case=False)
    df['Ethics_Flag'] = df['Short Description'].str.contains('bias|ethics|fairness|hiring', case=False)
    df['Safety_Score'] = 100 - (df['Privacy_Flag'].astype(int)*40 + df['Ethics_Flag'].astype(int)*40)
    return df

df = load_data()

# --- HEADER ---
st.title("🔭 GovIntel | AI Strategic Observatory")
st.write("OFFICIAL USE ONLY | National AI Investment & Risk Dashboard")

# --- NAVIGATION ---
tabs = st.tabs(["📊 National Overview", "🔍 Tool Intelligence Audit", "💰 Investment Strategy"])

# --- TAB 1: NATIONAL OVERVIEW ---
with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monitored Entities", len(df))
    col2.metric("Market Sectors", df['Category'].nunique())
    col3.metric("Critical Risk Alerts", (df['Safety_Score'] < 50).sum())
    col4.metric("Average Safety Rating", f"{df['Safety_Score'].mean():.1f}%")

    st.subheader("Market Concentration by Domain")
    # Sunburst Chart for deeper interaction
    fig_sun = px.sunburst(df.head(500), path=['Category', 'Name'], values='Safety_Score',
                          color='Safety_Score', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_sun, use_container_width=True)

# --- TAB 2: TOOL INTELLIGENCE AUDIT (Deep Interactivity) ---
with tabs[1]:
    st.subheader("Identify & Audit Specific Tools")
    search_col, filter_col = st.columns([2, 1])
    
    with search_col:
        tool_name = st.selectbox("Select a tool for a Deep-Dive Audit:", [""] + sorted(df['Name'].tolist()))
    
    if tool_name:
        tool_data = df[df['Name'] == tool_name].iloc[0]
        
        st.markdown(f"""
        <div class="report-card">
            <h3>AUDIT REPORT: {tool_data['Name']}</h3>
            <p><b>Category:</b> {tool_data['Category']} | <b>Safety Rating:</b> {tool_data['Safety_Score']}%</p>
            <hr>
            <p><b>Risk Profile:</b> {'🔴 HIGH RISK' if tool_data['Safety_Score'] < 60 else '🟢 COMPLIANT'}</p>
            <p><b>Description:</b> {tool_data['Short Description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Comparison logic
        st.write("### How it compares to the Sector Average")
        avg_safety = df[df['Category'] == tool_data['Category']]['Safety_Score'].mean()
        st.progress(tool_data['Safety_Score']/100, text=f"Tool Score: {tool_data['Safety_Score']}")
        st.progress(avg_safety/100, text=f"Sector Average ({tool_data['Category']}): {avg_safety:.1f}")

# --- TAB 3: INVESTMENT STRATEGY ---
with tabs[2]:
    st.subheader("White-Space Discovery: Where should the Government invest?")
    st.info("Showing sectors with high strategic value but low tool density.")
    
    low_density = df['Category'].value_counts().nsmallest(10).reset_index()
    fig_invest = px.bar(low_density, x='count', y='Category', orientation='h',
                       title="Under-served AI Markets (Investment Opportunities)",
                       color='count', color_continuous_scale='Viridis')
    st.plotly_chart(fig_invest, use_container_width=True)

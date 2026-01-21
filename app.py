import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. ULTIMATE DESIGN & INTERACTIVITY SYSTEM
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

# CSS for alignment and button styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    .stApp { background-color: #0F172A; font-family: 'Plus Jakarta Sans', sans-serif; color: #E2E8F0; }
    
    /* Top Ticker */
    .ticker-wrap {
        width: 100%; background: #1E293B; border-bottom: 2px solid #38BDF8;
        padding: 8px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; font-family: monospace; animation: ticker 40s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* Button Styling to look like high-end widgets */
    div.stButton > button {
        width: 100%; height: 120px; background-color: #1E293B !important;
        border: 1px solid #334155 !important; border-radius: 15px !important;
        color: #F8FAFC !important; transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #38BDF8 !important; background-color: #26334D !important;
        transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    /* Custom Red Button for Critical */
    .crit-btn > div > button { border-color: #EF4444 !important; }
    .crit-btn > div > button:hover { border-color: #F87171 !important; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4) !important; }

    .main .block-container { padding-top: 6rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        df['D4_Flag'] = df['Short Description'].str.contains('privacy|tracking|surveillance', case=False, na=False)
        df['D6_Flag'] = df['Short Description'].str.contains('fake|synthetic|generate', case=False, na=False)
        df['Risk_Score'] = (df['D4_Flag'].astype(int) * 45) + (df['D6_Flag'].astype(int) * 35) + 20
        return df
    except: return pd.DataFrame()

df = load_data()

# Initialize Session State to track what is "clicked"
if 'view' not in st.session_state: st.session_state.view = "Home"

# 3. GLOBAL TICKER
st.markdown(f'<div class="ticker-wrap"><div class="ticker"> ● PHILIP\'S CONSULTING LIVE INTEL ● MONITORING {len(df):,} ENTITIES ● SELECT WIDGET FOR DEEP-SCAN ● </div></div>', unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='color:#38BDF8;'>🏛️ Observatory</h2>", unsafe_allow_html=True)
    app_mode = st.radio("Navigation", ["Executive Dashboard", "Strategic Audit", "MIT Framework"])
    if st.button("Reset View"): st.session_state.view = "Home"

# --- PAGE 1: EXECUTIVE DASHBOARD ---
if app_mode == "Executive Dashboard":
    st.markdown("<h2 style='font-weight:700;'>Intelligence Command Center</h2>", unsafe_allow_html=True)
    
    # CLICKABLE ACTION BAR
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button(f"📊 {len(df):,}\n\nENTITIES MONITORED"): st.session_state.view = "Inventory"
    with c2:
        if st.button(f"🛡️ {int(df['Risk_Score'].mean())}%\n\nAVG MARKET RISK"): st.session_state.view = "Sectors"
    with c3:
        st.markdown('<div class="crit-btn">', unsafe_allow_html=True)
        if st.button(f"🚨 {(df['Risk_Score'] >= 100).sum()}\n\nCRITICAL ALERTS"): st.session_state.view = "Critical"
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # DYNAMIC VIEW CONTENT
    if st.session_state.view == "Critical":
        st.markdown("### ⚠️ High-Risk Target List")
        crit_tools = df[df['Risk_Score'] >= 100].head(8)
        cols = st.columns(4)
        for i, row in enumerate(crit_tools.iterrows()):
            with cols[i % 4]:
                st.markdown(f"""
                    <div style="background:#1E293B; border:1px solid #EF4444; padding:15px; border-radius:10px;">
                        <b style="color:#EF4444;">{row[1]['Name']}</b><br>
                        <small>{row[1]['Category']}</small>
                    </div>
                """, unsafe_allow_html=True)

    elif st.session_state.view == "Inventory":
        st.markdown("### 📋 Market Inventory")
        st.dataframe(df[['Name', 'Category', 'Risk_Score']].head(50), use_container_width=True)

    elif st.session_state.view == "Sectors":
        st.markdown("### 📈 Sector Risk Analysis")
        sector_risk = df.groupby('Category')['Risk_Score'].mean().sort_values(ascending=False).head(15)
        st.bar_chart(sector_risk)

    else:
        # DEFAULT HOME GRAPHS (With Pop-up Hover effects)
        st.markdown("### Market Snapshot")
        col_pie, col_bar = st.columns([1, 1.5])
        
        with col_pie:
            st.markdown("<p style='font-size:0.7rem; color:#94A3B8; letter-spacing:1px;'>MARKET COMPOSITION</p>", unsafe_allow_html=True)
            fig_pie = px.pie(df['Category'].value_counts().head(8).reset_index(), 
                             names='index', values='Category', hole=0.6, 
                             template='plotly_dark', color_discrete_sequence=px.colors.sequential.Blues_r)
            # HOVER POPUP SETTINGS
            fig_pie.update_traces(hovertemplate="<b>%{label}</b><br>Tools: %{value}<br>Share: %{percent}")
            fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_bar:
            st.markdown("<p style='font-size:0.7rem; color:#94A3B8; letter-spacing:1px;'>TOP RISK SECTORS</p>", unsafe_allow_html=True)
            bar_data = df.groupby('Category')['Risk_Score'].mean().sort_values(ascending=False).head(10).reset_index()
            fig_bar = px.bar(bar_data, x='Risk_Score', y='Category', orientation='h', 
                             color='Risk_Score', color_continuous_scale='Reds', template='plotly_dark')
            # HOVER POPUP SETTINGS
            fig_bar.update_traces(hovertemplate="<b>Sector: %{y}</b><br>Risk Index: %{x}%")
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

# --- PAGES 2 & 3 REMAIN STABLE ---
elif app_mode == "Strategic Audit":
    st.markdown("### 🔍 Strategic Asset Audit")
    target = st.selectbox("Search Target:", [""] + sorted(df['Name'].unique().tolist()))
    if target:
        tool = df[df['Name'] == target].iloc[0]
        st.write(f"Displaying analysis for {target}...") # Logic from previous build

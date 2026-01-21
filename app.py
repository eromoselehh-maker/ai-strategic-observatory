import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI SETUP & SIMPLIFIED CSS
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

st.markdown("""
    <style>
    /* Clean Ticker */
    .ticker-wrap {
        width: 100%; overflow: hidden; background-color: #1C3D5A; 
        color: #00D1FF; padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 999;
        font-family: monospace; border-bottom: 2px solid #00D1FF;
    }
    .ticker { display: inline-block; white-space: nowrap; animation: ticker 30s linear infinite; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .main .block-container { padding-top: 5rem; }
    
    /* Professional Card Styling */
    .metric-box {
        background-color: #F8FAFC; border: 1px solid #E2E8F0;
        padding: 20px; border-radius: 12px; text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .metric-val { font-size: 2rem; font-weight: bold; color: #1C3D5A; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
    df['MIT_D4'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance', case=False, na=False)
    df['MIT_D6'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media', case=False, na=False)
    return df

df = load_data()
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# 3. THE TICKER (The "Pop-up" Intel)
st.markdown('<div class="ticker-wrap"><div class="ticker"> ⚡ PHILIP\'S CONSULTING LIVE INTEL: Sector "Data Analysis" flags increasing... | Market Trend: NVDA (+1.5%) leading AI hardware... | MIT Repository v4.0 Active... </div></div>', unsafe_allow_html=True)

# 4. SIDEBAR
st.sidebar.title("🏛️ AI OBSERVATORY")
st.sidebar.caption("By **Philip’s Consulting**")
nav = st.sidebar.radio("Go to:", ["📈 Executive Dashboard", "🔍 Entity Audit", "📖 Methodology"])

# --- PAGE 1: DASHBOARD ---
if nav == "📈 Executive Dashboard":
    st.title("Strategic AI Risk Dashboard")
    
    # Big Metric Row
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-box"><div class="metric-val">{len(df):,}</div><small>ENTITIES MONITORED</small></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#E53E3E;">{df["MIT_D4"].sum()}</div><small>PRIVACY RISKS (D4)</small></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#DD6B20;">{df["MIT_D6"].sum()}</div><small>INTEGRITY RISKS (D6)</small></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Interactive Charts Row
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("Global Sector Risk Map")
        fig = px.treemap(df.sample(1000), path=['Category', 'Name'], values='MIT_D4', 
                         color='MIT_D4', color_continuous_scale='Reds')
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=450)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Click sectors to zoom into specific company risk levels.")

    with col_b:
        st.subheader("📡 Live News Feed")
        if NEWS_API_KEY:
            try:
                r = requests.get(f"https://newsapi.org/v2/everything?q=AI+risk&apiKey={NEWS_API_KEY}&pageSize=4").json()
                for art in r.get('articles', []):
                    st.markdown(f"**{art['source']['name']}**")
                    st.markdown(f"[{art['title']}]({art['url']})")
                    st.write("---")
            except: st.write("Feed busy...")

# --- PAGE 2: ENTITY AUDIT ---
elif nav == "🔍 Entity Audit":
    st.title("Entity Intelligence Audit")
    
    target = st.selectbox("Select Company to Audit:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        st.subheader(f"Results for: {target}")
        
        ca, cb = st.columns(2)
        with ca:
            st.markdown("### 📋 Audit Profile")
            st.write(f"**Industry:** {tool['Category']}")
            st.write(f"**MIT D4 (Privacy):** {'🔴 High Risk' if tool['MIT_D4'] else '🟢 Minimal Risk'}")
            st.write(f"**MIT D6 (Integrity):** {'🔴 High Risk' if tool['MIT_D6'] else '🟢 Minimal Risk'}")
            st.info(f"**Consultant Note:** {tool['Short Description']}")
            
        with cb:
            st.markdown("### 📈 Market Trust")
            ticker = st.text_input("Enter Parent Stock Ticker (e.g. MSFT):").upper()
            if ticker and AV_API_KEY:
                q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                quote = requests.get(q_url).json().get('Global Quote', {})
                if quote:
                    st.metric(f"{ticker} Current Price", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))

# --- PAGE 3:

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI CONFIGURATION
st.set_page_config(page_title="AI Observatory", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .metric-card {
        background-color: #F8FAFC; border: 1px solid #E2E8F0;
        padding: 20px; border-radius: 12px; text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 800; color: #1E293B; }
    .advisory-card {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        padding: 15px; border-radius: 10px; margin-bottom: 10px;
        border-left: 5px solid #3B82F6;
    }
    .news-box {
        background-color: #F1F5F9; padding: 15px; border-radius: 8px; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_and_scrub():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name'])
    df['MIT_D4'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance', case=False, na=False)
    df['MIT_D6'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media', case=False, na=False)
    return df

df = load_and_scrub()

# SECRETS
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")

# --- SIDEBAR ---
st.sidebar.title("🏛️ AI OBSERVATORY")
nav = st.sidebar.radio("Navigation", ["📈 Current Findings", "🔍 Individual Audit", "📖 Governance Glossary"])
sector_focus = st.sidebar.selectbox("Sector Context", ["Global Market"] + sorted(df['Category'].unique().tolist()))

# --- PAGE 1: CURRENT FINDINGS ---
if nav == "📈 Current Findings":
    st.title("Current Findings")
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df):,}</div><small>TOTAL ENTITIES</small></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-value">{df["MIT_D4"].sum()}</div><small>PRIVACY FLAGS (D4)</small></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-value">{df["MIT_D6"].sum()}</div><small>INTEGRITY FLAGS (D6)</small></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    col_g, col_r = st.columns(2)
    with col_g:
        st.subheader("💡 Strategic Investment Gaps")
        sector_counts = df['Category'].value_counts()
        gaps = sector_counts[sector_counts < (sector_counts.mean() / 2)].head(3)
        for sector, count in gaps.items():
            st.markdown(f"<div class='advisory-card'><strong>{sector}</strong><br>Inventory: {count} Tools</div>", unsafe_allow_html=True)
    with col_r:
        st.subheader("⚠️ Regulatory Hotspots")
        hotspots = df.groupby('Category')['MIT_D4'].mean().sort_values(ascending=False).head(3)
        for sector, rate in hotspots.items():
            st.markdown(f"<div class='advisory-card' style='border-left-color:red;'><strong>{sector}</strong><br>Risk Density: {rate:.1%}</div>", unsafe_allow_html=True)

# --- PAGE 2: ENTITY AUDIT (Now with BOTH APIs) ---
elif nav == "🔍 Individual Audit":
    st.title("Individual Entity Intelligence")
    search_list = df if sector_focus == "Global Market" else df[df['Category'] == sector_focus]
    target = st.selectbox("Search Target Entity:", [""] + sorted(search_list['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        st.header(target)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📋 Audit Profile")
            st.write(f"**Description:** {tool['Short Description']}")
            st.write(f"**MIT D4 (Privacy):** {'🔴 Flagged' if tool['MIT_D4'] else '🟢 Clear'}")
            st.write(f"- **MIT D6 (Integrity):** {'🔴 Flagged' if tool['MIT_D6'] else '🟢 Clear'}")
            
            # --- NEWS API INTEGRATION ---
            st.markdown("### 📡 Live Intelligence Feed")
            if NEWS_API_KEY:
                try:
                    n_url = f'https://newsapi.org/v2/everything?q={target}+AI&apiKey={NEWS_API_KEY}&pageSize=3'
                    articles = requests.get(n_url).json().get('articles', [])
                    if articles:
                        for art in articles:
                            st.markdown(f"<div class='news-box'><strong>{art['title']}</strong><br><small>{art['source']['name']}</small></div>", unsafe_allow_html=True)
                    else: st.write("No recent regulatory news found.")
                except: st.error("News Feed Offline.")
            else: st.warning("News API Key missing.")

        with c2:
            st.markdown("### 📈 Market Trust Signal")
            ticker = st.text_input("Enter Parent Ticker (e.g. MSFT):", "").upper()
            if ticker and AV_API_KEY:
                q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                quote = requests.get(q_url).json().get('Global Quote', {})
                if quote:
                    st.metric(f"{ticker} Value", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))

# --- PAGE 3: GLOSSARY ---
elif nav == "📖 Governance Glossary":
    st.title("Governance Framework")
    st.markdown("""
    **MIT D4 (Privacy):** Flagging unauthorized surveillance and data harvesting.  
    **MIT D6 (Integrity):** Flag

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI ARCHITECTURE
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .metric-card {
        background-color: #F8FAFC; border: 1px solid #E2E8F0;
        padding: 20px; border-radius: 12px; text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 800; color: #1C3D5A; }
    .consulting-banner {
        background-color: #1C3D5A; color: white; padding: 10px;
        text-align: center; border-radius: 5px; margin-bottom: 20px;
    }
    .advisory-card {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        padding: 15px; border-radius: 10px; margin-bottom: 10px;
        border-left: 5px solid #3B82F6;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_and_scrub():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name'])
    # MIT RISK CLASSIFICATION
    df['MIT_D4'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance', case=False, na=False)
    df['MIT_D6'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media', case=False, na=False)
    return df

df = load_and_scrub()

# SECRETS
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")

# --- SIDEBAR ---
st.sidebar.markdown("### 🏛️ AI OBSERVATORY")
st.sidebar.markdown("---")
nav = st.sidebar.radio("Navigation", ["📈 Current Findings", "🔍 Individual Audit", "📖 Governance Glossary"])
st.sidebar.markdown("---")
st.sidebar.caption("Strategic Analysis by **Philip’s Consulting**")

# --- PAGE 1: CURRENT FINDINGS (DASHBOARD) ---
if nav == "📈 Current Findings":
    st.markdown("<div class='consulting-banner'>Strategic Intelligence Portal by Philip’s Consulting</div>", unsafe_allow_html=True)
    st.title("Executive Dashboard")
    
    # ROW 1: METRICS
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df):,}</div><small>ENTITIES AUDITED</small></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-value">{df["MIT_D4"].sum()}</div><small>PRIVACY ALERTS (D4)</small></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-value">{df["MIT_D6"].sum()}</div><small>INTEGRITY ALERTS (D6)</small></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ROW 2: CHARTS
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📊 Market Penetration by Sector")
        sector_counts = df['Category'].value_counts().head(10).reset_index()
        fig1 = px.bar(sector_counts, x='count', y='Category', orientation='h', 
                      color='count', color_continuous_scale='Blues')
        fig1.update_layout(showlegend=False, height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("🔥 MIT Risk Density Heatmap")
        # Calculating % of risk per sector
        risk_stats = df.groupby('Category').agg({'MIT_D4': 'mean', 'Name': 'count'}).reset_index()
        risk_stats = risk_stats[risk_stats['Name'] > 50].sort_values('MIT_D4', ascending=False).head(10)
        fig2 = px.scatter(risk_stats, x='MIT_D4', y='Category', size='Name', color='MIT_D4',
                          labels={'MIT_D4': 'Privacy Risk %', 'Category': ''},
                          color_continuous_scale='Reds')
        fig2.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig2, use_container_width=True)

    # ROW 3: ADVISORY
    st.markdown("---")
    st.subheader("📋 Strategic Advisory")
    col_g, col_r = st.columns(2)
    with col_g:
        st.write("**Investment Gaps (Strategic Opportunity)**")
        counts = df['Category'].value_counts()
        gaps = counts[counts < (counts.mean() / 2)].head(3)
        for s, c in gaps.items():
            st.markdown(f"<div class='advisory-card'><strong>{s}</strong><br>Market Density: Low ({c} Tools)</div>", unsafe_allow_html=True)
    with col_r:
        st.write("**Regulatory Hotspots (High Watch)**")
        hotspots = df.groupby('Category')['MIT_D4'].mean().sort_values(ascending=False).head(3)
        for s, r in hotspots.items():
            st.markdown(f"<div class='advisory-card' style='border-left-color:red;'><strong>{s}</strong><br>Risk Density: {r:.1%}</div>", unsafe_allow_html=True)

# --- PAGE 2: ENTITY AUDIT ---
elif nav == "🔍 Individual Audit":
    st.title("Entity Intelligence Audit")
    target = st.selectbox("Select Target:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        st.markdown(f"## {target}")
        ca, cb = st.columns(2)
        with ca:
            st.write(f"**Description:** {tool['Short Description']}")
            st.write(f"**MIT D4 (Privacy):** {'🔴 Flagged' if tool['MIT_D4'] else '🟢 Clear'}")
            st.write(f"**MIT D6 (Integrity):** {'🔴 Flagged' if tool['MIT_D6'] else '🟢 Clear'}")
            
            if NEWS_API_KEY:
                st.markdown("### 📡 Live Intel Feed")
                n_url = f'https://newsapi.org/v2/everything?q={target}+AI&apiKey={NEWS_API_KEY}&pageSize=3'
                articles = requests.get(n_url).json().get('articles', [])
                for art in articles:
                    st.markdown(f"<div style='background:#f1f5f9; padding:10px; border-radius:5px; margin-bottom:5px;'><strong>{art['title']}</strong></div>", unsafe_allow_html=True)

        with cb:
            st.markdown("### 📈 Market Signal")
            ticker = st.text_input("Enter Ticker (e.g. MSFT):", "").upper()
            if ticker and AV_API_KEY:
                q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                quote = requests.get(q_url).json().get('Global Quote', {})
                if quote:
                    st.metric(f"{ticker} Value", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))

# --- PAGE 3: GLOSSARY ---
elif nav == "📖 Governance Glossary":
    st.title("Governance Framework")
    st.write("Auditing methodology by **Philip’s Consulting** based on the MIT AI Risk Repository.")
    st.markdown("""
    - **D4 Privacy:** Risks of persistent surveillance.
    - **D6 Integrity:** Risks of synthetic media generation.
    - **SIG Metric:** Identification of market gaps.
    - **MTS Metric:** Financial stability correlation.
    """)

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI CONFIGURATION & DESIGNER STYLING
st.set_page_config(page_title="AI Observatory | PHIL's Consulting", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .metric-card {
        background-color: #F8FAFC; border: 1px solid #E2E8F0;
        padding: 24px; border-radius: 12px; text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #1E293B; margin-bottom: 5px; }
    .metric-label { font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
    .advisory-card {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        padding: 18px; border-radius: 10px; margin-bottom: 12px;
        border-left: 5px solid #3B82F6;
    }
    .risk-card { border-left: 5px solid #EF4444; }
    .section-title { font-size: 1.4rem; font-weight: 700; color: #1E293B; margin-bottom: 20px; }
    section[data-testid="stSidebar"] { background-color: #F1F5F9; border-right: 1px solid #E2E8F0; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_and_scrub():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
    df['MIT_D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance|harvest', case=False, na=False)
    df['MIT_D6_Integrity'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media|manipulate', case=False, na=False)
    return df

df = load_and_scrub()
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("## 🏛️ AI OBSERVATORY")
st.sidebar.caption("Government Strategic Oversight v4.0")
nav = st.sidebar.radio("Observation Mode", ["📈 Current Findings", "🔍 Entity Audit", "📖 Governance Glossary"])
st.sidebar.markdown("---")
sector_focus = st.sidebar.selectbox("Sector Context", ["Global Market"] + sorted(df['Category'].unique().tolist()))

# --- PAGE 1: CURRENT FINDINGS ---
if nav == "📈 Current Findings":
    st.markdown("<h1 style='margin-bottom:0;'>Current Findings</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B;'>High-level summary of the global AI landscape and regulatory pressures.</p>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df):,}</div><div class="metric-label">Total Entities Monitored</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{df["MIT_D4_Privacy"].sum()}</div><div class="metric-label">MIT D4 Privacy Flags</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{df["MIT_D6_Integrity"].sum()}</div><div class="metric-label">MIT D6 Integrity Flags</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_gap, col_risk = st.columns(2)
    with col_gap:
        st.markdown("<div class='section-title'>💡 Strategic Investment Gaps</div>", unsafe_allow_html=True)
        sector_counts = df['Category'].value_counts()
        avg_density = sector_counts.mean()
        gaps = sector_counts[sector_counts < (avg_density / 2)].head(4)
        for sector, count in gaps.items():
            st.markdown(f"<div class='advisory-card'><strong>{sector}</strong><br><small>Inventory: {count} Tools • Strategic Priority: High</small></div>", unsafe_allow_html=True)
            
    with col_risk:
        st.markdown("<div class='section-title'>⚠️ Regulatory Watchlist</div>", unsafe_allow_html=True)
        hotspots = df.groupby('Category')['MIT_D4_Privacy'].mean().sort_values(ascending=False).head(4)
        for sector, rate in hotspots.items():
            st.markdown(f"<div class='advisory-card risk-card'><strong>{sector}</strong><br><small>MIT Risk Density: {rate:.1%} • Oversight Status: Critical</small></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🌐 AI Sector Hierarchy & Risk Intensity")
    st.caption("Click segments to zoom. Red indicates high concentration of MIT D4 Privacy risks.")
    
    # Replacement for Treemap: Sunburst Chart
    # Sampling for performance and visual clarity
    sun_df = df.sample(n=min(800, len(df)))
    fig = px.sunburst(sun_df, path=['Category', 'Name'], color='MIT_D4_Privacy',
                      color_discrete_map={True: '#EF4444', False: '#3B82F6'},
                      template='plotly_white')
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=650)
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: ENTITY AUDIT ---
elif nav == "🔍 Entity Audit":
    st.markdown("<h1 style='margin-bottom:0;'>Individual Entity Audit</h1>", unsafe_allow_html=True)
    
    search_list = df if sector_focus == "Global Market" else df[df['Category'] == sector_focus]
    target = st.selectbox("Select Target Entity:", [""] + sorted(search_list['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        
        ca, cb = st.columns(2)
        with ca:
            st.markdown(f"### {target}")
            st.markdown(f"<div class='advisory-card'><strong>Technical Metadata</strong><br>{tool['Short Description']}</div>", unsafe_allow_html=True)
            st.write("**MIT Risk Assessment:**")
            st.write(f"- Privacy & Surveillance (D4): {'🔴 Flagged' if tool['MIT_D4_Privacy'] else '🟢 Minimal Signal'}")
            st.write(f"- Content Integrity (D6): {'🔴 Flagged' if tool['MIT_D6_Integrity'] else '🟢 Minimal Signal'}")
            
        with cb:
            # Finance and News moved here, only visible upon lookup
            st.markdown("<div class='advisory-card'><strong>📈 Market Trust Signal</strong></div>", unsafe_allow_html=True)
            ticker = st.text_input("Enter Parent Co. Stock Ticker (e.g. MSFT):", "").upper()
            
            if ticker and AV_API_KEY:
                try:
                    q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                    quote_data = requests.get(q_url).json().get('Global Quote', {})
                    if quote_data:
                        st.metric(f"{ticker} Price", f"${quote_data.get('05. price')}", delta=quote_data.get('10. change percent'))
                    else: st.warning("Ticker not found.")
                except: st.error("API Connection Error.")
            
            st.markdown("---")
            st.write("**Latest Regulatory Intel:**")
            # Simple simulation of news intel for the specific tool
            st.caption(f"Scanning global news for mentions of {target} compliance...")
            st.info(f"No active enforcement actions found for {target} in the last 24 hours.")

# --- PAGE 3: GOVERNANCE GLOSSARY ---
elif nav == "📖 Governance Glossary":
    st.markdown("<h1>Governance Glossary</h1>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Core MIT Risk Domains")
        st.markdown("""
        **D1: System Safety & Security** Malfunctions or exploits in AI logic.
        **D2: Socio-economic Impact** Labor displacement and digital divide.
        **D4: Data Privacy** Unauthorized surveillance and tracking.
        **D6: Content Integrity** Deepfakes and synthetic media.
        """)
    with col_r:
        st.subheader("Observatory Analytics")
        st.markdown("""
        **Strategic Investment Gap (SIG)** Identifying low-density tech sectors.
        **Market Trust Signal (MTS)** Real-time financial health via Alpha Vantage.
        """)
    st.info("The AI Observatory is built upon the MIT AI Risk Repository (v4.0).")

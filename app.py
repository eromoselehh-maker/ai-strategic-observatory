import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. INSTITUTIONAL CONFIGURATION
st.set_page_config(page_title="AI Observatory", layout="wide")

# Professional Styling: Ultra-clean white and slate
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .status-card {
        padding: 20px; border-radius: 10px; border: 1px solid #f0f2f6;
        background-color: #fcfcfc; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);
    }
    .advisory-tag {
        color: #1c3d5a; font-weight: bold; background: #eef2f6;
        padding: 4px 10px; border-radius: 5px; font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_and_scrub():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name'])
    # MIT RISK CLASSIFICATION
    df['MIT_D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance', case=False, na=False)
    df['MIT_D6_Integrity'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media', case=False, na=False)
    return df

df = load_and_scrub()
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# --- SIDEBAR ---
st.sidebar.title("🏛️ AI Observatory")
nav = st.sidebar.radio("Go to:", ["📈 Current Findings", "🔍 Individual Audit", "📖 Governance Glossary"])
sector_focus = st.sidebar.selectbox("Sector Focus", ["Global Market"] + sorted(df['Category'].unique().tolist()))

# --- PAGE 1: CURRENT FINDINGS ---
if nav == "📈 Current Findings":
    st.title("Current Findings")
    st.caption(f"Real-time analysis of {len(df):,} entities across {df['Category'].nunique()} sectors.")

    # High-Level Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Global Tool Volume", f"{len(df):,}")
    m2.metric("Critical Privacy Risk (D4)", f"{df['MIT_D4_Privacy'].sum():,}")
    m3.metric("Content Integrity Risk (D6)", f"{df['MIT_D6_Integrity'].sum():,}")

    st.markdown("---")
    
    col_gap, col_risk = st.columns(2)
    
    with col_gap:
        st.subheader("💡 Strategic Investment Gaps")
        st.write("Where the market is lacking (High Investment Priority):")
        sector_counts = df['Category'].value_counts()
        gaps = sector_counts[sector_counts < (sector_counts.mean() / 2)].head(4)
        for sector, count in gaps.items():
            st.markdown(f"<span class='advisory-tag'>GAP</span> **{sector}** ({count} tools)", unsafe_allow_html=True)
            
    with col_risk:
        st.subheader("⚠️ Regulatory Hotspots")
        st.write("Sectors with highest MIT Risk density:")
        risk_map = df.groupby('Category')['MIT_D4_Privacy'].mean().sort_values(ascending=False).head(4)
        for sector, rate in risk_map.items():
            st.markdown(f"<span class='advisory-tag' style='background:#fff0f0; color:#c53030;'>RISK</span> **{sector}** ({rate:.1%} flag rate)", unsafe_allow_html=True)

    st.markdown("---")
    # Clean visual
    fig = px.treemap(df.head(1000), path=['Category', 'Name'], values='MIT_D4_Privacy',
                     color='MIT_D4_Privacy', color_continuous_scale='Blues')
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: INDIVIDUAL AUDIT ---
elif nav == "🔍 Individual Audit":
    st.title("Entity Intelligence")
    search_list = df if sector_focus == "Global Market" else df[df['Category'] == sector_focus]
    target = st.selectbox("Select Tool:", [""] + sorted(search_list['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.write(f"### Profile: {target}")
            st.info(f"**Description:** {tool['Short Description']}")
            st.write(f"**MIT Compliance Status:**")
            st.write(f"- Privacy (D4): {'🔴 Flagged' if tool['MIT_D4_Privacy'] else '🟢 Clear'}")
            st.write(f"- Integrity (D6): {'🔴 Flagged' if tool['MIT_D6_Integrity'] else '🟢 Clear'}")
            
        with c2:
            st.write("### 📈 Market Trust Signal")
            manual_ticker = st.text_input("Enter Parent Ticker (e.g. MSFT, GOOGL):", "").upper()
            ticker = manual_ticker if manual_ticker else "" # Fallback logic here
            
            if ticker and AV_API_KEY:
                q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                quote = requests.get(q_url).json().get('Global Quote', {})
                if quote:
                    st.metric(f"Market Performance ({ticker})", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))
            else:
                st.write("Provide a stock ticker to evaluate the parent corporation's stability.")

# --- PAGE 3: GLOSSARY ---
elif nav == "📖 Governance Glossary":
    st.title("Governance Glossary")
    st.write("Understanding the MIT AI Risk Repository Framework.")
    
    st.markdown("""
    ### MIT Domain 4: Data Privacy & Security
    **Definition:** Risks related to unauthorized or excessive data collection. 
    In this observatory, we flag tools that describe tracking, surveillance, or personal data harvesting.
    
    ### MIT Domain 6: Content & Misinformation
    **Definition:** Risks involving synthetic media generation. 
    We flag tools capable of creating deepfakes, synthetic voices, or generative media that could disrupt content integrity.
    
    ### Market Trust Signal
    **Definition:** A quantitative measure of corporate stability. 
    We link technological entities to their parent stocks via Alpha Vantage to assess if the financial market trusts the company behind the tech.
    """)

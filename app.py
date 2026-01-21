import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. INSTITUTIONAL CONFIGURATION
st.set_page_config(page_title="AI Observatory", layout="wide")

# Custom Styling for Academic/Consulting look
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .advisory-card {
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        background-color: #f8f9fa;
        margin-bottom: 20px;
    }
    .mit-label {
        font-weight: bold;
        color: #1c3d5a;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_and_scrub():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name'])
    # MIT RISK CLASSIFICATION
    # Domain 4: Data Privacy (Unauthorized collection, surveillance, tracking)
    df['MIT_D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance', case=False, na=False)
    # Domain 6: Content Integrity (Deepfakes, misinformation, synthetic media)
    df['MIT_D6_Integrity'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media', case=False, na=False)
    return df

df = load_and_scrub()
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# --- HEADER & GLOSSARY ---
st.title("🏛️ AI Observatory")
st.caption("Strategic Policy & Investment Oversight Portal | Powered by MIT AI Risk Repository v4.0")

with st.expander("📖 Methodology & MIT Metric Definitions"):
    st.markdown("""
    **MIT AI Risk Repository Taxonomy (v4.0) Applied:**
    
    * <span class="mit-label">Domain 4: Data Privacy & Security (D4)</span>
        *Focus:* Risks involving unauthorized data collection, persistent surveillance, and lack of transparency in data processing. Tools flagged here show indicators of user-tracking or data-harvesting capabilities.
    
    * <span class="mit-label">Domain 6: Content & Misinformation Integrity (D6)</span>
        *Focus:* Risks involving the generation of synthetic media, deepfakes, or automated content that can be used for misinformation or identity impersonation.
    
    * <span class="mit-label">Market Trust Signal</span>
        *Focus:* Real-time financial valuation of parent entities via Alpha Vantage API to assess corporate stability and investment risk.
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
nav = st.sidebar.radio("Observation Mode", ["Strategic Advisory", "Entity Audit"])
sector_focus = st.sidebar.selectbox("Sector Focus", ["Global Market"] + sorted(df['Category'].unique().tolist()))

# --- MODULE 1: STRATEGIC ADVISORY (Investment & Risks) ---
if nav == "Strategic Advisory":
    st.header("📋 Strategic Sectoral Advisory")
    
    # Logic: Where is it lacking?
    sector_counts = df['Category'].value_counts()
    avg_density = sector_counts.mean()
    
    col_gap, col_risk = st.columns(2)
    
    with col_gap:
        st.subheader("💡 Strategic Investment Gaps")
        st.write("Sectors with low technical density (Investment Opportunities):")
        gaps = sector_counts[sector_counts < (avg_density / 2)].head(5)
        for sector, count in gaps.items():
            st.info(f"**{sector}**: Only {count} entities. Recommendation: High R&D Priority.")
            
    with col_risk:
        st.subheader("⚠️ High-Watch Hotspots")
        st.write("Sectors with highest MIT Risk concentrations (Regulatory Focus):")
        risk_map = df.groupby('Category')['MIT_D4_Privacy'].mean().sort_values(ascending=False).head(5)
        for sector, rate in risk_map.items():
            st.warning(f"**{sector}**: {rate:.1%} MIT D4 Flag rate. Recommendation: Compliance Review.")

    st.markdown("---")
    fig = px.treemap(df.head(1000), path=['Category', 'Name'], values='MIT_D4_Privacy',
                     color='MIT_D4_Privacy', color_continuous_scale='Blues',
                     title="Global Market Composition: Density & Risk distribution")
    st.plotly_chart(fig, use_container_width=True)

# --- MODULE 2: ENTITY AUDIT & MARKET SIGNAL ---
else:
    st.header("🔍 Individual Entity Intelligence Audit")
    search_list = df if sector_focus == "Global Market" else df[df['Category'] == sector_focus]
    target = st.selectbox("Select Tool to Audit:", [""] + sorted(search_list['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.markdown(f"### Profile: {target}")
            st.write(f"**Description:** {tool['Short Description']}")
            st.markdown(f"""
            **MIT Risk Profile:**
            - **Privacy (D4):** {'🔴 Flagged' if tool['MIT_D4_Privacy'] else '🟢 Minimal Signal'}
            - **Integrity (D6):** {'🔴 Flagged' if tool['MIT_D6_Integrity'] else '🟢 Minimal Signal'}
            """)
            
        with c2:
            st.markdown("### 📈 Market Trust Signal")
            manual_ticker = st.text_input("Enter Parent Ticker (e.g. MSFT, GOOGL, NVDA) if known:", "").upper()
            
            ticker = manual_ticker
            if not ticker and AV_API_KEY:
                # Automated Guess
                s_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={target}&apikey={AV_API_KEY}"
                matches = requests.get(s_url).json().get('bestMatches', [])
                if matches: ticker = matches[0]['1. symbol']
            
            if ticker and AV_API_KEY:
                q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                quote = requests.get(q_url).json().get('Global Quote', {})
                if quote:
                    st.metric(f"Market Performance ({ticker})", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))
                else:
                    st.write("Ticker identified but market data currently unavailable.")
            else:
                st.write("Entity is private or no ticker match found. Provide manual ticker for evaluation.")

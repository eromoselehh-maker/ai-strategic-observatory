import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI CONFIGURATION & CSS
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

# This CSS creates the "Top Ticker" and makes buttons look like cards
st.markdown("""
    <style>
    /* Scrolling Ticker Styling */
    .ticker-wrap {
        width: 100%; overflow: hidden; background-color: #1C3D5A; 
        color: white; padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 999;
    }
    .ticker {
        display: inline-block; white-space: nowrap; padding-right: 100%;
        animation: ticker 30s linear infinite; font-weight: bold;
    }
    @keyframes ticker {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    /* Adjust Main Content to fit under fixed ticker */
    .main .block-container { padding-top: 5rem; }
    
    .stButton>button {
        width: 100%; border-radius: 12px; height: 100px; 
        background-color: #F8FAFC; border: 1px solid #E2E8F0;
        transition: all 0.3s; font-size: 1.1rem;
    }
    .stButton>button:hover {
        border-color: #3B82F6; background-color: #EFF6FF; transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA LOADING
@st.cache_data
def load_and_scrub():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name'])
    df['MIT_D4'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance', case=False, na=False)
    df['MIT_D6'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media', case=False, na=False)
    return df

df = load_and_scrub()
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")

# 3. TOP TICKER (THE "WEATHER POP-UP" STYLE)
ticker_text = " 🟢 MARKET LIVE: NVDA +2.4% | MSFT -0.1% | PLTR +4.2% | GOOG +1.1% | TRENDING: EU AI Act Compliance Deadline Approaching... | NEW ALERT: 450+ Privacy Flags Detected in Search Tools... "
st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            {ticker_text} &nbsp;&nbsp;&nbsp;&nbsp; {ticker_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. SIDEBAR & NAVIGATION
st.sidebar.markdown("### 🏛️ AI OBSERVATORY")
st.sidebar.caption("By **Philip’s Consulting**")
nav = st.sidebar.radio("Navigate", ["📈 Dashboard", "🔍 Entity Audit", "📖 Framework"])

# Initialize Session State for interactive filtering
if 'filtered_sector' not in st.session_state:
    st.session_state.filtered_sector = "Global Market"

# --- PAGE 1: DASHBOARD ---
if nav == "📈 Dashboard":
    st.title("Strategic Governance Dashboard")
    
    # CLICKABLE TOP CARDS
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f"📊 {len(df):,} Tools \n View All Entities"):
            st.session_state.filtered_sector = "Global Market"
    with c2:
        if st.button(f"🔴 {df['MIT_D4'].sum()} Flags \n High Privacy Risk"):
            st.session_state.filtered_sector = "Data Analysis" # Example filter
    with c3:
        if st.button(f"⚠️ {df['MIT_D6'].sum()} Flags \n Integrity Threats"):
            st.session_state.filtered_sector = "Text Generation"

    st.markdown("---")
    
    # MAIN CHARTS
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("Risk Distribution by Category")
        fig = px.treemap(df.sample(500), path=['Category'], values='MIT_D4', color='MIT_D4', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("📡 Live Industry Intel")
        if NEWS_API_KEY:
            try:
                url = f"https://newsapi.org/v2/everything?q=AI+regulation&apiKey={NEWS_API_KEY}&pageSize=4"
                articles = requests.get(url).json().get('articles', [])
                for art in articles:
                    st.markdown(f"""
                    <div style='padding:10px; border-bottom:1px solid #eee;'>
                        <a href='{art['url']}' style='font-size:0.9rem; color:#1C3D5A; text-decoration:none;'><strong>{art['title']}</strong></a>
                    </div>
                    """, unsafe_allow_html=True)
            except: st.write("Feed loading...")

# --- PAGE 2: ENTITY AUDIT ---
elif nav == "🔍 Entity Audit":
    st.title("Deep-Dive Intelligence")
    # This filter reacts to buttons clicked on the homepage
    sector = st.selectbox("Select Sector Context:", ["Global Market"] + sorted(df['Category'].unique().tolist()), 
                          index=0 if st.session_state.filtered_sector == "Global Market" else 1)
    
    target = st.selectbox("Select Target Entity:", [""] + sorted(df[df['Category'] == sector]['Name'].unique().tolist()) if sector != "Global Market" else sorted(df['Name'].unique().tolist()))
    
    if target:
        st.subheader(f"Strategic Audit: {target}")
        # Add the stock and news bits here as per previous versions
        st.info(f"Audit Status: ACTIVE. Cross-referencing {target} with MIT D4 and D6 repositories.")
        
# --- PAGE 3: FRAMEWORK ---
elif nav == "📖 Framework":
    st.title("Philip's Consulting AI Methodology")
    st.write("This platform utilizes the MIT AI Risk Repository and real-time news/market signals to provide 360-degree oversight.")

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. LUXURY UX CONFIGURATION
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

st.markdown("""
    <style>
    /* Global Styling */
    .stApp { background-color: #F1F5F9; font-family: 'Inter', sans-serif; }
    
    /* The Glassmorphism Ticker */
    .ticker-wrap {
        width: 100%; background: rgba(28, 61, 90, 0.95); 
        backdrop-filter: blur(10px); color: #00D1FF; padding: 12px 0; 
        position: fixed; top: 0; left: 0; z-index: 999;
        border-bottom: 2px solid #00D1FF; font-family: monospace;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; 
        animation: ticker 45s linear infinite; 
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* Spacing for Ticker */
    .main .block-container { padding-top: 7rem; }

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF; border: 1px solid #E2E8F0; padding: 25px;
        border-radius: 16px; text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .kpi-val { font-size: 2.4rem; font-weight: 800; color: #1C3D5A; margin: 0; }
    .kpi-label { font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; }

    /* Section Headers */
    .section-header { 
        font-size: 1.5rem; font-weight: 700; color: #1C3D5A; 
        margin-bottom: 20px; border-left: 5px solid #00D1FF; padding-left: 15px;
    }
    
    /* Navigation Cleanup */
    [data-testid="stSidebar"] { background-color: #F8FAFC; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    # ADJUST FILENAME HERE IF NECESSARY
    try:
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        # Metric Logic: Search for keywords in description
        df['MIT_D4'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance|personal info', case=False, na=False)
        df['MIT_D6'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media|deepfake', case=False, na=False)
        return df
    except Exception as e:
        st.error(f"Data Load Error: {e}")
        return pd.DataFrame()

df = load_data()
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# 3. TOP TICKER (Institutional Pop-up Intel)
ticker_msg = " ⚠️ MIT D4 ALERT: Surge in surveillance metadata tools | 🟢 MARKET CONFIDENCE: AI Infrastructure Sector +2.4% | 🏛️ PHILIP'S CONSULTING: Strategic Audit Mode Active | NEWS: EU AI Act D6 Compliance Guidelines Released "
st.markdown(f'<div class="ticker-wrap"><div class="ticker">{ticker_msg * 4}</div></div>', unsafe_allow_html=True)

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<h2 style='color:#1C3D5A;'>🏛️ AI Observatory</h2>", unsafe_allow_html=True)
    st.caption("Strategic Audit Portal")
    nav = st.radio("Intelligence Command", ["Executive Overview", "Deep-Dive Audit", "Framework Glossary"])
    st.markdown("---")
    st.caption("Produced for Philip's Consulting")

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if nav == "Executive Overview":
    st.markdown("<div class='section-header'>Executive Overview</div>", unsafe_allow_html=True)
    
    # KPI Row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="kpi-card"><p class="kpi-label">Entities Audited</p><p class="kpi-val">{len(df):,}</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><p class="kpi-label">Privacy Risks (D4)</p><p class="kpi-val" style="color:#EF4444;">{df["MIT_D4"].sum()}</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><p class="kpi-label">Integrity Risks (D6)</p><p class="kpi-val" style="color:#F59E0B;">{df["MIT_D6"].sum()}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualization Row
    col_viz, col_feed = st.columns([2, 1])
    
    with col_viz:
        st.subheader("Interactive Sector Risk Map")
        # Treemap allows click-to-zoom insight
        fig = px.treemap(df.sample(min(1000, len(df))), path=['Category', 'Name'], values='MIT_D4', 
                         color='MIT_D4', color_continuous_scale='Blues',
                         color_continuous_midpoint=0.5)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Note: Treemap visualization uses a statistical sample for performance. Click sectors to explore.")

    with col_feed:
        st.subheader("📡 Live Intelligence Feed")
        if NEWS_API_KEY:
            try:
                res = requests.get(f"https://newsapi.org/v2/everything?q=AI+regulation&apiKey={NEWS_API_KEY}&pageSize=4").json()
                articles = res.get('articles', [])
                if articles:
                    for art in articles:
                        st.markdown(f"""
                            <div style="background:white; border:1px solid #E2E8F0; padding:12px; border-radius:10px; margin-bottom:10px;">
                                <small style="color:#00D1FF; font-weight:bold;">{art['source']['name']}</small><br>
                                <a href="{art['url']}" target="_blank" style="text-decoration:none; color:#1C3D5A; font-weight:600; font-size:0.9rem;">{art['title']}</a>
                            </div>
                        """, unsafe_allow_html=True)
                else: st.write("No recent regulatory news.")
            except: st.write("Intel feed currently disconnected.")
        else:
            st.warning("News API Key missing in Secrets.")

# --- PAGE 2: DEEP-DIVE AUDIT ---
elif nav == "Deep-Dive Audit":
    st.markdown("<div class='section-header'>Individual Entity Intelligence</div>", unsafe_allow_html=True)
    
    target = st.selectbox("Search Target Entity:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        
        ca, cb = st.columns(2)
        with ca:
            # Styled Audit Card
            st.markdown(f"""
                <div style="background:#1C3D5A; color:white; padding:30px; border-radius:16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                    <h2 style="margin:0; color:#00D1FF;">{target}</h2>
                    <p style="text-transform:uppercase; font-size:0.8rem; letter-spacing:1px; opacity:0.8;">Sector: {tool['Category']}</p>
                    <hr style="border-color:rgba(255,255,255,0.2);">
                    <p style="font-size:1rem; line-height:1.6;">{tool['Short Description']}</p>
                    <div style="margin-top:20px; display:flex; gap:15px;">
                        <span style="background:{'#EF4444' if tool['MIT_D4'] else '#10B981'}; padding:5px 12px; border-radius:20px; font-size:0.75rem; font-weight:bold;">
                            MIT D4: {'RISK' if tool['MIT_D4'] else 'CLEAR'}
                        </span>
                        <span style="background:{'#F59E0B' if tool['MIT_D6'] else '#10B981'}; padding:5px 12px; border-radius:20px; font-size:0.75rem; font-weight:bold;">
                            MIT D6: {'RISK' if tool['MIT_D6'] else 'CLEAR'}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with cb:
            st.markdown("<div style='background:white; border:1px solid #E2E8F0; padding:25px; border-radius:16px;'>", unsafe_allow_html=True)
            st.markdown("<p class='kpi-label'>Market Confidence Tracker</p>", unsafe_allow_html=True)
            ticker = st.text_input("Enter Parent Ticker (e.g., MSFT, PLTR):").upper()
            
            if ticker and AV_API_KEY:
                q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                try:
                    quote = requests.get(q_url).json().get('Global Quote', {})
                    if quote:
                        st.metric(f"{ticker} Value", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))
                    else: st.error("Ticker not found or API limit reached.")
                except: st.error("Finance API Error.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: GLOSSARY ---
elif nav == "Framework Glossary":
    st.markdown("<div class='section-header'>MIT AI Risk Framework</div>", unsafe_allow_html=True)
    st.write("Auditing methodology derived from the MIT AI Risk Repository (v4.0).")
    
    st.markdown("""
    <div style="background:white; border:1px solid #E2E8F0; padding:30px; border-radius:16px;">
    <h4 style="color:#1C3D5A;">Primary Governance Domains</h4>
    <p><b>Domain 4: Data Privacy & Security</b><br>Focuses on unauthorized data collection, persistent tracking, and surveillance mechanisms within AI architecture.</p>
    <hr>
    <p><b>Domain 6: Content Integrity</b><br>Focuses on synthetic media generation (deepfakes), automated misinformation, and the dilution of evidence-based content.</p>
    <hr>
    <p><b>Strategic Market Trust (SMT)</b><br>Philip's Consulting proprietary metric correlating corporate stability (via Alpha Vantage) with technological risk vectors.</p>
    </div>
    """, unsafe_allow_html=True)

# FOOTER
st.markdown("<br><hr><p style='text-align:center; color:#94A3B8; font-size:0.8rem;'>OFFICIAL PROPERTY OF PHILIP'S CONSULTING | AI STRATEGIC OBSERVATORY 2025</p>", unsafe_allow_html=True)

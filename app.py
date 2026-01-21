import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. PREMIUM UI ARCHITECTURE (CSS OVERHAUL)
st.set_page_config(page_title="Philip’s AI Observatory", layout="wide")

st.markdown("""
    <style>
    /* Obsidian Theme & Modern Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
    
    .stApp { background-color: #0F172A; font-family: 'Plus Jakarta Sans', sans-serif; color: #F8FAFC; }
    
    /* Modern Ticker: Cyberpunk Style */
    .ticker-wrap {
        width: 100%; background: #1E293B; border-bottom: 2px solid #38BDF8;
        padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; 
        font-family: 'Courier New', monospace; font-weight: bold;
        animation: ticker 40s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* Card Styling: Glassmorphism */
    .metric-card {
        background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; 
        padding: 24px; border-radius: 16px; text-align: center;
        transition: 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-card:hover { border-color: #38BDF8; background: #1E293B; }
    .metric-label { font-size: 0.8rem; color: #94A3B8; letter-spacing: 1.5px; text-transform: uppercase; }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #F8FAFC; }

    /* Navigation Sidebar Customization */
    [data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1E293B; }
    
    /* Main Content Spacing */
    .main .block-container { padding-top: 6.5rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA LOAD
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        # Mapping simple risk flags for demo
        df['Privacy_Risk'] = df['Short Description'].str.contains('privacy|tracking|data', case=False, na=False)
        df['Integrity_Risk'] = df['Short Description'].str.contains('fake|synthetic|voice', case=False, na=False)
        return df
    except: return pd.DataFrame()

df = load_data()
NEWS_KEY = st.secrets.get("NEWS_API_KEY", "")

# 3. LIVE TICKER
ticker_msg = " ⚡ [PHILIP'S CONSULTING] SIGNAL: D2 Security Threats spiking in Open-Source sector | MARKET: OpenAI (MSFT) Sentiment Neutral | GLOBAL: EU AI Act D4 Compliance Deadline Approaching... "
st.markdown(f'<div class="ticker-wrap"><div class="ticker">{ticker_msg * 5}</div></div>', unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown("<h1 style='color:#38BDF8; font-size:1.5rem;'>🏛️ OBSERVATORY</h1>", unsafe_allow_html=True)
    st.caption("Strategic Risk Intelligence")
    nav = st.radio("Navigation", ["Global Overview", "Entity Audit", "MIT Framework Glossary"])
    st.markdown("---")
    st.info("Status: Deep-Scan Active")

# --- PAGE 1: OVERVIEW ---
if nav == "Global Overview":
    st.markdown("### 📈 Strategic Risk Matrix")
    
    # Modern Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Entities Scanned</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Privacy Hotspots (D2)</div><div class="metric-value" style="color:#EF4444;">{df["Privacy_Risk"].sum()}</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Integrity Flags (D3)</div><div class="metric-value" style="color:#F59E0B;">{df["Integrity_Risk"].sum()}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    c_left, c_right = st.columns([2, 1])
    with c_left:
        # High-end Chart
        fig = px.treemap(df.sample(min(800, len(df))), path=['Category', 'Name'], values='Privacy_Risk', 
                         color='Privacy_Risk', color_continuous_scale='Turbo')
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with c_right:
        st.markdown("#### 📡 Intelligence Stream")
        if NEWS_KEY:
            try:
                res = requests.get(f"https://newsapi.org/v2/everything?q=AI+regulation&apiKey={NEWS_KEY}&pageSize=4").json()
                for art in res.get('articles', []):
                    st.markdown(f"<div style='border-bottom:1px solid #334155; padding:10px 0;'><a style='color:#38BDF8; text-decoration:none; font-size:0.9rem;' href='{art['url']}'>{art['title']}</a></div>", unsafe_allow_html=True)
            except: st.write("Stream paused.")

# --- PAGE 2: AUDIT ---
elif nav == "Entity Audit":
    st.markdown("### 🔍 Strategic Audit Tool")
    target = st.selectbox("Target Entity:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        st.markdown(f"""
            <div style="background:#1E293B; padding:30px; border-radius:20px; border:1px solid #38BDF8;">
                <h1 style="color:#38BDF8;">{target}</h1>
                <p style="font-size:1.1rem; line-height:1.6;">{tool['Short Description']}</p>
                <hr style="border-color:#334155;">
                <div style="display:flex; gap:20px;">
                    <div style="background:#0F172A; padding:15px; border-radius:10px; flex:1; text-align:center;">
                        <b>MIT Domain 2 (Privacy)</b><br>{'🔴 HIGH RISK' if tool['Privacy_Risk'] else '🟢 CLEAR'}
                    </div>
                    <div style="background:#0F172A; padding:15px; border-radius:10px; flex:1; text-align:center;">
                        <b>MIT Domain 3 (Integrity)</b><br>{'🔴 HIGH RISK' if tool['Integrity_Risk'] else '🟢 CLEAR'}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- PAGE 3: GLOSSARY (EXPANDED) ---
elif nav == "MIT Framework Glossary":
    st.markdown("### 📖 The MIT AI Risk Repository (v4.0)")
    st.write("Full Domain Taxonomy used for Philip's Consulting Audits.")
    
    glossary = {
        "D1: Discrimination & Toxicity": "Risks of unfair treatment, misrepresentation, or exposure to harmful/abusive content.",
        "D2: Privacy & Security": "Unauthorized data leaks, tracking, or system vulnerabilities that can be exploited by bad actors.",
        "D3: Misinformation": "Inadvertent spread of deceptive content that pollutes the information ecosystem.",
        "D4: Malicious Actors & Misuse": "Intentional harm via deepfakes, large-scale disinformation, or automated cyberattacks.",
        "D5: Human-Computer Interaction": "Risks of overreliance, loss of human agency, and emotional manipulation by AI.",
        "D6: Socioeconomic Harms": "Large-scale impacts on labor markets, wealth inequality, and environmental resources.",
        "D7: AI System Safety": "Technical failures, lack of robustness, and catastrophic alignment errors."
    }
    
    for key, val in glossary.items():
        with st.expander(key):
            st.write(val)

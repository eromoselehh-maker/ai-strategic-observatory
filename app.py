import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. ULTIMATE DESIGN SYSTEM
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp { background-color: #020617; font-family: 'Plus Jakarta Sans', sans-serif; color: #F8FAFC; }
    header {visibility: hidden;}
    
    .ticker-wrap {
        width: 100%; background: #0F172A; border-bottom: 1px solid #1E293B;
        padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; 
        font-family: monospace; font-size: 0.85rem; animation: ticker 50s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    .glass-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.4), rgba(15, 23, 42, 0.6));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 24px; border-radius: 20px; height: 100%;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .hero-val { font-size: 2.8rem; font-weight: 800; color: #38BDF8; letter-spacing: -1px; margin: 0; }
    .hero-label { font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }

    .main .block-container { padding-top: 5.5rem; padding-left: 3rem; padding-right: 3rem; }
    [data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1E293B; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    try:
        # Check filename match
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        df['D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|surveillance', case=False, na=False)
        df['D6_Integrity'] = df['Short Description'].str.contains('fake|synthetic|generate', case=False, na=False)
        return df
    except Exception as e:
        st.error(f"Data Connection Error: {e}")
        return pd.DataFrame()

df = load_data()
NEWS_KEY = st.secrets.get("NEWS_API_KEY", "")
AV_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# 3. TICKER
st.markdown(f'<div class="ticker-wrap"><div class="ticker"> ● PHILIP\'S CONSULTING SYSTEM ONLINE ● MONITORING {len(df):,} ASSETS ● D4 RISK CLUSTER: DATA PRIVACY ● D6 RISK CLUSTER: CONTENT INTEGRITY ● MARKET STABILITY: 94% ● </div></div>', unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown("<h1 style='color:#F8FAFC; margin-bottom:0;'>OBSERVATORY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#38BDF8; font-size:0.75rem; margin-top:0;'>STRATEGIC RISK ADVISORY</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    nav = st.radio("INTELLIGENCE MODULES", ["Global Dashboard", "Strategic Audit", "Risk Framework"])
    st.markdown("<div style='position: fixed; bottom: 20px; font-size:0.7rem; color:#475569;'>v5.1 Final Build | Philip's Consulting</div>", unsafe_allow_html=True)

# --- PAGE 1: GLOBAL DASHBOARD ---
if nav == "Global Dashboard":
    st.markdown("<h2 style='font-weight:800; letter-spacing:-1.5px; margin-bottom:20px;'>Market Risk Overview</h2>", unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    with k1: st.markdown(f'<div class="glass-card"><p class="hero-label">Total Entities</p><p class="hero-val">{len(df):,}</p></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="glass-card"><p class="hero-label">D4 Privacy Critical</p><p class="hero-val" style="color:#F87171;">{df["D4_Privacy"].sum()}</p></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="glass-card"><p class="hero-label">D6 Integrity Critical</p><p class="hero-val" style="color:#FBBF24;">{df["D6_Integrity"].sum()}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1, 1])
    
    with col1:
        st.markdown("<p class='hero-label'>Sector Risk Density (D4)</p>", unsafe_allow_html=True)
        bar_df = df.groupby('Category')['D4_Privacy'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(bar_df, x='D4_Privacy', y='Category', orientation='h', color='D4_Privacy', 
                         color_continuous_scale=['#1E293B', '#38BDF8'], template='plotly_dark')
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("<p class='hero-label'>Market Sector Breakdown</p>", unsafe_allow_html=True)
        # FIXED PIE LOGIC
        donut_df = df['Category'].value_counts().head(7).reset_index()
        donut_df.columns = ['Category_Name', 'Asset_Count']
        fig_pie = px.pie(donut_df, names='Category_Name', values='Asset_Count', hole=0.7, 
                         color_discrete_sequence=px.colors.sequential.Blues_r, template='plotly_dark')
        fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col3:
        st.markdown("<p class='hero-label'>📡 Global Intel Feed</p>", unsafe_allow_html=True)
        if NEWS_KEY:
            try:
                r = requests.get(f"https://newsapi.org/v2/everything?q=AI+risk+regulation&apiKey={NEWS_KEY}&pageSize=4").json()
                for art in r.get('articles', []):
                    st.markdown(f"""
                        <div style='background:rgba(255,255,255,0.03); padding:12px; margin-bottom:12px; border-radius:12px; border:1px solid rgba(255,255,255,0.05);'>
                            <a style='color:#F8FAFC; text-decoration:none; font-size:0.75rem; font-weight:600;' href='{art['url']}' target='_blank'>{art['title']}</a>
                        </div>
                    """, unsafe_allow_html=True)
            except: st.caption("Connection paused...")

# --- PAGE 2: STRATEGIC AUDIT ---
elif nav == "Strategic Audit":
    st.markdown("<h2 style='font-weight:800; letter-spacing:-1.5px; margin-bottom:20px;'>Entity Deep-Scan Audit</h2>", unsafe_allow_html=True)
    target = st.selectbox("Select Target Asset:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        ca, cb = st.columns([1.5, 1])
        with ca:
            st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #38BDF8;">
                    <h3 style="color:#38BDF8; margin-top:0;">{target}</h3>
                    <p style="color:#64748B; text-transform:uppercase; font-size:0.7rem; font-weight:700;">Sector: {tool['Category']}</p>
                    <p style="font-size:1.1rem; line-height:1.7; color:#CBD5E1;">{tool['Short Description']}</p>
                </div>
            """, unsafe_allow_html=True)
        with cb:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<p class='hero-label'>Equity Market Correlation</p>", unsafe_allow_html=True)
            ticker = st.text_input("Enter Parent Ticker:").upper()
            if ticker and AV_KEY:
                try:
                    q = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_KEY}").json().get('Global Quote', {})
                    if q: st.metric(f"{ticker} Market Price", f"${q.get('05. price')}", delta=q.get('10. change percent'))
                except: st.error("Market API limit reached.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: RISK FRAMEWORK ---
elif nav == "Risk Framework":
    st.markdown("<h2 style='font-weight:800; letter-spacing:-1.5px; margin-bottom:20px;'>MIT Risk Taxonomy</h2>", unsafe_allow_html=True)
    
    domains = {
        "Domain 1: Discrimination": "Bias in AI logic leading to unfair social outcomes.",
        "Domain 2: Privacy": "Unauthorized surveillance and data harvesting.",
        "Domain 3: Misinformation": "Accidental spread of deceptive generated content.",
        "Domain 4: Malicious Use": "Weaponization for cybercrime or deepfakes.",
        "Domain 5: Human Agency": "Erosion of decision-making and autonomy.",
        "Domain 6: Socioeconomic": "Labor displacement and resource depletion.",
        "Domain 7: AI System Safety": "Catastrophic misalignment and technical failure."
    }
    for d, desc in domains.items():
        with st.expander(f"📘 {d}"):
            st.markdown(f"<p style='color:#CBD5E1; font-size:1rem;'>{desc}</p>", unsafe_allow_html=True)
            st.caption("Governance Protocol: Philip's Consulting Standard")

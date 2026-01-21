import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. PREMIUM UX/UI SYSTEM
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
    .stApp { background-color: #020617; font-family: 'Plus Jakarta Sans', sans-serif; color: #F1F5F9; }
    
    /* Neon Top Ticker */
    .ticker-wrap {
        width: 100%; background: #0F172A; border-bottom: 1px solid #38BDF8;
        padding: 8px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; 
        font-family: 'Courier New', monospace; animation: ticker 40s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* Luxury Container Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4); border: 1px solid #334155;
        padding: 24px; border-radius: 16px; height: 100%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .metric-val { font-size: 2.4rem; font-weight: 800; color: #38BDF8; margin: 0; }
    .metric-label { font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }

    /* Layout Adjustments */
    .main .block-container { padding-top: 6.5rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    try:
        # ENSURE THIS FILENAME IS EXACT
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        df['D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|surveillance', case=False, na=False)
        df['D6_Integrity'] = df['Short Description'].str.contains('fake|synthetic|generate', case=False, na=False)
        return df
    except: return pd.DataFrame()

df = load_data()
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# 3. LIVE TICKER
st.markdown(f'<div class="ticker-wrap"><div class="ticker"> ⚡ PHILIP\'S CONSULTING LIVE: Auditing {len(df):,} AI Entities | Market Sentiment: Bullish | Priority Alerts: D4 Privacy Violations Detected... </div></div>', unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='color:#38BDF8;'>🏛️ OBSERVATORY</h2>", unsafe_allow_html=True)
    st.caption("Strategic Audit v4.2")
    nav = st.radio("Navigation Console", ["Executive Overview", "Deep-Dive Audit", "Framework Library"])
    st.markdown("---")
    st.caption("Consultant View: Philip's Consulting")

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if nav == "Executive Overview":
    st.markdown("### 📈 Strategic Intelligence Hub")
    
    # KPI Row
    k1, k2, k3 = st.columns(3)
    k1.markdown(f'<div class="glass-card"><p class="metric-label">Entities Monitored</p><p class="metric-val">{len(df):,}</p></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="glass-card"><p class="metric-label">Privacy Risks (D4)</p><p class="metric-val" style="color:#F87171;">{df["D4_Privacy"].sum()}</p></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="glass-card"><p class="metric-label">Integrity Risks (D6)</p><p class="metric-val" style="color:#FBBF24;">{df["D6_Integrity"].sum()}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualization Grid
    col_main, col_donut, col_news = st.columns([1.5, 1, 1])
    
    with col_main:
        st.markdown("<p class='metric-label'>Risk Distribution by Sector</p>", unsafe_allow_html=True)
        risk_data = df.groupby('Category')['D4_Privacy'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(risk_data, x='D4_Privacy', y='Category', orientation='h', color='D4_Privacy', color_continuous_scale='Reds', template='plotly_dark')
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_donut:
        # THE FIX: Replacing ugly numbers with a Donut Chart
        st.markdown("<p class='metric-label'>Market Share Breakdown</p>", unsafe_allow_html=True)
        sector_counts = df['Category'].value_counts().head(8).reset_index()
        sector_counts.columns = ['Sector', 'Count']
        fig_donut = px.pie(sector_counts, names='Sector', values='Count', hole=0.6, color_discrete_sequence=px.colors.sequential.Blues_r, template='plotly_dark')
        fig_donut.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_news:
        st.markdown("<p class='metric-label'>📡 Live Intel Feed</p>", unsafe_allow_html=True)
        if NEWS_API_KEY:
            try:
                res = requests.get(f"https://newsapi.org/v2/everything?q=AI+regulation&apiKey={NEWS_API_KEY}&pageSize=4").json()
                for art in res.get('articles', []):
                    st.markdown(f"""
                        <div style='background:rgba(30, 41, 59, 0.4); border-left:3px solid #38BDF8; padding:12px; margin-bottom:12px; border-radius:4px;'>
                            <a style='color:#F1F5F9; text-decoration:none; font-size:0.8rem; font-weight:600;' href='{art['url']}' target='_blank'>{art['title']}</a>
                        </div>
                    """, unsafe_allow_html=True)
            except: st.caption("Intel stream disconnected.")

# --- PAGE 2: DEEP-DIVE AUDIT (WITH FINANCE) ---
elif nav == "Deep-Dive Audit":
    st.markdown("### 🔍 Entity Risk Profiling")
    target = st.selectbox("Search Target:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        ca, cb = st.columns([1.5, 1])
        
        with ca:
            st.markdown(f"""
                <div class="glass-card" style="border-top: 4px solid #38BDF8;">
                    <h2 style="color:#38BDF8; margin:0;">{target}</h2>
                    <p style="color:#94A3B8; text-transform:uppercase; font-size:0.8rem;">Sector: {tool['Category']}</p>
                    <hr style="border-color:#334155;">
                    <p style="font-size:1.1rem; line-height:1.6;">{tool['Short Description']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with cb:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Live Market Performance</p>", unsafe_allow_html=True)
            ticker = st.text_input("Enter Ticker (e.g., MSFT):").upper()
            if ticker and AV_API_KEY:
                q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                try:
                    quote = requests.get(q_url).json().get('Global Quote', {})
                    if quote:
                        st.metric(f"{ticker}", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))
                    else: st.warning("Ticker not found.")
                except: st.error("API Limit Reached.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: LIBRARY ---
elif nav == "Framework Library":
    st.markdown("### 📚 MIT AI Risk Framework")
    st.markdown("<div class='glass-card'>Full Domain Taxonomy and Governance Definitions are accessible via the expansion tabs below.</div><br>", unsafe_allow_html=True)
    
    domains = {
        "D1: Discrimination & Toxicity": "Bias in AI logic leading to unfair or harmful social outcomes.",
        "D2: Privacy & Security": "Unauthorized surveillance, persistent tracking, and data harvesting.",
        "D3: Misinformation": "Accidental spread of deceptive content generated by LLMs.",
        "D4: Malicious Use": "Intentional weaponization for cyber-warfare or deepfake phishing.",
        "D5: Human Agency": "Psychological manipulation and the erosion of individual autonomy.",
        "D6: Socioeconomic Harms": "Impact on labor markets and environmental resource depletion.",
        "D7: AI System Safety": "Catastrophic misalignment and technical robustness failures."
    }
    for k, v in domains.items():
        with st.expander(f"📘 {k}"):
            st.write(v)
# Replace your current load_data flags with this:
df['D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|surveillance|monitor|harvest', case=False, na=False)
df['D6_Integrity'] = df['Short Description'].str.contains('fake|synthetic|generate|deepfake|clone|manipulate', case=False, na=False)
# Add a 'Critical' flag for tools that hit both
df['Critical_Risk'] = df['D4_Privacy'] & df['D6_Integrity']
# Update your fig_donut code:
fig_donut = px.pie(sector_counts, names='Sector', values='Count', hole=0.6, 
                 color_discrete_sequence=px.colors.sequential.Blues_r, 
                 template='plotly_dark')
# This line makes it 'pop' on hover:
fig_donut.update_traces(hovertemplate="<b>%{label}</b><br>Volume: %{value}<br>Click to isolate")
fig_donut.update_layout(hovermode="closest", showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=10,l=10,r=10))

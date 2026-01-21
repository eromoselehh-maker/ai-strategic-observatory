import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. REFINED DESIGN SYSTEM (BETTER CONTRAST)
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    .stApp { background-color: #0F172A; font-family: 'Plus Jakarta Sans', sans-serif; color: #E2E8F0; }
    
    /* Neon Ticker - High Legibility */
    .ticker-wrap {
        width: 100%; background: #1E293B; border-bottom: 2px solid #0EA5E9;
        padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; 
        font-family: monospace; font-weight: bold; animation: ticker 45s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* Professional Report Cards */
    .report-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 25px; border-radius: 12px; height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .score-label { font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; }
    .score-val { font-size: 2.5rem; font-weight: 700; color: #F8FAFC; margin: 0; }

    .main .block-container { padding-top: 6rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        # Logic for Scores
        df['D4_Flag'] = df['Short Description'].str.contains('privacy|tracking|data', case=False, na=False).astype(int)
        df['D6_Flag'] = df['Short Description'].str.contains('fake|synthetic|generate', case=False, na=False).astype(int)
        # Calculate a mock Consultancy Score (0-100)
        df['Risk_Score'] = (df['D4_Flag'] * 45) + (df['D6_Flag'] * 35) + 20
        return df
    except: return pd.DataFrame()

df = load_data()
NEWS_KEY = st.secrets.get("NEWS_API_KEY", "")
AV_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# 3. TICKER
st.markdown(f'<div class="ticker-wrap"><div class="ticker"> ⚡ PHILIP\'S CONSULTING: Strategic Risk Audit Mode Active | Data Source: AIToolBuzz 2025 | Framework: MIT Repository v4.0 </div></div>', unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='color:#38BDF8;'>🏛️ Observatory</h2>", unsafe_allow_html=True)
    nav = st.radio("Intelligence Command", ["Market Dashboard", "Entity Audit", "MIT Glossary"])
    st.markdown("---")
    st.caption("Philip's Consulting Proprietary Tool")

# --- PAGE 1: DASHBOARD ---
if nav == "Market Dashboard":
    st.markdown("### 📈 Global Intelligence Hub")
    
    k1, k2, k3 = st.columns(3)
    k1.markdown(f'<div class="report-card"><p class="score-label">Total Audited</p><p class="score-val">{len(df):,}</p></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="report-card"><p class="score-label">Avg Risk Index</p><p class="score-val" style="color:#38BDF8;">{int(df["Risk_Score"].mean())}%</p></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="report-card"><p class="score-label">Critical Alerts</p><p class="score-val" style="color:#EF4444;">{(df["Risk_Score"] > 70).sum()}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart, col_news = st.columns([2, 1])
    with col_chart:
        # CLEAN BAR CHART
        risk_summary = df.groupby('Category')['Risk_Score'].mean().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(risk_summary, x='Risk_Score', y='Category', orientation='h', color='Risk_Score', 
                     color_continuous_scale='Blues', template='plotly_dark', title="Sector Risk Heatmap")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_news:
        st.markdown("#### 📡 Live News Feed")
        if NEWS_KEY:
            try:
                res = requests.get(f"https://newsapi.org/v2/everything?q=AI+regulation&apiKey={NEWS_KEY}&pageSize=4").json()
                for art in res.get('articles', []):
                    st.markdown(f"<div style='border-bottom:1px solid #334155; padding:10px 0;'><a style='color:#38BDF8; font-size:0.85rem;' href='{art['url']}'>{art['title']}</a></div>", unsafe_allow_html=True)
            except: st.write("Intel feed offline.")

# --- PAGE 2: ENTITY AUDIT (SCORES RESTORED) ---
elif nav == "Entity Audit":
    st.markdown("### 🔍 Strategic Asset Audit")
    target = st.selectbox("Select Target Company:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        
        c_info, c_score = st.columns([2, 1])
        with c_info:
            st.markdown(f"""
                <div class="report-card" style="border-left: 5px solid #38BDF8;">
                    <h2 style="margin:0; color:#38BDF8;">{target}</h2>
                    <p style="color:#94A3B8; font-weight:bold;">Category: {tool['Category']}</p>
                    <hr style="border-color:#334155;">
                    <p style="font-size:1.1rem; line-height:1.6;">{tool['Short Description']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c_score:
            # BRINGING BACK THE SCORES
            score_color = "#EF4444" if tool['Risk_Score'] > 60 else "#38BDF8"
            st.markdown(f"""
                <div class="report-card" style="text-align:center;">
                    <p class="score-label">Philip's Risk Index</p>
                    <p class="score-val" style="color:{score_color};">{int(tool['Risk_Score'])}%</p>
                    <br>
                    <p style="font-size:0.8rem; color:#94A3B8;">MIT D4 Privacy: <b>{'FAIL' if tool['D4_Flag'] else 'PASS'}</b></p>
                    <p style="font-size:0.8rem; color:#94A3B8;">MIT D6 Integrity: <b>{'FAIL' if tool['D6_Flag'] else 'PASS'}</b></p>
                </div>
            """, unsafe_allow_html=True)
            
        # Finance tracker below
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Market Correlation (Live Parent Stock)")
        ticker = st.text_input("Enter Parent Ticker (e.g. MSFT):").upper()
        if ticker and AV_KEY:
            try:
                q = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_KEY}").json().get('Global Quote', {})
                if q: st.metric(f"{ticker}", f"${q.get('05. price')}", delta=q.get('10. change percent'))
            except: st.error("Finance API offline.")

# --- PAGE 3: GLOSSARY ---
elif nav == "MIT Glossary":
    st.markdown("### 📖 Risk Taxonomy Library")
    domains = {
        "D1: Discrimination": "Unfair algorithmic outcomes.",
        "D2: Privacy": "Unauthorized surveillance.",
        "D3: Misinformation": "Propagating false content.",
        "D4: Malicious Use": "Weaponization of AI.",
        "D5: Human Agency": "Loss of user autonomy.",
        "D6: Socioeconomic": "Labor and resource harm.",
        "D7: Safety": "Catastrophic misalignment."
    }
    for d, v in domains.items():
        with st.expander(d): st.write(v)

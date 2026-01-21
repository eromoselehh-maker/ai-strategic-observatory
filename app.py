import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. ELITE UI ARCHITECTURE
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    .stApp { background-color: #0F172A; font-family: 'Plus Jakarta Sans', sans-serif; color: #E2E8F0; }
    
    /* Clean Ticker */
    .ticker-wrap {
        width: 100%; background: #1E293B; border-bottom: 2px solid #38BDF8;
        padding: 8px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; font-family: monospace; animation: ticker 40s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* Metric Cards as Buttons */
    .metric-btn {
        background: #1E293B; border: 1px solid #334155; padding: 20px;
        border-radius: 15px; text-align: center; transition: 0.3s; cursor: pointer;
    }
    .metric-btn:hover { border-color: #38BDF8; background: #26334D; transform: translateY(-3px); }
    .m-label { font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.5px; }
    .m-val { font-size: 2.2rem; font-weight: 700; color: #F8FAFC; margin: 0; }

    /* Tool Insight Cards */
    .tool-card {
        background: rgba(15, 23, 42, 0.8); border: 1px solid #EF4444;
        padding: 15px; border-radius: 12px; margin-bottom: 15px;
    }
    
    .main .block-container { padding-top: 6rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA LOAD & RISK LOGIC
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        df['D4_Flag'] = df['Short Description'].str.contains('privacy|tracking|surveillance', case=False, na=False)
        df['D6_Flag'] = df['Short Description'].str.contains('fake|synthetic|generate', case=False, na=False)
        # Score calculation
        df['Risk_Score'] = (df['D4_Flag'].astype(int) * 40) + (df['D6_Flag'].astype(int) * 40) + 20
        return df
    except: return pd.DataFrame()

df = load_data()

# 3. GLOBAL NAVIGATION
st.markdown(f'<div class="ticker-wrap"><div class="ticker"> ● SYSTEM ONLINE ● PHILIP\'S CONSULTING STRATEGIC OVERVIEW ● MONITORING {len(df):,} ASSETS ● CRITICAL ALERTS ACTIVE ● </div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#38BDF8;'>🏛️ Observatory</h2>", unsafe_allow_html=True)
    nav = st.radio("Intelligence Modules", ["Executive Dashboard", "Strategic Audit", "MIT Framework"])

# --- PAGE 1: EXECUTIVE DASHBOARD ---
if nav == "Executive Dashboard":
    st.markdown("<h2 style='font-weight:700;'>Market Intelligence</h2>", unsafe_allow_html=True)
    
    # KPIs as Interactive-looking blocks
    k1, k2, k3 = st.columns(3)
    with k1: st.markdown('<div class="metric-btn"><p class="m-label">Entities Monitored</p><p class="m-val">'+f"{len(df):,}"+'</p></div>', unsafe_allow_html=True)
    with k2: st.markdown('<div class="metric-btn"><p class="m-label">Avg Market Risk</p><p class="m-val" style="color:#38BDF8;">'+f"{int(df['Risk_Score'].mean())}%"+'</p></div>', unsafe_allow_html=True)
    with k3:
        # The Critical Alert "Button"
        show_critical = st.button("🚨 VIEW CRITICAL ALERTS")
        st.markdown('<div class="metric-btn" style="border-color:#EF4444;"><p class="m-label">Critical Risks</p><p class="m-val" style="color:#EF4444;">'+f"{(df['Risk_Score'] >= 100).sum()}"+'</p></div>', unsafe_allow_html=True)

    if show_critical:
        st.markdown("---")
        st.markdown("### ⚠️ High-Risk Intelligence Portal")
        # Creative layout for critical tools
        critical_tools = df[df['Risk_Score'] >= 100].head(6)
        c_cols = st.columns(3)
        for idx, row in enumerate(critical_tools.iterrows()):
            with c_cols[idx % 3]:
                st.markdown(f"""
                    <div class="tool-card">
                        <small style="color:#EF4444; font-weight:bold;">CRITICAL THREAT</small>
                        <h4 style="margin:5px 0;">{row[1]['Name']}</h4>
                        <p style="font-size:0.8rem; color:#94A3B8;">{row[1]['Category']}</p>
                        <p style="font-size:0.85rem;">{row[1]['Short Description'][:100]}...</p>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("---")

    # The Visual Center: Donut + Detailed Bar
    st.markdown("<br>", unsafe_allow_html=True)
    col_donut, col_details = st.columns([1, 1.5])
    
    with col_donut:
        st.markdown("<p class='m-label'>Sector Composition</p>", unsafe_allow_html=True)
        donut_data = df['Category'].value_counts().head(8).reset_index()
        donut_data.columns = ['Sector', 'Count']
        fig_pie = px.pie(donut_data, names='Sector', values='Count', hole=0.6, 
                         color_discrete_sequence=px.colors.sequential.Blues_r, template='plotly_dark')
        fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=10,l=10,r=10))
        # This graph is interactive!
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_details:
        st.markdown("<p class='m-label'>Risk Density Index (Click to Inspect)</p>", unsafe_allow_html=True)
        bar_data = df.groupby('Category')['Risk_Score'].mean().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(bar_data, x='Risk_Score', y='Category', orientation='h', 
                         color='Risk_Score', color_continuous_scale='Reds', template='plotly_dark')
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

# --- PAGE 2: STRATEGIC AUDIT ---
elif nav == "Strategic Audit":
    st.markdown("<h2 style='font-weight:700;'>Asset Deep-Dive Audit</h2>", unsafe_allow_html=True)
    target = st.selectbox("Search Target Entity:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"""
                <div style="background:#1E293B; padding:30px; border-radius:20px; border-left:5px solid #38BDF8;">
                    <h1 style="color:#38BDF8; margin:0;">{target}</h1>
                    <p style="color:#94A3B8;">Sector: {tool['Category']}</p>
                    <hr style="border-color:#334155;">
                    <p style="font-size:1.2rem; line-height:1.7;">{tool['Short Description']}</p>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            # Score Gauge
            st.markdown(f"""
                <div style="background:#1E293B; padding:30px; border-radius:20px; text-align:center;">
                    <p class="m-label">Consultancy Risk Rating</p>
                    <p style="font-size:4rem; font-weight:800; color:{'#EF4444' if tool['Risk_Score'] > 60 else '#10B981'};">
                        {int(tool['Risk_Score'])}%
                    </p>
                    <p style="color:#94A3B8;">MIT Domain Flags: <b>{(tool['D4_Flag'] + tool['D6_Flag'])}</b></p>
                </div>
            """, unsafe_allow_html=True)

# --- PAGE 3: MIT FRAMEWORK ---
elif nav == "MIT Framework":
    st.markdown("### 📘 Governance Framework Library")
    domains = {
        "D1: Discrimination": "Bias and toxic outcomes.",
        "D2: Privacy": "Surveillance and data harvest.",
        "D3: Misinformation": "Factual inaccuracy risks.",
        "D4: Malicious Use": "Cyber-warfare weaponization.",
        "D5: Human Agency": "Manipulation and loss of control.",
        "D6: Socioeconomic": "Labor and resource impacts.",
        "D7: AI Safety": "Technical robustness failures."
    }
    for d, v in domains.items():
        with st.expander(d):
            st.write(v)
            st.info("Protocol Integrated into Philip's Observatory Engine")

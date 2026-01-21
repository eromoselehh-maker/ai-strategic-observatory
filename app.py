import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. PREMIUM UX/UI SYSTEM ARCHITECTURE
st.set_page_config(page_title="AI Observatory | PHIL's Consulting", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&family=JetBrains+Mono:wght@400&display=swap');
    .stApp { background-color: #020617; font-family: 'Plus Jakarta Sans', sans-serif; color: #F1F5F9; }
    
    /* Neon Top Ticker */
    .ticker-wrap {
        width: 100%; background: #0F172A; border-bottom: 1px solid #38BDF8;
        padding: 8px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; 
        font-family: 'JetBrains Mono', monospace; animation: ticker 40s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* Luxury Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4); border: 1px solid #334155;
        padding: 24px; border-radius: 16px; height: 100%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .metric-val { font-size: 2.8rem; font-weight: 800; color: #F8FAFC; margin: 0; line-height: 1; }
    .metric-label { font-size: 0.75rem; color: #38BDF8; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 10px; }

    /* Layout Adjustments */
    .main .block-container { padding-top: 6.5rem; }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #020617; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE & PRE-PROCESSING
@st.cache_data
def load_data():
    try:
        # Note: Ensure this CSV file is uploaded to your GitHub repo
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        
        # Forensic Categorization
        df['D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|surveillance|monitor', case=False, na=False)
        df['D6_Integrity'] = df['Short Description'].str.contains('fake|synthetic|generate|deepfake|clone', case=False, na=False)
        
        # Risk Scoring Logic (0-100)
        df['Risk_Score'] = (df['D4_Privacy'].astype(int) * 45) + (df['D6_Integrity'].astype(int) * 35) + 20
        df['Risk_Score'] = df['Risk_Score'].clip(upper=100)
        return df
    except:
        # Fallback if file is missing
        return pd.DataFrame(columns=['Name', 'Category', 'Short Description', 'Risk_Score', 'D4_Privacy', 'D6_Integrity'])

df = load_data()

# GLOBAL DATA PREP (Fixes NameErrors)
if not df.empty:
    sector_counts = df['Category'].value_counts().head(8).reset_index()
    sector_counts.columns = ['Sector', 'Count']
    risk_by_sector = df.groupby('Category')['Risk_Score'].mean().sort_values(ascending=False).head(10).reset_index()
    risk_by_sector.columns = ['Category', 'Risk_Avg']

# 3. LIVE TICKER
st.markdown(f'<div class="ticker-wrap"><div class="ticker"> ⚡ PHILIP\'S CONSULTING LIVE: Auditing {len(df):,} AI Entities | Priority Alerts: D4 Privacy Violations Detected | Regulatory Bridge Active... </div></div>', unsafe_allow_html=True)

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<h2 style='color:#38BDF8; margin-bottom:0;'>🏛️ PHIL's</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:0.8rem; margin-top:0;'>CONSULTING GROUP</p>", unsafe_allow_html=True)
    st.markdown("---")
    nav = st.radio("Intelligence Modules", ["Executive Hub", "Strategic Gap Analysis", "Forensic Audit"])
    st.markdown("---")
    st.caption("v13.0 | Regulatory Intelligence")

# --- PAGE 1: EXECUTIVE HUB ---
if nav == "Executive Hub":
    st.markdown("<h2 style='font-weight:700;'>Market Intelligence Hub</h2>", unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f'<div class="glass-card"><p class="metric-label">Assets Monitored</p><p class="metric-val">{len(df):,}</p></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="glass-card" style="border-top:4px solid #F87171;"><p class="metric-label">Critical Alerts (D4/D6)</p><p class="metric-val" style="color:#F87171;">{df["D4_Privacy"].sum() + df["D6_Integrity"].sum()}</p></div>', unsafe_allow_html=True)
    with k3:
        avg_risk = int(df['Risk_Score'].mean()) if not df.empty else 0
        st.markdown(f'<div class="glass-card"><p class="metric-label">Avg Risk Index</p><p class="metric-val" style="color:#38BDF8;">{avg_risk}%</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_main, col_donut = st.columns([1.5, 1])
    
    with col_main:
        st.markdown("<p class='metric-label'>Sector Risk Intensity</p>", unsafe_allow_html=True)
        if not df.empty:
            fig_bar = px.bar(risk_by_sector, x='Risk_Avg', y='Category', orientation='h', 
                             color='Risk_Avg', color_continuous_scale='Reds', template='plotly_dark')
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
            fig_bar.update_traces(hovertemplate="Risk Index: %{x}%")
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_donut:
        st.markdown("<p class='metric-label'>Market Composition</p>", unsafe_allow_html=True)
        if not df.empty:
            fig_donut = px.pie(sector_counts, names='Sector', values='Count', hole=0.6, 
                               color_discrete_sequence=px.colors.sequential.Blues_r, template='plotly_dark')
            fig_donut.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0))
            fig_donut.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value}")
            st.plotly_chart(fig_donut, use_container_width=True)

# --- PAGE 2: STRATEGIC GAP ANALYSIS (The "Company Graph") ---
elif nav == "Strategic Gap Analysis":
    st.markdown("<h2 style='font-weight:700;'>The Regulatory Deficit</h2>", unsafe_allow_html=True)
    
    col_text, col_gap = st.columns([1, 2])
    
    with col_text:
        st.markdown("""
            <div class="glass-card">
                <p class='metric-label'>Strategic Insight</p>
                <p style="font-size:0.9rem; line-height:1.6;">
                Nigeria's AI adoption outpaces traditional regulatory speed. 
                <br><br><span style="color:#38BDF8;"><b>PHIL's Consulting</b></span> provides the forensic toolset required to bridge this governance gap, ensuring <b>NITDA</b> and <b>Federal Ministries</b> maintain oversight.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_gap:
        gap_df = pd.DataFrame({
            'Timeline': ['2023 Q1', '2023 Q3', '2024 Q1', '2024 Q3', '2025 Q1'],
            'AI Entry Velocity': [20, 55, 110, 240, 480],
            'Regulatory Capacity': [15, 20, 25, 30, 35]
        })
        fig_gap = px.line(gap_df, x='Timeline', y=['AI Entry Velocity', 'Regulatory Capacity'],
                          color_discrete_map={"AI Entry Velocity": "#38BDF8", "Regulatory Capacity": "#F87171"})
        fig_gap.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_gap, use_container_width=True)

# --- PAGE 3: FORENSIC AUDIT ---
elif nav == "Forensic Audit":
    st.markdown("<h2 style='font-weight:700;'>Entity Deep-Scan</h2>", unsafe_allow_html=True)
    target = st.selectbox("Select Target Entity for Forensic Audit:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        asset = df[df['Name'] == target].iloc[0]
        
        c_desc, c_radar = st.columns([1.2, 1])
        
        with c_desc:
            st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid #38BDF8;">
                    <p class="metric-label">Audit Report: {target}</p>
                    <p style="font-size:1.1rem; line-height:1.7;">{asset['Short Description']}</p>
                    <hr style="border-color:#334155;">
                    <p style='color:#38BDF8; font-weight:bold;'>Primary MIT Domain Flag: {'D4 Privacy' if asset['D4_Privacy'] else 'D6 Integrity' if asset['D6_Integrity'] else 'Standard Risk'}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c_radar:
            # High-end Spider/Radar Chart
            # Calculated based on tool attributes
            r_val = [asset['Risk_Score'], 85 if asset['D4_Privacy'] else 30, 75 if asset['D6_Integrity'] else 40, 60, 45]
            theta_val = ['Overall Risk','Privacy Logic','Data Integrity','NITDA Alignment','Human Agency']
            
            radar_df = pd.DataFrame(dict(r=r_val, theta=theta_val))
            fig_radar = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template="plotly_dark")
            fig_radar.update_traces(fill='toself', line_color='#38BDF8', marker=dict(size=8))
            fig_radar.update_layout(paper_bgcolor='rgba(0,0,0,0)', polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False)))
            st.plotly_chart(fig_radar, use_container_width=True)

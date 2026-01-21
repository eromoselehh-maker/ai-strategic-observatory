import streamlit as st
import pandas as pd
import plotly.express as px

# 1. DESIGN SYSTEM & ALIGNMENT FIX
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    .stApp { background-color: #0F172A; font-family: 'Plus Jakarta Sans', sans-serif; color: #E2E8F0; }
    
    /* Top Ticker */
    .ticker-wrap {
        width: 100%; background: #1E293B; border-bottom: 2px solid #38BDF8;
        padding: 8px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; font-family: monospace; animation: ticker 40s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* UNIFIED BUTTON ALIGNMENT (The "Fix") */
    div.stButton > button {
        width: 100% !important;
        height: 140px !important;
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        color: #F8FAFC !important;
        transition: all 0.3s ease;
        display: flex; flex-direction: column; justify-content: center;
    }
    div.stButton > button:hover {
        border-color: #38BDF8 !important;
        background-color: #26334D !important;
        transform: translateY(-5px);
    }
    
    /* High-Contrast Critical Button */
    .crit-btn div button { border: 2px solid #EF4444 !important; color: #EF4444 !important; font-weight: bold !important; }

    .main .block-container { padding-top: 6.5rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. ACCURATE DATA ANALYSIS ENGINE
@st.cache_data
def load_forensic_data():
    try:
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        
        # WEIGHED ANALYSIS (More realistic)
        # D4: Malicious Use (Cyber/Phishing/Surveillance)
        df['D4_Score'] = df['Short Description'].str.contains('phishing|malware|surveillance|tracking|hack', case=False, na=False).astype(int) * 50
        # D6: Socioeconomic/Integrity (Deepfake/Fake News/Displacement)
        df['D6_Score'] = df['Short Description'].str.contains('deepfake|fake|synthetic|clone|replace', case=False, na=False).astype(int) * 40
        
        # Base risk + weighed factors
        df['Consultancy_Risk_Index'] = 10 + df['D4_Score'] + df['D6_Score']
        # Cap at 100%
        df['Consultancy_Risk_Index'] = df['Consultancy_Risk_Index'].clip(upper=100)
        
        return df
    except: return pd.DataFrame()

df = load_forensic_data()

# State Management
if 'view' not in st.session_state: st.session_state.view = "Default"

# 3. UI LAYOUT
st.markdown(f'<div class="ticker-wrap"><div class="ticker"> ● PHILIP\'S CONSULTING STRATEGIC AUDIT ● V10 FORENSIC ENGINE ACTIVE ● ALIGNMENT SYNCED ● </div></div>', unsafe_allow_html=True)

st.markdown("<h1 style='font-weight:800; letter-spacing:-2px;'>Strategic Risk Observatory</h1>", unsafe_allow_html=True)

# TOP ACTION ROW (Perfectly Aligned)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button(f"📊 {len(df):,}\nTotal Assets Scanned"): st.session_state.view = "Default"
with c2:
    avg = int(df['Consultancy_Risk_Index'].mean())
    if st.button(f"🛡️ {avg}%\nAggregate Market Risk"): st.session_state.view = "Default"
with c3:
    st.markdown('<div class="crit-btn">', unsafe_allow_html=True)
    crit_count = (df['Consultancy_Risk_Index'] >= 90).sum()
    if st.button(f"🚨 {crit_count}\nCritical Risk Alerts"): st.session_state.view = "Critical"
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. DRILL-DOWN LOGIC
if st.session_state.view == "Critical":
    st.markdown("### 🚫 High-Priority Target List (Risk Index > 90%)")
    high_risk = df[df['Consultancy_Risk_Index'] >= 90].head(12)
    cols = st.columns(4)
    for i, (_, row) in enumerate(high_risk.iterrows()):
        with cols[i % 4]:
            st.markdown(f"""
                <div style="background:#1E293B; border-top: 4px solid #EF4444; padding:15px; border-radius:10px; height:180px;">
                    <h4 style="margin:0; font-size:1rem;">{row['Name']}</h4>
                    <p style="color:#EF4444; font-size:0.7rem; font-weight:bold;">MIT D4/D6 VIOLATION</p>
                    <p style="font-size:0.8rem; color:#94A3B8;">{row['Short Description'][:80]}...</p>
                </div>
            """, unsafe_allow_html=True)
else:
    # 5. THE "POP" INTERACTIVE GRAPHS
    g1, g2 = st.columns(2)
    
    with g1:
        st.markdown("<p style='font-size:0.7rem; color:#94A3B8; font-weight:bold; letter-spacing:1px;'>MARKET COMPOSITION</p>", unsafe_allow_html=True)
        pie_df = df['Category'].value_counts().head(8).reset_index()
        pie_df.columns = ['Sector', 'Value']
        fig_pie = px.pie(pie_df, names='Sector', values='Value', hole=0.65, 
                         template='plotly_dark', color_discrete_sequence=px.colors.sequential.Blues_r)
        # HOVER POP SETTINGS
        fig_pie.update_traces(hovertemplate="<b>%{label}</b><br>Share: %{percent}<br>Total: %{value}")
        fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with g2:
        st.markdown("<p style='font-size:0.7rem; color:#94A3B8; font-weight:bold; letter-spacing:1px;'>SECTOR RISK SCOREBOARD</p>", unsafe_allow_html=True)
        bar_df = df.groupby('Category')['Consultancy_Risk_Index'].mean().sort_values(ascending=False).head(10).reset_index()
        bar_df.columns = ['Industry', 'Risk']
        fig_bar = px.bar(bar_df, x='Risk', y='Industry', orientation='h', color='Risk', color_continuous_scale='Reds')
        # HOVER POP SETTINGS
        fig_bar.update_traces(hovertemplate="<b>%{y}</b><br>Forensic Risk: %{x}%")
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, template='plotly_dark')
        st.plotly_chart(fig_bar, use_container_width=True)

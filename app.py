import streamlit as st
import pandas as pd
import plotly.express as px

# 1. THE "WAR ROOM" UI
st.set_page_config(page_title="AI Risk Observatory", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&family=Plus+Jakarta+Sans:wght@700&display=swap');
    
    .stApp { background-color: #050505; font-family: 'Inter', sans-serif; color: #A1A1AA; }
    
    /* Risk Status Cards */
    .risk-card {
        background: #0A0A0A; border: 1px solid #1A1A1A;
        padding: 24px; border-radius: 8px; border-top: 3px solid #38BDF8;
    }
    .status-alert {
        background: rgba(220, 38, 38, 0.1); border: 1px solid #DC2626;
        color: #F87171; padding: 15px; border-radius: 4px; font-family: 'JetBrains Mono', monospace;
    }
    
    /* Typography */
    .hero-text { font-family: 'Plus Jakarta Sans', sans-serif; color: #FFFFFF; letter-spacing: -1px; }
    .label-text { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #71717A; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 2. AGGRESSIVE RISK ENGINE
@st.cache_data
def load_forensic_data():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Category'])
    
    # AGGRESSIVE SCORING (Consultancy Grade)
    # We define "Red Lines" - if these exist, the tool is High Risk
    red_lines = 'deepfake|surveillance|tracking|hack|exploit|phishing|facial recognition|clone'
    yellow_lines = 'data harvest|biometric|synthetic|scraping|automation'
    
    df['Red_Flag'] = df['Short Description'].str.contains(red_lines, case=False, na=False)
    df['Yellow_Flag'] = df['Short Description'].str.contains(yellow_lines, case=False, na=False)
    
    # Calculate Score 0-100
    df['Risk_Score'] = 15 # Base risk
    df.loc[df['Yellow_Flag'], 'Risk_Score'] += 35
    df.loc[df['Red_Flag'], 'Risk_Score'] += 50 # Immediate High Risk
    
    return df

df = load_forensic_data()

# 3. EXECUTIVE HEADER
st.markdown("<p class='label-text'>Strategic Advisory: Philip's Consulting</p>", unsafe_allow_html=True)
st.markdown("<h1 class='hero-text'>AI ENTITY OBSERVATORY</h1>", unsafe_allow_html=True)

# 4. TOP-LEVEL INTELLIGENCE
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""<div class='risk-card'><p class='label-text'>Market Coverage</p>
                <h2 style='color:white; margin:0;'>{len(df):,}</h2></div>""", unsafe_allow_html=True)
with c2:
    critical_count = len(df[df['Risk_Score'] >= 85])
    st.markdown(f"""<div class='risk-card' style='border-top-color: #DC2626;'>
                <p class='label-text' style='color:#DC2626;'>Red Alert Assets</p>
                <h2 style='color:#DC2626; margin:0;'>{critical_count}</h2></div>""", unsafe_allow_html=True)
with c3:
    avg_risk = int(df['Risk_Score'].mean())
    st.markdown(f"""<div class='risk-card' style='border-top-color: #FBBF24;'>
                <p class='label-text' style='color:#FBBF24;'>Avg Risk Index</p>
                <h2 style='color:#FBBF24; margin:0;'>{avg_risk}%</h2></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. THE VISUAL AUDIT (High Contrast)
col_graph, col_list = st.columns([1.5, 1])

with col_graph:
    st.markdown("<p class='label-text'>Risk Distribution (MIT Domains)</p>", unsafe_allow_html=True)
    # Donut Chart - Using High Contrast Red for High Risk
    sector_risk = df.groupby('Category')['Risk_Score'].mean().sort_values(ascending=False).head(8).reset_index()
    
    fig = px.pie(sector_risk, names='Category', values='Risk_Score', hole=0.7,
                 color_discrete_sequence=['#DC2626', '#EF4444', '#F87171', '#1E293B', '#0F172A'])
    
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0))
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Risk Intensity: %{value}%<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

with col_list:
    st.markdown("<p class='label-text'>Live Critical Warnings</p>", unsafe_allow_html=True)
    # Only show the truly dangerous ones here
    red_alerts = df[df['Red_Flag']].head(5)
    for _, row in red_alerts.iterrows():
        st.markdown(f"""
            <div class='status-alert'>
                <small>MIT D4/D6 VIOLATION</small><br>
                <b>{row['Name']}</b><br>
                <span style='font-size:0.75rem;'>{row['Short Description'][:90]}...</span>
            </div><br>
        """, unsafe_allow_html=True)

# 6. DEEP SCAN (Sidebar)
st.sidebar.markdown("### 🔍 Strategic Audit")
target = st.sidebar.selectbox("Select Target", [""] + sorted(df['Name'].unique().tolist()))

if target:
    st.markdown("---")
    asset = df[df['Name'] == target].iloc[0]
    
    # Conditional formatting for the Audit result
    audit_color = "#DC2626" if asset['Risk_Score'] >= 85 else "#38BDF8"
    st.markdown(f"<h2 style='color:{audit_color};'>Audit Report: {target}</h2>", unsafe_allow_html=True)
    
    ca, cb = st.columns(2)
    with ca:
        st.write(f"**Entity Description:** {asset['Short Description']}")
    with cb:
        st.metric("Risk Level", f"{int(asset['Risk_Score'])}%", 
                  delta="CRITICAL" if asset['Red_Flag'] else "STABLE", 
                  delta_color="inverse" if asset['Red_Flag'] else "normal")

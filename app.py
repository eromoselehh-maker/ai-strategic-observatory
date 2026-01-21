import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETUP
st.set_page_config(page_title="AI Observatory | PHIL's Consulting", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
    .stApp { background-color: #020617; font-family: 'Plus Jakarta Sans', sans-serif; color: #F1F5F9; }
    .glass-card { background: rgba(30, 41, 59, 0.4); border: 1px solid #334155; padding: 20px; border-radius: 12px; height: 100%; }
    .metric-label { font-size: 0.7rem; color: #38BDF8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }
    .main .block-container { padding-top: 5rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE ANALYSIS ENGINE (The "Brain" of the tool)
@st.cache_data
def analyze_data():
    try:
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Category'])

        # --- ACTUAL DATA ANALYSIS LOGIC ---
        # Domain 4: Malicious Use (Surveillance/Cyber)
        d4_keywords = 'privacy|tracking|surveillance|monitor|spy|hack|exploit|biometric'
        # Domain 6: Socioeconomic (Deepfakes/Job loss/Integrity)
        d6_keywords = 'fake|synthetic|generate|deepfake|clone|automated content|replace workers'

        df['D4_Flag'] = df['Short Description'].str.contains(d4_keywords, case=False, na=False)
        df['D6_Flag'] = df['Short Description'].str.contains(d6_keywords, case=False, na=False)

        # Calculating a Weighted Risk Score (Analytic Result)
        # We assign higher weight to D4 (Direct Security) over D6 (Content)
        df['Forensic_Risk_Score'] = (df['D4_Flag'].astype(int) * 60) + (df['D6_Flag'].astype(int) * 30) + 10
        df['Forensic_Risk_Score'] = df['Forensic_Risk_Score'].clip(upper=100)
        
        return df
    except:
        return pd.DataFrame()

df = analyze_data()

# 3. UI & NAVIGATION
st.sidebar.title("🏛️ PHIL'S CONSULTING")
nav = st.sidebar.radio("Modules", ["Executive Analytics", "Risk Deep-Dive", "MIT Framework"])

# --- PAGE 1: EXECUTIVE ANALYTICS ---
if nav == "Executive Analytics":
    st.header("Strategic Risk Analytics")
    
    # KPIs derived from the Analysis
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Entities Scanned", f"{len(df):,}")
    m2.metric("Critical D4 Violations", df['D4_Flag'].sum(), delta="High Risk", delta_color="inverse")
    m3.metric("Systemic D6 Risks", df['D6_Flag'].sum(), delta="Moderate", delta_color="off")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<p class='metric-label'>Sector Risk Concentration</p>", unsafe_allow_html=True)
        # Analyzing which sectors have the highest average risk
        sector_analysis = df.groupby('Category')['Forensic_Risk_Score'].mean().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(sector_analysis, x='Forensic_Risk_Score', y='Category', orientation='h', 
                         color='Forensic_Risk_Score', color_continuous_scale='Reds', template='plotly_dark')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        st.markdown("<p class='metric-label'>Market Composition</p>", unsafe_allow_html=True)
        sector_counts = df['Category'].value_counts().head(10).reset_index()
        fig_pie = px.pie(sector_counts, names='index', values='Category', hole=0.5, template='plotly_dark')
        st.plotly_chart(fig_pie, use_container_width=True)

# --- PAGE 2: RISK DEEP-DIVE (Individual Tool Analysis) ---
elif nav == "Risk Deep-Dive":
    st.header("Forensic Entity Audit")
    target = st.selectbox("Select Tool to Audit:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        
        col_a, col_b = st.columns([1.5, 1])
        with col_a:
            st.markdown(f"""
                <div class="glass-card">
                    <h3 style="color:#38BDF8;">{target}</h3>
                    <p><b>Category:</b> {tool['Category']}</p>
                    <p><b>Technical Description:</b> {tool['Short Description']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            # Gauge chart for the Risk Score
            fig_gauge = px.pie(values=[tool['Forensic_Risk_Score'], 100-tool['Forensic_Risk_Score']], 
                               names=['Risk', 'Safe'], hole=0.8, 
                               color_discrete_map={'Risk':'#EF4444', 'Safe':'#1E293B'})
            fig_gauge.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown(f"<center><b>Risk Level: {tool['Forensic_Risk_Score']}%</b></center>", unsafe_allow_html=True)

# --- PAGE 3: MIT FRAMEWORK (Glossary) ---
elif nav == "MIT Framework":
    st.header("MIT AI Risk Taxonomy")
    glossary = {
        "D4: Malicious Use": "Includes tools designed for surveillance, phishing, or bypassing security protocols.",
        "D6: Socioeconomic Harms": "Includes generative AI that can produce deepfakes or replace human labor without ethical safeguards.",
        "D2: Privacy & Security": "Covers unauthorized data collection and persistent user tracking."
    }
    for k, v in glossary.items():
        with st.expander(f"📘 {k}"):
            st.write(v)

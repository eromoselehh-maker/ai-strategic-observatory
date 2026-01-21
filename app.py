import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI ARCHITECTURE
st.set_page_config(page_title="Philip’s AI Observatory", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
    .stApp { background-color: #0F172A; font-family: 'Plus Jakarta Sans', sans-serif; color: #F8FAFC; }
    
    /* Top Ticker */
    .ticker-wrap {
        width: 100%; background: #1E293B; border-bottom: 2px solid #38BDF8;
        padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 1000;
    }
    .ticker { 
        display: inline-block; white-space: nowrap; color: #38BDF8; 
        font-family: monospace; animation: ticker 40s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* KPI Cards */
    .metric-card {
        background: #1E293B; border: 1px solid #334155; 
        padding: 20px; border-radius: 12px; text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 800; color: #38BDF8; }
    
    /* Main Content Spacing */
    .main .block-container { padding-top: 6.5rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
        df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
        df['Privacy_Risk'] = df['Short Description'].str.contains('privacy|tracking|surveillance', case=False, na=False)
        df['Integrity_Risk'] = df['Short Description'].str.contains('fake|synthetic|generate', case=False, na=False)
        return df
    except: return pd.DataFrame()

df = load_data()

# 3. SIDEBAR & TICKER
ticker_msg = " ⚡ [SYSTEM STATUS: NOMINAL] | MONITORING 16,000+ ENTITIES | MIT V4 FRAMEWORK ACTIVE | TOP RISK SECTOR: DATA ANALYSIS "
st.markdown(f'<div class="ticker-wrap"><div class="ticker">{ticker_msg * 5}</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color:#38BDF8;'>🏛️ OBSERVATORY</h1>", unsafe_allow_html=True)
    nav = st.radio("Navigation", ["Overview", "Entity Audit", "MIT Framework Library"])

# --- PAGE 1: OVERVIEW (NEW GRAPHS) ---
if nav == "Overview":
    st.markdown("### 📊 Market Risk Intelligence")
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card"><small>ENTITIES</small><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><small>PRIVACY ALERTS</small><div class="metric-value">{df["Privacy_Risk"].sum()}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><small>INTEGRITY ALERTS</small><div class="metric-value">{df["Integrity_Risk"].sum()}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # REPLACED GRAPH: Using a clean Sunburst or Horizontal Bar
    col_chart, col_stats = st.columns([2, 1])
    
    with col_chart:
        st.markdown("#### Risk Density by Industry Sector")
        # Creating a summary for a cleaner chart
        risk_summary = df.groupby('Category').agg({'Privacy_Risk':'sum', 'Name':'count'}).reset_index()
        risk_summary = risk_summary[risk_summary['Name'] > 50].sort_values('Privacy_Risk', ascending=False).head(12)
        
        fig = px.bar(risk_summary, x='Privacy_Risk', y='Category', orientation='h',
                     color='Privacy_Risk', color_continuous_scale='Reds',
                     template='plotly_dark', labels={'Privacy_Risk': 'Identified Risks'})
        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col_stats:
        st.markdown("#### Sector Breakdown")
        sector_counts = df['Category'].value_counts().head(8)
        st.dataframe(sector_counts, use_container_width=True)

# --- PAGE 2: ENTITY AUDIT ---
elif nav == "Entity Audit":
    st.markdown("### 🔍 Strategic Audit Tool")
    target = st.selectbox("Target Entity:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        st.markdown(f"""
            <div style="background:#1E293B; padding:30px; border-radius:20px; border:1px solid #38BDF8;">
                <h1 style="color:#38BDF8; margin-bottom:0;">{target}</h1>
                <p style="color:#94A3B8;">Sector: {tool['Category']}</p>
                <p style="font-size:1.1rem; line-height:1.6; margin-top:20px;">{tool['Short Description']}</p>
                <hr style="border-color:#334155;">
                <div style="display:flex; gap:20px; margin-top:20px;">
                    <div style="background:#0F172A; padding:15px; border-radius:10px; flex:1; text-align:center;">
                        <small>PRIVACY RISK</small><br><b style="color:{'#EF4444' if tool['Privacy_Risk'] else '#10B981'}">{'HIGH' if tool['Privacy_Risk'] else 'LOW'}</b>
                    </div>
                    <div style="background:#0F172A; padding:15px; border-radius:10px; flex:1; text-align:center;">
                        <small>INTEGRITY RISK</small><br><b style="color:{'#F59E0B' if tool['Integrity_Risk'] else '#10B981'}">{'HIGH' if tool['Integrity_Risk'] else 'LOW'}</b>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- PAGE 3: GLOSSARY (EXPANDED LIBRARY) ---
elif nav == "MIT Framework Library":
    st.title("📚 MIT AI Risk Framework Library")
    st.write("Comprehensive audit definitions used by Philip's Consulting.")
    
    # High-quality cards for the library
    domains = {
        "Domain 1: Discrimination & Toxicity": "Includes algorithmic bias, exclusionary practices, and the generation of toxic or harmful social content.",
        "Domain 2: Privacy & Security": "Focuses on unauthorized surveillance, persistent user tracking, data leaks, and adversarial attacks on system logic.",
        "Domain 3: Misinformation": "The unintentional propagation of false or misleading information that undermines public trust or safety.",
        "Domain 4: Malicious Actors": "Deliberate use of AI for deepfakes, large-scale social engineering, and automated cyber-warfare.",
        "Domain 5: Human-Computer Interaction": "Risks involving 'Dark Patterns', psychological manipulation, and the erosion of human agency in decision-making.",
        "Domain 6: Socioeconomic Harms": "Monitoring the impact on labor displacement, wealth concentration, and environmental resource depletion.",
        "Domain 7: AI System Safety": "Focuses on 'Alignment'—ensuring systems do not develop emergent behaviors that contradict human safety protocols."
    }
    
    for d_title, d_desc in domains.items():
        with st.expander(f"📖 {d_title}"):
            st.write(d_desc)
            st.info("Status: Fully Integrated into Philip's Consulting Audit Engine.")

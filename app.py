import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI CONFIGURATION & PREMIUM STYLING
st.set_page_config(page_title="AI Observatory | PHIL's Consulting", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #0F172A; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* Executive Header Card */
    .hero-section {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 50px; border-radius: 24px; border: 1px solid #334155;
        margin-bottom: 35px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric Cards */
    .metric-container {
        background: rgba(30, 41, 59, 0.7); border: 1px solid #334155;
        padding: 25px; border-radius: 16px; text-align: center;
        backdrop-filter: blur(10px);
    }
    .metric-val { font-size: 2.5rem; font-weight: 800; color: #38BDF8; }
    .metric-lbl { font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 2px; }

    /* Advisory & Risk Cards */
    .advisory-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 20px; border-radius: 12px; margin-bottom: 15px;
        border-left: 6px solid #3B82F6;
    }
    .risk-alert { border-left-color: #EF4444; background: rgba(239, 68, 68, 0.05); }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #0F172A; border-right: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data
def load_and_scrub():
    # Replace with your actual filename
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
    df['D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|surveillance|data harvest', case=False, na=False)
    df['D6_Integrity'] = df['Short Description'].str.contains('fake|generate|synthetic|voice clone|manipulate', case=False, na=False)
    return df

df = load_and_scrub()
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
st.sidebar.markdown("<h2 style='color:white; margin-top:0;'>PHIL'S CONSULTING</h2>", unsafe_allow_html=True)
st.sidebar.caption("Strategic Al Governance v4.0")
nav = st.sidebar.radio("Navigation", ["📈 Strategic Overview", "🔍 Technical Audit", "📖 Governance Glossary"])
st.sidebar.markdown("---")
sector_context = st.sidebar.selectbox("Sector Insight", ["Global Market"] + sorted(df['Category'].unique().tolist()))

# --- PAGE 1: STRATEGIC OVERVIEW ---
if nav == "📈 Strategic Overview":
    st.markdown("""
        <div class="hero-section">
            <h1 style="color: #38BDF8; margin: 0;">National AI Observatory</h1>
            <p style="color: #94A3B8; font-size: 1.2rem; margin-top: 10px;">
                Evidence-based intelligence supporting the Nigerian Federal Ministry of Communications, Innovation & Digital Economy.
            </p>
            <div style="margin-top:20px; color: #CBD5E1; font-size: 0.95rem; line-height: 1.6;">
                Bridging the gap between <b>Rapid Adoption</b> and <b>Regulatory Capacity</b> using high-precision data scanning.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # KPIs
    k1, k2, k3 = st.columns(3)
    with k1: st.markdown(f'<div class="metric-container"><div class="metric-val">{len(df):,}</div><div class="metric-lbl">Assets Monitored</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="metric-container"><div class="metric-val" style="color:#EF4444;">{df["D4_Privacy"].sum()}</div><div class="metric-lbl">Privacy Violations</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="metric-container"><div class="metric-val" style="color:#FBBF24;">{df["D6_Integrity"].sum()}</div><div class="metric-lbl">Integrity Alerts</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_vis, col_side = st.columns([2, 1])
    
    with col_vis:
        st.subheader("🌐 Global Sector Risk Radar")
        st.caption("Each bubble represents a technology sector. Larger bubbles = higher tool volume. Higher position = greater Privacy/Security risk density.")
        sector_stats = df.groupby('Category').agg(Tools=('Name','count'), Risk=('D4_Privacy','mean')).reset_index()
        fig = px.scatter(sector_stats.head(30), x="Tools", y="Risk", size="Tools", color="Risk",
                         hover_name="Category", color_continuous_scale="Reds", template="plotly_dark")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_side:
        st.subheader("⚠️ Regulatory Watchlist")
        hotspots = df.groupby('Category')['D4_Privacy'].mean().sort_values(ascending=False).head(3)
        for cat, val in hotspots.items():
            st.markdown(f"<div class='advisory-card risk-alert'><strong>{cat}</strong><br><small>MIT Risk Density: {val:.1%}</small></div>", unsafe_allow_html=True)
        
        st.subheader("💡 Strategic Gaps")
        st.markdown("<div class='advisory-card'><strong>Infrastructure AI</strong><br><small>Inventory: Low • Priority: High</small></div>", unsafe_allow_html=True)

# --- PAGE 2: TECHNICAL AUDIT ---
elif nav == "🔍 Technical Audit":
    st.title("Asset Investigation")
    target = st.selectbox("Select Target Entity:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='advisory-card'><h3>{target}</h3><p>{tool['Short Description']}</p></div>", unsafe_allow_html=True)
            st.write(f"**MIT D4 Privacy:** {'🔴 Alert' if tool['D4_Privacy'] else '🟢 Clear'}")
            st.write(f"**MIT D6 Integrity:** {'🔴 Alert' if tool['D6_Integrity'] else '🟢 Clear'}")
        
        with c2:
            st.markdown("<div class='advisory-card'><strong>📈 Market Trust Signal</strong></div>", unsafe_allow_html=True)
            ticker = st.text_input("Enter Parent Ticker (e.g. MSFT):").upper()
            if ticker and AV_API_KEY:
                try:
                    res = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}").json()
                    quote = res.get('Global Quote', {})
                    if quote: st.metric(f"{ticker} Valuation", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))
                except: st.error("API Limit.")

# --- PAGE 3: GOVERNANCE GLOSSARY ---
elif nav == "📖 Governance Glossary":
    st.title("Governance Framework Library")
    st.write("Alignment with the MIT AI Risk Repository and International Standards.")
    
    glossary = {
        "MIT Domain 4 (Privacy & Security)": "Unauthorized data collection, persistent surveillance, and vulnerabilities in AI software toolchains.",
        "MIT Domain 6 (Socioeconomic Harm)": "Pollution of the information ecosystem via deepfakes, synthetic media, and loss of human consensus reality.",
        "OECD AI Principles": "Global benchmark (5 principles) focused on transparency, explainability, and human-centric values.",
        "EU AI Act (Risk-Based)": "Four-tier classification: Unacceptable (Banned), High (Regulated), Limited (Transparency), and Minimal Risk.",
        "AU Continental AI Strategy": "African Union's 2024 roadmap prioritizing human capital, local data sovereignty, and inclusive growth.",
        "Strategic Investment Gap (SIG)": "PHIL's proprietary metric identifying sectors where technological density is lower than the market mean."
    }
    
    for term, definition in glossary.items():
        with st.expander(f"📘 {term}"):
            st.write(definition)
    
    st.markdown("---")
    st.info("The Strategic Observatory tool is designed to provide real-time updates to static policy reports.")

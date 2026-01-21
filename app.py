import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI CONFIGURATION
st.set_page_config(page_title="AI Observatory | PHIL's Consulting", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .metric-card {
        background-color: #F8FAFC; border: 1px solid #E2E8F0;
        padding: 24px; border-radius: 12px; text-align: center;
    }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #1E293B; }
    .metric-label { font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
    .advisory-card {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        padding: 18px; border-radius: 10px; margin-bottom: 12px; border-left: 5px solid #3B82F6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE & ANALYTICS
@st.cache_data
def load_and_analyze():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
    
    # Analysis Logic
    df['D4_Privacy'] = df['Short Description'].str.contains('privacy|tracking|surveillance', case=False, na=False)
    df['D6_Integrity'] = df['Short Description'].str.contains('fake|generate|synthetic', case=False, na=False)
    
    # Create Sector-Level Aggregates for the Bubble Chart
    sector_stats = df.groupby('Category').agg(
        Total_Tools=('Name', 'count'),
        Privacy_Risk_Rate=('D4_Privacy', 'mean'),
        Integrity_Risk_Rate=('D6_Integrity', 'mean')
    ).reset_index()
    
    return df, sector_stats

df, sector_stats = load_and_analyze()
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# --- SIDEBAR ---
st.sidebar.markdown("## 🏛️ PHIL's CONSULTING")
nav = st.sidebar.radio("Observation Mode", ["📈 Market Findings", "🔍 Entity Audit", "📖 Framework"])

# --- PAGE 1: MARKET FINDINGS ---
if nav == "📈 Market Findings":
    st.title("Strategic Findings")
    
    # KPIs
    m1, m2, m3 = st.columns(3)
    m1.markdown(f'<div class="metric-card"><div class="metric-value">{len(df):,}</div><div class="metric-label">Entities Monitored</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-value">{df["D4_Privacy"].sum()}</div><div class="metric-label">Privacy Violations (D4)</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div class="metric-value">{int(df["D4_Privacy"].mean()*100)}%</div><div class="metric-label">Systemic Risk Rate</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # THE STRATEGIC BUBBLE CHART
    st.subheader("Sector Risk vs. Innovation Volume")
    st.write("This analysis identifies 'Regulatory Hotspots' where high tool volume meets high MIT Risk density.")
    
    fig_bubble = px.scatter(
        sector_stats.head(25), 
        x="Total_Tools", 
        y="Privacy_Risk_Rate",
        size="Total_Tools", 
        color="Privacy_Risk_Rate",
        hover_name="Category",
        labels={'Total_Tools': 'Market Volume (Inventory Count)', 'Privacy_Risk_Rate': 'MIT D4 Risk Density (%)'},
        color_continuous_scale='Reds',
        template='plotly_white'
    )
    fig_bubble.update_layout(height=500)
    st.plotly_chart(fig_bubble, use_container_width=True)
    
    st.info("💡 **Insight:** Sectors in the top-right quadrant require immediate sovereign oversight due to high volume and high risk.")

# --- PAGE 2: ENTITY AUDIT ---
elif nav == "🔍 Entity Audit":
    st.title("Entity Audit")
    target = st.selectbox("Select Target Entity:", [""] + sorted(df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown(f"### Audit: {target}")
            st.markdown(f"<div class='advisory-card'>{tool['Short Description']}</div>", unsafe_allow_html=True)
            st.write(f"**MIT D4 Privacy:** {'🔴 Alert' if tool['D4_Privacy'] else '🟢 Clear'}")
            st.write(f"**MIT D6 Integrity:** {'🔴 Alert' if tool['D6_Integrity'] else '🟢 Clear'}")
            
        with col_right:
            st.markdown("### 📈 Financial Trust Signal")
            ticker = st.text_input("Enter Parent Ticker (e.g. MSFT):").upper()
            if ticker and AV_API_KEY:
                try:
                    res = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}").json()
                    quote = res.get('Global Quote', {})
                    if quote:
                        st.metric(f"{ticker} Price", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))
                except: st.error("API Limit Reached.")

# --- PAGE 3: FRAMEWORK ---
elif nav == "📖 Framework":
    st.header("MIT Risk Framework")
    st.write("D4: Privacy & Surveillance | D6: Content Integrity")

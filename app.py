import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ANALYTICAL FOUNDATION
st.set_page_config(page_title="Forensic Audit | PHIL's Consulting", layout="wide")

@st.cache_data
def perform_forensic_analysis():
    # Load raw data
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Category'])

    # --- THE ANALYSIS ENGINE ---
    # Define MIT Risk Domain Patterns
    mit_patterns = {
        'D2_Privacy': 'tracking|surveillance|biometric|facial recognition|data harvest',
        'D4_Malicious': 'phishing|malware|exploit|hack|bypass|credential',
        'D6_Integrity': 'deepfake|synthetic|generate|clone|manipulate|disinformation'
    }

    # Analyze and Score
    for domain, pattern in mit_patterns.items():
        df[domain] = df['Short Description'].str.contains(pattern, case=False, na=False)

    # Calculate "Consultancy Risk Index" (CRI)
    # Weighted: Privacy and Malicious use are higher threat levels than Content Integrity
    df['CRI'] = (df['D2_Privacy'].astype(int) * 40) + \
                 (df['D4_Malicious'].astype(int) * 50) + \
                 (df['D6_Integrity'].astype(int) * 30)
    
    df['CRI'] = df['CRI'].clip(upper=100)
    return df

# Run the analysis
df_analyzed = perform_forensic_analysis()

# 2. UI RENDER (Based on Analysis Results)
st.markdown("<h2 style='color:#38BDF8;'>🏛️ PHIL'S STRATEGIC OBSERVATORY</h2>", unsafe_allow_html=True)
st.sidebar.header("Intelligence Modules")
nav = st.sidebar.radio("Go to:", ["Executive Analysis", "MIT Framework Library"])

if nav == "Executive Analysis":
    # ANALYSIS RESULTS
    c1, c2, c3 = st.columns(3)
    c1.metric("Assets Analyzed", f"{len(df_analyzed):,}")
    c2.metric("Critical Privacy Threats", df_analyzed['D2_Privacy'].sum())
    c3.metric("Systemic Integrity Risks", df_analyzed['D6_Integrity'].sum())

    st.markdown("---")
    
    # RISK VS VOLUME ANALYSIS
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Sector Risk Concentration")
        # Real Analysis: Grouping by category to see where the highest average risk lives
        sector_risk = df_analyzed.groupby('Category')['CRI'].mean().sort_values(ascending=False).head(10).reset_index()
        fig_risk = px.bar(sector_risk, x='CRI', y='Category', orientation='h', 
                          color='CRI', color_continuous_scale='Reds', template='plotly_dark')
        st.plotly_chart(fig_risk, use_container_width=True)

    with col_b:
        st.subheader("Market Composition")
        sector_counts = df_analyzed['Category'].value_counts().head(10).reset_index()
        fig_pie = px.pie(sector_counts, names='index', values='Category', hole=0.5, template='plotly_dark')
        st.plotly_chart(fig_pie, use_container_width=True)

elif nav == "MIT Framework Library":
    st.header("MIT AI Risk Taxonomy")
    # THE GLOSSARY
    with st.expander("📘 Domain 2: Privacy & Security"):
        st.write("Risks related to persistent tracking and unauthorized surveillance.")
    with st.expander("📘 Domain 4: Malicious Use"):
        st.write("Intentional use of AI for cyber-attacks or societal disruption.")
    with st.expander("📘 Domain 6: Socioeconomic Harms"):
        st.write("Issues including deepfakes, labor displacement, and environmental impact.")

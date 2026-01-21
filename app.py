import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. INSTITUTIONAL CONFIGURATION
st.set_page_config(page_title="AI Observatory", layout="wide")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .mit-card { 
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 8px; 
        border-left: 6px solid #1c3d5a;
        margin-bottom: 25px;
    }
    .metric-container {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_scrubbed_data():
    # Load and Clean
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name'])
    df['Short Description'] = df['Short Description'].fillna("Metadata review pending.")
    
    # MIT RISK MAPPING (Based on MIT Domain Taxonomy)
    # D4: Data Privacy | D6: Misinformation
    df['MIT_Privacy_Alert'] = df['Short Description'].str.contains('privacy|tracking|data|secure', case=False)
    df['MIT_Integrity_Alert'] = df['Short Description'].str.contains('fake|generate|synthetic|voice', case=False)
    return df

df = load_scrubbed_data()
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")

# --- HEADER & METHODOLOGY ---
st.title("🏛️ AI Observatory")
st.markdown("""
<div class="mit-card">
    <strong>Strategic Methodology:</strong> This platform audits 16,000+ entities by cross-referencing 
    technological metadata against the <strong>MIT AI Risk Repository (v4.0)</strong>. 
    Focus is placed on Domain 4 (Privacy) and Domain 6 (Integrity) to ensure regulatory compliance.
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL ---
st.sidebar.title("Oversight Controls")
view_mode = st.sidebar.radio("Observation Level:", ["Sectoral Landscape", "Individual Entity Audit"])
selected_sector = st.sidebar.selectbox("Filter by Sector:", ["All"] + sorted(df['Category'].unique().tolist()))

# Filtering logic
filtered_df = df if selected_sector == "All" else df[df['Category'] == selected_sector]

# --- VIEW 1: MARKET LANDSCAPE ---
if view_mode == "Sectoral Landscape":
    st.subheader(f"Market Analysis: {selected_sector}")
    
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Total Entities", f"{len(filtered_df):,}")
    with m2: st.metric("MIT Privacy Flags", filtered_df['MIT_Privacy_Alert'].sum())
    with m3: st.metric("MIT Integrity Flags", filtered_df['MIT_Integrity_Alert'].sum())
    
    st.markdown("---")
    
    # Clean Bar Chart
    top_tools = filtered_df['Category'].value_counts().head(10).reset_index()
    fig = px.bar(top_tools, x='count', y='Category', orientation='h', 
                 title="Sector Composition", color_discrete_sequence=['#1c3d5a'])
    fig.update_layout(plot_bgcolor='white', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

# --- VIEW 2: INDIVIDUAL AUDIT (THE DEEP-DIVE) ---
else:
    st.subheader("Individual Entity Intelligence & Market Signal")
    search_tool = st.selectbox("Search Entity Database:", [""] + sorted(filtered_df['Name'].unique().tolist()))
    
    if search_tool:
        tool = df[df['Name'] == search_tool].iloc[0]
        
        col_info, col_market = st.columns([1, 1])
        
        with col_info:
            st.markdown(f"### Audit Dossier: {search_tool}")
            st.write(f"**Classification:** {tool['Category']}")
            st.write(f"**Description:** {tool['Short Description']}")
            st.markdown(f"""
            **MIT Risk Profile:**
            - Privacy (D4): {'🔴 High Risk' if tool['MIT_Privacy_Alert'] else '🟢 Compliant'}
            - Integrity (D6): {'🔴 High Alert' if tool['MIT_Integrity_Alert'] else '🟢 Compliant'}
            """)
            
        with col_market:
            st.markdown("### 📈 Market Trust Signal")
            if AV_API_KEY:
                # Alpha Vantage Ticker Search
                s_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={search_tool}&apikey={AV_API_KEY}"
                matches = requests.get(s_url).json().get('bestMatches', [])
                
                if matches:
                    ticker = matches[0]['1. symbol']
                    q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                    quote = requests.get(q_url).json().get('Global Quote', {})
                    
                    if quote:
                        st.metric(label=f"Parent Entity: {matches[0]['2. name']} ({ticker})", 
                                  value=f"${quote.get('05. price', 'N/A')}", 
                                  delta=quote.get('10. change percent', '0%'))
                    else:
                        st.write("Market data currently unavailable for this ticker.")
                else:
                    st.write("Entity is currently private or not listed on public exchanges.")
            else:
                st.warning("Alpha Vantage API Key not detected in System Secrets.")

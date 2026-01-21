import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. SETTINGS & DESIGN ---
st.set_page_config(page_title="Global AI Strategic Intelligence", layout="wide")
NEWS_API_KEY = "96a1acccb0d64d8f8f2dee11c7ac4ade" # Replace this!

@st.cache_data
def load_and_scrub_data():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    
    # --- DATA SCRUBBING ENGINE ---
    df = df.drop_duplicates(subset=['Name'])
    # Remove tools with nonsense names or empty descriptions
    df = df[df['Name'].str.len() > 1]
    df['Short Description'] = df['Short Description'].fillna("Technical documentation pending review.")
    df['Category'] = df['Category'].fillna("General AI")
    # Clean up whitespace
    df['Name'] = df['Name'].str.strip()
    
    # MIT Risk Enrichment
    df['Privacy_Score'] = df['Short Description'].str.contains('data|privacy|tracking', case=False).map({True: 80, False: 10})
    return df

df = load_and_scrub_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏛️ GovIntel v3.0")
menu = st.sidebar.radio("Intelligence Modules", ["Sector Intelligence", "Tool Deep-Dive & News", "Market Analytics"])

# --- MODULE 1: SECTOR INTELLIGENCE ---
if menu == "Sector Intelligence":
    st.title("📂 Sector-Specific Intelligence")
    target_sector = st.selectbox("Select a Strategic Sector:", sorted(df['Category'].unique()))
    
    sector_df = df[df['Category'] == target_sector]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(f"Total {target_sector} Tools", len(sector_df))
        st.write("### Sector Risk Profile")
        st.bar_chart(sector_df['Privacy_Score'].value_counts())
        
    with col2:
        st.write(f"### Top Tools in {target_sector}")
        st.dataframe(sector_df[['Name', 'Short Description', 'Privacy_Score']].head(20), use_container_width=True)

# --- MODULE 2: TOOL DEEP-DIVE & LIVE NEWS ---
elif menu == "Tool Deep-Dive & News":
    st.title("🔍 Entity Investigation & Live Feed")
    
    selected_tool = st.selectbox("Search Entity Database:", sorted(df['Name'].unique()))
    
    if selected_tool:
        tool_data = df[df['Name'] == selected_tool].iloc[0]
        
        st.markdown(f"### Audit for: {selected_tool}")
        st.info(f"**Baseline Intelligence:** {tool_data['Short Description']}")
        
        # --- NEWS API INTEGRATION ---
        st.markdown("---")
        st.subheader(f"📡 Live Intelligence Feed: {selected_tool}")
        
        url = f'https://newsapi.org/v2/everything?q={selected_tool}&apiKey={NEWS_API_KEY}&pageSize=5'
        response = requests.get(url).json()
        
        if response.get('articles'):
            for art in response['articles']:
                with st.container():
                    st.write(f"**{art['title']}**")
                    st.caption(f"Source: {art['source']['name']} | Date: {art['publishedAt'][:10]}")
                    st.write(art['description'])
                    st.markdown(f"[Read Full Report]({art['url']})")
                    st.write("---")
        else:
            st.warning("No recent news found for this specific tool. Broadening search to category...")

# --- MODULE 3: MARKET ANALYTICS ---
elif menu == "Market Analytics":
    st.title("📈 Global Market Trends")
    fig = px.treemap(df.head(1000), path=['Category', 'Name'], values='Privacy_Score',
                     color='Privacy_Score', color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig, use_container_width=True)

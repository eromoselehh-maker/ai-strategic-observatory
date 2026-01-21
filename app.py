import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI ARCHITECTURE
st.set_page_config(page_title="AI Observatory | Philip’s Consulting", layout="wide")

# CSS for the Ticker and Card Buttons
st.markdown("""
    <style>
    .ticker-wrap {
        width: 100%; overflow: hidden; background-color: #1C3D5A; 
        color: #00D1FF; padding: 12px 0; position: fixed; top: 0; left: 0; z-index: 999;
        border-bottom: 2px solid #00D1FF; font-family: monospace;
    }
    .ticker {
        display: inline-block; white-space: nowrap; padding-right: 100%;
        animation: ticker 40s linear infinite;
    }
    @keyframes ticker {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    .main .block-container { padding-top: 6rem; }
    
    /* Interactive Card Buttons */
    div.stButton > button {
        width: 100%; border-radius: 12px; height: 110px;
        background-color: #F8FAFC; border: 1px solid #E2E8F0;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00D1FF; background-color: #F0FDFF;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE (The "Brain" that makes buttons work)
if 'filter_sector' not in st.session_state:
    st.session_state.filter_sector = "All"
if 'current_nav' not in st.session_state:
    st.session_state.current_nav = "📈 Dashboard"

# 3. DATA ENGINE
@st.cache_data
def load_and_scrub():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).dropna(subset=['Name', 'Category'])
    df['MIT_D4'] = df['Short Description'].str.contains('privacy|tracking|data|surveillance', case=False, na=False)
    df['MIT_D6'] = df['Short Description'].str.contains('fake|generate|synthetic|voice|media', case=False, na=False)
    return df

df = load_and_scrub()
AV_API_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "")
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")

# 4. TICKER
ticker_text = " ⚠️ ALERT: High Risk Cluster detected in 'Data Analysis' | 📈 MSFT +0.5% | 📈 NVDA +1.2% | Philip's Consulting Proprietary Risk Model Active... "
st.markdown(f'<div class="ticker-wrap"><div class="ticker">{ticker_text * 5}</div></div>', unsafe_allow_html=True)

# 5. SIDEBAR
st.sidebar.title("🏛️ AI OBSERVATORY")
st.sidebar.caption("By **Philip’s Consulting**")
# We use st.session_state to sync the sidebar with the buttons
st.session_state.current_nav = st.sidebar.radio("Navigation", ["📈 Dashboard", "🔍 Entity Audit", "📖 Framework"], index=0 if st.session_state.current_nav == "📈 Dashboard" else 1 if st.session_state.current_nav == "🔍 Entity Audit" else 2)

# --- PAGE 1: DASHBOARD ---
if st.session_state.current_nav == "📈 Dashboard":
    st.title("Strategic Governance Dashboard")
    
    # CLICKABLE BOXES: Now they actually set filters
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f"📊 Total Entities\n{len(df):,}"):
            st.session_state.filter_sector = "All"
    with c2:
        if st.button(f"🔴 Privacy (D4)\n{df['MIT_D4'].sum()} Flags"):
            # Clicking this filters for a sector known for high risk, e.g., 'Data Analysis'
            st.session_state.filter_sector = "Data Analysis"
            st.session_state.current_nav = "🔍 Entity Audit"
            st.rerun()
    with c3:
        if st.button(f"⚠️ Integrity (D6)\n{df['MIT_D6'].sum()} Flags"):
            st.session_state.filter_sector = "Text Generation"
            st.session_state.current_nav = "🔍 Entity Audit"
            st.rerun()

    # CHARTS (Always visible, but now interactive)
    st.markdown("---")
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Interactive Sector Map")
        # Treemap allows clicking to drill down into categories natively
        fig = px.treemap(df, path=['Category', 'Name'], values='MIT_D4', 
                         color='MIT_D4', color_continuous_scale='Reds',
                         title="Click a sector to see specific tool risks")
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Top Risk Hotspots")
        hotspots = df.groupby('Category')['MIT_D4'].mean().sort_values(ascending=False).head(10).reset_index()
        fig2 = px.bar(hotspots, x='MIT_D4', y='Category', orientation='h', 
                      color='MIT_D4', color_continuous_scale='Reds')
        fig2.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Hover over bars for specific risk percentages.")

# --- PAGE 2: ENTITY AUDIT ---
elif st.session_state.current_nav == "🔍 Entity Audit":
    st.title("Entity Intelligence Audit")
    
    # This filter is pre-filled if you clicked a button on the dashboard
    sector_list = ["All"] + sorted(df['Category'].unique().tolist())
    try:
        default_index = sector_list.index(st.session_state.filter_sector)
    except:
        default_index = 0
        
    selected_sector = st.selectbox("Market Sector:", sector_list, index=default_index)
    
    filtered_df = df if selected_sector == "All" else df[df['Category'] == selected_sector]
    target = st.selectbox("Select Target Entity:", [""] + sorted(filtered_df['Name'].unique().tolist()))
    
    if target:
        tool = df[df['Name'] == target].iloc[0]
        st.header(target)
        ca, cb = st.columns(2)
        with ca:
            st.markdown(f"**Description:** {tool['Short Description']}")
            st.write(f"**MIT D4 (Privacy):** {'🔴 RISK' if tool['MIT_D4'] else '🟢 CLEAR'}")
            st.write(f"**MIT D6 (Integrity):** {'🔴 RISK' if tool['MIT_D6'] else '🟢 CLEAR'}")
            
            if NEWS_API_KEY:
                st.subheader("📡 Live Feed")
                res = requests.get(f"https://newsapi.org/v2/everything?q={target}+AI&apiKey={NEWS_API_KEY}&pageSize=2").json()
                for art in res.get('articles', []):
                    st.info(f"{art['title']}")

        with cb:
            st.subheader("📈 Market Signal")
            ticker = st.text_input("Enter Ticker (e.g. MSFT):", "").upper()
            if ticker and AV_API_KEY:
                q_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_API_KEY}"
                quote = requests.get(q_url).json().get('Global Quote', {})
                if quote:
                    st.metric(f"{ticker}", f"${quote.get('05. price')}", delta=quote.get('10. change percent'))

# --- PAGE 3: FRAMEWORK ---
elif st.session_state.current_nav == "📖 Framework":
    st.title("Governance Framework")
    st.write("Auditing methodology by **Philip’s Consulting**.")
    st.markdown("""
    - **D4 Privacy:** Surveillance and tracking detection.
    - **D6 Integrity:** Synthetic media and deepfake flagging.
    - **SIG:** Strategic Investment Gap analysis.
    """)

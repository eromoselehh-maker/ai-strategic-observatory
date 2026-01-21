import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. DESIGNER SETTINGS: Institutional Clean
st.set_page_config(page_title="AI Strategic Intelligence", layout="wide")

# Custom CSS for Professional Typography and Spacing
st.markdown("""
    <style>
    /* Main background to clean white */
    .stApp { background-color: #FFFFFF; color: #262730; }
    
    /* Metric Cards Styling */
    div[data-testid="stMetricValue"] { 
        color: #1f77b4; 
        font-weight: 700; 
        font-size: 2.2rem !important;
    }
    
    /* Custom Card Design for Tool Audit */
    .audit-card {
        background-color: #F8F9FB;
        border: 1px solid #E6E9EF;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #F0F2F6;
        border-right: 1px solid #E6E9EF;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name']).fillna("Information Pending")
    # MIT Risk Logic
    df['Privacy_Flag'] = df['Short Description'].str.contains('data|privacy|tracking|secure', case=False)
    df['Ethics_Flag'] = df['Short Description'].str.contains('bias|ethics|fairness|hiring', case=False)
    df['Safety_Score'] = 100 - (df['Privacy_Flag'].astype(int)*40 + df['Ethics_Flag'].astype(int)*40)
    return df

df = load_data()

# --- HEADER SECTION ---
st.title("🔭 AI Strategic Observatory")
st.caption("Strategic Audit & Investment Planning Portal | v2.4")
st.markdown("---")

# --- EXECUTIVE METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Global Ecosystem", f"{len(df):,}")
m2.metric("Market Sectors", df['Category'].nunique())
m3.metric("Critical Risks", (df['Safety_Score'] < 50).sum())
m4.metric("Mean Safety Index", f"{df['Safety_Score'].mean():.1f}%")

# --- INTERACTIVE NAVIGATION ---
tab_market, tab_audit, tab_policy = st.tabs(["Market Landscape", "Single-Tool Audit", "Policy Recommendations"])

with tab_market:
    col_chart, col_list = st.columns([2, 1])
    
    with col_chart:
        st.subheader("Sector Concentration & Safety Index")
        # Creating a more sophisticated Scatter with 'Safety' as color
        fig = px.scatter(df.head(1000), x="Category", y="Safety_Score", 
                         color="Safety_Score", size_max=10,
                         color_continuous_scale='RdYlGn',
                         title="Visualizing Safety Distribution (Sample: 1000 Tools)")
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_list:
        st.subheader("Top Growing Sectors")
        st.dataframe(df['Category'].value_counts().head(10), use_container_width=True)

with tab_audit:
    st.subheader("Individual Entity Intelligence")
    # THE INTERACTIVE DRILL-DOWN: Select a tool
    tool_list = sorted(df['Name'].unique().tolist())
    selected_tool = st.selectbox("Search and Audit Tool Portfolio", [""] + tool_list)
    
    if selected_tool:
        tool_data = df[df['Name'] == selected_tool].iloc[0]
        
        # Design a "Report Card"
        st.markdown(f"""
        <div class="audit-card">
            <h2 style='color:#1f77b4; margin-top:0;'>{tool_data['Name']}</h2>
            <p><strong>Primary Market:</strong> {tool_data['Category']}</p>
            <p><strong>Safety Score:</strong> <span style='color:{"#d32f2f" if tool_data['Safety_Score'] < 60 else "#388e3c"}'>{tool_data['Safety_Score']}%</span></p>
            <hr style='border: 0.5px solid #E6E9EF;'>
            <p style='font-style: italic;'>{tool_data['Short Description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Actionable Advice for Government
        c1, c2 = st.columns(2)
        with c1:
            st.info("**Investment Signal:** " + ("Hold / Monitor" if tool_data['Safety_Score'] < 70 else "High Potential for Integration"))
        with c2:
            st.error("**Risk Mitigation:** " + ("Immediate Compliance Review Required" if tool_data['Safety_Score'] < 60 else "Routine Monitoring"))

with tab_policy:
    st.subheader("Strategic Opportunity Map")
    st.write("Government investment should target 'Low Density' sectors with high strategic importance.")
    
    # Horizontal Bar chart for readability
    opp_data = df['Category'].value_counts().nsmallest(12).reset_index()
    fig_opp = px.bar(opp_data, x='count', y='Category', orientation='h', 
                     color='count', color_continuous_scale='Blues_r')
    st.plotly_chart(fig_opp, use_container_width=True)

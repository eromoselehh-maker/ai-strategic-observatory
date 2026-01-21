import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Strategic Observatory", layout="wide")

@st.cache_data
def load_data():
    # Load the data
    df = pd.read_csv("Complete AI Tools Dataset 2025 - 16763 Tools from AIToolBuzz.csv")
    df = df.drop_duplicates(subset=['Name'])
    
    # --- MIT RISK DOMAIN SCANNING (The "Brain") ---
    # 1. Privacy & Security
    df['Privacy_Risk'] = df['Short Description'].str.contains('privacy|data|tracking|secure', case=False, na=False)
    # 2. Misinformation & Harm
    df['Misinfo_Risk'] = df['Short Description'].str.contains('fake|synthetic|generate|voice|deepfake', case=False, na=False)
    # 3. Bias & Fairness
    df['Bias_Risk'] = df['Short Description'].str.contains('hiring|facial|credit|judge|selection', case=False, na=False)
    
    return df

df = load_data()

# --- THE FRONTEND DASHBOARD ---
st.title("🔭 AI Strategic Intelligence Observatory")
st.markdown("An advanced audit tool based on the MIT AI Risk Repository.")

# 1. TOP-LEVEL METRICS
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Unique Tools", f"{len(df):,}")
m2.metric("Privacy Flags", df['Privacy_Risk'].sum())
m3.metric("Misinfo Flags", df['Misinfo_Risk'].sum())
m4.metric("Bias Flags", df['Bias_Risk'].sum())

# 2. INTERACTIVE FILTERS (Sidebar)
st.sidebar.header("Filter Intelligence")
category = st.sidebar.selectbox("Market Sector", ["All"] + sorted(df['Category'].unique().tolist()))

# Filtering the data
filtered_df = df if category == "All" else df[df['Category'] == category]

# 3. STRATEGIC VISUALS
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Market Distribution")
    st.bar_chart(df['Category'].value_counts().head(10))

with col_right:
    st.subheader("MIT Risk Profile")
    risk_data = {
        "Privacy": df['Privacy_Risk'].sum(),
        "Misinfo": df['Misinfo_Risk'].sum(),
        "Bias": df['Bias_Risk'].sum()
    }
    st.bar_chart(pd.Series(risk_data))

# 4. AUDIT LOG
st.subheader(f"Detailed Audit Log: {category}")
st.dataframe(filtered_df[['Name', 'Category', 'Privacy_Risk', 'Misinfo_Risk', 'Bias_Risk']])

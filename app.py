import streamlit as st
from mock_data_generator import generate_campaign_data, generate_click_logs
from fraud_detector import detect_fraud
from trend_analyzer import analyze_trends
from asset_generator import generate_campaign_assets, MOCK_INPUTS

st.set_page_config(page_title="AI Marketing Optimizer", layout="wide")

st.title("AI Marketing Optimizer Dashboard")

# --- Campaign Performance ---
st.header("Campaign Performance")
st.subheader("Campaign Data Simulation")
with st.spinner("Generating campaign data..."):
    df = generate_campaign_data()

# Metrics
total_cost = df["Cost"].sum()
total_conversions = df["Conversions"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Cost", f"${total_cost:,.2f}")
col2.metric("Total Conversions", f"{total_conversions:,}")

# AI Insights
st.subheader("AI Insights")
insights = analyze_trends(df)
for insight in insights:
    if "Rising CPA" in insight:
        st.warning(insight)
    else:
        st.success(insight)

# Display Data
with st.expander("View Raw Campaign Data"):
    st.dataframe(df)

st.markdown("---")

# --- Ad Asset Generator ---
st.header("Ad Asset Generator")
st.write("Generate creative assets for your campaign.")

col1, col2 = st.columns(2)
with col1:
    st.info(f"**Product:** {MOCK_INPUTS['Product']}")
with col2:
    st.info(f"**Audience:** {MOCK_INPUTS['Audience']}")

if st.button("Generate Assets"):
    assets = generate_campaign_assets()
    
    st.subheader("Generated Assets")
    
    # Display Raw JSON for verification
    with st.expander("View Raw JSON Output"):
        st.json(assets)
    
    st.markdown("### Headlines")
    for item in assets.get("Headlines", []):
        st.write(f"- {item}")
        
    st.markdown("### Slogans")
    for item in assets.get("Slogans", []):
        st.write(f"- {item}")
        
    st.markdown("### Social Media Posts")
    for item in assets.get("Social Media Posts", []):
        st.write(f"- {item}")

st.markdown("---")

st.markdown("---")

# --- Fraud Detection ---
st.header("Fraud Detection System")
st.write("Simulate click logs and detect suspicious IP addresses using Isolation Forest.")

if st.button("Generate Logs & Detect Fraud"):
    with st.spinner("Generating 1000 click logs (including fraud scenario)..."):
        click_df = generate_click_logs(num_clicks=1000)
    
    st.subheader("Raw Click Logs")
    st.dataframe(click_df.head())
    st.write(f"Total Clicks: {len(click_df)}")
    
    with st.spinner("Running Fraud Detection Model..."):
        suspicious_ips = detect_fraud(click_df)
    
    st.subheader("Detected Suspicious IPs")
    if suspicious_ips:
        st.error(f"Suspicious Activity Detected from: {', '.join(suspicious_ips)}")
        
        # Show details for suspicious IPs
        st.write("Details for Suspicious IPs:")
        suspicious_data = click_df[click_df["IP_Address"].isin(suspicious_ips)]
        st.dataframe(suspicious_data.groupby("IP_Address").size().reset_index(name="Click Count"))
    else:
        st.success("No suspicious activity detected.")


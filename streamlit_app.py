import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Cybercrime & Forensics Dashboard", layout="wide")

# ---------------------------------
# TITLE
# ---------------------------------
st.title("🕵️ Cybercrime Intelligence & Forensics Dashboard")
st.markdown("Analyze cybercrime trends and investigate suspicious network activity.")

# ---------------------------------
# SIDEBAR CONTROLS
# ---------------------------------
st.sidebar.header("Controls")

crime_type = st.sidebar.selectbox(
    "Select Cybercrime Type",
    ["All", "Phishing", "Malware", "Ransomware"]
)

threshold = st.sidebar.slider(
    "Suspicious Request Threshold",
    10, 200, 75
)

show_raw = st.sidebar.checkbox("Show Raw Data")

# ---------------------------------
# CYBERCRIME TREND DATA (SIMULATED)
# ---------------------------------
st.header("📊 Cybercrime Trends")

trend_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Phishing": [120, 150, 170, 200, 230],
    "Malware": [80, 90, 100, 120, 140],
    "Ransomware": [50, 60, 65, 70, 85]
}).set_index("Month")

st.line_chart(trend_data)

st.info("Cybercrime incidents are increasing over time, especially phishing attacks.")

# ---------------------------------
# FORENSIC DATA (REALISTIC LOGS)
# ---------------------------------
st.header("🔍 Digital Forensics Case Analyzer")

log_data = {
    "IP": [
        "8.8.8.8", "1.1.1.1", "142.250.72.14",
        "172.217.3.110", "185.199.108.153",
        "151.101.1.69", "192.168.1.1"
    ],
    "Requests": [45, 12, 180, 95, 30, 110, 10],
    "Time": [
        "10:00", "10:05", "10:10",
        "10:15", "10:20", "10:25", "10:30"
    ]
}

df = pd.DataFrame(log_data)

# ---------------------------------
# ANALYZE BUTTON
# ---------------------------------
if st.button("Analyze Case"):

    st.info("Fetching IP location data...")

    latitudes = []
    longitudes = []
    countries = []

    for ip in df["IP"]:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}").json()
            latitudes.append(response.get("lat", 0))
            longitudes.append(response.get("lon", 0))
            countries.append(response.get("country", "Unknown"))
        except:
            latitudes.append(0)
            longitudes.append(0)
            countries.append("Error")

    df["lat"] = latitudes
    df["lon"] = longitudes
    df["Country"] = countries

    st.success("Analysis Complete!")

    # ---------------------------------
    # TABLE
    # ---------------------------------
    st.subheader("📋 Network Activity Table")
    st.dataframe(df)

    # ---------------------------------
    # BAR CHART
    # ---------------------------------
    st.subheader("📊 Requests per IP")
    st.bar_chart(df.set_index("IP")["Requests"])

    # ---------------------------------
    # MAP
    # ---------------------------------
    st.subheader("🌍 IP Geolocation Map")
    st.map(df[["lat", "lon"]])

    # ---------------------------------
    # SUSPICIOUS DETECTION
    # ---------------------------------
    suspicious = df[df["Requests"] > threshold]

    st.subheader("🚨 Suspicious Activity Detection")

    if not suspicious.empty:
        st.warning("⚠️ Suspicious IPs Detected!")
        st.write(suspicious)
    else:
        st.success("No suspicious activity detected.")

    # ---------------------------------
    # OPTIONAL RAW DATA
    # ---------------------------------
    if show_raw:
        st.subheader("Raw Data")
        st.write(df)

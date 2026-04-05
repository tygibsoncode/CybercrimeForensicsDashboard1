import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Cybercrime & Forensics Dashboard", layout="wide")

# ---------------------------
# TITLE
# ---------------------------
st.title("🕵️ Cybercrime Intelligence & Forensics Dashboard")

# ---------------------------
# SIDEBAR (Widgets)
# ---------------------------
st.sidebar.header("Controls")

region = st.sidebar.selectbox(
    "Select Region",
    ["Global", "USA", "Europe", "Asia"]
)

threshold = st.sidebar.slider(
    "Suspicious Activity Threshold",
    1, 100, 10
)

show_data = st.sidebar.checkbox("Show Raw Data")

# ---------------------------
# SAMPLE DATA (we’ll replace later)
# ---------------------------
data = {
    "IP": ["8.8.8.8", "1.1.1.1", "142.250.72.14", "172.217.3.110"],
    "Requests": [50, 5, 80, 20]
}

df = pd.DataFrame(data)

# ---------------------------
# BUTTON
# ---------------------------
if st.button("Analyze Data"):

    st.info("Fetching IP location data...")

    latitudes = []
    longitudes = []
    countries = []

    # API CALL (IP → location)
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

    df["Latitude"] = latitudes
    df["Longitude"] = longitudes
    df["Country"] = countries

    st.success("Analysis Complete!")

    # ---------------------------
    # TABLE
    # ---------------------------
    st.subheader("📋 Data Table")
    st.dataframe(df)

    # ---------------------------
    # CHART
    # ---------------------------
    st.subheader("📊 Requests per IP")
    st.bar_chart(df.set_index("IP")["Requests"])

    # ---------------------------
    # MAP
    # ---------------------------
    st.subheader("🌍 IP Locations")
    map_data = df[["Latitude", "Longitude"]]
    st.map(map_data)

    # ---------------------------
    # FORENSIC LOGIC (simple but powerful)
    # ---------------------------
    suspicious = df[df["Requests"] > threshold]

    if not suspicious.empty:
        st.warning("⚠️ Suspicious activity detected!")
        st.write(suspicious)
    else:
        st.success("No suspicious activity detected.")

    # ---------------------------
    # OPTIONAL TOGGLE
    # ---------------------------
    if show_data:
        st.write("Raw Data:")
        st.write(df)

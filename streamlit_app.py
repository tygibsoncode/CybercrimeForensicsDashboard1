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
# SIDEBAR
# ---------------------------------
st.sidebar.header("Controls")

threshold = st.sidebar.slider(
    "Suspicious Request Threshold",
    10, 200, 75
)

show_raw = st.sidebar.checkbox("Show Raw Data")

# ---------------------------------
# CYBERCRIME NEWS + ANALYSIS
# ---------------------------------
st.header("📰 Live Cybercrime Intelligence")

API_KEY = "839a767348614c338279472de3c82615"

crime_filter = st.selectbox(
    "Filter by Cybercrime Type",
    ["All", "Phishing", "Ransomware", "Malware", "Hacking"]
)

query = "cybercrime OR hacking OR ransomware OR phishing OR malware"

if crime_filter != "All":
    query = crime_filter.lower()

url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"

response = requests.get(url)

phishing_count = ransomware_count = malware_count = hacking_count = 0
trending_threat = "Unknown"

if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])

    if articles:

        for article in articles:
            text = (article["title"] or "").lower() + " " + (article["description"] or "").lower()

            if "phishing" in text:
                phishing_count += 1
            if "ransomware" in text:
                ransomware_count += 1
            if "malware" in text:
                malware_count += 1
            if "hack" in text:
                hacking_count += 1

        # Chart
        count_df = pd.DataFrame({
            "Type": ["Phishing", "Ransomware", "Malware", "Hacking"],
            "Count": [phishing_count, ransomware_count, malware_count, hacking_count]
        }).set_index("Type")

        st.subheader("📊 Cybercrime Type Distribution")
        st.bar_chart(count_df)

        # Trending threat
        trend_counts = {
            "Phishing": phishing_count,
            "Ransomware": ransomware_count,
            "Malware": malware_count,
            "Hacking": hacking_count
        }

        trending_threat = max(trend_counts, key=trend_counts.get)

        st.subheader("🔥 Current Trending Threat")
        st.warning(f"Most reported threat: {trending_threat}")

        # Show articles
        st.subheader("🗞️ Latest Articles")
        for article in articles[:5]:
            st.markdown(f"### {article['title']}")
            st.write(article["description"])
            st.markdown(f"[Read more]({article['url']})")
            st.write("---")

        st.success("Live cybercrime data analyzed successfully!")

    else:
        st.warning("No articles found.")
else:
    st.error("Failed to fetch news data.")

# ---------------------------------
# FORENSICS SECTION
# ---------------------------------
st.header("🔍 Digital Forensics Case Analyzer")

# DEFAULT DATA
default_data = {
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

df = pd.DataFrame(default_data)

# FILE UPLOAD
uploaded_file = st.file_uploader("📁 Upload Network Log CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
else:
    st.info("Using default sample data.")

# VALIDATION
required_columns = {"IP", "Requests", "Time"}

if not required_columns.issubset(df.columns):
    st.error("CSV must contain columns: IP, Requests, Time")
    st.stop()

# Example format
with st.expander("📄 Example CSV Format"):
    st.code("""IP,Requests,Time
8.8.8.8,50,10:00
1.1.1.1,10,10:05
142.250.72.14,120,10:10
""")

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

    # TABLE
    st.subheader("📋 Network Activity Table")
    st.dataframe(df)

    # CHART
    st.subheader("📊 Requests per IP")
    st.bar_chart(df.set_index("IP")["Requests"])

    # MAP
    st.subheader("🌍 IP Geolocation Map")
    st.map(df[["lat", "lon"]])

    # SMART DETECTION
    st.subheader("🚨 Smart Threat Detection")

    suspicious = df[df["Requests"] > threshold]

    if not suspicious.empty:

        st.warning("⚠️ Suspicious activity detected!")

        if trending_threat == "Ransomware":
            st.error("High ransomware activity globally. Investigate immediately.")

        elif trending_threat == "Phishing":
            st.warning("Phishing attacks trending. Check for unusual access patterns.")

        elif trending_threat == "Malware":
            st.warning("Malware threats increasing. Monitor repeated requests.")

        elif trending_threat == "Hacking":
            st.error("Hacking attempts rising. Possible intrusion detected.")

        st.write(suspicious)

    else:
        st.success("No suspicious activity detected.")

    # RAW DATA
    if show_raw:
        st.subheader("Raw Data")
        st.write(df)

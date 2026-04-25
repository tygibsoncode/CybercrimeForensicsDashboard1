# Cybercrime & Forensics Dashboard

An interactive Streamlit dashboard for analyzing cybercrime trends and investigating suspicious network activity.

## Overview
This project combines cybersecurity intelligence with digital forensics techniques.  
It allows users to:
- Monitor real-time cybercrime trends
- Analyze uploaded network logs
- Detect suspicious activity based on request patterns
- Visualize IP geolocation and threat distribution

## Features

### Live Cybercrime Intelligence
- Fetches real-time cybersecurity news using NewsAPI
- Categorizes threats (Phishing, Ransomware, Malware, Hacking)
- Identifies the current trending threat

### Network Log Analysis
- Upload CSV files containing IP activity
- Analyze request frequency per IP
- Detect suspicious behavior using configurable thresholds

### Threat Detection
- Flags IPs with unusually high request counts
- Adapts warnings based on trending global threats

### Data Visualization
- Bar charts for request activity
- Tables for structured investigation
- Map visualization of IP geolocation

## Technologies Used
- Python
- Streamlit
- Pandas
- REST APIs (NewsAPI, IP geolocation API)

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt

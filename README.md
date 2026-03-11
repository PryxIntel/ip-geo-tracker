# IP OSINT Investigation Tool 🔍

An **Open Source Intelligence (OSINT)** cybersecurity tool that converts an IP address into a **detailed security investigation report**.

This tool combines **IP geolocation, threat intelligence, and VPN/proxy detection** to help security analysts investigate suspicious IP addresses.

---

# 🚀 Features

## 🌍 IP Geolocation Tracking

* Retrieves **Country, Region, City, ISP, Timezone, and Coordinates**
* Generates an **interactive map using Folium**
* Saves the map locally for visual investigation

## 🛡 Threat Intelligence

* Integrates with the **AbuseIPDB API**
* Detects whether the IP has been reported for:

  * Malware activity
  * Brute force attacks
  * Spam
  * Bot activity

## 🔐 Network Security Analysis

Detects whether the IP belongs to:

* VPN
* Proxy
* Tor Exit Node
* Hosting Provider

## 📄 Automated Investigation Reports

Automatically generates **clean text reports** containing:

* IP Information
* Geolocation
* Security Analysis
* Threat Intelligence Summary

All outputs are automatically organized inside the **`reports/` directory**.

## 🖥 Dual Interface

Supports both:

* **Command Line Interface (CLI)**
* **GUI Interface (Tkinter)**

---

# ⚙️ Setup & Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/PryxIntel/ip-geo-tracker.git
cd ip-geo-tracker
```

---

## 2️⃣ Set Up Virtual Environment & Install Libraries

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure API Keys

Create a `.env` file in the project root directory.

Example:

```text
ABUSEIPDB_API_KEY=your_key_here
IPScore_API_KEY=your_key_here
```

These API keys will be automatically loaded using **python-dotenv**.

---

# 🔑 APIs Used

## AbuseIPDB

Used for **malicious IP reputation detection and threat intelligence scoring**.

Website:
https://www.abuseipdb.com

---

## IPScore API

Used to detect:

* VPN usage
* Proxy servers
* Tor exit nodes
* Hosting providers

---

# 🧪 Example Output

### CLI Investigation Report

`reports/investigation_report_8_8_8_8.txt`

```
=== SECURITY INVESTIGATION REPORT ===

Target IP : 8.8.8.8
Date      : 2026-03-12 12:00:00 UTC

[ 1. IP INFORMATION & GEOLOCATION ]

City      : Mountain View
Region    : California
Country   : US
ISP/Org   : Google LLC

[ 2. NETWORK SECURITY ANALYSIS ]

VPN       : False
Proxy     : False
Tor Node  : False

[ 3. THREAT INTELLIGENCE (AbuseIPDB) ]

Confidence Score : 0%
Total Reports    : 0
Last Reported    : N/A
```

---

# 📁 Project Structure

```
ip-geo-tracker/
│
├── core_engine.py       # Core OSINT logic and API integration
├── main.py              # CLI and GUI application router
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
│
├── reports/             # Auto-generated investigation outputs
│   ├── investigation_report_8_8_8_8.txt
│   └── map_8_8_8_8.html
│
├── .env                 # API keys (ignored by Git)
└── .gitignore           # Git ignore rules
```

---

# 🛠 Technologies Used

* Python 3
* Requests (API communication)
* Folium (interactive mapping)
* Tkinter (GUI)
* python-dotenv (environment variable management)

---

# 📌 Use Cases

This tool can be used for:

* Cybersecurity investigations
* OSINT research
* Threat intelligence analysis
* SOC analyst workflows
* Network monitoring

---

# ⚠️ Disclaimer

This tool is intended **for educational and cybersecurity research purposes only**.

Unauthorized or illegal investigations are strictly discouraged.

---

# 👨‍💻 Author

Developed by **Priyanshu Singh Chauhan (PryxIntel)**

GitHub:
https://github.com/PryxIntel

---

# ⭐ Future Improvements

Planned upgrades for future releases:

* ASN lookup
* WHOIS lookup
* Shodan integration
* Port scanning
* Web dashboard integration

import os
import re
import csv
import requests
import folium
from datetime import datetime
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
VPNAPI_KEY = os.getenv("VPNAPI_KEY")

class OSINTTracker:
    def __init__(self):
        self.report_data = {}

    def is_valid_ip(self, ip):
        """Validates IPv4 format."""
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        return pattern.match(ip) is not None

    def get_geolocation(self, ip):
        """Fetches standard geolocation data."""
        url = f"http://ip-api.com/json/{ip}"
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200 and r.json().get("status") == "success":
                data = r.json()
                self.report_data['geo'] = data
                return data
        except requests.RequestException:
            pass
        return None

    def get_threat_intelligence(self, ip):
        """Queries AbuseIPDB for malicious activity reports."""
        if not ABUSEIPDB_API_KEY:
            return {"error": "Missing AbuseIPDB API Key"}
        
        url = "https://api.abuseipdb.com/api/v2/check"
        querystring = {'ipAddress': ip, 'maxAgeInDays': '90'}
        headers = {'Accept': 'application/json', 'Key': ABUSEIPDB_API_KEY}
        
        try:
            r = requests.get(url, headers=headers, params=querystring, timeout=8)
            if r.status_code == 200:
                data = r.json()['data']
                self.report_data['threat'] = data
                return data
        except requests.RequestException:
            pass
        return {"error": "Threat intel query failed"}

    def get_vpn_status(self, ip):
        """Checks if IP is a VPN, Proxy, or Tor node using VPNAPI.io."""
        if not VPNAPI_KEY:
             return {"error": "Missing VPNAPI Key"}
             
        url = f"https://vpnapi.io/api/{ip}?key={VPNAPI_KEY}"
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                data = r.json().get('security', {})
                self.report_data['security'] = data
                return data
        except requests.RequestException:
            pass
        return {"error": "VPN query failed"}

    def generate_report(self, ip):
        """Generates a structured OSINT text report in the reports folder."""
        os.makedirs("reports", exist_ok=True)
        filename = os.path.join("reports", f"investigation_report_{ip.replace('.', '_')}.txt")
        
        geo = self.report_data.get('geo', {})
        threat = self.report_data.get('threat', {})
        sec = self.report_data.get('security', {})

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== SECURITY INVESTIGATION REPORT ===\n")
            f.write(f"Target IP : {ip}\n")
            f.write(f"Date      : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n")
            
            f.write("[ 1. IP INFORMATION & GEOLOCATION ]\n")
            f.write(f"City      : {geo.get('city', 'N/A')}\n")
            f.write(f"Region    : {geo.get('regionName', 'N/A')}\n")
            f.write(f"Country   : {geo.get('country', 'N/A')}\n")
            f.write(f"ISP/Org   : {geo.get('isp', 'N/A')}\n\n")
            
            f.write("[ 2. NETWORK SECURITY ANALYSIS ]\n")
            f.write(f"VPN       : {sec.get('vpn', 'Unknown')}\n")
            f.write(f"Proxy     : {sec.get('proxy', 'Unknown')}\n")
            f.write(f"Tor Node  : {sec.get('tor', 'Unknown')}\n\n")
            
            f.write("[ 3. THREAT INTELLIGENCE (AbuseIPDB) ]\n")
            f.write(f"Confidence Score : {threat.get('abuseConfidenceScore', 'N/A')}%\n")
            f.write(f"Total Reports    : {threat.get('totalReports', 'N/A')}\n")
            f.write(f"Last Reported    : {threat.get('lastReportedAt', 'N/A')}\n")

        return filename

    def generate_map(self, ip):
        """Generates the Folium map in the reports folder."""
        os.makedirs("reports", exist_ok=True)
        geo = self.report_data.get('geo', {})
        if 'lat' in geo and 'lon' in geo:
            m = folium.Map(location=[geo['lat'], geo['lon']], zoom_start=10)
            folium.Marker([geo['lat'], geo['lon']], popup=ip).add_to(m)
            
            map_file = os.path.join("reports", f"map_{ip.replace('.', '_')}.html")
            m.save(map_file)
            return map_file
        return None
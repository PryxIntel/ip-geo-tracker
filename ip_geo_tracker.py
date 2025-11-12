#!/usr/bin/env python3
"""
IP Geolocation Tracker
Saves an interactive map as ip_location.html (if coordinates available)
"""

import requests
import folium
import argparse
import sys
import csv
from datetime import datetime

# ---- Helper functions ----
def query_ipinfo(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

def query_ipapi(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return None
        data = r.json()
        if data.get("status") != "success":
            return None
        # normalize keys similar to ipinfo
        return {
            "ip": data.get("query"),
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("countryCode"),
            "org": data.get("isp"),
            "timezone": data.get("timezone"),
            "loc": f"{data.get('lat')},{data.get('lon')}" if data.get('lat') and data.get('lon') else None
        }
    except Exception:
        return None

def get_ip_data(ip):
    # if ip == 'json', ipinfo returns caller IP
    data = query_ipinfo(ip)
    if data and ("bogon" not in data):  # simple check
        return data
    # fallback
    data2 = query_ipapi(ip if ip else "")
    return data2

def print_pretty(data):
    if not data:
        print("No data found for this IP or API limit reached.")
        return
    print("\n📍 IP GEOLOCATION DETAILS")
    print("="*40)
    print(f"IP Address : {data.get('ip','N/A')}")
    print(f"City       : {data.get('city','N/A')}")
    print(f"Region     : {data.get('region','N/A')}")
    print(f"Country    : {data.get('country','N/A')}")
    print(f"Org/ISP    : {data.get('org','N/A')}")
    print(f"Timezone   : {data.get('timezone','N/A')}")
    print(f"Coordinates: {data.get('loc','N/A')}")
    print("="*40)

def save_map(data, filename="ip_location.html"):
    loc = data.get('loc')
    if not loc:
        return False
    try:
        lat, lon = map(float, loc.split(','))
        m = folium.Map(location=[lat, lon], zoom_start=8)
        popup_text = f"{data.get('city','')}, {data.get('region','')}, {data.get('country','')}"
        folium.Marker([lat, lon], popup=popup_text).add_to(m)
        m.save(filename)
        return True
    except Exception:
        return False

def save_csv(data, out_file="ip_log.csv"):
    header = ["timestamp","ip","city","region","country","org","timezone","loc"]
    row = [datetime.utcnow().isoformat(), data.get('ip'), data.get('city'), data.get('region'),
           data.get('country'), data.get('org'), data.get('timezone'), data.get('loc')]
    write_header = False
    try:
        with open(out_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # write header if file empty
            if f.tell() == 0:
                writer.writerow(header)
            writer.writerow(row)
        return True
    except Exception:
        return False

# ---- CLI ----
def main():
    parser = argparse.ArgumentParser(description="IP Geolocation Tracker")
    parser.add_argument("--ip", "-i", default="json",
                        help="IP address to lookup. Use empty or 'json' to detect your public IP.")
    parser.add_argument("--map", "-m", action="store_true", help="Save interactive map (ip_location.html)")
    parser.add_argument("--csv", "-c", action="store_true", help="Append result to ip_log.csv")
    args = parser.parse_args()

    ip_arg = args.ip
    ip_arg = ip_arg.strip() if ip_arg else "json"
    data = get_ip_data(ip_arg)

    if not data:
        print("Error: Could not retrieve geolocation data. Try again later or check your network.")
        sys.exit(1)

    print_pretty(data)

    if args.map:
        ok = save_map(data)
        if ok:
            print("🗺️  Map saved to ip_location.html")
        else:
            print("Map could not be created (no coordinates).")

    if args.csv:
        ok = save_csv(data)
        if ok:
            print("✅  Logged to ip_log.csv")
        else:
            print("Could not save CSV log.")

if __name__ == "__main__":
    main()

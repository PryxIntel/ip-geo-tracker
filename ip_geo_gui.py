#!/usr/bin/env python3
"""
IP Geolocation Tracker
MY FIRST PROJECT FOR CN
Roll: 2023021244
"""

import requests
import folium
import csv
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys
import traceback

def log_exceptions(exc_type, exc_value, exc_traceback):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write("---- Error ----\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

sys.excepthook = log_exceptions


# --- core functions (same logic as before) ---

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
    data = query_ipinfo(ip)
    if data and ("bogon" not in data):
        return data
    return query_ipapi(ip if ip else "")

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
    try:
        with open(out_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(header)
            writer.writerow(row)
        return True
    except Exception:
        return False

#  main function with GUI input 

def main():
    root = tk.Tk()
    root.withdraw()  # hide main window

    ip = simpledialog.askstring("IP Geolocation Tracker", "Enter an IP address: ")
    if ip is None:  # user pressed cancel
        return

    ip = ip.strip() if ip else "json"
    data = get_ip_data(ip)

    if not data:
        messagebox.showerror("Error", "Could not retrieve geolocation data.")
        return

    # prepare result string
    result = (
        f"IP Address : {data.get('ip','N/A')}\n"
        f"City       : {data.get('city','N/A')}\n"
        f"Region     : {data.get('region','N/A')}\n"
        f"Country    : {data.get('country','N/A')}\n"
        f"Org/ISP    : {data.get('org','N/A')}\n"
        f"Timezone   : {data.get('timezone','N/A')}\n"
        f"Coordinates: {data.get('loc','N/A')}\n\n"
        "Map saved to ip_location.html\nCSV log updated (ip_log.csv)"
    )

    # Save map and CSV
    save_map(data)
    save_csv(data)

    messagebox.showinfo("Geolocation Result", result)

if __name__ == "__main__":
    main()

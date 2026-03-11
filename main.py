import argparse
import tkinter as tk
from tkinter import simpledialog, messagebox
from core_engine import OSINTTracker

def run_cli(ip):
    print(f"[*] Starting OSINT investigation on {ip}...")
    tracker = OSINTTracker()
    
    if not tracker.is_valid_ip(ip):
        print("[-] Invalid IP Address format.")
        return

    tracker.get_geolocation(ip)
    tracker.get_threat_intelligence(ip)
    tracker.get_vpn_status(ip)
    
    report_file = tracker.generate_report(ip)
    map_file = tracker.generate_map(ip)
    
    print(f"[+] Investigation complete.")
    print(f"[+] Report saved to: {report_file}")
    if map_file:
        print(f"[+] Map saved to: {map_file}")

def run_gui():
    root = tk.Tk()
    root.withdraw()
    
    ip = simpledialog.askstring("OSINT Tracker", "Enter an IP address to investigate:")
    if not ip:
        return

    tracker = OSINTTracker()
    if not tracker.is_valid_ip(ip):
        messagebox.showerror("Error", "Invalid IP Address format.")
        return

    tracker.get_geolocation(ip)
    tracker.get_threat_intelligence(ip)
    tracker.get_vpn_status(ip)
    
    report_file = tracker.generate_report(ip)
    tracker.generate_map(ip)
    
    messagebox.showinfo("Success", f"Investigation complete!\nDetailed report saved to {report_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IP OSINT Investigation Tool")
    parser.add_argument("ip", nargs="?", help="Target IP address for CLI mode")
    args = parser.parse_args()

    if args.ip:
        run_cli(args.ip)
    else:
        run_gui()
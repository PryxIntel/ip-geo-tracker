import argparse
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from core_engine import OSINTTracker

# ==========================================
# CLI MODE (Terminal Execution)
# ==========================================
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

# ==========================================
# CYBERSECURITY GUI MODE
# ==========================================
class CyberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OSINT IP Investigation Terminal")
        self.root.geometry("800x600")
        self.root.configure(bg="#0a0a0a")  # Deep black background

        # Cyber Theme Colors & Fonts
        self.bg_color = "#0a0a0a"
        self.fg_color = "#00FF41"  # Matrix/Terminal Green
        self.accent_color = "#1a1a1a"
        self.font_title = ("Consolas", 14, "bold")
        self.font_main = ("Consolas", 11)

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="[ SYSTEM: OSINT IP INVESTIGATION DASHBOARD ]", 
                          bg=self.bg_color, fg=self.fg_color, font=self.font_title)
        header.pack(pady=15)

        # Input Frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="TARGET IP >", bg=self.bg_color, fg=self.fg_color, font=self.font_title).pack(side=tk.LEFT, padx=5)
        
        self.ip_entry = tk.Entry(input_frame, bg=self.accent_color, fg=self.fg_color, font=self.font_main, 
                                 insertbackground=self.fg_color, width=25, relief=tk.SUNKEN, borderwidth=2)
        self.ip_entry.pack(side=tk.LEFT, padx=10)
        
        # Allow hitting "Enter" to start the scan
        self.root.bind('<Return>', lambda event: self.start_scan_thread())

        self.scan_btn = tk.Button(input_frame, text="INITIATE SCAN", bg="#2b2b2b", fg=self.fg_color, font=self.font_main, 
                                  activebackground=self.fg_color, activeforeground="black", relief=tk.RAISED, 
                                  command=self.start_scan_thread)
        self.scan_btn.pack(side=tk.LEFT, padx=10)

        # Console Output Screen
        self.console = scrolledtext.ScrolledText(self.root, bg=self.accent_color, fg=self.fg_color, font=self.font_main, 
                                                 wrap=tk.WORD, height=22, width=85, borderwidth=2, relief=tk.SUNKEN)
        self.console.pack(pady=10, padx=20)
        self.console.insert(tk.END, "System Ready. Awaiting target coordinates...\n\n")
        self.console.config(state=tk.DISABLED)

    def print_to_console(self, text):
        """Helper to print text to the GUI console."""
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    def start_scan_thread(self):
        """Runs the scan in a background thread so the GUI doesn't freeze."""
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showwarning("Input Error", "Target IP cannot be empty.")
            return

        self.scan_btn.config(state=tk.DISABLED, text="SCANNING...")
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)  # Clear previous results
        self.console.config(state=tk.DISABLED)
        
        self.print_to_console(f"[*] Initializing connection to target: {ip}...")

        # Start the background thread
        threading.Thread(target=self.run_scan, args=(ip,), daemon=True).start()

    def run_scan(self, ip):
        """The actual scanning process running in the background."""
        tracker = OSINTTracker()
        
        if not tracker.is_valid_ip(ip):
            self.print_to_console("[-] ERROR: Invalid IPv4 format detected.")
            self.reset_button()
            return

        self.print_to_console("[+] Format verified. Querying Geolocation databases...")
        tracker.get_geolocation(ip)
        
        self.print_to_console("[+] Querying Threat Intelligence (AbuseIPDB)...")
        tracker.get_threat_intelligence(ip)
        
        self.print_to_console("[+] Analyzing Network Topology (VPN/Proxy/Tor)...")
        tracker.get_vpn_status(ip)
        
        self.print_to_console("[*] Compiling intelligence report...")
        report_file = tracker.generate_report(ip)
        map_file = tracker.generate_map(ip)

        # Print the final result to the screen
        self.print_to_console("\n" + "="*60)
        self.print_to_console("                 INVESTIGATION COMPLETE")
        self.print_to_console("="*60 + "\n")
        
        # Read the generated text report and print it to the GUI console
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                self.print_to_console(f.read())
        except Exception:
            self.print_to_console("[+] Report saved successfully to directory.")

        if map_file:
            self.print_to_console(f"\n[+] Interactive map saved to: {map_file}")
            
        self.reset_button()

    def reset_button(self):
        """Re-enables the scan button after completion."""
        self.scan_btn.config(state=tk.NORMAL, text="INITIATE SCAN")

def run_gui():
    root = tk.Tk()
    app = CyberGUI(root)
    root.mainloop()

# ==========================================
# ENTRY POINT ROUTER
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IP OSINT Investigation Tool")
    parser.add_argument("ip", nargs="?", help="Target IP address for CLI mode")
    args = parser.parse_args()

    if args.ip:
        run_cli(args.ip)
    else:
        run_gui()
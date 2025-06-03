import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os
import psutil
import platform
import subprocess
import threading
import time
from datetime import datetime
import glob
import winreg
import json
import sqlite3
import shutil

print("Please do NOT close this window while scanning")
print("use the interface to use this tool!")

class PCCheckerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PC System Checker & Scanner")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)
        
        self.colors = {
            'bg': '#0d1117',
            'card': '#161b22',
            'accent': '#238636',
            'accent_hover': '#2ea043',
            'text': '#f0f6fc',
            'text_dim': '#8b949e',
            'border': '#30363d',
            'danger': '#da3633',
            'warning': '#d29922',
            'info': '#1f6feb'
        }
        
        self.scan_results = {}
        
        self.setup_styles()
        self.create_widgets()
        self.start_system_monitor()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_header(main_frame)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        self.create_system_tab()
        self.create_scanner_tab()
        self.create_processes_tab()
        self.create_registry_tab()
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['card'])
        header_frame.pack(fill='x', pady=(0, 10))
        
        header_inner = tk.Frame(header_frame, bg=self.colors['card'])
        header_inner.pack(fill='x', padx=20, pady=15)
        
        title_label = tk.Label(header_inner, 
                              text="🔍 PC System Checker & Scanner",
                              font=('Helvetica', 20, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['card'])
        title_label.pack(side='left')
        
        self.status_label = tk.Label(header_inner,
                                    text="🟢 System Online",
                                    font=('Helvetica', 12),
                                    fg=self.colors['accent'],
                                    bg=self.colors['card'])
        self.status_label.pack(side='right')
        
    def create_system_tab(self):
        system_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(system_frame, text="💻 System Info")
        
        info_frame = tk.Frame(system_frame, bg=self.colors['card'])
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(info_frame, text="System Information", 
                font=('Helvetica', 14, 'bold'),
                fg=self.colors['text'], bg=self.colors['card']).pack(pady=10)
        
        self.system_text = scrolledtext.ScrolledText(info_frame, 
                                                    height=20,
                                                    bg=self.colors['bg'],
                                                    fg=self.colors['text'],
                                                    font=('Consolas', 10))
        self.system_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        refresh_btn = tk.Button(info_frame, text="🔄 Refresh System Info",
                               command=self.load_system_info,
                               bg=self.colors['accent'], fg=self.colors['text'],
                               font=('Helvetica', 10, 'bold'))
        refresh_btn.pack(pady=10)
        
        self.load_system_info()
        
    def create_scanner_tab(self):
        scanner_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(scanner_frame, text="🔍 File Scanner")
        
        controls_frame = tk.Frame(scanner_frame, bg=self.colors['card'])
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(controls_frame, text="File & Program Scanner", 
                font=('Helvetica', 14, 'bold'),
                fg=self.colors['text'], bg=self.colors['card']).pack(pady=10)
        
        buttons_frame = tk.Frame(controls_frame, bg=self.colors['card'])
        buttons_frame.pack(pady=10)
        
        scan_games_btn = tk.Button(buttons_frame, text="🎮 Scan for Games",
                                  command=self.scan_games,
                                  bg=self.colors['info'], fg=self.colors['text'],
                                  font=('Helvetica', 10))
        scan_games_btn.grid(row=0, column=0, padx=5, pady=5)
        
        scan_cheat_btn = tk.Button(buttons_frame, text="🎯 Scan for Cheat Tools",
                                  command=self.scan_cheat_tools,
                                  bg=self.colors['warning'], fg=self.colors['text'],
                                  font=('Helvetica', 10))
        scan_cheat_btn.grid(row=0, column=1, padx=5, pady=5)
        
        scan_suspicious_btn = tk.Button(buttons_frame, text="⚠️ Scan Suspicious Files",
                                       command=self.scan_suspicious_files,
                                       bg=self.colors['danger'], fg=self.colors['text'],
                                       font=('Helvetica', 10))
        scan_suspicious_btn.grid(row=0, column=2, padx=5, pady=5)
        
        export_btn = tk.Button(buttons_frame, text="💾 Save All to check.txt",
                              command=self.export_all_results,
                              bg='#6f42c1', fg=self.colors['text'],
                              font=('Helvetica', 10, 'bold'))
        export_btn.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
        
        custom_scan_btn = tk.Button(buttons_frame, text="📁 Custom Directory Scan",
                                   command=self.custom_directory_scan,
                                   bg=self.colors['accent'], fg=self.colors['text'],
                                   font=('Helvetica', 10))
        custom_scan_btn.grid(row=1, column=0, padx=5, pady=5)
        
        scan_browser_btn = tk.Button(buttons_frame, text="🌐 Scan Browser History",
                                     command=self.scan_browser_history,
                                     bg='#e74c3c', fg=self.colors['text'],
                                     font=('Helvetica', 10))
        scan_browser_btn.grid(row=1, column=2, padx=5, pady=5)
        
        export_btn = tk.Button(buttons_frame, text="💾 Save All to check.txt",
                              command=self.export_all_results,
                              bg='#6f42c1', fg=self.colors['text'],
                              font=('Helvetica', 10, 'bold'))
        export_btn.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
        
        results_frame = tk.Frame(scanner_frame, bg=self.colors['card'])
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(results_frame, text="Scan Results", 
                font=('Helvetica', 12, 'bold'),
                fg=self.colors['text'], bg=self.colors['card']).pack(pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     height=15,
                                                     bg=self.colors['bg'],
                                                     fg=self.colors['text'],
                                                     font=('Consolas', 9))
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_processes_tab(self):
        processes_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(processes_frame, text="⚡ Processes")
        
        controls_frame = tk.Frame(processes_frame, bg=self.colors['card'])
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(controls_frame, text="Running Processes Monitor", 
                font=('Helvetica', 14, 'bold'),
                fg=self.colors['text'], bg=self.colors['card']).pack(pady=10)
        
        refresh_processes_btn = tk.Button(controls_frame, text="🔄 Refresh Processes",
                                         command=self.load_processes,
                                         bg=self.colors['accent'], fg=self.colors['text'],
                                         font=('Helvetica', 10))
        refresh_processes_btn.pack(pady=5)
        
        self.processes_text = scrolledtext.ScrolledText(processes_frame,
                                                       height=20,
                                                       bg=self.colors['bg'],
                                                       fg=self.colors['text'],
                                                       font=('Consolas', 9))
        self.processes_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.load_processes()
        
    def create_registry_tab(self):
        registry_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(registry_frame, text="🗃️ Registry")
        
        controls_frame = tk.Frame(registry_frame, bg=self.colors['card'])
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(controls_frame, text="Registry Scanner", 
                font=('Helvetica', 14, 'bold'),
                fg=self.colors['text'], bg=self.colors['card']).pack(pady=10)
        
        scan_startup_btn = tk.Button(controls_frame, text="🚀 Scan Startup Programs",
                                    command=self.scan_startup_programs,
                                    bg=self.colors['info'], fg=self.colors['text'],
                                    font=('Helvetica', 10))
        scan_startup_btn.pack(pady=5)
        
        self.registry_text = scrolledtext.ScrolledText(registry_frame,
                                                      height=20,
                                                      bg=self.colors['bg'],
                                                      fg=self.colors['text'],
                                                      font=('Consolas', 9))
        self.registry_text.pack(fill='both', expand=True, padx=10, pady=10)
        
    def load_system_info(self):
        def get_info():
            self.system_text.delete(1.0, tk.END)
            self.system_text.insert(tk.END, "Loading system information...\n\n")
            
            try:
                info = f"""
=== SYSTEM INFORMATION ===
OS: {platform.system()} {platform.release()} ({platform.architecture()[0]})
Computer: {platform.node()}
Processor: {platform.processor()}
Python: {platform.python_version()}

=== HARDWARE INFO ===
CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical
CPU Usage: {psutil.cpu_percent()}%
Memory: {round(psutil.virtual_memory().total / (1024**3), 2)} GB total
Memory Usage: {psutil.virtual_memory().percent}%
Available Memory: {round(psutil.virtual_memory().available / (1024**3), 2)} GB

=== DISK INFO ===
"""
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        info += f"Drive {partition.device}: {round(usage.total / (1024**3), 2)} GB total, "
                        info += f"{round(usage.used / (1024**3), 2)} GB used ({round(usage.percent, 1)}%)\n"
                    except:
                        info += f"Drive {partition.device}: Access denied\n"
                
                info += f"\n=== NETWORK INFO ===\n"
                net_info = psutil.net_if_addrs()
                for interface, addresses in net_info.items():
                    info += f"\nInterface: {interface}\n"
                    for addr in addresses:
                        if addr.family == 2:  # IPv4
                            info += f"  IPv4: {addr.address}\n"
                
                self.system_text.delete(1.0, tk.END)
                self.system_text.insert(tk.END, info)
                
            except Exception as e:
                self.system_text.insert(tk.END, f"Error loading system info: {str(e)}")
        
        threading.Thread(target=get_info, daemon=True).start()
        
    def scan_games(self):
        def scan():
            self.results_text.insert(tk.END, "\n🎮 SCANNING FOR GAMES...\n" + "="*50 + "\n")
            
            game_locations = [
                r"C:\Program Files (x86)\Steam\steamapps\common",
                r"C:\Program Files\Steam\steamapps\common",
                r"C:\Program Files (x86)\Epic Games",
                r"C:\Program Files\Epic Games",
                r"C:\Program Files (x86)\Origin Games",
                r"C:\Program Files\Origin Games",
                r"C:\Program Files (x86)",
                r"C:\Program Files",
                r"C:\Games"
            ]
            
            games_found = []
            
            for location in game_locations:
                if os.path.exists(location):
                    try:
                        for item in os.listdir(location):
                            item_path = os.path.join(location, item)
                            if os.path.isdir(item_path):
                                games_found.append(f"{item} - {item_path}")
                    except PermissionError:
                        self.results_text.insert(tk.END, f"❌ Access denied: {location}\n")
            
            if games_found:
                self.results_text.insert(tk.END, f"\n✅ Found {len(games_found)} potential games:\n")
                for game in games_found[:20]:  # Limit to first 20
                    self.results_text.insert(tk.END, f"  🎮 {game}\n")
                if len(games_found) > 20:
                    self.results_text.insert(tk.END, f"  ... and {len(games_found) - 20} more\n")
            else:
                self.results_text.insert(tk.END, "❌ No games found in common locations\n")
                
            self.scan_results['games'] = games_found
            
        threading.Thread(target=scan, daemon=True).start()
        
    def scan_cheat_tools(self):
        def scan():
            self.results_text.insert(tk.END, "\n🎯 SCANNING FOR CHEAT TOOLS...\n" + "="*50 + "\n")
            
            cheat_patterns = [
                "*cheat*", "*hack*", "*trainer*", "*mod*", "*injector*",
                "*aimbot*", "*wallhack*", "*speedhack*", "*engine*"
            ]
            
            search_locations = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Downloads"),
                os.path.expanduser("~\\Documents"),
                r"C:\Program Files",
                r"C:\Program Files (x86)"
            ]
            
            suspicious_files = []
            
            for location in search_locations:
                if os.path.exists(location):
                    try:
                        for pattern in cheat_patterns:
                            for file_path in glob.glob(os.path.join(location, "**", pattern), recursive=True):
                                if os.path.isfile(file_path):
                                    suspicious_files.append(file_path)
                    except PermissionError:
                        self.results_text.insert(tk.END, f"❌ Access denied: {location}\n")
            
            suspicious_files = list(set(suspicious_files))
            
            if suspicious_files:
                self.results_text.insert(tk.END, f"\n⚠️ Found {len(suspicious_files)} potentially suspicious files:\n")
                for file_path in suspicious_files[:15]:  # Limit display
                    self.results_text.insert(tk.END, f"  🎯 {os.path.basename(file_path)} - {file_path}\n")
                if len(suspicious_files) > 15:
                    self.results_text.insert(tk.END, f"  ... and {len(suspicious_files) - 15} more\n")
            else:
                self.results_text.insert(tk.END, "✅ No obvious cheat tools found\n")
                
            self.scan_results['cheat_tools'] = suspicious_files
            
        threading.Thread(target=scan, daemon=True).start()
        
    def scan_suspicious_files(self):
        def scan():
            self.results_text.insert(tk.END, "\n⚠️ SCANNING FOR SUSPICIOUS FILES...\n" + "="*50 + "\n")
            
            suspicious_extensions = ['.exe', '.dll', '.bat', '.cmd', '.scr', '.vbs']
            suspicious_keywords = ['crack', 'keygen', 'patch', 'loader', 'bypass']
            
            locations = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Downloads"),
                os.path.expanduser("~\\AppData\\Roaming"),
                os.path.expanduser("~\\AppData\\Local\\Temp")
            ]
            
            found_files = []
            
            for location in locations:
                if os.path.exists(location):
                    try:
                        for root, dirs, files in os.walk(location):
                            for file in files:
                                file_lower = file.lower()
                                file_path = os.path.join(root, file)
                                
                                # Check for suspicious patterns
                                if any(keyword in file_lower for keyword in suspicious_keywords):
                                    found_files.append(f"KEYWORD: {file} - {file_path}")
                                elif any(file_lower.endswith(ext) for ext in suspicious_extensions):
                                    if any(keyword in file_lower for keyword in ['temp', 'tmp', 'unknown']):
                                        found_files.append(f"TEMP: {file} - {file_path}")
                    except (PermissionError, OSError):
                        continue
            
            if found_files:
                self.results_text.insert(tk.END, f"\n⚠️ Found {len(found_files)} suspicious files:\n")
                for file_info in found_files[:20]:
                    self.results_text.insert(tk.END, f"  ⚠️ {file_info}\n")
            else:
                self.results_text.insert(tk.END, "✅ No obviously suspicious files found\n")
                
            self.scan_results['suspicious_files'] = found_files
            
        threading.Thread(target=scan, daemon=True).start()
        
    def custom_directory_scan(self):
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        if directory:
            def scan():
                self.results_text.insert(tk.END, f"\n📁 SCANNING DIRECTORY: {directory}\n" + "="*50 + "\n")
                
                try:
                    file_count = 0
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            file_count += 1
                            if file_count <= 50:  # Limit display
                                file_path = os.path.join(root, file)
                                file_size = os.path.getsize(file_path)
                                self.results_text.insert(tk.END, f"  📄 {file} ({file_size} bytes) - {file_path}\n")
                    
                    self.results_text.insert(tk.END, f"\n✅ Scan complete. Found {file_count} files total.\n")
                    
                except Exception as e:
                    self.results_text.insert(tk.END, f"❌ Error scanning directory: {str(e)}\n")
                    
            threading.Thread(target=scan, daemon=True).start()
        
    def load_processes(self):
        def get_processes():
            self.processes_text.delete(1.0, tk.END)
            self.processes_text.insert(tk.END, "Loading running processes...\n\n")
            
            try:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
                    try:
                        processes.append(proc.info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                # Sort by memory usage
                processes.sort(key=lambda x: x['memory_info'].rss if x['memory_info'] else 0, reverse=True)
                
                self.processes_text.delete(1.0, tk.END)
                self.processes_text.insert(tk.END, f"{'PID':<8} {'NAME':<25} {'MEMORY (MB)':<12} {'CPU %':<8}\n")
                self.processes_text.insert(tk.END, "="*60 + "\n")
                
                for proc in processes[:50]:  # Show top 50
                    memory_mb = proc['memory_info'].rss / (1024 * 1024) if proc['memory_info'] else 0
                    cpu_percent = proc['cpu_percent'] if proc['cpu_percent'] else 0
                    
                    line = f"{proc['pid']:<8} {proc['name'][:24]:<25} {memory_mb:<12.1f} {cpu_percent:<8.1f}\n"
                    self.processes_text.insert(tk.END, line)
                    
            except Exception as e:
                self.processes_text.insert(tk.END, f"Error loading processes: {str(e)}")
        
        threading.Thread(target=get_processes, daemon=True).start()
        
    def scan_startup_programs(self):
        def scan():
            self.registry_text.delete(1.0, tk.END)
            self.registry_text.insert(tk.END, "🚀 SCANNING STARTUP PROGRAMS...\n" + "="*50 + "\n")
            
            startup_locations = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            ]
            
            startup_programs = []
            
            for hive, key_path in startup_locations:
                try:
                    with winreg.OpenKey(hive, key_path) as key:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                startup_programs.append(f"{name}: {value}")
                                i += 1
                            except WindowsError:
                                break
                except WindowsError:
                    continue
            
            if startup_programs:
                self.registry_text.insert(tk.END, f"Found {len(startup_programs)} startup programs:\n\n")
                for program in startup_programs:
                    self.registry_text.insert(tk.END, f"🚀 {program}\n")
            else:
                self.registry_text.insert(tk.END, "No startup programs found in registry.\n")
                
            self.scan_results['startup_programs'] = startup_programs
            
        threading.Thread(target=scan, daemon=True).start()
        
    def scan_browser_history(self):
        def scan():
            self.results_text.insert(tk.END, "\n🌐 SCANNING BROWSER HISTORY...\n" + "="*50 + "\n")
            
            search_keywords = ['1377', 'aimbot', 'softaim', 'wallhack', 'esp', 'cheat', 'hack', 'mod', 'trainer']
            
            game_keywords = [
                'valorant', 'csgo', 'cs2', 'fortnite', 'apex', 'cod', 'warzone', 'pubg',
                'overwatch', 'rainbow six', 'tarkov', 'rust', 'gta', 'minecraft'
            ]
            
            all_keywords = search_keywords + game_keywords
            
            found_entries = []
            browsers_checked = []
            
            chrome_history = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History")
            if os.path.exists(chrome_history):
                browsers_checked.append("Chrome")
                try:
                    temp_history = os.path.join(os.getcwd(), "temp_chrome_history.db")
                    shutil.copy2(chrome_history, temp_history)
                    
                    conn = sqlite3.connect(temp_history)
                    cursor = conn.cursor()
                    
                    for keyword in all_keywords:
                        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls WHERE url LIKE ? OR title LIKE ?", 
                                     (f'%{keyword}%', f'%{keyword}%'))
                        results = cursor.fetchall()
                        
                        for url, title, visit_count, last_visit_time in results:
                            found_entries.append(f"CHROME: {keyword.upper()} - {title} | {url} (Visits: {visit_count})")
                    
                    conn.close()
                    os.remove(temp_history)
                    
                except Exception as e:
                    self.results_text.insert(tk.END, f"❌ Chrome history error: {str(e)}\n")
            
            firefox_profile_path = os.path.expanduser(r"~\AppData\Roaming\Mozilla\Firefox\Profiles")
            if os.path.exists(firefox_profile_path):
                try:
                    for profile in os.listdir(firefox_profile_path):
                        places_db = os.path.join(firefox_profile_path, profile, "places.sqlite")
                        if os.path.exists(places_db):
                            browsers_checked.append("Firefox")
                            try:
                                temp_places = os.path.join(os.getcwd(), "temp_firefox_places.db")
                                shutil.copy2(places_db, temp_places)
                                
                                conn = sqlite3.connect(temp_places)
                                cursor = conn.cursor()
                                
                                for keyword in all_keywords:
                                    cursor.execute("SELECT url, title, visit_count FROM moz_places WHERE url LIKE ? OR title LIKE ?", 
                                                 (f'%{keyword}%', f'%{keyword}%'))
                                    results = cursor.fetchall()
                                    
                                    for url, title, visit_count in results:
                                        found_entries.append(f"FIREFOX: {keyword.upper()} - {title} | {url} (Visits: {visit_count})")
                                
                                conn.close()
                                os.remove(temp_places)
                                break
                                
                            except Exception as e:
                                self.results_text.insert(tk.END, f"❌ Firefox history error: {str(e)}\n")
                except Exception:
                    pass
            
            edge_history = os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\History")
            if os.path.exists(edge_history):
                browsers_checked.append("Edge")
                try:
                    temp_edge_history = os.path.join(os.getcwd(), "temp_edge_history.db")
                    shutil.copy2(edge_history, temp_edge_history)
                    
                    conn = sqlite3.connect(temp_edge_history)
                    cursor = conn.cursor()
                    
                    for keyword in all_keywords:
                        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls WHERE url LIKE ? OR title LIKE ?", 
                                     (f'%{keyword}%', f'%{keyword}%'))
                        results = cursor.fetchall()
                        
                        for url, title, visit_count, last_visit_time in results:
                            found_entries.append(f"EDGE: {keyword.upper()} - {title} | {url} (Visits: {visit_count})")
                    
                    conn.close()
                    os.remove(temp_edge_history)
                    
                except Exception as e:
                    self.results_text.insert(tk.END, f"❌ Edge history error: {str(e)}\n")
            
            self.results_text.insert(tk.END, f"Browsers checked: {', '.join(browsers_checked)}\n\n")
            
            if found_entries:
                found_entries = list(set(found_entries))
                self.results_text.insert(tk.END, f"🚨 FOUND {len(found_entries)} SUSPICIOUS BROWSER ENTRIES:\n\n")
                
                for entry in found_entries:
                    self.results_text.insert(tk.END, f"  🌐 {entry}\n")
                    
                self.scan_results['browser_history'] = found_entries
            else:
                self.results_text.insert(tk.END, "✅ No suspicious browser history found\n")
                self.scan_results['browser_history'] = []
            
            self.results_text.insert(tk.END, f"\n{'='*50}\n")
            
        threading.Thread(target=scan, daemon=True).start()
    
    def export_all_results(self):
        """Export all scan results to check.txt in the same folder as the script"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, "check.txt")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("PC SYSTEM CHECK REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                
                f.write("SYSTEM INFORMATION:\n")
                f.write("-" * 40 + "\n")
                f.write(f"OS: {platform.system()} {platform.release()} ({platform.architecture()[0]})\n")
                f.write(f"Computer: {platform.node()}\n")
                f.write(f"Processor: {platform.processor()}\n")
                f.write(f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical\n")
                f.write(f"Memory: {round(psutil.virtual_memory().total / (1024**3), 2)} GB total\n")
                f.write(f"Memory Usage: {psutil.virtual_memory().percent}%\n\n")
                
                if hasattr(self, 'scan_results') and self.scan_results:
                    
                    if 'browser_history' in self.scan_results:
                        f.write("BROWSER HISTORY SCAN RESULTS:\n")
                        f.write("-" * 40 + "\n")
                        if self.scan_results['browser_history']:
                            f.write(f"FOUND {len(self.scan_results['browser_history'])} SUSPICIOUS ENTRIES:\n\n")
                            for entry in self.scan_results['browser_history']:
                                f.write(f"  🚨 {entry}\n")
                        else:
                            f.write("No suspicious browser history found.\n")
                        f.write("\n")
                    
                    if 'games' in self.scan_results:
                        f.write("GAMES FOUND:\n")
                        f.write("-" * 40 + "\n")
                        if self.scan_results['games']:
                            for game in self.scan_results['games']:
                                f.write(f"  🎮 {game}\n")
                        else:
                            f.write("No games found.\n")
                        f.write("\n")
                    
                    if 'cheat_tools' in self.scan_results:
                        f.write("CHEAT TOOLS & SUSPICIOUS FILES:\n")
                        f.write("-" * 40 + "\n")
                        if self.scan_results['cheat_tools']:
                            f.write(f"FOUND {len(self.scan_results['cheat_tools'])} SUSPICIOUS FILES:\n\n")
                            for tool in self.scan_results['cheat_tools']:
                                f.write(f"  🎯 {tool}\n")
                        else:
                            f.write("No cheat tools found.\n")
                        f.write("\n")
                    
                    if 'suspicious_files' in self.scan_results:
                        f.write("OTHER SUSPICIOUS FILES:\n")
                        f.write("-" * 40 + "\n")
                        if self.scan_results['suspicious_files']:
                            for file_info in self.scan_results['suspicious_files']:
                                f.write(f"  ⚠️ {file_info}\n")
                        else:
                            f.write("No additional suspicious files found.\n")
                        f.write("\n")
                    
                    if 'startup_programs' in self.scan_results:
                        f.write("STARTUP PROGRAMS:\n")
                        f.write("-" * 40 + "\n")
                        if self.scan_results['startup_programs']:
                            for program in self.scan_results['startup_programs']:
                                f.write(f"  🚀 {program}\n")
                        else:
                            f.write("No startup programs found in registry.\n")
                        f.write("\n")
                
                f.write("TOP RUNNING PROCESSES (by memory usage):\n")
                f.write("-" * 40 + "\n")
                try:
                    processes = []
                    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                        try:
                            processes.append(proc.info)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    processes.sort(key=lambda x: x['memory_info'].rss if x['memory_info'] else 0, reverse=True)
                    
                    for proc in processes[:20]:
                        memory_mb = proc['memory_info'].rss / (1024 * 1024) if proc['memory_info'] else 0
                        f.write(f"  {proc['name']} (PID: {proc['pid']}) - {memory_mb:.1f} MB\n")
                except Exception as e:
                    f.write(f"Error getting process list: {str(e)}\n")
                
                f.write("\n" + "="*80 + "\n")
                f.write("END OF REPORT\n")
                f.write("="*80 + "\n")
            
            messagebox.showinfo("Export Complete", 
                              f"All results saved to:\n{output_file}\n\n"
                              f"File size: {os.path.getsize(output_file)} bytes")
            
            self.results_text.insert(tk.END, f"\n✅ ALL RESULTS EXPORTED TO: {output_file}\n")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save check.txt:\n{str(e)}")
    
    def export_results(self):
        self.export_all_results()
        
    def start_system_monitor(self):
        def monitor():
            while True:
                try:
                    cpu_usage = psutil.cpu_percent()
                    memory_usage = psutil.virtual_memory().percent
                    
                    if cpu_usage > 80 or memory_usage > 90:
                        status = "🔴 High Usage"
                        color = self.colors['danger']
                    elif cpu_usage > 50 or memory_usage > 70:
                        status = "🟡 Medium Load"
                        color = self.colors['warning']
                    else:
                        status = "🟢 System Normal"
                        color = self.colors['accent']
                    
                    self.status_label.config(text=status, fg=color)
                    
                except Exception:
                    pass
                    
                time.sleep(5)
                
        threading.Thread(target=monitor, daemon=True).start()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PCCheckerApp()
    app.run()
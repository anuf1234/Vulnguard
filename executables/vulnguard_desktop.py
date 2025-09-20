#!/usr/bin/env python3
"""
VulnGuard Desktop Application
Cross-platform GUI application for vulnerability management
Built with tkinter for maximum compatibility
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import requests
import json
import threading
import queue
import os
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VulnGuardDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("VulnGuard - Vulnerability Management")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configuration
        self.server_url = os.getenv('VULNGUARD_SERVER', 'https://securityscan-15.preview.emergentagent.com')
        self.api_key = os.getenv('VULNGUARD_API_KEY', '')
        
        # Queue for thread communication
        self.queue = queue.Queue()
        
        # Data storage
        self.assets = []
        self.findings = []
        self.scans = []
        
        self.setup_ui()
        self.setup_menu()
        
        # Start periodic updates
        self.root.after(1000, self.process_queue)
        
    def setup_ui(self):
        """Setup the main UI"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Create sidebar
        self.setup_sidebar(main_frame)
        
        # Create main content area
        self.setup_content_area(main_frame)
        
        # Create status bar
        self.setup_status_bar(main_frame)
        
    def setup_menu(self):
        """Setup the application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Upload Scan File", command=self.upload_scan_file)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Start Network Scan", command=self.start_network_scan)
        tools_menu.add_command(label="Run Agent Scan", command=self.run_agent_scan)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings", command=self.show_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def setup_sidebar(self, parent):
        """Setup the sidebar navigation"""
        sidebar = ttk.Frame(parent, width=200)
        sidebar.grid(row=0, column=0, sticky=(tk.N, tk.S), padx=(0, 10))
        sidebar.grid_propagate(False)
        
        # VulnGuard logo/title
        title_frame = ttk.Frame(sidebar)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🛡️ VulnGuard", font=('Arial', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Desktop v2.0", font=('Arial', 8))
        subtitle_label.pack()
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("🖥️ Assets", self.show_assets),
            ("⚠️ Findings", self.show_findings),
            ("🔍 Scans", self.show_scans),
            ("🔧 Remediation", self.show_remediation),
            ("📋 Audit Trail", self.show_audit),
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(sidebar, text=text, command=command, width=25)
            btn.pack(fill=tk.X, pady=2)
        
        # Server status
        status_frame = ttk.LabelFrame(sidebar, text="Server Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.server_status_label = ttk.Label(status_frame, text="Checking...", foreground="orange")
        self.server_status_label.pack()
        
        # Check server status
        self.check_server_status()
        
    def setup_content_area(self, parent):
        """Setup the main content area"""
        self.content_frame = ttk.Frame(parent)
        self.content_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Show dashboard by default
        self.show_dashboard()
        
    def setup_status_bar(self, parent):
        """Setup the status bar"""
        self.status_frame = ttk.Frame(parent)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(self.status_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
        
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def set_status(self, message, show_progress=False):
        """Set status bar message"""
        self.status_label.config(text=message)
        if show_progress:
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_content()
        self.set_status("Loading dashboard...")
        
        # Create dashboard frame
        dashboard_frame = ttk.Frame(self.content_frame)
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(dashboard_frame, text="Security Dashboard", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Stats frame
        stats_frame = ttk.Frame(dashboard_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create stat cards
        self.create_stat_card(stats_frame, "Total Assets", "Loading...", 0, 0)
        self.create_stat_card(stats_frame, "Active Findings", "Loading...", 0, 1)
        self.create_stat_card(stats_frame, "Critical Issues", "Loading...", 0, 2)
        self.create_stat_card(stats_frame, "Pending Approvals", "Loading...", 0, 3)
        
        # Charts placeholder
        charts_frame = ttk.LabelFrame(dashboard_frame, text="Security Metrics", padding=10)
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        chart_label = ttk.Label(charts_frame, text="📊 Charts and visualizations would be displayed here\n(Requires additional libraries like matplotlib)", 
                               font=('Arial', 12), anchor=tk.CENTER)
        chart_label.pack(expand=True)
        
        # Load dashboard data
        threading.Thread(target=self.load_dashboard_data, daemon=True).start()
        
    def create_stat_card(self, parent, title, value, row, col):
        """Create a statistics card"""
        card_frame = ttk.LabelFrame(parent, text=title, padding=10)
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky=(tk.W, tk.E))
        parent.columnconfigure(col, weight=1)
        
        value_label = ttk.Label(card_frame, text=str(value), font=('Arial', 16, 'bold'))
        value_label.pack()
        
        return value_label
    
    def show_assets(self):
        """Show assets view"""
        self.clear_content()
        self.set_status("Loading assets...")
        
        # Create assets frame
        assets_frame = ttk.Frame(self.content_frame)
        assets_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title and controls
        header_frame = ttk.Frame(assets_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Asset Inventory", font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        add_asset_btn = ttk.Button(header_frame, text="Add Asset", command=self.add_asset_dialog)
        add_asset_btn.pack(side=tk.RIGHT)
        
        refresh_btn = ttk.Button(header_frame, text="Refresh", command=lambda: threading.Thread(target=self.load_assets, daemon=True).start())
        refresh_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Assets treeview
        columns = ('Hostname', 'IP Address', 'Type', 'Environment', 'Criticality', 'Owner')
        self.assets_tree = ttk.Treeview(assets_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.assets_tree.heading(col, text=col)
            self.assets_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(assets_frame, orient=tk.VERTICAL, command=self.assets_tree.yview)
        self.assets_tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(assets_frame, orient=tk.HORIZONTAL, command=self.assets_tree.xview)
        self.assets_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.assets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load assets data
        threading.Thread(target=self.load_assets, daemon=True).start()
    
    def show_findings(self):
        """Show findings view"""
        self.clear_content()
        self.set_status("Loading findings...")
        
        # Create findings frame
        findings_frame = ttk.Frame(self.content_frame)
        findings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title and controls
        header_frame = ttk.Frame(findings_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Security Findings", font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Filters
        filter_frame = ttk.Frame(header_frame)
        filter_frame.pack(side=tk.RIGHT)
        
        ttk.Label(filter_frame, text="Severity:").pack(side=tk.LEFT, padx=(0, 5))
        self.severity_filter = ttk.Combobox(filter_frame, values=['All', 'Critical', 'High', 'Medium', 'Low'], 
                                           state='readonly', width=10)
        self.severity_filter.set('All')
        self.severity_filter.pack(side=tk.LEFT, padx=(0, 10))
        
        filter_btn = ttk.Button(filter_frame, text="Filter", command=self.filter_findings)
        filter_btn.pack(side=tk.LEFT)
        
        # Findings treeview
        columns = ('Title', 'Severity', 'Type', 'Asset', 'CVE IDs', 'First Seen')
        self.findings_tree = ttk.Treeview(findings_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.findings_tree.heading(col, text=col)
            if col == 'Title':
                self.findings_tree.column(col, width=300)
            else:
                self.findings_tree.column(col, width=120)
        
        # Double-click binding
        self.findings_tree.bind('<Double-1>', self.show_finding_details)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(findings_frame, orient=tk.VERTICAL, command=self.findings_tree.yview)
        self.findings_tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.findings_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load findings data
        threading.Thread(target=self.load_findings, daemon=True).start()
    
    def show_scans(self):
        """Show scans view"""
        self.clear_content()
        self.set_status("Loading scans...")
        
        # Create scans frame
        scans_frame = ttk.Frame(self.content_frame)
        scans_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title and controls
        header_frame = ttk.Frame(scans_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Vulnerability Scans", font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        start_scan_btn = ttk.Button(header_frame, text="Start Network Scan", command=self.start_network_scan)
        start_scan_btn.pack(side=tk.RIGHT)
        
        upload_btn = ttk.Button(header_frame, text="Upload Scan File", command=self.upload_scan_file)
        upload_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Scan history (placeholder)
        history_frame = ttk.LabelFrame(scans_frame, text="Scan History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        history_text = scrolledtext.ScrolledText(history_frame, height=20, state='disabled')
        history_text.pack(fill=tk.BOTH, expand=True)
        
        self.scan_history_text = history_text
        
        # Load recent scans
        self.update_scan_history("No recent scans available.")
    
    def show_remediation(self):
        """Show remediation view"""
        self.clear_content()
        
        # Create remediation frame
        remediation_frame = ttk.Frame(self.content_frame)
        remediation_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(remediation_frame, text="Ansible Remediation", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Remediation options
        options_frame = ttk.LabelFrame(remediation_frame, text="Remediation Options", padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(options_frame, text="Select a finding to generate Ansible remediation playbooks", 
                 font=('Arial', 12)).pack()
        
        # Playbook display area
        playbook_frame = ttk.LabelFrame(remediation_frame, text="Generated Playbooks", padding=10)
        playbook_frame.pack(fill=tk.BOTH, expand=True)
        
        self.playbook_text = scrolledtext.ScrolledText(playbook_frame, height=20, font=('Courier', 10))
        self.playbook_text.pack(fill=tk.BOTH, expand=True)
        
        # Sample playbook
        sample_playbook = """---
- name: VulnGuard Security Remediation
  hosts: all
  become: yes
  
  tasks:
    - name: Update system packages
      package:
        name: '*'
        state: latest
      
    - name: Configure SSH security
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^PermitRootLogin'
        line: 'PermitRootLogin no'
      notify: restart ssh
      
  handlers:
    - name: restart ssh
      service:
        name: sshd
        state: restarted
"""
        self.playbook_text.insert('1.0', sample_playbook)
        self.playbook_text.config(state='disabled')
    
    def show_audit(self):
        """Show audit trail view"""
        self.clear_content()
        
        # Create audit frame  
        audit_frame = ttk.Frame(self.content_frame)
        audit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(audit_frame, text="Audit Trail", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Audit log display
        log_frame = ttk.LabelFrame(audit_frame, text="Security Operations Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columns for audit log
        columns = ('Timestamp', 'User', 'Action', 'Resource', 'Details')
        self.audit_tree = ttk.Treeview(log_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.audit_tree.heading(col, text=col)
            self.audit_tree.column(col, width=150)
        
        self.audit_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load audit data
        threading.Thread(target=self.load_audit_logs, daemon=True).start()
    
    def check_server_status(self):
        """Check VulnGuard server connectivity"""
        def check():
            try:
                response = requests.get(f"{self.server_url}/api/", timeout=5)
                if response.status_code == 200:
                    self.queue.put(('server_status', 'Connected', 'green'))
                else:
                    self.queue.put(('server_status', 'Error', 'red'))
            except:
                self.queue.put(('server_status', 'Offline', 'red'))
        
        threading.Thread(target=check, daemon=True).start()
    
    def load_dashboard_data(self):
        """Load dashboard statistics"""
        try:
            response = requests.get(f"{self.server_url}/api/dashboard/stats", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.queue.put(('dashboard_data', data))
            else:
                self.queue.put(('dashboard_error', 'Failed to load dashboard data'))
        except Exception as e:
            self.queue.put(('dashboard_error', str(e)))
    
    def load_assets(self):
        """Load assets data"""
        try:
            response = requests.get(f"{self.server_url}/api/assets", timeout=10)
            if response.status_code == 200:
                assets = response.json()
                self.queue.put(('assets_data', assets))
            else:
                self.queue.put(('assets_error', 'Failed to load assets'))
        except Exception as e:
            self.queue.put(('assets_error', str(e)))
    
    def load_findings(self):
        """Load findings data"""
        try:
            response = requests.get(f"{self.server_url}/api/findings", timeout=10)
            if response.status_code == 200:
                findings = response.json()
                self.queue.put(('findings_data', findings))
            else:
                self.queue.put(('findings_error', 'Failed to load findings'))
        except Exception as e:
            self.queue.put(('findings_error', str(e)))
    
    def load_audit_logs(self):
        """Load audit logs"""
        try:
            response = requests.get(f"{self.server_url}/api/audit-logs?limit=100", timeout=10)
            if response.status_code == 200:
                logs = response.json()
                self.queue.put(('audit_data', logs))
            else:
                self.queue.put(('audit_error', 'Failed to load audit logs'))
        except Exception as e:
            self.queue.put(('audit_error', str(e)))
    
    def process_queue(self):
        """Process messages from background threads"""
        try:
            while True:
                message_type, data, *extra = self.queue.get_nowait()
                
                if message_type == 'server_status':
                    color = extra[0] if extra else 'black'
                    self.server_status_label.config(text=data, foreground=color)
                
                elif message_type == 'dashboard_data':
                    self.update_dashboard(data)
                
                elif message_type == 'assets_data':
                    self.update_assets_tree(data)
                
                elif message_type == 'findings_data':
                    self.update_findings_tree(data)
                
                elif message_type == 'audit_data':
                    self.update_audit_tree(data)
                
                elif message_type.endswith('_error'):
                    self.set_status(f"Error: {data}")
                    messagebox.showerror("Error", data)
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(1000, self.process_queue)
    
    def update_dashboard(self, data):
        """Update dashboard with loaded data"""
        # This would update the dashboard widgets with real data
        self.set_status("Dashboard loaded successfully")
    
    def update_assets_tree(self, assets):
        """Update assets treeview"""
        # Clear existing items
        for item in self.assets_tree.get_children():
            self.assets_tree.delete(item)
        
        # Add new items
        for asset in assets:
            self.assets_tree.insert('', 'end', values=(
                asset.get('hostname', ''),
                asset.get('ip_address', ''),
                asset.get('asset_type', ''),
                asset.get('environment', ''),
                asset.get('criticality', ''),
                asset.get('owner', '')
            ))
        
        self.set_status(f"Loaded {len(assets)} assets")
    
    def update_findings_tree(self, findings):
        """Update findings treeview"""
        # Clear existing items
        for item in self.findings_tree.get_children():
            self.findings_tree.delete(item)
        
        # Add new items
        for finding in findings:
            cve_ids = ', '.join(finding.get('cve_ids', [])[:2])  # Show first 2 CVEs
            first_seen = finding.get('first_seen', '')
            if first_seen:
                try:
                    first_seen = datetime.fromisoformat(first_seen.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                except:
                    pass
            
            self.findings_tree.insert('', 'end', values=(
                finding.get('title', '')[:50],  # Truncate long titles
                finding.get('severity', '').upper(),
                finding.get('finding_type', ''),
                finding.get('asset_id', '')[:10],  # Show first 10 chars of asset ID
                cve_ids,
                first_seen
            ))
        
        self.set_status(f"Loaded {len(findings)} findings")
    
    def update_audit_tree(self, logs):
        """Update audit trail treeview"""
        # Clear existing items
        for item in self.audit_tree.get_children():
            self.audit_tree.delete(item)
        
        # Add new items
        for log in logs:
            timestamp = log.get('timestamp', '')
            if timestamp:
                try:
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            
            self.audit_tree.insert('', 'end', values=(
                timestamp,
                log.get('user_id', ''),
                log.get('action', ''),
                log.get('resource_type', ''),
                str(log.get('details', {}))[:50]  # Truncate details
            ))
        
        self.set_status(f"Loaded {len(logs)} audit entries")
    
    def add_asset_dialog(self):
        """Show add asset dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Asset")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Form fields
        ttk.Label(dialog, text="Asset Details", font=('Arial', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        fields = {}
        
        # Hostname
        ttk.Label(form_frame, text="Hostname:").grid(row=0, column=0, sticky=tk.W, pady=5)
        fields['hostname'] = ttk.Entry(form_frame, width=30)
        fields['hostname'].grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # IP Address
        ttk.Label(form_frame, text="IP Address:").grid(row=1, column=0, sticky=tk.W, pady=5)
        fields['ip_address'] = ttk.Entry(form_frame, width=30)
        fields['ip_address'].grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Asset Type
        ttk.Label(form_frame, text="Asset Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        fields['asset_type'] = ttk.Combobox(form_frame, values=['server', 'workstation', 'network_device', 'database'], 
                                           state='readonly', width=28)
        fields['asset_type'].set('server')
        fields['asset_type'].grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Environment
        ttk.Label(form_frame, text="Environment:").grid(row=3, column=0, sticky=tk.W, pady=5)
        fields['environment'] = ttk.Combobox(form_frame, values=['production', 'staging', 'development'], 
                                           state='readonly', width=28)
        fields['environment'].set('production')
        fields['environment'].grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Owner
        ttk.Label(form_frame, text="Owner:").grid(row=4, column=0, sticky=tk.W, pady=5)
        fields['owner'] = ttk.Entry(form_frame, width=30)
        fields['owner'].grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def create_asset():
            # Validate required fields
            if not fields['hostname'].get().strip():
                messagebox.showerror("Error", "Hostname is required")
                return
            
            # Prepare asset data
            asset_data = {
                'hostname': fields['hostname'].get().strip(),
                'ip_address': fields['ip_address'].get().strip() or None,
                'asset_type': fields['asset_type'].get(),
                'environment': fields['environment'].get(),
                'owner': fields['owner'].get().strip() or None,
                'criticality': 3  # Default criticality
            }
            
            # Remove None values
            asset_data = {k: v for k, v in asset_data.items() if v is not None}
            
            try:
                response = requests.post(f"{self.server_url}/api/assets", json=asset_data, timeout=10)
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Asset created successfully")
                    dialog.destroy()
                    # Refresh assets view if currently displayed
                    threading.Thread(target=self.load_assets, daemon=True).start()
                else:
                    messagebox.showerror("Error", f"Failed to create asset: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create asset: {str(e)}")
        
        ttk.Button(button_frame, text="Create", command=create_asset).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=(0, 10))
    
    def start_network_scan(self):
        """Show network scan dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Start Network Scan")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        ttk.Label(dialog, text="Network Vulnerability Scan", font=('Arial', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scan name
        ttk.Label(form_frame, text="Scan Name:").pack(anchor=tk.W, pady=(0, 5))
        scan_name_entry = ttk.Entry(form_frame, width=50)
        scan_name_entry.pack(fill=tk.X, pady=(0, 10))
        scan_name_entry.insert(0, f"Desktop Scan {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Targets
        ttk.Label(form_frame, text="Targets (comma-separated):").pack(anchor=tk.W, pady=(0, 5))
        targets_text = tk.Text(form_frame, height=5, width=50)
        targets_text.pack(fill=tk.X, pady=(0, 10))
        targets_text.insert('1.0', '192.168.1.0/24, 10.0.0.1-10.0.0.50')
        
        # Options
        options_frame = ttk.Frame(form_frame)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        include_misconfigs = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include misconfiguration detection", 
                       variable=include_misconfigs).pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def start_scan():
            targets = [t.strip() for t in targets_text.get('1.0', tk.END).strip().split(',')]
            scan_data = {
                'targets': targets,
                'scan_name': scan_name_entry.get(),
                'include_misconfigs': include_misconfigs.get()
            }
            
            try:
                response = requests.post(f"{self.server_url}/api/scan/network", json=scan_data, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    messagebox.showinfo("Success", 
                        f"Network scan started successfully!\n"
                        f"Scan ID: {result.get('scan_id')}\n"
                        f"Findings: {result.get('findings_count', 0)}\n"
                        f"Misconfigurations: {result.get('misconfigurations', 0)}")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to start scan: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start scan: {str(e)}")
        
        ttk.Button(button_frame, text="Start Scan", command=start_scan).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=(0, 10))
    
    def upload_scan_file(self):
        """Upload scan file"""
        file_path = filedialog.askopenfilename(
            title="Select Scan File",
            filetypes=[
                ("JSON files", "*.json"),
                ("XML files", "*.xml"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # For now, just show a message
            messagebox.showinfo("File Selected", f"Selected file: {file_path}\n\nFile upload functionality would process this file.")
    
    def filter_findings(self):
        """Filter findings based on selected criteria"""
        # This would filter the findings tree based on selected criteria
        messagebox.showinfo("Filter", "Filtering functionality would be implemented here")
    
    def show_finding_details(self, event):
        """Show detailed information about selected finding"""
        selection = self.findings_tree.selection()
        if selection:
            item = self.findings_tree.item(selection[0])
            values = item['values']
            messagebox.showinfo("Finding Details", 
                f"Title: {values[0]}\n"
                f"Severity: {values[1]}\n"
                f"Type: {values[2]}\n"
                f"Asset: {values[3]}\n"
                f"CVE IDs: {values[4]}")
    
    def run_agent_scan(self):
        """Run local agent scan"""
        messagebox.showinfo("Agent Scan", "This would run the VulnGuard agent on the local machine")
    
    def export_report(self):
        """Export security report"""
        file_path = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("PDF files", "*.pdf"),
                ("CSV files", "*.csv")
            ]
        )
        
        if file_path:
            messagebox.showinfo("Export", f"Report would be exported to: {file_path}")
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="VulnGuard Settings", font=('Arial', 14, 'bold')).pack(pady=10)
        
        settings_frame = ttk.Frame(dialog)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Server URL
        ttk.Label(settings_frame, text="Server URL:").pack(anchor=tk.W, pady=(0, 5))
        server_entry = ttk.Entry(settings_frame, width=50)
        server_entry.pack(fill=tk.X, pady=(0, 10))
        server_entry.insert(0, self.server_url)
        
        # API Key
        ttk.Label(settings_frame, text="API Key:").pack(anchor=tk.W, pady=(0, 5))
        api_key_entry = ttk.Entry(settings_frame, width=50, show="*")
        api_key_entry.pack(fill=tk.X, pady=(0, 10))
        api_key_entry.insert(0, self.api_key)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def save_settings():
            self.server_url = server_entry.get()
            self.api_key = api_key_entry.get()
            messagebox.showinfo("Settings", "Settings saved successfully")
            dialog.destroy()
            # Recheck server status
            self.check_server_status()
        
        ttk.Button(button_frame, text="Save", command=save_settings).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=(0, 10))
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About VulnGuard", 
            "VulnGuard Desktop v2.0\n\n"
            "Comprehensive vulnerability management platform\n"
            "with AI-powered analysis and Ansible remediation\n\n"
            "Features:\n"
            "• Asset inventory management\n"
            "• Vulnerability and misconfiguration scanning\n"
            "• Cross-host vulnerability analysis\n"
            "• AI-powered remediation with Ansible\n"
            "• Change management workflows\n"
            "• Comprehensive audit trails\n\n"
            "Built with Python and tkinter")
    
    def update_scan_history(self, message):
        """Update scan history display"""
        self.scan_history_text.config(state='normal')
        self.scan_history_text.insert('1.0', f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        self.scan_history_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = VulnGuardDesktop(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application terminated by user")

if __name__ == '__main__':
    main()
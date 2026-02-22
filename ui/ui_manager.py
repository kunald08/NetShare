"""
UIManager — Production-Grade UI for NetShare
Clean, professional light theme. No heavy dependencies.
Author: kunald08
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime


# ─── Palette ──────────────────────────────────────────────────────────────────
BG         = "#ffffff"
BG_ALT     = "#f9fafb"
BG_SECTION = "#f3f4f6"
BG_CARD    = "#eff6ff"          # soft blue tint for stat cards
PRIMARY    = "#2563eb"
PRIMARY_H  = "#1d4ed8"
SUCCESS    = "#16a34a"
SUCCESS_H  = "#15803d"
DANGER     = "#dc2626"
DANGER_H   = "#b91c1c"
MUTED      = "#64748b"
TEXT       = "#111827"
BORDER     = "#e5e7eb"
CARD_BDR   = "#bfdbfe"          # blue-tinted card border
LOG_BG     = "#1e293b"
LOG_FG     = "#e2e8f0"

FONT       = "Helvetica"


class UIManager:
    def __init__(self, app):
        self.app = app
        self._apply_theme()

    # ──────────────────────────────────────────────────────────────────────────
    # Theme
    # ──────────────────────────────────────────────────────────────────────────
    def _apply_theme(self):
        style = ttk.Style()
        style.theme_use("clam")

        self.app.root.configure(bg=BG)

        # ── Frames ──
        style.configure("TFrame",       background=BG)
        style.configure("Section.TFrame", background=BG_SECTION,
                        relief="flat")

        # ── Labels ──
        style.configure("TLabel",       background=BG, foreground=TEXT,
                        font=(FONT, 10))
        style.configure("H1.TLabel",    background=BG, foreground=TEXT,
                        font=(FONT, 18, "bold"))
        style.configure("H2.TLabel",    background=BG, foreground=TEXT,
                        font=(FONT, 11, "bold"))
        style.configure("Muted.TLabel", background=BG, foreground=MUTED,
                        font=(FONT, 9))
        style.configure("Primary.TLabel", background=BG,
                        foreground=PRIMARY, font=(FONT, 10, "bold"))
        style.configure("Success.TLabel", background=BG,
                        foreground=SUCCESS, font=(FONT, 10, "bold"))
        style.configure("Danger.TLabel",  background=BG,
                        foreground=DANGER,  font=(FONT, 10, "bold"))

        # ── LabelFrame ──
        style.configure("TLabelframe",       background=BG,
                        bordercolor=BORDER, relief="groove")
        style.configure("TLabelframe.Label", background=BG,
                        foreground=PRIMARY,  font=(FONT, 10, "bold"))

        # ── Notebook ──
        style.configure("TNotebook",     background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_SECTION,
                        foreground=MUTED,  padding=[18, 9],
                        font=(FONT, 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", PRIMARY), ("active", BG)],
                  foreground=[("selected", "white"), ("active", TEXT)])

        # ── Button ──
        style.configure("TButton",       background=PRIMARY,  foreground="white",
                        padding=[14, 7], font=(FONT, 10, "bold"),
                        borderwidth=0, focuscolor="none")
        style.map("TButton",
                  background=[("active", PRIMARY_H), ("pressed", PRIMARY_H),
                               ("disabled", "#9ca3af")])

        style.configure("Success.TButton", background=SUCCESS, foreground="white",
                        padding=[14, 7], font=(FONT, 10, "bold"))
        style.map("Success.TButton",
                  background=[("active", SUCCESS_H), ("pressed", SUCCESS_H),
                               ("disabled", "#9ca3af")])

        style.configure("Danger.TButton",  background=DANGER,  foreground="white",
                        padding=[14, 7], font=(FONT, 10, "bold"))
        style.map("Danger.TButton",
                  background=[("active", DANGER_H), ("pressed", DANGER_H),
                               ("disabled", "#9ca3af")])

        style.configure("Ghost.TButton",   background=BG_SECTION, foreground=TEXT,
                        padding=[10, 6],  font=(FONT, 9, "bold"),
                        borderwidth=1, relief="solid")
        style.map("Ghost.TButton",
                  background=[("active", BORDER), ("pressed", BORDER)],
                  relief=[("active", "solid"), ("pressed", "solid")])

        # ── Entry ──
        style.configure("TEntry", fieldbackground="white", foreground=TEXT,
                        padding=[8, 5], relief="flat",
                        insertcolor=TEXT)

        # ── Treeview ──
        style.configure("Treeview",
                        background="white", foreground=TEXT,
                        fieldbackground="white", rowheight=32,
                        font=(FONT, 10), borderwidth=0)
        style.configure("Treeview.Heading",
                        background=BG_SECTION, foreground=PRIMARY,
                        font=(FONT, 10, "bold"), padding=[8, 6],
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", PRIMARY)],
                  foreground=[("selected", "white")])

        # ── Progressbar ──
        style.configure("TProgressbar", background=PRIMARY,
                        troughcolor=BG_SECTION, borderwidth=0, thickness=14)
        style.configure("green.Horizontal.TProgressbar",
                        background=SUCCESS, troughcolor=BG_SECTION,
                        borderwidth=0, thickness=14)

        # ── Checkbutton ──
        style.configure("TCheckbutton", background=BG, foreground=TEXT,
                        font=(FONT, 10))
        style.map("TCheckbutton", background=[("active", BG)])

        # ── Spinbox ──
        style.configure("TSpinbox", fieldbackground="white", foreground=TEXT,
                        padding=[8, 5])

        # ── Separator ──
        style.configure("TSeparator", background=BORDER)

        # ── Scrollbar ──
        style.configure("TScrollbar", background=BG_SECTION,
                        troughcolor=BG, borderwidth=0, arrowsize=13)
        style.map("TScrollbar", background=[("active", "#d1d5db")])

    # ──────────────────────────────────────────────────────────────────────────
    # Root UI
    # ──────────────────────────────────────────────────────────────────────────
    def setup_main_ui(self):
        root = self.app.root

        outer = ttk.Frame(root, padding=0)
        outer.pack(fill="both", expand=True)

        # ── Top bar ──
        self._build_topbar(outer)

        # ── Separator ──
        ttk.Separator(outer).pack(fill="x")

        # ── Notebook ──
        self.app.notebook = ttk.Notebook(outer)
        self.app.notebook.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_send_tab()
        self._build_receive_tab()
        self._build_monitor_tab()
        self._build_settings_tab()
        self._build_history_tab()

        # ── Status bar ──
        self._build_statusbar(outer)

    # ── Top bar ──────────────────────────────────────────────────────────────
    def _build_topbar(self, parent):
        bar = ttk.Frame(parent, padding=(0, 0, 0, 0))
        bar.pack(fill="x")

        # solid blue left accent strip
        accent = tk.Frame(bar, width=5, bg=PRIMARY)
        accent.pack(side="left", fill="y")

        inner = ttk.Frame(bar, padding=(16, 12, 20, 12))
        inner.pack(side="left", fill="both", expand=True)

        ttk.Label(inner, text="NetShare", style="H1.TLabel").pack(side="left")
        ttk.Label(inner, text="High-speed LAN file sharing",
                  style="Muted.TLabel").pack(side="left", padx=(14, 0))

        right = ttk.Frame(inner)
        right.pack(side="right")
        ttk.Label(right, text="v1.0  •  by kunald08",
                  style="Muted.TLabel").pack(anchor="e")

    # ── Status bar ───────────────────────────────────────────────────────────
    def _build_statusbar(self, parent):
        ttk.Separator(parent).pack(fill="x")
        bar = ttk.Frame(parent, padding=(20, 6, 20, 6))
        bar.pack(fill="x")

        self.app.status_label = ttk.Label(bar, text="Ready", style="Muted.TLabel")
        self.app.status_label.pack(side="left")

        from network.transfer_manager import TransferManager
        ip = TransferManager(self.app).get_local_ip()
        self.app.network_label = ttk.Label(bar, text=f"Local IP: {ip}",
                                           style="Muted.TLabel")
        self.app.network_label.pack(side="right")

    # ──────────────────────────────────────────────────────────────────────────
    # SEND TAB
    # ──────────────────────────────────────────────────────────────────────────
    def _build_send_tab(self):
        tab = ttk.Frame(self.app.notebook, padding=(20, 15, 20, 15))
        self.app.notebook.add(tab, text="  Send  ")

        # ── Left / Right panes ──
        panes = ttk.Frame(tab)
        panes.pack(fill="both", expand=True)
        panes.columnconfigure(0, weight=3)
        panes.columnconfigure(1, weight=2)
        panes.rowconfigure(0, weight=1)

        left  = ttk.Frame(panes)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right = ttk.Frame(panes)
        right.grid(row=0, column=1, sticky="nsew")

        self._section_discovery(left)
        self._section_files(left)
        self._section_send_control(right)

    # ── Discovery ────────────────────────────────────────────────────────────
    def _section_discovery(self, parent):
        frame = ttk.LabelFrame(parent, text="Connection", padding=(12, 10))
        frame.pack(fill="x", pady=(0, 12))

        # Header row
        hdr = ttk.Frame(frame)
        hdr.pack(fill="x", pady=(0, 8))
        ttk.Label(hdr, text="Available receivers on your network",
                  style="Muted.TLabel").pack(side="left")
        ttk.Button(hdr, text="Refresh", command=self.app.discover_hosts,
                   style="Ghost.TButton").pack(side="right")

        # Tree
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        cols = ("Name", "IP Address", "Status", "Last Seen")
        self.app.host_tree = ttk.Treeview(tree_frame, columns=cols,
                                           show="headings", height=4)
        _col_setup = [
            ("Name",       "w", 150),
            ("IP Address", "w", 140),
            ("Status",     "center", 90),
            ("Last Seen",  "center", 90),
        ]
        for col, anchor, w in _col_setup:
            self.app.host_tree.heading(col, text=col)
            self.app.host_tree.column(col, width=w, minwidth=60,
                                      anchor=anchor, stretch=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self.app.host_tree.yview)
        self.app.host_tree.configure(yscrollcommand=vsb.set)
        self.app.host_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self._auto_resize_columns(self.app.host_tree,
            {"Name": 3, "IP Address": 3, "Status": 2, "Last Seen": 2})

        # Trigger on tab switch so columns fill correctly
        self.app.notebook.bind("<<NotebookTabChanged>>",
            lambda e: self.app.root.after(50, lambda: self._force_resize(self.app.host_tree)))

        # Manual row
        manual = ttk.Frame(frame)
        manual.pack(fill="x", pady=(10, 0))

        ttk.Label(manual, text="Or enter IP manually:", style="Muted.TLabel").pack(
            side="left")
        self.app.manual_host_entry = ttk.Entry(manual, width=16)
        self.app.manual_host_entry.pack(side="left", padx=(8, 16))
        ttk.Label(manual, text="Port:").pack(side="left")
        self.app.sender_port_entry = ttk.Entry(manual, width=7)
        self.app.sender_port_entry.insert(0, "12345")
        self.app.sender_port_entry.pack(side="left", padx=(6, 0))

    # ── File selection ────────────────────────────────────────────────────────
    def _section_files(self, parent):
        frame = ttk.LabelFrame(parent, text="Selected Files", padding=(12, 10))
        frame.pack(fill="both", expand=True)

        # Toolbar
        tb = ttk.Frame(frame)
        tb.pack(fill="x", pady=(0, 8))
        ttk.Button(tb, text="Add Files",  command=self.app.add_files).pack(side="left")
        ttk.Button(tb, text="Add Folder", command=self.app.add_folder,
                   style="Ghost.TButton").pack(side="left", padx=(8, 0))
        ttk.Button(tb, text="Remove",     command=self.app.remove_selected_files,
                   style="Danger.TButton").pack(side="left", padx=(8, 0))
        ttk.Button(tb, text="Clear All",  command=self.app.clear_files,
                   style="Ghost.TButton").pack(side="left", padx=(8, 0))

        # Tree
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        cols = ("Name", "Size", "Type", "Path")
        self.app.files_tree = ttk.Treeview(tree_frame, columns=cols,
                                            show="headings", height=7)
        _col_setup = [
            ("Name",  "w",      160),
            ("Size",  "e",       70),
            ("Type",  "center",  70),
            ("Path",  "w",      250),
        ]
        for col, anchor, w in _col_setup:
            self.app.files_tree.heading(col, text=col)
            self.app.files_tree.column(col, width=w, minwidth=50,
                                       anchor=anchor, stretch=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self.app.files_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal",
                            command=self.app.files_tree.xview)
        self.app.files_tree.configure(yscrollcommand=vsb.set,
                                      xscrollcommand=hsb.set)
        self.app.files_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self._auto_resize_columns(self.app.files_tree,
            {"Name": 3, "Size": 1, "Type": 1, "Path": 5})

        self._setup_files_context_menu()

        # Summary label
        self.app.file_summary = ttk.Label(frame, text="No files selected",
                                          style="Muted.TLabel")
        self.app.file_summary.pack(anchor="w", pady=(8, 0))

    def _setup_files_context_menu(self):
        m = tk.Menu(self.app.root, tearoff=0)
        m.add_command(label="Remove Selected",
                      command=self.app.remove_selected_files)
        m.add_separator()
        m.add_command(label="Clear All", command=self.app.clear_files)
        self.app.files_context_menu = m

        self.app.files_tree.bind("<Button-3>", self.app.show_files_context_menu)
        self.app.files_tree.bind("<Delete>",   self.app.on_delete_key)
        self.app.files_tree.bind("<Double-1>", self.app.on_file_double_click)

    # ── Send control panel ────────────────────────────────────────────────────
    def _section_send_control(self, parent):
        # Options
        opt = ttk.LabelFrame(parent, text="Options", padding=(12, 10))
        opt.pack(fill="x", pady=(0, 12))
        ttk.Checkbutton(opt, text="Compress files",
                        variable=self.app.compression_enabled).pack(anchor="w")
        ttk.Checkbutton(opt, text="Encrypt transfer",
                        variable=self.app.encryption_enabled).pack(anchor="w", pady=(6, 0))

        # Transfer
        ctrl = ttk.LabelFrame(parent, text="Transfer", padding=(12, 10))
        ctrl.pack(fill="both", expand=True)

        # Progress
        prog_hdr = ttk.Frame(ctrl)
        prog_hdr.pack(fill="x", pady=(0, 4))
        self.app.send_status = ttk.Label(prog_hdr, text="Ready to send",
                                         style="Muted.TLabel")
        self.app.send_status.pack(side="left")
        self.app.send_speed = ttk.Label(prog_hdr, text="", style="Muted.TLabel")
        self.app.send_speed.pack(side="right")

        self.app.send_progress = ttk.Progressbar(
            ctrl, mode="determinate",
            style="green.Horizontal.TProgressbar")
        self.app.send_progress.pack(fill="x", pady=(0, 12))

        # Buttons — full-width primary action
        self.app.send_button = ttk.Button(
            ctrl, text="\u25b6  Send Files",
            command=self.app.send_files, style="Success.TButton")
        self.app.send_button.pack(fill="x", pady=(0, 6))
        self.app.cancel_send_button = ttk.Button(
            ctrl, text="Cancel",
            command=self.app.cancel_send,
            state="disabled", style="Danger.TButton")
        self.app.cancel_send_button.pack(fill="x", pady=(0, 12))

        # Log
        self._build_log(ctrl, "send_log", label="Transfer Log")

    # ──────────────────────────────────────────────────────────────────────────
    # RECEIVE TAB
    # ──────────────────────────────────────────────────────────────────────────
    def _build_receive_tab(self):
        tab = ttk.Frame(self.app.notebook, padding=(20, 15, 20, 15))
        self.app.notebook.add(tab, text="  Receive  ")

        panes = ttk.Frame(tab)
        panes.pack(fill="both", expand=True)
        panes.columnconfigure(0, weight=2)
        panes.columnconfigure(1, weight=3)
        panes.rowconfigure(0, weight=1)

        left  = ttk.Frame(panes)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right = ttk.Frame(panes)
        right.grid(row=0, column=1, sticky="nsew")

        self._section_identity(left)
        self._section_recv_config(left)
        self._section_recv_control(left)

        log_frame = ttk.LabelFrame(right, text="Activity Log", padding=(12, 10))
        log_frame.pack(fill="both", expand=True)
        self._build_log(log_frame, "recv_log", label="Receive Log")

    def _section_identity(self, parent):
        frame = ttk.LabelFrame(parent, text="Your Identity", padding=(12, 10))
        frame.pack(fill="x", pady=(0, 12))

        row = ttk.Frame(frame)
        row.pack(fill="x")
        ttk.Label(row, text="Display Name:").pack(side="left")
        ttk.Entry(row, textvariable=self.app.receiver_name,
                  width=20).pack(side="left", padx=(8, 10))
        ttk.Button(row, text="Save", command=self.app.save_settings,
                   style="Ghost.TButton").pack(side="left")

        ttk.Label(frame,
                  text="Visible to senders during network discovery",
                  style="Muted.TLabel").pack(anchor="w", pady=(8, 0))

    def _section_recv_config(self, parent):
        frame = ttk.LabelFrame(parent, text="Configuration", padding=(12, 10))
        frame.pack(fill="x", pady=(0, 12))

        # Port + size
        r1 = ttk.Frame(frame)
        r1.pack(fill="x")
        ttk.Label(r1, text="Port:").pack(side="left")
        self.app.recv_port_entry = ttk.Entry(r1, width=7)
        self.app.recv_port_entry.insert(0, "12345")
        self.app.recv_port_entry.pack(side="left", padx=(6, 20))
        ttk.Label(r1, text="Max size (MB):").pack(side="left")
        self.app.size_limit_var = tk.StringVar(value="1024")
        ttk.Spinbox(r1, from_=1, to=10240,
                    textvariable=self.app.size_limit_var,
                    width=7).pack(side="left", padx=(6, 0))

        # Save directory
        r2 = ttk.Frame(frame)
        r2.pack(fill="x", pady=(12, 0))
        ttk.Label(r2, text="Save to:").pack(anchor="w")
        r2b = ttk.Frame(r2)
        r2b.pack(fill="x", pady=(4, 0))
        self.app.save_dir_entry = ttk.Entry(r2b)
        self.app.save_dir_entry.insert(0, os.path.expanduser("~/Downloads"))
        self.app.save_dir_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(r2b, text="Browse",
                   command=self.app.browse_directory,
                   style="Ghost.TButton").pack(side="right", padx=(8, 0))

        # Options
        r3 = ttk.Frame(frame)
        r3.pack(fill="x", pady=(12, 0))
        ttk.Checkbutton(r3, text="Auto-accept incoming transfers",
                        variable=self.app.auto_accept).pack(anchor="w")
        ttk.Checkbutton(r3, text="Sound notifications",
                        variable=self.app.notification_sound).pack(anchor="w",
                        pady=(6, 0))
        ttk.Checkbutton(r3, text="Create subfolder per batch",
                        variable=self.app.create_subfolders).pack(anchor="w",
                        pady=(6, 0))

    def _section_recv_control(self, parent):
        frame = ttk.LabelFrame(parent, text="Controls", padding=(12, 10))
        frame.pack(fill="x")

        btns = ttk.Frame(frame)
        btns.pack(fill="x")
        self.app.start_button = ttk.Button(
            btns, text="Start Receiving",
            command=self.app.start_receiving, style="Success.TButton")
        self.app.start_button.pack(side="left")
        self.app.stop_button = ttk.Button(
            btns, text="Stop",
            command=self.app.stop_receiving,
            state="disabled", style="Danger.TButton")
        self.app.stop_button.pack(side="left", padx=(10, 0))
        self.app.open_folder_button = ttk.Button(
            btns, text="Open Folder",
            command=self.app.open_save_folder, style="Ghost.TButton")
        self.app.open_folder_button.pack(side="right")

        status_row = ttk.Frame(frame)
        status_row.pack(fill="x", pady=(10, 0))
        self.app.receiver_status = ttk.Label(
            status_row, text="Not receiving", style="Muted.TLabel")
        self.app.receiver_status.pack(side="left")
        self.app.receiver_stats = ttk.Label(
            status_row, text="", style="Muted.TLabel")
        self.app.receiver_stats.pack(side="right")

    # ──────────────────────────────────────────────────────────────────────────
    # MONITOR TAB
    # ──────────────────────────────────────────────────────────────────────────
    def _build_monitor_tab(self):
        tab = ttk.Frame(self.app.notebook, padding=(20, 15, 20, 15))
        self.app.notebook.add(tab, text="  Monitor  ")

        self._section_stats(tab)
        self._section_transfers(tab)

    def _section_stats(self, parent):
        outer = ttk.LabelFrame(parent, text="Statistics", padding=(12, 10))
        outer.pack(fill="x", pady=(0, 12))

        self.app.stats_labels = {}
        items = [
            ("Files Sent",      "files_sent",       "\u2191"),
            ("Files Received",  "files_received",   "\u2193"),
            ("Data Sent",       "data_sent",         "\u2191"),
            ("Data Received",   "data_received",     "\u2193"),
            ("Active",          "active_transfers",  "\u21c4"),
        ]
        for label, key, icon in items:
            card = tk.Frame(outer, bg=BG_CARD,
                            highlightbackground=CARD_BDR,
                            highlightthickness=1)
            card.pack(side="left", padx=(0, 10), pady=2, ipadx=14, ipady=8)

            tk.Label(card, text=f"{icon}  {label}", bg=BG_CARD,
                     fg=MUTED, font=(FONT, 9)).pack(anchor="w")

            lbl = tk.Label(card, text="0", bg=BG_CARD,
                           fg=PRIMARY, font=(FONT, 16, "bold"))
            lbl.pack(anchor="w")
            self.app.stats_labels[key] = lbl

    def _section_transfers(self, parent):
        frame = ttk.LabelFrame(parent, text="Active Transfers", padding=(12, 10))
        frame.pack(fill="both", expand=True)

        tb = ttk.Frame(frame)
        tb.pack(fill="x", pady=(0, 8))
        ttk.Button(tb, text="Refresh", command=self.app.refresh_monitor,
                   style="Ghost.TButton").pack(side="left")
        ttk.Button(tb, text="Cancel All",
                   command=self.app.cancel_all_transfers,
                   style="Danger.TButton").pack(side="left", padx=(10, 0))

        cols = ("Direction", "File", "Peer", "Progress", "Speed", "ETA", "Status")
        self.app.transfer_tree = ttk.Treeview(
            frame, columns=cols, show="headings", height=12)
        _col_setup = [
            ("Direction", "center",  70),
            ("File",      "w",      200),
            ("Peer",      "w",      110),
            ("Progress",  "center",  80),
            ("Speed",     "e",       80),
            ("ETA",       "center",  70),
            ("Status",    "center",  80),
        ]
        for col, anchor, w in _col_setup:
            self.app.transfer_tree.heading(col, text=col)
            self.app.transfer_tree.column(col, width=w, minwidth=50,
                                          anchor=anchor, stretch=True)

        vsb = ttk.Scrollbar(frame, orient="vertical",
                            command=self.app.transfer_tree.yview)
        self.app.transfer_tree.configure(yscrollcommand=vsb.set)
        self.app.transfer_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._auto_resize_columns(self.app.transfer_tree,
            {"Direction": 1, "File": 5, "Peer": 2,
             "Progress": 2, "Speed": 2, "ETA": 2, "Status": 2})

        m = tk.Menu(self.app.root, tearoff=0)
        m.add_command(label="Cancel Transfer",
                      command=self.app.cancel_selected_transfer)
        m.add_command(label="Details", command=self.app.show_transfer_details)
        self.app.transfer_context_menu = m
        self.app.transfer_tree.bind("<Button-3>", self.app.show_context_menu)

    # ──────────────────────────────────────────────────────────────────────────
    # SETTINGS TAB
    # ──────────────────────────────────────────────────────────────────────────
    def _build_settings_tab(self):
        tab = ttk.Frame(self.app.notebook, padding=(20, 15, 20, 15))
        self.app.notebook.add(tab, text="  Settings  ")

        panes = ttk.Frame(tab)
        panes.pack(fill="both", expand=True)
        panes.columnconfigure(0, weight=1)
        panes.columnconfigure(1, weight=1)

        left  = ttk.Frame(panes)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right = ttk.Frame(panes)
        right.grid(row=0, column=1, sticky="nsew")

        self._settings_network(left)
        self._settings_discovery(right)
        self._settings_files(right)

        ttk.Button(tab, text="Apply & Save Settings",
                   command=self.app.apply_settings,
                   style="Success.TButton").pack(pady=(20, 0))

    def _settings_network(self, parent):
        frame = ttk.LabelFrame(parent, text="Network", padding=(12, 10))
        frame.pack(fill="x", pady=(0, 12))

        defs = [
            ("Buffer Size (KB)",        "buffer_size_var",    "16",  1,    1024),
            ("Connection Timeout (sec)", "timeout_var",       "30",  5,    300),
            ("Max Parallel Threads",    "max_threads_var",    "4",   1,    8),
            ("Split Threshold (MB)",    "split_threshold_var","200", 50,   1000),
        ]
        for label, varname, default, lo, hi in defs:
            row = ttk.Frame(frame)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=label, width=26, anchor="w").pack(side="left")
            var = tk.StringVar(value=default)
            setattr(self.app, varname, var)
            ttk.Spinbox(row, from_=lo, to=hi, textvariable=var,
                        width=9).pack(side="left")

    def _settings_discovery(self, parent):
        frame = ttk.LabelFrame(parent, text="Discovery", padding=(12, 10))
        frame.pack(fill="x", pady=(0, 12))

        ttk.Checkbutton(frame, text="Auto-discover on startup",
                        variable=self.app.auto_discover).pack(anchor="w")
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(8, 0))
        ttk.Label(row, text="Interval (sec):", width=16, anchor="w").pack(side="left")
        self.app.discovery_interval_var = tk.StringVar(value="30")
        ttk.Spinbox(row, from_=10, to=300,
                    textvariable=self.app.discovery_interval_var,
                    width=9).pack(side="left")

    def _settings_files(self, parent):
        frame = ttk.LabelFrame(parent, text="File Handling", padding=(12, 10))
        frame.pack(fill="x")

        ttk.Checkbutton(frame, text="Overwrite existing files",
                        variable=self.app.overwrite_files).pack(anchor="w")
        ttk.Checkbutton(frame, text="Create subfolder per batch",
                        variable=self.app.create_subfolders).pack(anchor="w",
                        pady=(8, 0))

    # ──────────────────────────────────────────────────────────────────────────
    # HISTORY TAB
    # ──────────────────────────────────────────────────────────────────────────
    def _build_history_tab(self):
        tab = ttk.Frame(self.app.notebook, padding=(20, 15, 20, 15))
        self.app.notebook.add(tab, text="  History  ")

        tb = ttk.Frame(tab)
        tb.pack(fill="x", pady=(0, 12))
        ttk.Button(tb, text="Refresh", command=self.app.refresh_history,
                   style="Ghost.TButton").pack(side="left")
        ttk.Button(tb, text="Export CSV", command=self.app.export_history,
                   style="Ghost.TButton").pack(side="left", padx=(10, 0))
        ttk.Button(tb, text="Clear", command=self.app.clear_history,
                   style="Danger.TButton").pack(side="left", padx=(10, 0))

        cols = ("Time", "Direction", "File(s)", "Peer", "Size", "Status", "Duration")
        hist_frame = ttk.Frame(tab)
        hist_frame.pack(fill="both", expand=True)
        hist_frame.columnconfigure(0, weight=1)
        hist_frame.rowconfigure(0, weight=1)

        self.app.history_tree = ttk.Treeview(
            hist_frame, columns=cols, show="headings")
        _col_setup = [
            ("Time",      "w",      120),
            ("Direction", "center",  70),
            ("File(s)",   "w",      200),
            ("Peer",      "w",      110),
            ("Size",      "e",       75),
            ("Status",    "center",  75),
            ("Duration",  "e",       75),
        ]
        for col, anchor, w in _col_setup:
            self.app.history_tree.heading(col, text=col)
            self.app.history_tree.column(col, width=w, minwidth=50,
                                         anchor=anchor, stretch=True)

        vsb = ttk.Scrollbar(hist_frame, orient="vertical",
                            command=self.app.history_tree.yview)
        hsb = ttk.Scrollbar(hist_frame, orient="horizontal",
                            command=self.app.history_tree.xview)
        self.app.history_tree.configure(yscrollcommand=vsb.set,
                                        xscrollcommand=hsb.set)
        self.app.history_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self._auto_resize_columns(self.app.history_tree,
            {"Time": 2, "Direction": 1, "File(s)": 5, "Peer": 2,
             "Size": 1, "Status": 1, "Duration": 1})

    # ──────────────────────────────────────────────────────────────────────────
    # Log widget
    # ──────────────────────────────────────────────────────────────────────────
    def _build_log(self, parent, attr_name, label="Log"):
        # mini header row
        hdr = ttk.Frame(parent)
        hdr.pack(fill="x", pady=(0, 4))
        ttk.Label(hdr, text=label, style="Muted.TLabel").pack(side="left")
        ttk.Button(
            hdr, text="Clear",
            command=lambda a=attr_name: self._clear_log(a),
            style="Ghost.TButton"
        ).pack(side="right")

        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)

        widget = tk.Text(container, height=8, font=("Consolas", 10),
                         wrap="word",
                         bg=LOG_BG, fg=LOG_FG,
                         insertbackground=LOG_FG,
                         selectbackground=PRIMARY, selectforeground="white",
                         relief="flat", padx=12, pady=10, state="disabled")

        vsb = ttk.Scrollbar(container, orient="vertical", command=widget.yview)
        widget.configure(yscrollcommand=vsb.set)
        widget.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Define colour tags
        widget.tag_configure("info",    foreground="#94a3b8")
        widget.tag_configure("success", foreground="#4ade80")
        widget.tag_configure("error",   foreground="#f87171")
        widget.tag_configure("warning", foreground="#fbbf24")
        widget.tag_configure("ts",      foreground="#475569")

        setattr(self.app, attr_name, widget)

    def _clear_log(self, attr_name):
        widget = getattr(self.app, attr_name, None)
        if widget:
            widget.configure(state="normal")
            widget.delete("1.0", "end")
            widget.configure(state="disabled")

    # ──────────────────────────────────────────────────────────────────────────
    # Column auto-resize
    # ──────────────────────────────────────────────────────────────────────────
    def _auto_resize_columns(self, tree, weights: dict):
        """Proportionally redistribute column widths whenever the tree is resized."""
        cols  = list(weights.keys())
        total = sum(weights.values())

        def _apply(width):
            avail = max(100, width - 20)
            for col in cols:
                tree.column(col, width=max(40, int(avail * weights[col] / total)))

        tree.bind("<Configure>", lambda e: _apply(e.width))
        # Fire once the widget is fully rendered
        tree.bind("<Map>", lambda e: tree.after(50, lambda: _apply(tree.winfo_width())))

    def _force_resize(self, tree):
        """Force column recompute using current widget width."""
        w = tree.winfo_width()
        if w > 1:
            tree.event_generate("<Configure>", width=w, height=tree.winfo_height())

    # ──────────────────────────────────────────────────────────────────────────
    # Public helpers called by app.py
    # ──────────────────────────────────────────────────────────────────────────
    def update_files_display(self, new_count=0):
        for item in self.app.files_tree.get_children():
            self.app.files_tree.delete(item)

        total = 0
        all_items = []
        for idx, fi in enumerate(self.app.selected_files):
            total += fi["size"]
            tag = "oddrow" if idx % 2 == 0 else "evenrow"
            iid = self.app.files_tree.insert("", "end", values=(
                fi["name"],
                _fmt(fi["size"]),
                _friendly_type(fi["type"]),
                fi["path"],
            ), tags=(tag,))
            all_items.append(iid)

        self.app.files_tree.tag_configure("oddrow",  background="#ffffff")
        self.app.files_tree.tag_configure("evenrow", background="#f8faff")
        self.app.files_tree.tag_configure("newrow",  background="#dbeafe")

        # Briefly highlight the newly added rows
        if new_count > 0 and all_items:
            new_items = all_items[-new_count:]
            for iid in new_items:
                self.app.files_tree.item(iid, tags=("newrow",))
                self.app.files_tree.see(iid)
            # Restore normal row colours after 900 ms
            def _restore():
                for i, iid in enumerate(new_items):
                    if self.app.files_tree.exists(iid):
                        self.app.files_tree.item(
                            iid, tags=("oddrow" if (len(all_items) - new_count + new_items.index(iid)) % 2 == 0 else "evenrow",))
            self.app.root.after(900, _restore)

        n = len(self.app.selected_files)
        self.app.file_summary.config(
            text="No files selected" if n == 0
            else f"{n} file{'s' if n > 1 else ''}  —  Total: {_fmt(total)}")

    def flash_file_summary(self):
        """Briefly highlight the summary bar green, then revert."""
        lbl = self.app.file_summary
        lbl.configure(foreground=SUCCESS)
        self.app.root.after(1000, lambda: lbl.configure(foreground=MUTED))

    def show_error_dialog(self, title, msg):
        messagebox.showerror(title, msg)

    def show_info_dialog(self, title, msg):
        messagebox.showinfo(title, msg)

    def show_warning_dialog(self, title, msg):
        messagebox.showwarning(title, msg)

    def ask_yes_no(self, title, msg):
        return messagebox.askyesno(title, msg)

    def browse_files(self, title="Select Files", filetypes=None):
        return filedialog.askopenfilenames(
            title=title,
            filetypes=filetypes or [("All files", "*.*")])

    def browse_folder(self, title="Select Folder"):
        return filedialog.askdirectory(title=title)

    def browse_save_file(self, title="Save As", defaultextension=".txt",
                         filetypes=None):
        return filedialog.asksaveasfilename(
            title=title, defaultextension=defaultextension,
            filetypes=filetypes or [("Text files", "*.txt"), ("All files", "*.*")])


# ── Helpers ────────────────────────────────────────────────────────────────────
def _fmt(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

_TYPE_MAP = {
    "text":        "Text",
    "image":       "Image",
    "video":       "Video",
    "audio":       "Audio",
    "application": "App / Bin",
    "font":        "Font",
    "model":       "3D Model",
}

def _friendly_type(mime: str) -> str:
    """Turn 'image/png' → 'Image', 'text/plain' → 'Text', etc."""
    if not mime or mime.lower() in ('unknown', 'error'):
        return 'File'
    top = mime.split("/")[0].lower()
    return _TYPE_MAP.get(top, top.capitalize())
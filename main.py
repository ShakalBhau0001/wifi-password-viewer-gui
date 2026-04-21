import subprocess
import threading
import time
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0f1117"
BG2 = "#1a1d27"
BG3 = "#222638"
ACCENT = "#00c2ff"
ACCENT2 = "#0077aa"
GREEN = "#00e676"
RED = "#ff5252"
YELLOW = "#ffd740"
TEXT = "#e8eaf6"
TEXT_DIM = "#6c7293"
BORDER = "#2d3154"


# ── Backend Functions
def get_wifi_profiles():
    try:
        data = (
            subprocess.check_output(["netsh", "wlan", "show", "profiles"])
            .decode("utf-8", errors="backslashreplace")
            .split("\n")
        )
        return [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    except subprocess.CalledProcessError:
        return []


def get_wifi_password(profile):
    try:
        results = (
            subprocess.check_output(
                ["netsh", "wlan", "show", "profile", profile, "key=clear"]
            )
            .decode("utf-8", errors="backslashreplace")
            .split("\n")
        )
        passwords = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        return passwords[0] if passwords else None
    except subprocess.CalledProcessError:
        return "ENCODING ERROR"


# ── Main App
class WiFiViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("📶 Wi-Fi Password Viewer")
        self.geometry("900x680")
        self.minsize(700, 520)
        self.configure(fg_color=BG)
        self.resizable(True, True)
        self._all_rows = []
        self._build_ui()
        self.after(300, self._start_scan)

    # ── UI Layout
    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=BG2, corner_radius=0, height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📶  Wi-Fi Password Viewer",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=ACCENT,
        ).pack(side="left", padx=24, pady=18)

        self.status_label = ctk.CTkLabel(
            header,
            text="Initializing...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_DIM,
        )
        self.status_label.pack(side="right", padx=24)

        # Stats bar
        stats_frame = ctk.CTkFrame(self, fg_color=BG3, corner_radius=0, height=50)
        stats_frame.pack(fill="x")
        stats_frame.pack_propagate(False)
        self.stat_total = self._stat_badge(stats_frame, "Total", "–", ACCENT)
        self.stat_found = self._stat_badge(stats_frame, "✔ Found", "–", GREEN)
        self.stat_empty = self._stat_badge(stats_frame, "No Password", "–", YELLOW)
        self.stat_errors = self._stat_badge(stats_frame, "⚠ Errors", "–", RED)

        # Search And Rescan bar
        search_frame = ctk.CTkFrame(self, fg_color=BG2, corner_radius=0, height=48)
        search_frame.pack(fill="x")
        search_frame.pack_propagate(False)

        ctk.CTkLabel(
            search_frame, text="🔍", font=ctk.CTkFont(size=14), text_color=TEXT_DIM
        ).pack(side="left", padx=(16, 4), pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)
        ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search network name...",
            fg_color=BG3,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text_color=TEXT_DIM,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=32,
            corner_radius=8,
        ).pack(side="left", fill="x", expand=True, padx=(0, 16), pady=8)

        self.scan_btn = ctk.CTkButton(
            search_frame,
            text="⟳  Rescan",
            width=100,
            height=32,
            fg_color=ACCENT2,
            hover_color=ACCENT,
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8,
            command=self._start_scan,
        )
        self.scan_btn.pack(side="right", padx=(0, 16), pady=8)

        # Table
        table_frame = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        table_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "WiFi.Treeview",
            background=BG2,
            foreground=TEXT,
            fieldbackground=BG2,
            borderwidth=0,
            rowheight=36,
            font=("Segoe UI", 12),
        )
        style.configure(
            "WiFi.Treeview.Heading",
            background=BG3,
            foreground=ACCENT,
            borderwidth=0,
            font=("Segoe UI", 12, "bold"),
            relief="flat",
        )
        style.map("WiFi.Treeview", background=[("selected", ACCENT2)])
        style.map("WiFi.Treeview.Heading", background=[("active", BG3)])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("#", "SSID", "Password", "Status"),
            show="headings",
            style="WiFi.Treeview",
            selectmode="browse",
        )
        self.tree.heading("#", text="#", anchor="center")
        self.tree.heading("SSID", text="Network Name (SSID)", anchor="w")
        self.tree.heading("Password", text="Password", anchor="w")
        self.tree.heading("Status", text="Status", anchor="center")

        self.tree.column("#", width=48, minwidth=40, anchor="center", stretch=False)
        self.tree.column("SSID", width=240, minwidth=150, anchor="w", stretch=True)
        self.tree.column("Password", width=260, minwidth=150, anchor="w", stretch=True)
        self.tree.column(
            "Status", width=130, minwidth=100, anchor="center", stretch=False
        )

        self.tree.tag_configure("found", foreground=GREEN)
        self.tree.tag_configure("empty", foreground=YELLOW)
        self.tree.tag_configure("error", foreground=RED)
        self.tree.tag_configure("even", background="#1e2130")
        self.tree.tag_configure("odd", background=BG2)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self._on_row_select)
        self.tree.bind("<Double-1>", self._copy_password)

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            self, fg_color=BG3, progress_color=ACCENT, height=5, corner_radius=0
        )
        self.progress.set(0)
        self.progress.pack(fill="x", side="bottom")

        # ── Detail Bar
        self.detail_frame = ctk.CTkFrame(self, fg_color=BG3, corner_radius=0, height=42)
        self.detail_frame.pack(fill="x", side="bottom")
        self.detail_frame.pack_propagate(False)

        self.detail_icon = ctk.CTkLabel(
            self.detail_frame,
            text="📶",
            font=ctk.CTkFont(size=15),
            text_color=TEXT_DIM,
            width=30,
        )
        self.detail_icon.pack(side="left", padx=(14, 2), pady=10)

        self.detail_label = ctk.CTkLabel(
            self.detail_frame,
            text="Click on any row to see password details",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_DIM,
        )
        self.detail_label.pack(side="left", pady=10)

        self.copy_toast = ctk.CTkLabel(
            self.detail_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=GREEN,
        )
        self.copy_toast.pack(side="right", padx=14)

        # Footer
        footer = ctk.CTkFrame(self, fg_color=BG2, corner_radius=0, height=30)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        ctk.CTkLabel(
            footer,
            text="🔐  Double-click any row to copy password to clipboard",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_DIM,
        ).pack(side="left", padx=16, pady=5)

    def _stat_badge(self, parent, label, value, color):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(side="left", padx=20, pady=6)
        val_lbl = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=color,
        )
        val_lbl.pack()
        ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=TEXT_DIM,
        ).pack()
        return val_lbl

    # ── Row Selection and Detail Bar
    def _on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        tags = self.tree.item(selected[0])["tags"]
        ssid = values[1]
        tag = next((t for t in tags if t in ("found", "empty", "error")), "")

        if tag == "found":
            icon = "✔"
            color = GREEN
            desc = f'"{ssid}" — Password found. Double-click to copy it.'

        elif tag == "empty":
            icon = "ℹ"
            color = YELLOW
            desc = f'"{ssid}" — No password saved. This is an open network or password was not stored.'

        elif tag == "error":
            icon = "⚠"
            color = RED
            desc = f'"{ssid}" — Could not read password. Please run this app as Administrator.'

        else:
            icon, color, desc = "📶", TEXT_DIM, f"Selected: {ssid}"

        self.detail_icon.configure(text=icon, text_color=color)
        self.detail_label.configure(text=desc, text_color=color)

    # ── Scan Logic
    def _start_scan(self):
        self._clear_table()
        self._all_rows = []
        self.scan_btn.configure(state="disabled", text="Scanning...")
        self.status_label.configure(text="Scanning profiles...", text_color=ACCENT)
        self.detail_icon.configure(text="⏳", text_color=TEXT_DIM)
        self.detail_label.configure(
            text="Please wait while profiles are being scanned...", text_color=TEXT_DIM
        )
        self.progress.set(0)
        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self):
        profiles = get_wifi_profiles()

        if not profiles:
            self.after(
                0,
                lambda: self.status_label.configure(
                    text="No profiles found.", text_color=YELLOW
                ),
            )
            self.after(
                0, lambda: self.detail_icon.configure(text="ℹ", text_color=YELLOW)
            )
            self.after(
                0,
                lambda: self.detail_label.configure(
                    text="No Wi-Fi profiles found on this machine.", text_color=YELLOW
                ),
            )
            self.after(
                0, lambda: self.scan_btn.configure(state="normal", text="⟳  Rescan")
            )
            return

        total = len(profiles)
        found = empty = errors = 0

        for idx, profile in enumerate(profiles, start=1):
            password = get_wifi_password(profile)
            time.sleep(0.04)

            if password == "ENCODING ERROR":
                tag, status, pw_show = "error", "⚠ Error", "Encoding Error"
                errors += 1
            elif password is None:
                tag, status, pw_show = "empty", "No Password", "── none ──"
                empty += 1
            else:
                tag, status, pw_show = "found", "✔ Found", password
                found += 1

            row_tags = ("even" if idx % 2 == 0 else "odd", tag)
            row = (str(idx), profile, pw_show, status)
            self._all_rows.append((row, row_tags))

            pval = idx / total
            self.after(
                0,
                lambda r=row, t=row_tags, p=pval, f=found, e=empty, err=errors, tot=total: self._update_ui(
                    r, t, p, f, e, err, tot
                ),
            )

        self.after(
            0,
            lambda: self.status_label.configure(
                text=f"Done — {total} network(s) scanned.", text_color=GREEN
            ),
        )
        self.after(0, lambda: self.detail_icon.configure(text="✔", text_color=GREEN))
        self.after(
            0,
            lambda: self.detail_label.configure(
                text=f"Scan complete — {found} password(s) found, {empty} open network(s), {errors} error(s).  Click any row for details.",
                text_color=GREEN,
            ),
        )
        self.after(0, lambda: self.scan_btn.configure(state="normal", text="⟳  Rescan"))

    def _update_ui(self, row, tags, progress_val, found, empty, errors, total):
        self.tree.insert("", "end", values=row, tags=tags)
        self.progress.set(progress_val)
        self.stat_total.configure(text=str(total))
        self.stat_found.configure(text=str(found))
        self.stat_empty.configure(text=str(empty))
        self.stat_errors.configure(text=str(errors))

    def _clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.stat_total.configure(text="–")
        self.stat_found.configure(text="–")
        self.stat_empty.configure(text="–")
        self.stat_errors.configure(text="–")

    # ── Searching wifi name
    def _on_search(self, *args):
        query = self.search_var.get().lower().strip()
        self._clear_table()
        for row, tags in self._all_rows:
            if query in row[1].lower():
                self.tree.insert("", "end", values=row, tags=tags)

    # ── Copy password on double click
    def _copy_password(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        password = str(values[2])

        if password in ("── none ──", "Encoding Error"):
            self.copy_toast.configure(text="Nothing to copy", text_color=YELLOW)
        else:
            self.clipboard_clear()
            self.clipboard_append(password)
            self.copy_toast.configure(text="✔ Copied!", text_color=GREEN)

        self.after(2500, lambda: self.copy_toast.configure(text=""))


# ── Entry Point
if __name__ == "__main__":
    app = WiFiViewerApp()
    app.mainloop()

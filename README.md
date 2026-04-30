# 📶 WiFi Password Viewer (GUI) 🔐

A modern **GUI-based Wi-Fi Password Viewer** built using **Python + CustomTkinter**.
This tool scans all saved Wi-Fi networks on your Windows system and displays their passwords in a **beautiful, interactive desktop interface**.

---

## 🧱 Project Structure

```bash
wifi-password-viewer-gui/
│
├── assets/             # Screenshots
├── main.py             # Main GUI application
├── LICENSE
└── README.md           # Project documentation
```

---

## ✨ Features

### 📡 Smart Wi-Fi Scanner

* Automatically detects **all saved Wi-Fi profiles**
* Uses Windows built-in `netsh` command (no external API)

### 🔐 Password Extractor

* Retrieves passwords using `key=clear`
* Handles:

  * Open networks (no password)
  * Encoding errors gracefully

### 🖥️ Modern GUI Interface

* Built with **CustomTkinter (Dark Mode UI)**
* Clean, responsive and resizable window

### 📊 Live Stats Dashboard

* Total Networks
* ✔ Found Passwords
* ⚠ Errors
* 🔓 Open Networks

### 🔍 Search Functionality

* Instantly filter Wi-Fi networks by name

### 📋 Copy to Clipboard

* Double-click any row to copy password

### ⟳ Rescan Button

* Refresh and re-fetch all Wi-Fi profiles anytime

### 📈 Real-time Progress

* Smooth progress bar during scanning
* Live updates while fetching passwords

### 📌 Detail Panel

* Shows contextual info when selecting a network:

  * Password found
  * Open network
  * Error (Admin required)

---

## 🛠 Technologies Used

| Technology        | Role                  |
| ----------------- | --------------------- |
| **Python 3**      | Core programming      |
| **subprocess**    | Runs `netsh` commands |
| **CustomTkinter** | Modern GUI framework  |
| **Tkinter (ttk)** | Table & UI components |
| **threading**     | Background scanning   |
| **time**          | Smooth UI updates     |

---

## 📌 Requirements

```bash
Python 3.7+
Windows OS (netsh required)
```

Install dependencies:

```bash
pip install customtkinter
```

---

## ▶️ How to Run

### 1️⃣ Clone Repository

```bash
git clone https://github.com/ShakalBhau0001/wifi-password-viewer-gui.git
```

### 2️⃣ Navigate to Project

```bash
cd wifi-password-viewer-gui
```

### 3️⃣ Install Dependencies

```bash
pip install customtkinter
```

### 4️⃣ Run Application

```bash
python main.py
```

> ⚠️ Run as Administrator for full password access

---

## 🖥️ UI Preview (What You'll See)

* 📶 Header with app title
* 📊 Stats bar showing counts
* 🔍 Search bar + Rescan button
* 📋 Table with:

  * SSID
  * Password
  * Status
* 📌 Detail panel (bottom)
* 📈 Progress bar during scan

---

## ⚙️ How It Works

### 1️⃣ Scan Profiles

* Executes:

```bash
netsh wlan show profiles
```

### 2️⃣ Extract Passwords

* For each profile:

```bash
netsh wlan show profile <name> key=clear
```

* Parses `Key Content` field

### 3️⃣ Display in GUI

* Data is shown in a styled table with:

  * ✔ Found
  * No Password
  * ⚠ Error

---

## ⚠️ Limitations

* Windows only (uses `netsh`)
* Requires Administrator privileges
* Only shows networks saved on current system

---

## 🌟 Future Enhancements

* Export to `.txt` / `.csv`
* Show/hide password toggle
* Dark/Light theme switch
* Linux & macOS support
* Installer (.exe) using PyInstaller

---

## ⚠️ Disclaimer

> **Use responsibly**

* For **personal and educational use only**
* Only access networks you own or have permission for
* Developer is not responsible for misuse

---

## 🪪 Author

> **Creator: Shakal Bhau**

> **GitHub: [ShakalBhau0001](https://github.com/ShakalBhau0001)**


---

## 💙 Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🧠 Contribute ideas

---

> 🔐 *Stay ethical. Stay secure.*

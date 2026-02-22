# NetShare

A production-grade LAN file sharing application built with Python and Tkinter.  
Transfer files and folders between computers on the same network — no internet required, no third-party services, no size limits.

---

## Features

| Category | Details |
|---|---|
| **Auto Discovery** | UDP broadcast scans the local network and lists all online receivers instantly |
| **Multi-file & Folder** | Select individual files or entire directory trees in one batch |
| **Multi-threaded Transfer** | Large files are split into chunks and sent in parallel across multiple TCP connections |
| **Real-time Progress** | Live progress bar, transfer speed (MB/s), and ETA per transfer |
| **Transfer Monitor** | Dedicated tab showing all active and recently completed transfers |
| **History Log** | Persistent log of every send/receive with size, speed, and status |
| **Accept / Reject** | Prompted confirmation dialog for each incoming transfer (or auto-accept) |
| **Settings** | Configurable port, buffer size, thread count, save directory, and more |
| **Clean UI** | Light professional theme, proportional resizable columns, colour-coded logs |
| **Cross-platform** | Runs on Windows, macOS, and Linux — zero external dependencies |

---

## Screenshots

| Send Tab                           | Receive Tab                              |
| ---------------------------------- | ---------------------------------------- |
| ![Send Tab](assets/send%20tab.png) | ![Receive Tab](assets/receive%20tab.png) |

| Monitor Tab                              | History Tab                              |
| ---------------------------------------- | ---------------------------------------- |
| ![Monitor Tab](assets/monitor%20tab.png) | ![History Tab](assets/history%20tab.png) |

| Settings Tab                               |
| ------------------------------------------ |
| ![Settings Tab](assets/settings%20tab.png) |

---

## How It Works

```
Sender                                    Receiver
  │                                           │
  │── UDP broadcast (port 5000) ─────────────►│  Discovery
  │◄─ UDP announce (name, port, status) ──────│
  │                                           │
  │── TCP connect (port 12345) ──────────────►│  Handshake
  │── send metadata (JSON) ──────────────────►│
  │◄─ "READY" ────────────────────────────────│
  │                                           │
  │   Small files  (< 100 MB each)            │
  │── stream over main TCP connection ───────►│
  │                                           │
  │   Large files  (≥ 100 MB each)            │
  │── TCP chunk thread 1 (port 12346) ───────►│  Parallel
  │── TCP chunk thread 2 (port 12347) ───────►│  multi-threaded
  │── TCP chunk thread N (port 1234N) ───────►│  transfer
  │                                           │
  │── "TRANSFER_COMPLETE" ───────────────────►│
```

- **Discovery** — UDP broadcast on port `5000`. Every running instance announces its name, port, and availability status.
- **Handshake** — A primary TCP connection on port `12345` carries a JSON metadata envelope (file names, sizes, checksums, threading mode).
- **Small files** — Streamed directly over the main connection.
- **Large files** — Split into N equal byte ranges (up to 4 threads by default), each sent over a dedicated TCP connection on ports `12346–12365`, then reassembled in order.
- **Progress** — Chunk byte counts are aggregated in a thread-safe dictionary and pushed to the UI progress bar via `root.after()` (main-thread safe).

---

## Project Structure

```
netshare/
├── app.py                   # Main application class — coordinates all modules
├── requirements.txt
│
├── network/
│   ├── __init__.py
│   └── transfer_manager.py  # UDP discovery + TCP send/receive engine
│
├── ui/
│   ├── __init__.py
│   └── ui_manager.py        # All Tkinter UI — theme, tabs, widgets, helpers
│
├── utils/
│   ├── __init__.py
│   ├── app_utils.py         # Thread-safe logging, progress tracking, events
│   ├── file_manager.py      # File selection, MIME detection, folder walking
│   └── settings_manager.py  # Load / save persistent settings to JSON
│
└── assets/                  # Icons and screenshots
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `tkinter` — included in most Python installs
  - Arch Linux: `sudo pacman -S tk`
  - Ubuntu/Debian: `sudo apt install python3-tk`
  - macOS / Windows: bundled with Python

### Run

```bash
# 1. Clone
git clone https://github.com/kunald08/NetShare.git
cd netshare

# 2. (Optional) virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Launch
python app.py
```

> Run the app on **both** machines on the same Wi-Fi or LAN.  
> One instance sends, the other receives — they discover each other automatically via UDP broadcast.

---

## Usage

### Sending Files

1. Open the **Send** tab.
2. Click **Refresh** — online receivers appear in the *Connection* table automatically.
3. Click **Add Files** or **Add Folder** to build your send list.
4. Select a receiver row (or type an IP and port manually).
5. Hit **▶ Send Files**.

### Receiving Files

1. Open the **Receive** tab.
2. Set your *Display Name* (shown to senders during discovery).
3. Set the *Save to* directory and configure the port if needed.
4. Click **Start Receiving** — a green status confirms the listener is active.
5. Accept or decline each incoming request in the prompt dialog.

### Monitor Tab

Live table of every active transfer — direction, file name, peer, progress %, speed, and ETA.  
Right-click a row to cancel or view details.

### History Tab

Full log of completed and failed transfers.  
Export to CSV or clear with one click.

### Settings

| Setting | Default | Description |
|---|---|---|
| Buffer Size | 16 KB | Read/write chunk size per I/O call |
| Connection Timeout | 30 s | Socket idle timeout |
| Max Parallel Threads | 4 | Concurrent chunk threads per large file |
| Split Threshold | 200 MB | Files above this size use multi-threaded transfer |
| Discovery Interval | 30 s | Automatic re-discovery period |

---

## Technical Highlights

- **No external libraries** — built entirely on the Python standard library (`socket`, `threading`, `tkinter`, `json`, `os`)
- **Thread-safe UI updates** — all background threads communicate to the main thread via `root.after(0, callback)` — never touching widgets directly
- **Thread-safe dialogs** — incoming transfer prompts use a `queue.Queue` bridge so the background network thread blocks safely while the user decides
- **Graceful shutdown** — stopping the receiver closes all sockets cleanly; active transfer threads are joined before exit
- **Modular architecture** — networking, UI, file handling, and settings are fully decoupled; each layer communicates only through the central `app` instance

---

## Author

**[kunald08](https://github.com/kunald08)**

Built as a portfolio project demonstrating:
- Multi-threaded socket programming (TCP + UDP)
- Modular Python application architecture
- Production-grade Tkinter UI design
- Thread-safe inter-thread communication patterns

---

## License

MIT License — free to use, modify, and distribute.

# VerySSH - Windows SSH Launcher

A minimal, fast GUI for quickly launching SSH sessions from your `~/.ssh/config`.  
Built with native Python + Tkinter.

---

## 🔧 Features

- Parses `~/.ssh/config` and lists all hosts
- Click to connect via Windows Terminal (`wt ssh <host>`)
- Auto light/dark mode based on Windows settings
- No external dependencies
- Cross-compatible with any Python 3.x install on Windows

---

## 🚀 How to Run

### 1. Download the latest release

Go to the [Releases](https://github.com/your-repo/very-ssh/releases) page and download the pre-built `.exe` file for your platform.

### 2. Run the executable

Simply double-click the downloaded `.exe` file to launch the application.

---

## 📦 Build Standalone `.exe` (Optional)

If you prefer to build the executable yourself, follow these steps:

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Build executable

Run the build script:

```bash
build.bat
```

Output will be in the `dist/` folder.

---

## 📁 Project Structure

```
ssh_launcher/
├── __main__.py         # Entry point
├── config.py           # SSH config parsing
├── theme.py            # Windows theme detection
├── ui.py               # GUI logic
.github/
└── workflows/
    └── release.yml     # GitHub Actions workflow for releases
build.bat               # Build script for PyInstaller
launcher.py             # Launcher script for the standalone executable
README.md               # Project documentation
LICENSE                 # License file
```

---

## ✅ Example SSH Config

Make sure your `~/.ssh/config` has entries like:

```ssh
Host my-server
    HostName 192.168.1.10
    User max
```

---

## License

[MIT](./LICENSE). Do whatever the hell you want.

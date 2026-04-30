# 🔐 ConfigVault

> **Linux Config Explorer & Exporter** — A powerful TUI tool to discover, browse, search, and export your Linux configuration files as beautifully formatted PDFs.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux-orange?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Rich](https://img.shields.io/badge/TUI-Rich-purple?style=flat-square)

---

## 📸 Preview

```
 ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗ 
██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝ 
██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝ 
                                          VAULT
          Linux Config Explorer & Exporter
```

---

## ✨ Features

- 🔍 **Smart Scanner** — Automatically discovers all config files across `~/.config`, `$HOME`, and optionally `/etc`
- 🏷️ **Auto Categorization** — Groups configs into categories: Hyprland, Shell, Dev, Terminal, System, Display, Apps
- 📊 **Stats Dashboard** — Shows count and size breakdown per category
- 👀 **Syntax Highlighted Viewer** — View any config with full syntax highlighting (TOML, JSON, YAML, INI, and more)
- 🔎 **Search** — Search configs by name, path, or category instantly
- 📄 **PDF Exporter** — Export single files, categories, or your entire config collection as a styled PDF
- 📑 **Paginated Table View** — Navigate large config lists with pagination
- 🛡️ **Permission Safe** — Gracefully handles files you don't have access to

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `Python 3.10+` | Core language |
| `Rich` | Beautiful TUI — tables, syntax highlighting, panels |
| `ReportLab` | PDF generation with custom styling |
| `Watchdog` | File system watching (future feature) |
| `Pathspec` | Gitignore-style path matching |

---

## 📁 Project Structure

```
configvault/
├── main.py                  # Entry point — main TUI loop
├── src/
│   ├── __init__.py
│   ├── scanner/
│   │   └── __init__.py      # Config file discovery & categorization
│   ├── viewer/
│   │   └── __init__.py      # File reading & syntax detection
│   ├── exporter/
│   │   └── __init__.py      # PDF export engine
│   └── ui/
│       └── __init__.py      # UI helpers (future)
├── README.md
├── .gitignore
└── requirements.txt
```

---

## 🚀 Installation

### Prerequisites

- Linux (any distro)
- Python 3.10+
- pip / pacman / yay

### Arch Linux

```bash
sudo pacman -S python-rich python-reportlab python-watchdog python-pathspec
```

### Ubuntu / Debian

```bash
pip install rich reportlab watchdog pathspec
```

### Clone & Run

```bash
git clone https://github.com/abhinandbs12/configvault.git
cd configvault
python main.py
```

---

## 📖 Usage

### Launch

```bash
python main.py
```

You'll be asked if you want to include system configs (`/etc`). Then ConfigVault scans your system and displays all discovered config files.

### Commands

| Key | Action |
|-----|--------|
| `v` | View a config file with syntax highlighting |
| `s` | Search configs by name, path, or category |
| `e` | Export configs to PDF |
| `n` | Next page |
| `p` | Previous page |
| `r` | Reset search / show all |
| `q` | Quit |

### Export Options

When you press `e`, you get:

```
[1] Export current view
[2] Export by category
[3] Export selected files
[4] Export ALL configs
```

The exported PDF includes:
- File name, path, category, size, last modified
- Full syntax-highlighted content
- Generation timestamp

---

## 🗂️ Config Categories

| Category | Examples |
|----------|---------|
| `Hyprland` | hyprland.conf, caelestia configs, quickshell |
| `Shell` | fish config, starship.toml, .bashrc, .zshrc |
| `Dev` | nvim config, .gitconfig, LSP configs |
| `Terminal` | foot, kitty, alacritty configs |
| `System` | systemd units, /etc/default, pacman.conf |
| `Display` | SDDM, greetd configs |
| `Apps` | btop, brave, vscode settings |
| `Other` | Everything else |

---

## 🔮 Roadmap

- [ ] Config diff viewer — compare two configs side by side
- [ ] Backup manager — one-click backup all configs to a folder
- [ ] Restore from backup
- [ ] Auto-watch for config changes and notify
- [ ] Export as HTML
- [ ] Config templates — share your config setup
- [ ] GitHub Gist integration — push any config directly to a Gist
- [ ] Config health check — warn about broken or empty configs
- [ ] Filter by file extension

---

## 🤝 Contributing

Contributions are welcome! Here's how:

```bash
# Fork the repo on GitHub
git clone https://github.com/yourusername/configvault.git
cd configvault

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes, then
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name

# Open a Pull Request on GitHub
```

Please follow the existing code style and keep things modular.

---

## 📝 License

MIT License — feel free to use, modify, and distribute.

---

## 👤 Author

**Abhinand BS**  
GitHub: [@abhinandbs12](https://github.com/abhinandbs12)

---

## ⭐ If you find this useful, give it a star!

> Built with ❤️ on Arch Linux + Hyprland

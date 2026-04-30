<div align="center">
  <img src="https://img.shields.io/badge/Linux-ConfigVault-blue?style=for-the-badge&logo=linux" alt="ConfigVault Logo">
</div>

# 🔐 ConfigVault

> **Linux Config Explorer, Backup & Exporter** — A powerful, beautiful TUI tool to discover, browse, diff, search, backup, and export your Linux configuration files.

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Linux-orange?style=flat-square&logo=linux" alt="Linux">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</div>

---

## ✨ Features

- 🔍 **Deep Scanner** — Automatically discovers configs across `~/`, `~/.config`, and optionally `/etc`. Catches dotfiles (`.bashrc`, `.xinitrc`), `.conf`, `.json`, `.yaml`, and more.
- 🏷️ **Smart Categorization** — Groups configs logically (Hyprland, Shell, Dev, Apps, Terminal, System, etc.).
- 👀 **Syntax-highlighted Viewer** — View configuration files instantly with proper syntax highlighting directly in the terminal.
- 🗂️ **Export Everywhere** — Export selected files, categories, or your entire collection to:
  - **Raw Folders**: Copies your actual dotfiles into a structured directory.
  - **ZIP Archives**: Perfect for migrating or backing up your configs.
  - **PDF & HTML**: Beautifully formatted, syntax-highlighted reports.
- 🔄 **Config Diffing** — Compare any two configuration files side-by-side to spot changes.
- 🩺 **Health Checks** — Scans and identifies empty or broken config files (like invalid JSON).
- 💾 **Instant Backups** — One-press ZIP backup of your current setup to `~/ConfigVault_Backups`.

---

## 🚀 Installation

### Prerequisites

- Linux (any distro)
- Python 3.10+

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/abhinandbs12/configvault.git
cd configvault
pip install -r requirements.txt
```
*(Dependencies: `rich`, `reportlab`, `watchdog`, `pathspec`)*

### 2. Run

```bash
python main.py
```

---

## 📖 Usage Guide

When you launch `python main.py`, ConfigVault scans your system and displays all discovered config files in a paginated dashboard.

### TUI Commands

| Key | Action |
|-----|--------|
| `(v)` | **View**: Read a config file with full syntax highlighting |
| `(d)` | **Diff**: Compare two files side-by-side |
| `(h)` | **Health**: Check for broken/empty configuration files |
| `(s)` | **Search**: Instantly fuzzy-search configs by name or path |
| `(f)` | **Filter**: Show only files with a specific extension (e.g., `.json`) |
| `(e)` | **Export**: Export configs to Folder, ZIP, PDF, or HTML |
| `(b)` | **Backup**: Generate an instant layout backup zip |
| `(n)/(p)` | **Next/Prev**: Navigate pages |
| `(r)` | **Reset**: Clear searches and filters |
| `(q)` | **Quit**: Exit the application |

---

## 🔮 Roadmap

- [x] Config diff viewer
- [x] Backup manager
- [x] Config health check
- [x] Export to HTML, ZIP, and structured Folders
- [x] Deep dotfile scanning
- [ ] Restore from backup
- [ ] Auto-watch for config changes and notify
- [ ] GitHub Gist integration — push configs directly to a Gist
- [ ] Config templates

---

## 🤝 Contributing

Contributions are always welcome! 

1. Fork the repo 
2. Create your feature branch (`git checkout -b feature/cool-feature`)
3. Commit your changes (`git commit -m 'feat: added a cool feature'`)
4. Push to the branch (`git push origin feature/cool-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License. Built with ❤️ on Arch Linux.

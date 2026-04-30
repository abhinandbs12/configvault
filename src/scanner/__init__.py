import os
from pathlib import Path
from datetime import datetime

CATEGORIES = {
    "Hyprland": [".config/hypr", ".config/caelestia", ".config/quickshell"],
    "Shell": [".config/fish", ".config/starship.toml", ".bashrc", ".zshrc"],
    "Dev": [".config/nvim", ".config/git", ".gitconfig"],
    "Terminal": [".config/foot", ".config/kitty", ".config/alacritty"],
    "System": ["/etc/systemd", "/etc/default", "/etc/pacman.conf"],
    "Display": [".config/sddm", ".config/greetd"],
    "Apps": [".config/brave", ".config/code", ".config/btop"],
    "Other": []
}

CONFIG_EXTENSIONS = {'.conf', '.ini', '.toml', '.yaml', '.yml', '.json', '.cfg', '.config'}

def get_category(path: str) -> str:
    for category, paths in CATEGORIES.items():
        for p in paths:
            if p in path:
                return category
    return "Other"

def scan_configs(include_system=False) -> list:
    configs = []
    home = Path.home()
    
    scan_paths = [home / ".config", home]
    if include_system:
        scan_paths.extend([Path("/etc")])
    
    for base_path in scan_paths:
        if not base_path.exists():
            continue
        for root, dirs, files in os.walk(base_path):
            dirs[:] = [d for d in dirs if not d.startswith('.git') 
                      and d not in ['node_modules', '__pycache__', 'cache', 'Cache']]
            for file in files:
                filepath = Path(root) / file
                if filepath.suffix in CONFIG_EXTENSIONS or file.endswith('.conf'):
                    try:
                        stat = filepath.stat()
                        configs.append({
                            'name': file,
                            'path': str(filepath),
                            'category': get_category(str(filepath)),
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                            'extension': filepath.suffix
                        })
                    except (PermissionError, OSError):
                        continue
    return sorted(configs, key=lambda x: (x['category'], x['name']))

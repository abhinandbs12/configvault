import os
from pathlib import Path
from datetime import datetime

CATEGORIES = {
    "Hyprland": [".config/hypr", ".config/caelestia", ".config/quickshell"],
    "Shell": [".config/fish", "starship.toml", ".bashrc", ".zshrc", ".config/shell"],
    "Dev": [".config/nvim", ".config/git", ".gitconfig", ".config/lazygit"],
    "Terminal": [".config/foot", ".config/kitty", ".config/alacritty"],
    "System": ["/etc/systemd", "/etc/default", "pacman.conf"],
    "Display": [".config/sddm", ".config/greetd"],
    "Apps": [".config/btop", ".config/brave", ".config/Code", ".config/code"],
    "Other": []
}

CONFIG_EXTENSIONS = {
    '.conf', '.ini', '.toml', '.yaml', '.yml', '.cfg', 
    '.json', '.xml', '.lua', '.sh', '.zsh', '.env', 
    '.properties', '.rules', '.service', '.socket', 
    '.desktop', '.theme', '.bash'
}

CONFIG_FILENAMES = {
    '.gitconfig', '.bashrc', '.zshrc', '.profile', '.bash_profile',
    'starship.toml', 'config.json', 'settings.json', '.xinitrc', 
    '.Xresources', '.gtkrc-2.0', 'environment', 'profile'
}

SKIP_DIRS = {
    'node_modules', '__pycache__', 'cache', 'Cache',
    'CachedData', 'CachedExtensions', 'logs', 'Logs',
    'GPUCache', 'blob_storage', 'databases', 'Local Storage',
    'Session Storage', 'Service Worker', 'Code Cache',
    '.git', 'dist', 'build', '.next', 'venv', 'env'
}

def get_category(path: str) -> str:
    for category, paths in CATEGORIES.items():
        for p in paths:
            if p in path:
                return category
    return "Other"

def scan_configs(include_system=False) -> list:
    configs = []
    seen_paths = set()
    home = Path.home()

    scan_paths = [home / ".config"]

    # First explicitly scan given config files
    for name in CONFIG_FILENAMES:
        p = home / name
        if p.exists():
            try:
                stat = p.stat()
                path_str = str(p)
                if path_str not in seen_paths:
                    seen_paths.add(path_str)
                    configs.append({
                        'name': p.name,
                        'path': path_str,
                        'category': get_category(path_str),
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                        'extension': p.suffix
                    })
            except (PermissionError, OSError):
                continue
                
    # Also scan for any dotfiles in the home directory directly (like .bash_profile, .xinitrc, etc.)
    try:
        for p in home.iterdir():
            if p.is_file() and p.name.startswith('.'):
                if p.suffix.lower() in CONFIG_EXTENSIONS or p.name in CONFIG_FILENAMES or 'rc' in p.name.lower() or 'profile' in p.name.lower():
                    stat = p.stat()
                    path_str = str(p)
                    if path_str not in seen_paths and stat.st_size > 0 and stat.st_size < 500000:
                        seen_paths.add(path_str)
                        configs.append({
                            'name': p.name,
                            'path': path_str,
                            'category': get_category(path_str),
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                            'extension': p.suffix
                        })
    except (PermissionError, OSError):
        pass

    if include_system:
        scan_paths.append(Path("/etc"))

    for base_path in scan_paths:
        if not base_path.exists():
            continue
        for root, dirs, files in os.walk(base_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for file in files:
                filepath = Path(root) / file
                # Extended matcher: includes our file extensions, our exact filenames, or typical config extensions
                is_config = (
                    filepath.suffix.lower() in CONFIG_EXTENSIONS or
                    file in CONFIG_FILENAMES or
                    file.startswith('.') and filepath.suffix == ''
                )
                
                if is_config:
                    path_str = str(filepath)
                    if path_str in seen_paths:
                        continue
                    seen_paths.add(path_str)
                    try:
                        stat = filepath.stat()
                        if stat.st_size == 0 or stat.st_size > 500000:
                            continue
                        configs.append({
                            'name': file,
                            'path': path_str,
                            'category': get_category(path_str),
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                            'extension': filepath.suffix
                        })
                    except (PermissionError, OSError):
                        continue

    return sorted(configs, key=lambda x: (x['category'], x['name']))

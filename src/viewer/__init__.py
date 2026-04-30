from pathlib import Path

def read_config(path: str) -> tuple:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return content, None
    except PermissionError:
        return None, "Permission denied"
    except Exception as e:
        return None, str(e)

def get_syntax_type(path: str) -> str:
    ext_map = {
        '.toml': 'toml',
        '.json': 'json', 
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.ini': 'ini',
        '.conf': 'ini',
        '.py': 'python',
        '.sh': 'bash',
    }
    ext = Path(path).suffix.lower()
    return ext_map.get(ext, 'text')

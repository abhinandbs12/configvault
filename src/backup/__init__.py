import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def backup_configs(configs: list, backup_dir: str = None) -> tuple:
    try:
        if not backup_dir:
            backup_dir = str(Path.home() / "ConfigVault_Backups")
            
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"config_backup_{timestamp}.zip"
        zip_path = os.path.join(backup_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for config in configs:
                file_path = config['path']
                try:
                    if os.path.isfile(file_path):
                        # Archive name: category/filename
                        arcname = os.path.join(config['category'], config['name'])
                        zipf.write(file_path, arcname)
                except (PermissionError, OSError):
                    continue
                    
        return True, zip_path
    except Exception as e:
        return False, str(e)

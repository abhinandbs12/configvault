import os
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

def check_health(configs: list):
    table = Table(
        box=box.ROUNDED, 
        border_style="red",
        title="[bold red]🏥 Config Health Check[/bold red]",
        show_header=True,
        header_style="bold yellow"
    )
    table.add_column("Config File", style="cyan", no_wrap=True)
    table.add_column("Status", style="bold", justify="center")
    table.add_column("Issue Detected", style="dim")
    
    issues_found = 0
    for config in configs:
        path = str(config['path'])
        ext = config.get('extension', '').lower()
        size = config.get('size', 0)
        
        status = "[green]OK[/green]"
        issue_msg = ""
        
        # Check empty file
        if size == 0:
            status = "[red]ERROR[/red]"
            issue_msg = "File is completely empty (0 bytes)"
            issues_found += 1
            table.add_row(config['name'], status, issue_msg)
            continue
            
        # Basic JSON syntax validation
        if ext == '.json':
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                status = "[red]ERROR[/red]"
                issue_msg = f"Invalid JSON syntax: {str(e)}"
                issues_found += 1
                table.add_row(config['name'], status, issue_msg)
                
    if issues_found == 0:
        console.print("\n[bold green]✅ All configs passed the health check! No empty files or syntax errors detected.[/bold green]\n")
    else:
        console.print(table)
        console.print(f"[red]Found {issues_found} potential issue(s).[/red]\n")

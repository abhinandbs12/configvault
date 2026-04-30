from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

console = Console()

def show_diff(config1: dict, config2: dict):
    try:
        with open(config1['path'], 'r', encoding='utf-8', errors='ignore') as f:
            lines1 = f.readlines()
        with open(config2['path'], 'r', encoding='utf-8', errors='ignore') as f:
            lines2 = f.readlines()
    except Exception as e:
        console.print(f"[red]Error reading files: {e}[/red]")
        return

    max_lines = max(len(lines1), len(lines2))
    
    left = Text()
    right = Text()
    
    for i in range(max_lines):
        l = lines1[i].rstrip() if i < len(lines1) else ""
        r = lines2[i].rstrip() if i < len(lines2) else ""
        
        if l == r:
            left.append(f"{l}\n", style="dim")
            right.append(f"{r}\n", style="dim")
        else:
            left.append(f"{l}\n", style="bold red")
            right.append(f"{r}\n", style="bold green")

    console.print(
        Columns([
            Panel(left, title=f"[red]{config1['name']}[/red]", border_style="red"),
            Panel(right, title=f"[green]{config2['name']}[/green]", border_style="green")
        ])
    )

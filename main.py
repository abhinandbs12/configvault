from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich import box
from rich.columns import Columns
from rich.text import Text
import os
import sys
from pathlib import Path
from collections import defaultdict

from src.scanner import scan_configs
from src.viewer import read_config, get_syntax_type
from src.exporter import export_to_pdf, export_to_html

console = Console()

def show_banner():
    console.print(Panel.fit(
        """[bold blue]
 ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗ 
██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝ 
██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝ 
        [/bold blue][cyan]VAULT[/cyan]
        [dim]Linux Config Explorer & Exporter[/dim]""",
        border_style="blue",
        padding=(1, 4)
    ))

def show_stats(configs):
    categories = defaultdict(int)
    total_size = 0
    for c in configs:
        categories[c['category']] += 1
        total_size += c['size']
    
    table = Table(box=box.ROUNDED, border_style="blue", show_header=True, header_style="bold cyan")
    table.add_column("Category", style="cyan")
    table.add_column("Count", style="green", justify="right")
    
    for cat, count in sorted(categories.items()):
        table.add_row(cat, str(count))
    
    console.print(Panel(table, title="[bold]📊 Config Stats[/bold]", border_style="blue"))
    console.print(f"[dim]Total: {len(configs)} configs | {total_size/1024:.1f} KB[/dim]\n")

def show_configs_table(configs, page=0, per_page=20):
    start = page * per_page
    end = start + per_page
    page_configs = configs[start:end]
    
    table = Table(box=box.ROUNDED, border_style="blue", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="cyan", min_width=20)
    table.add_column("Category", style="green", width=12)
    table.add_column("Size", style="yellow", width=10, justify="right")
    table.add_column("Modified", style="dim", width=18)
    table.add_column("Path", style="dim", max_width=40)
    
    for i, config in enumerate(page_configs, start + 1):
        size = f"{config['size']/1024:.1f}KB" if config['size'] > 1024 else f"{config['size']}B"
        table.add_row(
            str(i),
            config['name'],
            config['category'],
            size,
            config['modified'],
            config['path']
        )
    
    console.print(table)
    total_pages = (len(configs) - 1) // per_page + 1
    console.print(f"[dim]Page {page+1}/{total_pages} | {len(configs)} total configs[/dim]\n")
    return page_configs, total_pages

def search_configs(configs, query):
    query = query.lower()
    return [c for c in configs if 
            query in c['name'].lower() or 
            query in c['path'].lower() or 
            query in c['category'].lower()]

def view_config(config):
    content, error = read_config(config['path'])
    if error:
        console.print(f"[red]Error: {error}[/red]")
        return
    
    syntax_type = get_syntax_type(config['path'])
    console.print(Panel(
        Syntax(content, syntax_type, theme="monokai", line_numbers=True, word_wrap=True),
        title=f"[bold cyan]📄 {config['name']}[/bold cyan] [dim]({config['path']})[/dim]",
        border_style="blue"
    ))

def export_menu(configs):
    console.print("\n[bold cyan]Export Options:[/bold cyan]")
    console.print("[1] Export current view")
    console.print("[2] Export by category")
    console.print("[3] Export selected files")
    console.print("[4] Export ALL configs")
    
    choice = Prompt.ask("Choose", choices=["1","2","3","4"])
    
    to_export = configs
    
    if choice == "2":
        categories = list(set(c['category'] for c in configs))
        for i, cat in enumerate(categories, 1):
            console.print(f"[{i}] {cat}")
        cat_choice = Prompt.ask("Category number")
        try:
            selected_cat = categories[int(cat_choice)-1]
            to_export = [c for c in configs if c['category'] == selected_cat]
        except:
            console.print("[red]Invalid choice[/red]")
            return
    
    elif choice == "3":
        indices = Prompt.ask("Enter numbers separated by comma (e.g. 1,3,5)")
        try:
            selected = [int(i.strip())-1 for i in indices.split(",")]
            to_export = [configs[i] for i in selected if 0 <= i < len(configs)]
        except:
            console.print("[red]Invalid input[/red]")
            return
    
    fmt_choice = Prompt.ask("Export Format", choices=["pdf", "html"], default="pdf")
    
    default_ext = f".{fmt_choice}"
    output_path = Prompt.ask("Output filename", default=f"configvault_export{default_ext}")
    if not output_path.endswith(default_ext):
        output_path += default_ext
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task(f"Exporting to {fmt_choice.upper()}...", total=None)
        if fmt_choice == 'pdf':
            success = export_to_pdf(to_export, output_path)
        else:
            success = export_to_html(to_export, output_path)
    
    if success:
        console.print(f"[bold green]✅ Exported {len(to_export)} configs to {output_path}[/bold green]")
    else:
        console.print("[red]Export failed![/red]")

def main():
    show_banner()
    
    include_system = Confirm.ask("Include system configs (/etc)?", default=False)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Scanning configs...", total=None)
        configs = scan_configs(include_system)
    
    console.print(f"[green]✅ Found {len(configs)} config files![/green]\n")
    show_stats(configs)
    
    current_configs = configs
    page = 0
    
    while True:
        page_configs, total_pages = show_configs_table(current_configs, page)
        
        console.print("[bold cyan]Commands:[/bold cyan]")
        console.print("(v) View  (d) Diff  (s) Search  (f) Filter  (h) Health  (e) Export  (b) Backup  (n) Next  (p) Prev  (r) Reset  (q) Quit\n")
        
        cmd = Prompt.ask("Command").strip().lower()
        
        if cmd == 'q':
            console.print("[bold blue]Goodbye! 👋[/bold blue]")
            break
        
        elif cmd == 'v':
            num = Prompt.ask("File number to view")
            try:
                idx = int(num) - 1
                if 0 <= idx < len(page_configs):
                    view_config(page_configs[idx])
                    input("\nPress Enter to continue...")
            except:
                console.print("[red]Invalid number[/red]")
        
        elif cmd == 's':
            query = Prompt.ask("Search query")
            current_configs = search_configs(configs, query)
            page = 0
            console.print(f"[green]Found {len(current_configs)} results[/green]")
        
        elif cmd == 'e':
            export_menu(current_configs)

        elif cmd == 'd':
            num1 = Prompt.ask("First file number")
            num2 = Prompt.ask("Second file number")
            try:
                c1 = page_configs[int(num1)-1]
                c2 = page_configs[int(num2)-1]
                from src.ui import show_diff
                show_diff(c1, c2)
                input("\nPress Enter to continue...")
            except Exception as e:
                console.print(f"[red]Error comparing: {e}[/red]")
        
        elif cmd == 'f':
            ext = Prompt.ask("Enter extension (e.g. .conf, .json)").strip().lower()
            if ext:
                if not ext.startswith('.'):
                    ext = '.' + ext
                current_configs = [c for c in configs if c['extension'] == ext]
                page = 0
                console.print(f"[green]Found {len(current_configs)} configs matching {ext}[/green]")
        
        elif cmd == 'b':
            if Confirm.ask("Create backup of currently shown configs?"):
                from src.backup import backup_configs
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                    task = progress.add_task("Creating ZIP backup...", total=None)
                    success, zip_path = backup_configs(current_configs)
                if success:
                    console.print(f"[bold green]✅ Backup created at: {zip_path}[/bold green]")
                else:
                    console.print(f"[red]❌ Backup failed: {zip_path}[/red]")

        elif cmd == 'h':
            from src.health import check_health
            check_health(current_configs)

        elif cmd == 'n':
            if page < total_pages - 1:
                page += 1
        
        elif cmd == 'p':
            if page > 0:
                page -= 1
        
        elif cmd == 'r':
            current_configs = configs
            page = 0

if __name__ == "__main__":
    main()

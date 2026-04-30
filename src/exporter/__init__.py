from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
from datetime import datetime
from pathlib import Path

BG_COLOR = HexColor('#1e1e2e')
TEXT_COLOR = HexColor('#cdd6f4')
ACCENT_COLOR = HexColor('#89b4fa')
GREEN_COLOR = HexColor('#a6e3a1')
YELLOW_COLOR = HexColor('#f9e2af')

def export_to_pdf(configs: list, output_path: str, title: str = "ConfigVault Export") -> bool:
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=ACCENT_COLOR,
            spaceAfter=20
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=14,
            textColor=GREEN_COLOR,
            spaceAfter=10,
            spaceBefore=20
        )
        
        meta_style = ParagraphStyle(
            'Meta',
            parent=styles['Normal'],
            fontSize=9,
            textColor=YELLOW_COLOR,
            spaceAfter=10
        )
        
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Code'],
            fontSize=8,
            textColor=TEXT_COLOR,
            fontName='Courier',
            spaceAfter=20,
            leftIndent=10
        )

        story = []
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total configs: {len(configs)}", meta_style))
        story.append(Spacer(1, 20))

        for config in configs:
            story.append(Paragraph(f"📄 {config['name']}", heading_style))
            story.append(Paragraph(
                f"Path: {config['path']} | Category: {config['category']} | Size: {config['size']} bytes | Modified: {config['modified']}",
                meta_style
            ))
            
            try:
                with open(config['path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if len(content) > 5000:
                    content = content[:5000] + "\n... (truncated)"
                story.append(Preformatted(content, code_style))
            except Exception as e:
                story.append(Paragraph(f"Could not read file: {str(e)}", meta_style))
            
            story.append(Spacer(1, 10))

        doc.build(story)
        return True
    except Exception as e:
        print(f"Export error: {e}")
        return False

def export_to_html(configs: list, output_path: str, title: str = "ConfigVault Export") -> bool:
    try:
        from rich.console import Console
        from rich.syntax import Syntax
        from src.viewer import get_syntax_type

        # We use a secondary console with record=True
        html_console = Console(record=True, width=150)
        html_console.print(f"[bold cyan]<h1>{title}</h1>[/bold cyan]", justify="center")
        html_console.print(f"[dim]Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total configs: {len(configs)}[/dim]\n")
        
        for config in configs:
            try:
                with open(config['path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                syntax_type = get_syntax_type(config['path'])
                
                html_console.print(f"[bold green]📄 {config['name']}[/bold green]")
                html_console.print(f"[dim]Path: {config['path']} | Category: {config['category']} | Size: {config['size']} bytes | Modified: {config['modified']}[/dim]")
                
                syntax = Syntax(content, syntax_type, theme="monokai", line_numbers=True, word_wrap=True)
                html_console.print(syntax)
                html_console.print("\n")
            except Exception as e:
                html_console.print(f"[red]Could not read file: {e}[/red]\n")
                
        html_content = html_console.export_html(clear=False)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"HTML Export error: {e}")
        return False
from shutil import copy2
import zipfile

def export_to_dir(configs: list, output_dir: str) -> bool:
    try:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        for config in configs:
            src = Path(config['path'])
            if src.exists():
                cat_dir = out_path / config['category']
                cat_dir.mkdir(exist_ok=True)
                dest = cat_dir / src.name
                # Avoid overwriting if multiple files have same name by appending a number
                counter = 1
                while dest.exists():
                    dest = cat_dir / f"{src.stem}_{counter}{src.suffix}"
                    counter += 1
                copy2(src, dest)
        return True
    except Exception as e:
        print(f"Directory Export error: {e}")
        return False

def export_to_zip(configs: list, output_path: str) -> bool:
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for config in configs:
                src = Path(config['path'])
                if src.exists():
                    arc_name = f"{config['category']}/{src.name}"
                    # Handle duplicate names in zip
                    counter = 1
                    base_arc = arc_name
                    while arc_name in zf.namelist():
                        arc_name = f"{config['category']}/{src.stem}_{counter}{src.suffix}"
                        counter += 1
                    zf.write(src, arc_name)
        return True
    except Exception as e:
        print(f"ZIP Export error: {e}")
        return False

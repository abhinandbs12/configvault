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

"""
Converts EasyCTET_Vision_Strategy_Malayalam.md into a beautifully formatted Word (.docx) document.
Uses Nirmala UI font for native, crisp Malayalam typography on Windows.
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

MD_PATH = r"C:\Users\Admin\Summs\EasyCTET-Branding\docs\EasyCTET_Vision_Strategy_Malayalam.md"
DOCX_OUT_1 = r"C:\Users\Admin\Summs\EasyCTET-Branding\EasyCTET-Branding\docs\EasyCTET_Vision_Strategy_Malayalam.docx"
DOCX_OUT_2 = r"C:\Users\Admin\Summs\EasyCTET-Branding\docs\EasyCTET_Vision_Strategy_Malayalam.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_styled_document():
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base font setup (Nirmala UI for crisp Malayalam rendering)
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Nirmala UI'
    font.size = Pt(11.5)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.3
    style_normal.paragraph_format.space_after = Pt(8)

    # Read Markdown
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\r\n') for line in f]

    # Title Banner
    title_p = doc.add_paragraph()
    title_run = title_p.add_run("ഡാ, നമ്മൾ ചെയ്യാൻ പോകുന്ന വലിയ കാര്യം ഇതാണ്...")
    title_run.font.name = 'Nirmala UI'
    title_run.font.size = Pt(20)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0x0B, 0x57, 0xD0)
    title_p.paragraph_format.space_after = Pt(2)

    sub_p = doc.add_paragraph()
    sub_run = sub_p.add_run("നമ്മുടെ EasyCTET പ്ലാൻ — മനസ്സുതുറന്നൊരു സംസാരം")
    sub_run.font.name = 'Nirmala UI'
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    sub_p.paragraph_format.space_after = Pt(16)

    # Divider line via a thin table or border
    div_table = doc.add_table(rows=1, cols=1)
    div_table.autofit = False
    div_table.columns[0].width = Inches(6.5)
    div_cell = div_table.cell(0, 0)
    set_cell_background(div_cell, "0B57D0")
    div_cell.paragraphs[0].paragraph_format.space_after = Pt(2)
    div_p = div_cell.paragraphs[0]
    div_p_run = div_p.add_run()
    div_p_run.font.size = Pt(2)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Process remaining content
    i = 2
    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith("# ") or line.startswith("### ("):
            i += 1
            continue

        if line == "---":
            # Subtle divider
            sep = doc.add_paragraph()
            sep.paragraph_format.space_before = Pt(8)
            sep.paragraph_format.space_after = Pt(8)
            i += 1
            continue

        if line.startswith("### "):
            # Heading 2 style
            h_text = line[4:].strip()
            hp = doc.add_paragraph()
            hp.paragraph_format.space_before = Pt(14)
            hp.paragraph_format.space_after = Pt(6)
            hrun = hp.add_run(h_text)
            hrun.font.name = 'Nirmala UI'
            hrun.font.size = Pt(14)
            hrun.font.bold = True
            hrun.font.color.rgb = RGBColor(0x0B, 0x57, 0xD0)
            i += 1
            continue

        if line.startswith("* **") or line.startswith("- **"):
            # Sub-bullet / bold header
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(4)
            content = line[2:].strip()
            # Parse bold parts
            parts = content.split("**")
            for idx, part in enumerate(parts):
                run = bp.add_run(part)
                run.font.name = 'Nirmala UI'
                if idx % 2 == 1:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
            i += 1
            continue

        if line.startswith("* ") or line.startswith("- "):
            # Normal bullet
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(4)
            content = line[2:].strip()
            parts = content.split("**")
            for idx, part in enumerate(parts):
                run = bp.add_run(part)
                run.font.name = 'Nirmala UI'
                if idx % 2 == 1:
                    run.font.bold = True
            i += 1
            continue

        # Regular paragraph or callout
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)

        parts = line.split("**")
        for idx, part in enumerate(parts):
            run = p.add_run(part)
            run.font.name = 'Nirmala UI'
            if idx % 2 == 1:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        i += 1

    # Save to both locations
    os.makedirs(os.path.dirname(DOCX_OUT_1), exist_ok=True)
    os.makedirs(os.path.dirname(DOCX_OUT_2), exist_ok=True)
    doc.save(DOCX_OUT_1)
    doc.save(DOCX_OUT_2)
    print(f"[OK] Word document successfully created at:\n  1. {DOCX_OUT_1}\n  2. {DOCX_OUT_2}")

if __name__ == "__main__":
    create_styled_document()

"""
Page header generator for DOCX documents
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import logging

logger = logging.getLogger(__name__)


def add_page_header(
        docx_path: str,
        header_text: str,
        skip_first_page: bool = True,
        font_name: str = 'Arial',
        font_size: int = 10,
        bold: bool = False,
        italic: bool = True,
        color: tuple[int, int, int] = (128, 128, 128),  # Gray
        alignment: str = 'left',
        add_bottom_border: bool = True,
) -> None:
    """
    Add a page header to all pages in the document.

    Args:
        docx_path: Path to the DOCX file
        header_text: Text to display in the header
        skip_first_page: If True, first page won't have header (default: True)
        font_name: Font name (default: Arial)
        font_size: Font size in points (default: 10)
        bold: Whether text is bold (default: False)
        italic: Whether text is italic (default: True)
        color: RGB color tuple (default: gray)
        alignment: Text alignment - 'left', 'center', 'right' (default: 'left')
        add_bottom_border: Whether to add a bottom border line (default: True)
    """
    try:
        doc = Document(docx_path)

        alignment_map = {
            'left': WD_PARAGRAPH_ALIGNMENT.LEFT,
            'center': WD_PARAGRAPH_ALIGNMENT.CENTER,
            'right': WD_PARAGRAPH_ALIGNMENT.RIGHT,
        }

        for section in doc.sections:
            # Enable different first page header/footer
            if skip_first_page:
                section.different_first_page_header_footer = True
                # First page header remains empty (no content added)

            # Get the default header (used for all pages except first if different_first_page is True)
            header = section.header

            # Clear existing header content
            for paragraph in header.paragraphs:
                paragraph.clear()

            # Add header text
            if header.paragraphs:
                para = header.paragraphs[0]
            else:
                para = header.add_paragraph()

            run = para.add_run(header_text)
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = RGBColor(*color)

            para.alignment = alignment_map.get(alignment, WD_PARAGRAPH_ALIGNMENT.LEFT)

            # Add bottom border to header paragraph
            if add_bottom_border:
                _add_header_bottom_border(para)

        doc.save(docx_path)
        logger.info(f"Page header added to: {docx_path}")

    except Exception as e:
        logger.error(f"Failed to add page header: {e}")
        raise


def _add_header_bottom_border(paragraph) -> None:
    """
    Add a bottom border line to the header paragraph
    """
    pPr = paragraph._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')

    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')  # Border width
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'CCCCCC')  # Light gray

    pBdr.append(bottom)
    pPr.append(pBdr)

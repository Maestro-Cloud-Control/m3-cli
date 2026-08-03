import pypandoc
from m3cli.docs.md_to_docx.custom_styles import apply_custom_styles
from m3cli.docs.commons.m3_preprocessor import replace_page_breaks_md
from m3cli.docs.commons import create_logger

_LOG = create_logger()


def convert_md_to_docx(md_file, docx_file):
    try:
        with open(md_file, "r", encoding="utf-8") as f:
            md_text = f.read()

        # Replace page break markers before Pandoc strips comments
        md_text = replace_page_breaks_md(md_text)
        _LOG.debug(f"Page break markers replaced for: {md_file}")

        # Convert from the in-memory string, leaving the source file untouched
        pypandoc.convert_text(
            source=md_text, to='docx', format='md', outputfile=docx_file
        )
        _LOG.info(f"Successfully converted: {md_file} to: {docx_file}")
    except Exception as e:
        _LOG.error(f"Failed to convert {md_file} to DOCX: {e}")
        raise

    try:
        # Apply custom styles to the newly created DOCX file
        apply_custom_styles(docx_file)
        _LOG.info(f"Custom styles applied successfully to: {docx_file}")
    except Exception as e:
        _LOG.error(f"Failed to apply custom styles to: {docx_file}: {e}")
        raise

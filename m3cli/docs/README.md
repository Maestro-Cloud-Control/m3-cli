# Guide for Generating Technical Documentation

This guide provides steps for generating technical documentation in both `.md` and `.docx` formats. The `.docx` format allows for final adjustments before manual conversion to `.pdf`.

## Prerequisites

1. **Download and Install Required Software:**
   - Download and install `pandoc`, a universal document converter.
     - Visit the Pandoc official website: [https://pandoc.org/](https://pandoc.org/)
     - Follow the instructions on the website to download and install Pandoc on your computer.

2. **Install Dependencies:**
   - Use the `requirements.txt` file located at `m3-cli\m3cli\docs\requirements.txt` to install the necessary packages:
     ```console
     pip install -r m3-cli\m3cli\docs\requirements.txt
     ```

## Generate Documentation

### M3 Usage Guide

Converts the setup guide markdown to a formatted DOCX document.

```console
py <path_to>\m3-cli\m3cli\docs\usage_docx.py --help
py <path_to>\m3-cli\m3cli\docs\usage_docx.py -name m3 -res_path <path_to>\m3-cli
```

**Full Example:**
```console
py C:\Maestro3\m3-cli\m3cli\docs\usage_docx.py -name m3 -res_path C:\Maestro3\m3-cli --cli-version "m3, version 4.158.1" --changelog-url "https://github.com/Maestro-Cloud-Control/m3-cli/blob/main/CHANGELOG.md" --header-text "M3 CLI – Usage Guide" --page-number-align right
```

### M3 Reference Guide

Generates documentation from CLI commands defined in `commands_def.json`.

```console
py <path_to>\m3-cli\m3cli\docs\cli_to_docx.py --help
py <path_to>\m3-cli\m3cli\docs\cli_to_docx.py -name m3 -cmd_path <path_to>\m3-cli\m3cli\commands_def.json -res_path <path_to>\m3-cli
```

**Full Example:**
```console
py C:\Maestro3\m3-cli\m3cli\docs\cli_to_docx.py -name m3 -cmd_path C:\Maestro3\m3-cli\m3cli\commands_def.json -res_path C:\Maestro3\m3-cli --header-text "M3 CLI – Reference Guide" --changelog-url "https://github.com/Maestro-Cloud-Control/m3-cli/blob/main/CHANGELOG.md"   
```

### M3 Developer Guide

Converts the developer guide markdown to a formatted DOCX document.

```console
py <path_to>\m3-cli\m3cli\docs\dev_guide_docx.py --help
py <path_to>\m3-cli\m3cli\docs\dev_guide_docx.py -name m3 -res_path <path_to>\m3-cli
```

**Full Example:**
```console
py C:\Maestro3\m3-cli\m3cli\docs\dev_guide_docx.py -name m3 -res_path C:\Maestro3\m3-cli --header-text "M3 CLI – Developer's Guide" --changelog-url "https://github.com/Maestro-Cloud-Control/m3-cli/blob/main/CHANGELOG.md"   
```

### Raw Markdown Only

Generate only the raw markdown file without DOCX conversion.

```console
py <path_to>\m3-cli\m3cli\docs\cli_to_md.py -name m3 -cmd_path <path_to>\m3-cli\m3cli\commands_def.json -res_path <path_to>\m3-cli
```

## Common Options

All DOCX generators (Usage Guide, Reference Guide, Developer Guide) support the following options:

### Page Numbers

| Argument | Description |
|----------|-------------|
| `--no-page-numbers` | Skip adding page numbers |
| `--page-number-format` | Page number format (see table below) |
| `--page-number-align` | Alignment: `left`, `center`, `right` (default: `right`) |
| `--page-number-custom` | Custom format using `{page}` and `{total}` placeholders |

**Page Number Formats:**

| Format | Example Output |
|--------|----------------|
| `simple` | 1, 2, 3... |
| `page_x` | Page 1, Page 2... |
| `page_x_of_y` | Page 1 of 10, Page 2 of 10... |
| `x_of_y` | 1 of 10, 2 of 10... |
| `dash` | - 1 -, - 2 -... |
| `dash_total` | - 1 of 10 -, - 2 of 10 -... |

**Examples:**
```console
# "Page X of Y" format, right-aligned
--page-number-format page_x_of_y --page-number-align right

# Custom format
--page-number-custom "[ {page} / {total} ]"
```

### Page Header

| Argument | Description |
|----------|-------------|
| `--header-text` | Text for page header |
| `--header-align` | Alignment: `left`, `center` (default), `right` |
| `--no-header-skip-first` | Include header on first page (default: skip) |

**Examples:**
```console
--header-text "M3 CLI – User Guide"
--header-text "M3 CLI – Reference Guide" --header-align right
```

### Last Page (Version History)

| Argument | Description |
|----------|-------------|
| `--changelog-url` | URL to the changelog (e.g., GitHub CHANGELOG.md URL) |
| `--changelog-path` | Local path to the changelog file |
| `--cli-version` | CLI version string (auto-detected if not provided) |
| `--no-last-page` | Skip adding the last page with version history |

The last page includes:
- **Version History** heading
- **Version History table** (with Version, Date, Summary columns)
- **Changelog link** (if provided)
- **CLI version** (auto-detected or manually specified)

**Examples:**
```console
# With changelog URL
--changelog-url "https://github.com/Maestro-Cloud-Control/m3-cli/blob/main/CHANGELOG.md"

# With local changelog path
--changelog-path "C:\Maestro3\m3-cli\CHANGELOG.md"

# With explicit CLI version
--cli-version "m3, version 4.158.0"

# Skip last page entirely
--no-last-page
```

## Output Files

The scripts generate DOCX files in the specified output directory:

| Document Type | Output File |
|---------------|-------------|
| M3 Usage Guide | `<res_path>/<tool_name>_usage_guide.docx` |
| M3 Reference Guide | `<res_path>/<tool_name>_reference_guide.docx` |
| M3 Developer Guide | `<res_path>/<tool_name>_developer_guide.docx` |
| Raw Markdown | `<res_path>/<tool_name>.md` |

## Converting DOCX to PDF

After generating DOCX files, convert them to PDF manually using Microsoft Word:

1. Open the generated `.docx` file in Microsoft Word
2. Review and make any final adjustments if needed
3. Go to **File** → **Save As** (or **Export**)
4. Select **PDF** as the file format
5. Click **Save**

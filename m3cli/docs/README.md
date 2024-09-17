# Guide for Generating Technical Documentation

This guide provides steps for generating technical documentation in both `.md` and `.docx` formats. The `.docx` format offers a flexible way to adjust and create `.pdf` files.

## Steps to Generate Documentation

1. **Download and Install Required Software:**
   - Begin by downloading `pandoc`, a universal document converter.
     - Visit the Pandoc official website: [https://pandoc.org/](https://pandoc.org/)
     - Follow the instructions on the website to download and install Pandoc on your computer.
   - Next, download `LaTeX`, a document preparation system.
     - Go to the LaTeX Project website: [https://miktex.org/](https://miktex.org/)
     - Choose the appropriate version for your operating system and follow the installation guide provided on the site.

2. **Install Dependencies:**
   - Use the `requirements.txt` file located at `m3-cli\m3cli\docs\requirements.txt` to install the necessary packages into the current virtual environment.

3. **Generate Documentation:**
   - **M3 Usage Guide:**
     ```console
     py <path_to>\m3-cli\m3cli\docs\usage_docx.py --help
     py <path_to>\m3-cli\m3cli\docs\usage_docx.py -name m3 -res_path <path_to>\m3-cli
     py C:\Maestro3\m3-cli\m3cli\docs\usage_docx.py -name m3 -res_path C:\Maestro3\m3-cli
     ```

   - **M3 Reference Guide:**
     ```console
     py <path_to>\m3-cli\m3cli\docs\cli_to_docx.py --help
     py <path_to>\m3-cli\m3cli\docs\cli_to_docx.py -name m3 -cmd_path <path_to>\m3-cli\m3cli\commands_def.json -res_path <path_to>\m3-cli
     py C:\Maestro3\m3-cli\m3cli\docs\cli_to_docx.py -name m3 -cmd_path C:\Maestro3\m3-cli\m3cli\commands_def.json -res_path C:\Maestro3\m3-cli
     ```

   - **Generate Raw `m3.md`:**
     ```console
     py <path_to>\m3-cli\m3cli\docs\cli_to_md.py --help
     py <path_to>\m3-cli\m3cli\docs\cli_to_md.py -name m3 -cmd_path <path_to>\m3-cli\m3cli\commands_def.json -res_path <path_to>\m3-cli
     py C:\Maestro3\m3-cli\m3cli\docs\cli_to_md.py -name m3 -cmd_path C:\Maestro3\m3-cli\m3cli\commands_def.json -res_path C:\Maestro3\m3-cli
     ```

The generated documents will be saved in the directory specified by the `-res_path` parameter, e.g., `<path_to>\m3-cli`.

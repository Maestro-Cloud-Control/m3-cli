# CHANGELOG

# [1.0.2] - 2026-06-22
* Add an ability to set commented pagebreaks `[//]: # ({{ pagebreak }})`
* Change `Introduction` to the `Preface`
* Regenerate docs:
  * `m3-cli\m3cli\docs\generated_docs\m3_developer_guide.docx`
  * `m3-cli\m3cli\docs\generated_docs\m3_reference_guide.docx`
  * `m3-cli\m3cli\docs\generated_docs\m3_usage_guide.docx`

# [1.0.1] - 2026-01-12
* Add page numbering feature to Reference Guide with multiple format options (`simple`, `page_x`, `page_x_of_y`, `x_of_y`, `dash`, `dash_total`)
* Add custom page number format support using `{page}` and `{total}` placeholders
* Add page number alignment options (`center`, `left`, `right`)
* Add last page with version history, changelog link, and CLI version auto-detection
* Add `--no-page-numbers` and `--no-last-page` flags to skip optional document sections

# [1.0.0] - 2025-10-07
* Initial release of the docs generator

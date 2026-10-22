# AGENTS.md

## Repository Guidelines

### Script Placement Rule
* **Put scripts you run into the `/scripts` folder.** Any helper scripts, data scraping scripts, or analysis utilities must reside inside the `scripts/` directory at the project root rather than cluttering the root directory or `src/`.

### Project & Folder Conventions
* **`/scripts`**: Python automation, data processing, and scraping scripts.
* **`/report`**: LaTeX source files (`.tex`), figures, and final compilation outputs for the report.
* **`/docs`**: Qualitative notes, research findings, and analytical write-ups.
* **`/data`**: Extracted CSVs, JSON manifest files, parsed datasets, or quantitative summaries.

### Technical Stack
* Package management is handled via `uv` (`pyproject.toml` and `uv.lock`). Use `uv run` to execute scripts.
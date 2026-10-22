# Credit Suisse Archive Downloader (`fraud1`)

A robust scraper and downloader for the Credit Suisse financial archive on the UBS Investor Relations portal.

## Overview

This project scrapes the UBS Credit Suisse archive page:
`https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-entities/archive-credit-suisse.html`

It extracts document metadata (titles, years, categories, and direct asset URLs) and downloads historical financial statements, Annual Reports (Form 20-F), Pillar 3 disclosures, 6-K filings, and financial reviews.

## Requirements

- Python >= 3.14
- `uv` package manager
- macOS / Linux `curl` (used for Akamai-compliant HTTP/2 document streaming)

## Usage

### Run the downloader

```bash
uv run fraud1
```

Or run via the scraper module:
```bash
uv run python -m fraud1.scraper
```

### Options

```bash
# Limit the number of documents to download (e.g. for testing)
uv run fraud1 --limit=10

# Change concurrency level (default is 8 workers)
uv run fraud1 --workers=12
```

## Output

Files are stored in:
- `credit_suisse_archive_downloads/`: Downloaded documents (`.pdf`, `.zip`, `.xlsx`).
- `credit_suisse_archive_downloads/manifest.json`: JSON metadata mapping document titles to local filenames, file sizes, statuses, and source URLs.
- `credit_suisse_archive_downloads/manifest.csv`: Tabular CSV version of the catalog.

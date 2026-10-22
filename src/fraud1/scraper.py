import csv
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import unquote, urljoin, urlparse

from bs4 import BeautifulSoup

ARCHIVE_URL = (
    "https://www.ubs.com/global/en/investor-relations/complementary-financial-information/"
    "disclosure-legal-entities/archive-credit-suisse.html"
)
OUTPUT_DIR = "credit_suisse_archive_downloads"
MANIFEST_JSON = os.path.join(OUTPUT_DIR, "manifest.json")
MANIFEST_CSV = os.path.join(OUTPUT_DIR, "manifest.csv")
ALLOWED_EXTENSIONS = {".pdf", ".zip", ".xlsx", ".xls", ".docx", ".csv"}


def fetch_url(url: str) -> str:
    """Fetch URL text using native curl with HTTP/2 (avoids Akamai TLS fingerprint mismatch)."""
    cmd = [
        "curl",
        "-sSL",
        "--retry", "3",
        "--retry-delay", "1",
        "--max-time", "30",
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"curl failed with code {proc.returncode}: {proc.stderr}")
    return proc.stdout


def sanitize_filename(name: str) -> str:
    name = unquote(name)
    name = re.sub(r'[\\/*?:"<>|]', "_", name).strip()
    return name


def collect_document_metadata() -> list[dict]:
    """Scrape archive page and extract document links, titles, and filenames."""
    print(f"Fetching archive page: {ARCHIVE_URL}")
    html_content = fetch_url(ARCHIVE_URL)
    soup = BeautifulSoup(html_content, "html.parser")

    documents = []
    seen_urls = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue

        full_url = urljoin(ARCHIVE_URL, href)
        if full_url in seen_urls:
            continue

        parsed = urlparse(full_url)
        path = parsed.path
        ext = os.path.splitext(path)[1].lower()

        if ext in ALLOWED_EXTENSIONS or "/dam/" in full_url.lower():
            # Must be a document path
            if ext not in ALLOWED_EXTENSIONS and not any(
                full_url.lower().endswith(e) for e in ALLOWED_EXTENSIONS
            ):
                continue

            seen_urls.add(full_url)

            # Extract title / description
            title = a_tag.get_text(separator=" ", strip=True)
            title = re.sub(r"\(PDF,\s*[\d.]+\s*[KMGT]?B\)", "", title, flags=re.IGNORECASE).strip()

            raw_filename = os.path.basename(path)
            if not raw_filename or "." not in raw_filename:
                raw_filename = f"doc_{len(documents) + 1}.pdf"

            filename = sanitize_filename(raw_filename)

            documents.append({
                "index": len(documents) + 1,
                "title": title or filename,
                "url": full_url,
                "filename": filename,
            })

    # Avoid duplicate filenames in output directory
    filename_counts: dict[str, int] = {}
    for doc in documents:
        fn = doc["filename"]
        if fn in filename_counts:
            filename_counts[fn] += 1
            name, ext = os.path.splitext(fn)
            doc["filename"] = f"{name}_{filename_counts[fn]}{ext}"
        else:
            filename_counts[fn] = 1

    return documents


def download_single_file(doc: dict, total: int) -> dict:
    """Download a single document via curl."""
    url = doc["url"]
    filename = doc["filename"]
    filepath = os.path.join(OUTPUT_DIR, filename)
    idx = doc["index"]

    # Check if already downloaded and non-empty
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        doc["status"] = "skipped"
        doc["filepath"] = filepath
        doc["size"] = os.path.getsize(filepath)
        return doc

    temp_filepath = f"{filepath}.part"
    cmd = [
        "curl",
        "-sSL",
        "--retry", "3",
        "--retry-delay", "1",
        "--max-time", "120",
        "-o", temp_filepath,
        url,
    ]
    proc = subprocess.run(cmd, check=False)
    if proc.returncode == 0 and os.path.exists(temp_filepath) and os.path.getsize(temp_filepath) > 0:
        os.replace(temp_filepath, filepath)
        size = os.path.getsize(filepath)
        doc["status"] = "downloaded"
        doc["filepath"] = filepath
        doc["size"] = size
        print(f"[{idx}/{total}] Saved: {filename} ({size / 1024:.1f} KB)")
    else:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        doc["status"] = "failed"
        doc["filepath"] = None
        doc["size"] = 0
        print(f"[{idx}/{total}] FAILED: {filename}")

    return doc


def run(max_workers: int = 8, limit: int | None = None) -> None:
    # Parse CLI flags if passed
    for arg in sys.argv[1:]:
        if arg.startswith("--limit="):
            limit = int(arg.split("=")[1])
        elif arg.startswith("--workers="):
            max_workers = int(arg.split("=")[1])

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Collecting document metadata from UBS Credit Suisse archive...")
    documents = collect_document_metadata()
    total = len(documents)
    print(f"Found {total} candidate documents.")

    if limit:
        documents = documents[:limit]
        total = len(documents)
        print(f"Applying limit: downloading first {limit} documents.")

    if total == 0:
        print("No documents found.")
        return

    # Check already existing
    already_have = sum(
        1 for d in documents
        if os.path.exists(os.path.join(OUTPUT_DIR, d["filename"]))
        and os.path.getsize(os.path.join(OUTPUT_DIR, d["filename"])) > 0
    )
    if already_have > 0:
        print(f"Found {already_have}/{total} files already downloaded in {OUTPUT_DIR}.")

    print(f"Starting downloads ({max_workers} worker threads)...")
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_single_file, doc, total): doc for doc in documents}
        for future in as_completed(futures):
            results.append(future.result())

    # Write JSON manifest
    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)

    # Write CSV manifest
    with open(MANIFEST_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["index", "title", "filename", "size", "status", "url"])
        writer.writeheader()
        for doc in documents:
            writer.writerow({
                "index": doc.get("index"),
                "title": doc.get("title"),
                "filename": doc.get("filename"),
                "size": doc.get("size", 0),
                "status": doc.get("status", "unknown"),
                "url": doc.get("url"),
            })

    downloaded = sum(1 for r in results if r.get("status") == "downloaded")
    skipped = sum(1 for r in results if r.get("status") == "skipped")
    failed = sum(1 for r in results if r.get("status") == "failed")
    total_bytes = sum(r.get("size", 0) for r in results if r.get("status") in ("downloaded", "skipped"))

    print("\n" + "=" * 55)
    print("Download Summary:")
    print(f"  Total archive documents: {total}")
    print(f"  Newly downloaded:        {downloaded}")
    print(f"  Already present:         {skipped}")
    print(f"  Failed:                  {failed}")
    print(f"  Total size on disk:      {total_bytes / (1024 * 1024):.2f} MB")
    print(f"  Directory:               {os.path.abspath(OUTPUT_DIR)}")
    print(f"  Manifest (JSON):         {os.path.abspath(MANIFEST_JSON)}")
    print(f"  Manifest (CSV):          {os.path.abspath(MANIFEST_CSV)}")
    print("=" * 55)


if __name__ == "__main__":
    run()

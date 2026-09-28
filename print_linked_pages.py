"""Save linked web pages from an HTML file as individual PDFs.

Uses an installed Edge or Chrome browser and Python's standard library.
Run with --dry-run first to review the URLs and output filenames.
Only save pages you are authorized to copy.
"""

from __future__ import annotations

import argparse
import csv
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from urllib.parse import parse_qs, unquote, urldefrag, urljoin, urlparse


class LinkCollector(HTMLParser):
    def __init__(self, required_class: str | None):
        super().__init__()
        self.required_class = required_class
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        values = dict(attrs)
        if self.required_class and self.required_class not in (values.get("class") or "").split():
            return
        if values.get("href"):
            self.hrefs.append(values["href"])


def find_browser(requested: Path | None) -> Path:
    candidates = [requested] if requested else [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate and candidate.is_file():
            return candidate
    raise SystemExit("No browser found. Pass --browser with the path to Edge or Chrome.")


def collect_urls(source: Path, required_class: str | None, domain: str | None) -> list[str]:
    parser = LinkCollector(required_class)
    parser.feed(source.read_text(encoding="utf-8-sig"))
    base = source.resolve().as_uri()
    seen: set[str] = set()
    urls: list[str] = []
    for href in parser.hrefs:
        url, _fragment = urldefrag(urljoin(base, href))
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            continue
        if domain and parsed.hostname != domain and not (parsed.hostname or "").endswith("." + domain):
            continue
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def filename_for(url: str, ordinal: int) -> str:
    parsed = urlparse(url)
    title = parse_qs(parsed.query).get("title", [""])[0]
    description = unquote(title or parsed.path.strip("/") or parsed.hostname or "page")
    description = re.sub(r"[^\w.-]+", "_", description, flags=re.UNICODE).strip("._")
    description = description[:125] or "page"
    return f"{ordinal:03d}_{description}.pdf"


def print_page(browser: Path, url: str, destination: Path, profile: Path, timeout: int) -> None:
    command = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={profile}",
        "--virtual-time-budget=10000",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={destination.resolve()}",
        url,
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0 or not destination.is_file() or destination.stat().st_size < 100:
        detail = (result.stderr or result.stdout).strip()[-500:]
        raise RuntimeError(detail or f"Browser exited with code {result.returncode}")
    with destination.open("rb") as pdf:
        if pdf.read(5) != b"%PDF-":
            raise RuntimeError("Browser output is not a PDF")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", type=Path, help="Input HTML file")
    ap.add_argument("output_dir", type=Path, help="Directory for PDF files")
    ap.add_argument("--link-class", help="Only use anchors with this CSS class")
    ap.add_argument("--domain", help="Only use links from this hostname or its subdomains")
    ap.add_argument("--browser", type=Path, help="Path to Edge or Chrome executable")
    ap.add_argument("--delay", type=float, default=3.0, help="Seconds between pages (default: 3)")
    ap.add_argument("--timeout", type=int, default=120, help="Seconds per page (default: 120)")
    ap.add_argument("--dry-run", action="store_true", help="List files and URLs without printing")
    args = ap.parse_args()

    if not args.html.is_file():
        ap.error(f"HTML file not found: {args.html}")
    if args.delay < 0 or args.timeout < 1:
        ap.error("--delay must be nonnegative and --timeout must be positive")
    urls = collect_urls(args.html, args.link_class, args.domain)
    jobs = [(url, filename_for(url, i)) for i, url in enumerate(urls, 1)]
    print(f"Found {len(jobs)} unique web pages.")
    if args.dry_run:
        for url, name in jobs:
            print(f"{name}\t{url}")
        return 0

    browser = find_browser(args.browser)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str, str]] = []
    with tempfile.TemporaryDirectory(prefix="linked_pages_browser_") as tmp:
        profile = Path(tmp) / "profile"
        for i, (url, name) in enumerate(jobs, 1):
            destination = args.output_dir / name
            try:
                print_page(browser, url, destination, profile, args.timeout)
                status = "saved"
            except (OSError, subprocess.TimeoutExpired, RuntimeError) as exc:
                destination.unlink(missing_ok=True)
                status = f"failed: {exc}"
            results.append((name, url, status))
            print(f"[{i}/{len(jobs)}] {status}: {name}", flush=True)
            if i < len(jobs):
                time.sleep(args.delay)

    manifest = args.output_dir / "print_manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("pdf_file", "source_url", "status"))
        writer.writerows(results)
    failed = sum(status.startswith("failed") for _, _, status in results)
    print(f"Finished: {len(jobs) - failed} PDFs saved, {failed} failed. Manifest: {manifest}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

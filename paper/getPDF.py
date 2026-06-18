#!/usr/bin/env python3
"""Download arXiv PDFs for the TAC-Graph literature index.

Reads ``index.csv`` in this folder and downloads each paper's PDF from
arXiv into the same folder, naming it after the ``pdf_filename`` column
(falling back to ``<arxiv_id>.pdf``). Already-present, non-empty files are
skipped so the script is safe to re-run / resume.

Usage:
    python3 getPDF.py                # download everything missing
    python3 getPDF.py --force        # re-download even if present
    python3 getPDF.py --list         # just print what would be fetched

Network only; no heavy compute (safe on a login node).
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "index.csv")
ARXIV_PDF = "https://arxiv.org/pdf/{id}"
HEADERS = {"User-Agent": "Mozilla/5.0 (TAC-Graph litreview getPDF.py)"}


def load_rows() -> list[dict]:
    if not os.path.exists(CSV_PATH):
        sys.exit(f"index.csv not found at {CSV_PATH}")
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r.get("arxiv_id")]


def target_name(row: dict) -> str:
    return row.get("pdf_filename") or f"{row['arxiv_id']}.pdf"


def download(arxiv_id: str, dest: str, retries: int = 3) -> bool:
    url = ARXIV_PDF.format(id=arxiv_id)
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if len(data) < 1024:
                raise ValueError(f"suspiciously small response ({len(data)} bytes)")
            with open(dest, "wb") as out:
                out.write(data)
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"  attempt {attempt}/{retries} failed for {arxiv_id}: {exc}")
            time.sleep(2 * attempt)
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-download even if file exists")
    ap.add_argument("--list", action="store_true", help="only list targets, do not download")
    args = ap.parse_args()

    rows = load_rows()
    print(f"{len(rows)} papers in index.csv")
    ok = skipped = failed = 0
    for row in rows:
        arxiv_id = row["arxiv_id"].strip()
        dest = os.path.join(HERE, target_name(row))
        if args.list:
            print(f"  {arxiv_id} -> {os.path.basename(dest)}")
            continue
        if (not args.force) and os.path.exists(dest) and os.path.getsize(dest) > 1024:
            skipped += 1
            continue
        print(f"downloading {arxiv_id} -> {os.path.basename(dest)}")
        if download(arxiv_id, dest):
            ok += 1
        else:
            failed += 1
        time.sleep(1)  # be polite to arXiv
    if not args.list:
        print(f"\ndone: {ok} downloaded, {skipped} already present, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

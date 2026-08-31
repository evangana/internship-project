import pymupdf
#import pdfplumber
#import pandas as pd
import json
#import re
from pathlib import Path

#from headings import detect_headings
from images import extract_images
from tables import extract_tables
from products import extract_products
from build_catalogue import build_catalogue

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_FILE = BASE_DIR / "source_documents" / "catalogue.pdf"

#IMAGE_DIR = Path("images")
#IMAGE_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

doc = pymupdf.open(PDF_FILE)

images = extract_images(doc)
tables = extract_tables(PDF_FILE)


# ============================================================
# TESTING
# Uncomment this section when you want to test product parsing
# on individual tables.
# ============================================================

# print(f"Tables found: {len(tables)}")

# for table_info in tables:
#     print(f"\n--- Testing table on page {table_info['page']} ---")

#     # table = table_info["table"]

#     products = extract_products(table_info["table"])

#     if products:
#         print(f"\n--- Products found on page {table_info['page']} ---")
#         print(f"Products: {len(products)}")
#         print(products[:3])
#         break


# ============================================================
# BUILD COMPLETE CATALOGUE
# ============================================================

catalogue = build_catalogue(doc, images, tables)

OUTPUT_FILE = OUTPUT_DIR / "catalogue.json"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(catalogue, f, ensure_ascii=False, indent=2)

print(f"Catalogue saved to {OUTPUT_FILE}")
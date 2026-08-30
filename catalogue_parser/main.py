import pymupdf
#import pdfplumber
#import pandas as pd
import json
#import re
from pathlib import Path

#from headings import detect_headings
from images import extract_images
from tables import extract_tables
#from products import extract_products
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

# print(f"Tables found: {len(tables)}")

# for table_info in tables:
#     print(f"\n--- Table on page {table_info['page']} ---")
#     print(table_info["dataframe"])

from products import extract_products

print(f"Tables found: {len(tables)}")

for table_info in tables[:5]:
  print(f"\n--- Testing table on page {table_info['page']} ---")

  df = table_info["dataframe"]

  print("Columns:")
  print(df.columns.tolist())

  products = extract_products(df)

  print(f"Products found: {len(products)}")

  if products:
      print(products[0])

catalogue = build_catalogue(doc, images, tables)

OUTPUT_FILE = OUTPUT_DIR / "catalogue.json"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(catalogue, f, ensure_ascii=False, indent=2)

print(f"Catalogue saved to {OUTPUT_FILE}")
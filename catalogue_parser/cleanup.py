import json
import pandas as pd
from pathlib import Path

#File paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "output" / "catalogue.json"
OUTPUT_FILE = BASE_DIR / "output" / "clean_catalogue.json"

#Load Catalogues
with open(INPUT_FILE, "r", encoding="utf-8") as f:
  data = json.load(f)

print("Catalogue Cleanup")
print("=======================")

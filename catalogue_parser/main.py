import fitz
import pdfplumber
import pandas as pd
import json
import re
from pathlib import Path

#from images import extract_images

PDF_FILE = Path("source_documents/catalogue.pdf")
IMAGE_DIR = Path("images")

IMAGE_DIR.mkdir(exist_ok=True)

catalogue = {}


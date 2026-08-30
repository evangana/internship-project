import pdfplumber
import pandas as pd

def extract_tables(pdf_file):
  tables = []
  with pdfplumber.open(pdf_file) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
      page_tables = page.extract_tables()
      for table in page_tables:
        if not table:
          continue
        headers = table[0]
        rows = table[1:]
        df = pd.DataFrame(rows, columns=headers)
        tables.append({
          "page": page_num,
          "table": table,
          "dataframe": df
        })
  return tables
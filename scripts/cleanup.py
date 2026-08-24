import json
import pandas as pd

with open("catalogue_extraction.json", "r", encoding="utf-8") as file:
    data = json.load(file)

rows = []

for page_number, page in enumerate(data["Pages"], start=1):
    for text_item in page.get("Texts", []):

        text = "".join(
            run.get("T", "")
            for run in text_item.get("R", [])
        ).strip()

        if text:
            rows.append({
                "page_number": page_number,
                "x": text_item.get("x"),
                "y": text_item.get("y"),
                "text": text
            })

df = pd.DataFrame(rows)

df.to_csv("catalogue_text_clean.csv", index=False)

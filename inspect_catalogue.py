import pymupdf
from typing import Any, cast

doc = pymupdf.open("source_documents/catalogue.pdf")
page = doc[0]

data = cast(dict[str, Any], page.get_text("dict"))

for block in data["blocks"]:
    if block["type"] != 0:
        continue

    for line in block["lines"]:
        for span in line["spans"]:
            print(
                f"Size={span['size']:.1f} "
                f"Font={span['font']} "
                f"Text={span['text']}"
            )
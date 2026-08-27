def detect_headings(page_dict):
  headings = []

  for block in page_dict["blocks"]:
    if block["type"] != 0:
      continue

    for line in block["lines"]:
      text = ""
      max_size = 0

      for span in line["spans"]:
        text += span ["text"]
        max_size = max(max_size, span["size"])

      text = text.strip()

      if not text:
        continue

      if max_size >= 12:
        headings.append({
          "text": text,
          "y": line["bbox"][1],
        })
  return headings
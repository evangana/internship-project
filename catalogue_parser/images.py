def extract_images(doc):
  images = []

  for page_num in range(len(doc)):
    page = doc[page_num]

    for idx, img in enumerate(page.get_images(full=True)):
      #xref = img[0]
      #image = doc.extract_image(xref)

      #ext = image["ext"]

      #filename = image_dir / f"page{page_num + 1}_img_{idx + 1}.{ext}"
      #with open(filename, "wb") as f:
      #  f.write(image["image"])

      
      images.append({
        "page": page_num + 1,
        "xref": img[0],
        "index": idx + 1,
        #"filename": str(filename),
      })
  return images
from headings import detect_headings
from products import extract_products

def build_catalogue(doc, images, tables):
  #Build page structure
  page_structure = []

  for page_num in range(len(doc)):
    page = doc[page_num]
    page_dict = page.get_text("dict")
    headings = detect_headings(page_dict)
    page_structure.append({
      "page": page_num + 1,
      "headings": headings,
    })

  #build catalogue hierarchy
  catalogue = {}
  current_heading = "Uncategorized"

  for page_info in page_structure:
    page_num = page_info["page"]
    if page_info["headings"]:
      current_heading = page_info["headings"][0]["text"]

    catalogue.setdefault(current_heading, {
      "images": [],
      "products": [],
      "text": [],
    })
    #Add images for the current page
    page_images = [
      image for image in images
      if image["page"] == page_num
    ]
    catalogue[current_heading]["images"].extend(page_images)

    #Add products from tables on this page
    page_tables = [
      table for table in tables
      if table["page"] == page_num
    ]

    for table_info in page_tables:
      products = extract_products(table_info["table"])
      catalogue[current_heading]["products"].extend(products)

  return catalogue
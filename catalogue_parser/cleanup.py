import json
from pathlib import Path
from rules import check_part_number_quality

#File paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "output" / "catalogue.json"
OUTPUT_FILE = BASE_DIR / "output" / "clean_catalogue.json"

#Load Catalogues
with open(INPUT_FILE, "r", encoding="utf-8") as f:
  catalogue = json.load(f)

print("Catalogue Cleanup")
print("=======================")

#Cleanup

clean_catalogue = {}

removed_products = []

total_products = 0
removed_count = 0

for section_name, section_data in catalogue.items():

  #Keep section if it isn't structured as expected
  if not isinstance(section_data,dict):
    clean_catalogue[section_name] = section_data
    continue

  products = section_data.get("products", [])

  clean_products = []

  for product in products:
    total_products += 1

    #Check product structure
    if not isinstance(product, dict):
      removed_count += 1
      removed_products.append({
        "section": section_name,
        "product": product,
        "reason": "Product is not a dictionary"
      })
      continue

    part_num = product.get("part_num")

    #Missing part number
    if not part_num:
      removed_count += 1

      removed_products.append({
        "section": section_name,
        "product": product,
        "reason": "Missing part number"
      })
      continue

    #Clearly invalid part number
    invalid_part_number = check_part_number_quality(part_num)
    if invalid_part_number:
      removed_count += 1

      removed_products.append({
        "section": section_name,
        "product": product,
        "reason": "Invalid part number"
      })
      continue

    #Keep product if part number passes quality check
    clean_products.append(product)

  #Copy the section
  clean_section = section_data.copy()

  #Replace products with cleaned list
  clean_section["products"] = clean_products

  #Add cleaned section to the clean catalogue
  clean_catalogue[section_name] = clean_section

#Save cleaned catalogue
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
  json.dump(clean_catalogue, f, indent=2, ensure_ascii=False)

#Summary
print()
print("Cleanup Complete")
print("=======================")
print(f"Original products: {total_products}")
print(f"Removed products: {removed_count}")
print(f"Remaining products: {total_products - removed_count}")
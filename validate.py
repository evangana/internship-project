import json
import re
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "catalogue_parser" / "output" / "catalogue.json"

#Load catalogue
with open(JSON_FILE, "r", encoding="utf-8") as f:
  catalogue = json.load(f)

#Inspect first catalogue section
for section_name, section_data in catalogue.items():
   if isinstance(section_data, dict):
      products = section_data.get("products", [])

      if products:
        print(f"\nFIRST NON-EMPTY PRODUCT SECTION")
        print("=====================")
        print(f"KEY: {section_name}")
        print("PRODUCTS:")
        print(json.dumps(products[:3], indent=2))
        break

print("Catalogue validation")
print("=====================")

#Basic structure

# print(f"Top-level type: {type(catalogue).__name__}")

# if isinstance(catalogue, dict):
#   print(f"Top-level keys: {list(catalogue.keys())}")

#Find pages
#pages = catalogue.get("pages", [])
#print(f"Number of pages: {len(pages)}")



#Count products
total_products = 0
products_with_part_numbers = 0
products_without_part_numbers = 0

part_numbers = []
suspicious_part_numbers = []
empty_product_sections = 0

for section_name, section_data in catalogue.items():
  #make sure section is a dictionary
  if not isinstance(section_data, dict):
    print(f"WARNING: Section '{section_name}' is not a dictionary.")
    continue
  products = section_data.get("products", [])

  #Check if product exists
  if not products:
    empty_product_sections += 1
    continue

  #Check each product
  for product in products:
    total_products += 1

    if not isinstance(product, dict):
      products_without_part_numbers += 1
      continue

    part_num = product.get("part_num") 

    if part_num:
      products_with_part_numbers += 1
      part_numbers.append(part_num)

    else:
      products_without_part_numbers += 1

#Duplicate part numbers
counter = Counter(part_numbers)

duplicates = {
  part_num: count
  for part_num, count in counter.items()
  if count > 1
}


#Output
print(f"Total products: {total_products}")
print(f"Products with part numbers: {products_with_part_numbers}")
print(f"Products without part numbers: {products_without_part_numbers}")
print(f"Empty product sections: {empty_product_sections}")
print(f"Duplicate part numbers: {len(duplicates)}")

print()
print(f"Suspicious part numbers: {len(suspicious_part_numbers)}")

if suspicious_part_numbers:
    for part_num in suspicious_part_numbers[:20]:
        print(f"  - {part_num}")

if duplicates:
    print()
    print("Duplicate part numbers:")

    for part_num, count in list(duplicates.items())[:20]:
        print(f"  - {part_num}: {count} occurrences")

print()

print("\nValidation complete.")
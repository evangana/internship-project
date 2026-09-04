import json
import re
from pathlib import Path
from collections import Counter, defaultdict


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "catalogue_parser" / "output" / "clean_catalogue.json"

#Load catalogue
with open(JSON_FILE, "r", encoding="utf-8") as f:
  catalogue = json.load(f)

#Inspect first catalogue section
# for section_name, section_data in catalogue.items():
#    if isinstance(section_data, dict):
#       products = section_data.get("products", [])

#       if products:
#         print(f"\nFIRST NON-EMPTY PRODUCT SECTION")
#         print("=====================")
#         print(f"KEY: {section_name}")
#         print("PRODUCTS:")
#         print(json.dumps(products[:3], indent=2))
#         break

print("Catalogue validation")
print("=====================")

#Basic structure

# print(f"Top-level type: {type(catalogue).__name__}")

# if isinstance(catalogue, dict):
#   print(f"Top-level keys: {list(catalogue.keys())}")

#Find pages
#pages = catalogue.get("pages", [])
#print(f"Number of pages: {len(pages)}")

#Part number quality check
def check_part_number_quality(part_num: str):
  """
  Returns a reason if value looks suspicious
  Returns None if it passes basic checks
  """
  if not isinstance(part_num, str):
    return "Part number is not a string"

  part_num = part_num.strip()

  if not part_num:
    return "empty part number"

  #Too long to reasonably be a part number
  if len(part_num) > 33:
    return "part number is too long"

  #Contains spaces
  #if " " in part_num:
  #  return "part number contains spaces"

  #Contains special characters (only allow alphanumeric and - _)
  # if not re.match(r"[A-Za-z0-9 -_]+", part_num):
  #   return "part number contains special characters"

  #Mostly words
  #if re.fullmatch(r"[A-Za-z]+", part_num):
  #  return "part number is mostly words"
  
  return None

#Count products
total_products = 0
products_with_part_numbers = 0
products_without_part_numbers = 0

part_numbers = []

#Store every occurrence of every part number
part_number_occurrences = defaultdict(list)

#Store suspicious products
suspicious_products = []
empty_product_sections = 0

#Inspect Catalogue
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
  for product_index,product in enumerate(products):
    total_products += 1

    if not isinstance(product, dict):
      products_without_part_numbers += 1

      suspicious_products.append({
        "section": section_name,
        "index": product_index,
        "part_num": None,
        "product": product,
        "reason": "Product is not a dictionary"
      })
      continue

    part_num = product.get("part_num") 

    #Missing part number
    if not part_num:
      products_without_part_numbers += 1

      suspicious_products.append({
        "section": section_name,
        "index": product_index,
        "part_num": part_num,
        "product": product,
        "reason": "Missing part number"
      })
      continue
    #Valid part number
    products_with_part_numbers += 1
    part_numbers.append(part_num)

    #Save occurrence information
    part_number_occurrences[part_num].append({
      "section": section_name,
      "index": product_index,
      "product": product
    })

    #Quality check
    reason = check_part_number_quality(part_num)
    if reason:
      suspicious_products.append({
        "section": section_name,
        "index": product_index,
        "part_num": part_num,
        "reason": reason,
        "product": product
      })

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
print(f"Suspicious part numbers: {len(suspicious_products)}")

#Suspicious products
if suspicious_products:
    print()
    print("=" * 20)
    print("Suspicious Products:")
    print("=" * 20)

    for item in suspicious_products:
        print()
        print(f"Section: {item['section']}")
        print(f"Product Index: {item['index']}")
        print(f"Part Number: {item['part_num']}")
        print(f"Reason: {item['reason']}")
        print("Full product:")

        print(json.dumps(
          item["product"], 
          indent=2,
          ensure_ascii=False
        ))

#Duplicate details
# if duplicates:
#     print()
#     print("=" * 20)
#     print("Duplicate part number details:")
#     print("=" * 20)

#     for part_num, count in duplicates.items():
#       print()
#       print(f"Part Number: {part_num}")
#       print(f"Occurrences: {count}")

#       occurrences = part_number_occurrences[part_num]
#       for occurrence_number, occurrence in enumerate(occurrences, start=1):
#         print()
#         print(f" Occurrence {occurrence_number}:")
#         print(f"  Section: {occurrence['section']}")
#         print(f"  Product Index: {occurrence['index']}")
#         print(" Product:")
#         print(json.dumps(
#           occurrence["product"], 
#           indent=4,
#           ensure_ascii=False
#         ))
print()
print("=" * 20)
print("\nValidation complete.")
print("=" * 20)
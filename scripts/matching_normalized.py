import json
import csv
import re

from excel_part_numbers import excel_part_number


# Load the JSON catalogue
with open("../source_documents/catalogue_extraction.json", "r", encoding="utf-8") as file:
    catalogue_extraction = json.load(file)


# Extract all values stored under "T"
def extract_T_values(data):
    values = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "T":
                values.append(value)
            else:
                values.extend(extract_T_values(value))

    elif isinstance(data, list):
        for item in data:
            values.extend(extract_T_values(item))

    return values


# Normalise part numbers
def normalize(value):
    return re.sub(r"[\s\-_/\.]", "", str(value)).upper()


# Extract catalogue text
catalogue_values = extract_T_values(catalogue_extraction)


# Exact catalogue values
catalogue_exact_lookup = set(catalogue_values)


# Normalised catalogue values
catalogue_normalized_lookup = {
    normalize(value)
    for value in catalogue_values
}


# Results
exact_found = 0
format_mismatch = 0
not_in_catalogue = 0

results = []


# Compare Excel parts
for excel_part in excel_part_number:

    # 1. Exact match
    if excel_part in catalogue_exact_lookup:
        exact_found += 1

        results.append({
            "part_number": excel_part,
            "status": "FOUND EXACTLY"
        })


    # 2. Exists after normalisation
    elif normalize(excel_part) in catalogue_normalized_lookup:
        format_mismatch += 1

        results.append({
            "part_number": excel_part,
            "status": "FOUND - FORMAT DIFFERENCE"
        })


    # 3. Does not exist in the old catalogue
    else:
        not_in_catalogue += 1

        results.append({
            "part_number": excel_part,
            "status": "NOT IN OLD CATALOGUE"
        })


# Total
total = len(excel_part_number)


# Print results
print(f"Total: {total}")
print(f"Found Exactly: {exact_found}")
print(f"Found - Format Difference: {format_mismatch}")
print(f"Not in Old Catalogue: {not_in_catalogue}")


# Save results to CSV
with open("matching_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["part_number", "status"]
    )

    writer.writeheader()
    writer.writerows(results)


# Create list of likely new/missing parts
not_in_catalogue_parts = [
    result["part_number"]
    for result in results
    if result["status"] == "NOT IN OLD CATALOGUE"
]


# Save likely new parts
with open("not_in_old_catalogue.txt", "w", encoding="utf-8") as file:
    for part in not_in_catalogue_parts:
        file.write(part + "\n")
        
import json

from scripts.excel_part_numbers import excel_part_number


# Load the JSON catalogue
with open("catalogue_extraction.json", "r", encoding="utf-8") as file:
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


# Extract all text values from the catalogue
catalogue_values = extract_T_values(catalogue_extraction)


# Create exact-match lookup set
catalogue_lookup = set(catalogue_values)


# Match Excel parts exactly as written
found_count = 0
results = []

for excel_part in excel_part_number:
    if excel_part in catalogue_lookup:
        found_count += 1
        results.append({
            "part_number": excel_part,
            "status": "FOUND"
        })
    else:
        results.append({
            "part_number": excel_part,
            "status": "NOT FOUND"
        })


# Calculate success rate
success_rate = (found_count / len(excel_part_number)) * 100


# Print results
print(f"Found: {found_count}")
print(f"Not Found: {len(excel_part_number) - found_count}")
print(f"Total: {len(excel_part_number)}")
print(f"Success Rate: {success_rate:.2f}%")
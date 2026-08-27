from pathlib import Path
import pandas as pd
import re

#project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

#input file
input_file = BASE_DIR / "scripts" / "catalogue_text_clean.csv"

#read CSV
df = pd.read_csv(input_file)

#Keep only rows with page numbers between 19 and 565
df = df[(df["page_number"] >= 19) & (df["page_number"] <= 565)]

def is_possible_part_number(text):
    if pd.isna(text):
        return False

    text = str(text).strip()

    if not text:
        return False

    # Must contain at least one number
    if not any(char.isdigit() for char in text):
        return False

    words = text.split()

    # More than 3 words is probably a description
    if len(words) > 3:
        return False

    # Only allow common part-number characters
    if not re.fullmatch(r"[A-Za-z0-9\s\-_/\.]+", text):
        return False

    #Longer than 5 characters
    if len(text) <= 5:
        return False

    # Reject common descriptive/specification patterns
    if re.search(r"\b\d+\s*x\s*\d+", text, re.IGNORECASE):
        return False

    if re.search(r"\b\d+\s*(mm|cm|m|v|a|w|hz)\b", text, re.IGNORECASE):
        return False

    # Reject wire descriptions
    if re.fullmatch(r"\d+\s*-\s*wire", text, re.IGNORECASE):
        return False

    # Reject coded descriptions
    if re.search(r"\b[DX]-Coded\s+M12\b", text, re.IGNORECASE):
        return False

    return True


# Identify possible part numbers
mask = df["text"].apply(is_possible_part_number)

# Save possible part numbers
part_numbers = df[mask].copy()
part_numbers.to_csv(
    BASE_DIR / "source_documents" / "catalogue_possible_part_numbers.csv",
    index=False
)

# Save non-part numbers
non_part_numbers = df[~mask].copy()
non_part_numbers.to_csv(
    BASE_DIR / "source_documents" / "catalogue_non_part_numbers.csv",
    index=False
)

print(f"Possible part numbers: {len(part_numbers)}")
print(f"Non-part numbers: {len(non_part_numbers)}")
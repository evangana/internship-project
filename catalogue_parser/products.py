import re


def looks_like_part_number(value):
    if value is None:
        return False

    value = str(value).strip()

    if not value:
        return False

    # Reject obvious headers
    header_words = [
        "part number",
        "part no",
        "description",
        "product",
        "model",
        "rated current",
    ]

    value_lower = value.lower()

    for word in header_words:
        if word in value_lower:
            return False

    # Part numbers should not be extremely long
    if len(value) > 50:
        return False

    # Must contain at least one letter or number
    if not re.search(r"[A-Za-z0-9]", value):
        return False

    return True


def find_part_number_columns(table):
    """
    Find columns that contain a PART NUMBER header.
    """

    if not table:
        return []

    max_columns = max(len(row) for row in table)

    part_number_columns = []

    # Look through every row for PART NUMBER
    for row in table:

        for col_index, value in enumerate(row):

            if value is None:
                continue

            value = str(value).strip().lower()

            if value in [
                "part number",
                "part no",
                "part num",
                "part_number",
                "part_no",
                "partnumber",
            ]:
                part_number_columns.append(col_index)

    # Remove duplicates
    return sorted(set(part_number_columns))


def extract_products(table):
    products = []

    if not table:
        return products

    part_number_columns = find_part_number_columns(table)

    # No PART NUMBER column found
    if not part_number_columns:
        return products

    # Determine where the actual data starts.
    #
    # We look for rows containing something that looks
    # like a part number.
    for row in table:

        for col_index in part_number_columns:

            if col_index >= len(row):
                continue

            value = row[col_index]

            if not looks_like_part_number(value):
                continue

            product = {
                "part_num": str(value).strip(),
                "specifications": {},
            }

            # Store the other values from this row
            for index, cell in enumerate(row):

                if index == col_index:
                    continue

                if cell is None:
                    continue

                cell = str(cell).strip()

                if not cell:
                    continue

                product["specifications"][
                    f"column_{index + 1}"
                ] = cell

            products.append(product)

    return products
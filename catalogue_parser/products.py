def extract_products(df):
  products = []
  columns_lower = [str(c).lower() for c in df.columns]
  possible_part_num_col = "PART NUMBER"
  part_num_col = None
  for col in df.columns:
    if str(col).lower().strip() in possible_part_num_col:
      part_num_col = col
      break
    if part_num_col is None:
      return products
    for _, row in df.iterrows():
      product = {
        "part_num": row.get(part_num_col),
        "specifications": {}
      }
      if "product" in columns_lower:
        idx = columns_lower.index("product")
        product["name"] = row[df.columns[idx]]
      elif "model" in columns_lower:
        idx = columns_lower.index("model")
        product["name"] = row[df.columns[idx]]
      for col in df.columns:
        if col == part_num_col:
          continue
        product["specifications"][str(col)] = str(row[col])
      products.append(product)
  return products
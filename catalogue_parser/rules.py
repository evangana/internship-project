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
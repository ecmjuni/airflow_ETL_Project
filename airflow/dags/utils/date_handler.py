import re

def extract_year(string):
  """Extracts the first year from a string.

  Args:
    string: The input string.

  Returns:
    The extracted year as a string, or None if no year is found.
  """

  match = re.search(r'\d{4}', string)
  return match.group() if match else None
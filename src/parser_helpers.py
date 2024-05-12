import ast
import re

def extract_list_from_string(s):
    # Find the start of the list
    start = s.find('[')
    if start != -1:
        # Slice from the opening bracket to the end of the string
        list_str = s[start:]
        return list_str
    return ""  # Return an empty string if '[' is not found

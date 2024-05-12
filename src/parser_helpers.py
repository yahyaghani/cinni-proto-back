import ast
import re
from PIL import Image
import os 


def extract_list_from_string(s):
    # Find the start of the list
    start = s.find('[')
    if start != -1:
        # Slice from the opening bracket to the end of the string
        list_str = s[start:]
        list_str = ast.literal_eval(list_str)

        return list_str
    return ""  # Return an empty string if '[' is not found



def convert_to_jpg_if_webp(image_path):
    # Check if the file has a .webp extension
    if image_path.lower().endswith('.webp'):
        # Load the image
        image = Image.open(image_path)
        # Convert and save the image as .jpg
        jpg_path = os.path.splitext(image_path)[0] + '.jpg'
        image.convert("RGB").save(jpg_path, "JPEG")
        # Close the image
        image.close()
        return jpg_path
    else:
        return image_path

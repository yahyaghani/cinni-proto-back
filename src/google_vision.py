from google.cloud import vision
import io
from PIL import Image
import numpy as np
import ast 
##

from src.open_calls.instruction_calls import davinci_results_sentence,chat_question_no_keywords_no_history,basic_shopping_prompt
from src.retrieval_engine import image_retrieval,image_text_retrieval
from src.parser_helpers import extract_list_from_string

def localize_objects(path):
    """Localizes objects in a given image and returns a dictionary with the details."""
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations
    objects_details = {}

    for object_ in objects:
        object_data = {
            'confidence': object_.score,
            'vertices': [(vertex.x, vertex.y) for vertex in object_.bounding_poly.normalized_vertices]
        }
        # Use object name as key, append if more than one object of the same type is detected
        if object_.name in objects_details:
            objects_details[object_.name].append(object_data)
        else:
            objects_details[object_.name] = [object_data]

    return objects_details


def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()
    labels_list = []

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    labels = response.label_annotations
    for label in labels:
        labels_list.append(label.description)
    
    return labels_list  # Return the list of labels

def crop_objects(image_path, detection_results, object_names):
    """Crops specified objects from the image based on detection results and returns a dictionary with numpy arrays."""
    cropped_images = {}
    with Image.open(image_path) as img:
        width, height = img.size
        
        for object_name in object_names:
            if object_name in detection_results:
                # It is assumed the first instance of the object is the target, modify as needed
                vertices = detection_results[object_name][0]['vertices']
                
                # Convert normalized coordinates to absolute pixel values
                left = int(vertices[0][0] * width)
                top = int(vertices[0][1] * height)
                right = int(vertices[2][0] * width)
                bottom = int(vertices[2][1] * height)
                
                # Crop the image using the calculated coordinates
                img_cropped = img.crop((left, top, right, bottom))
                # Convert cropped image to numpy array and store in the dictionary
                cropped_images[object_name] = np.array(img_cropped)

            else:
                print(f"No detected '{object_name}' in the image.")
    
    return cropped_images

def process_images_and_map_uris(cropped_images, actual_list):
    """
    Process each cropped image, retrieve corresponding image URIs from results,
    and map them to the respective clothing items in the actual_list.

    Parameters:
    cropped_images: Dictionary of cropped images with keys from actual_list.
    actual_list: List of clothing item names.

    Returns:
    final_dict: Dictionary mapping each clothing item to a list of image URIs.
    """
    final_dict = {}
    index = 0  # To keep track of the corresponding item in actual_list

    # Iterate over each cropped image and its associated item name
    for item_name in actual_list:
        if item_name in cropped_images:
            # Perform image retrieval for the current cropped image
            resulting_dict = image_retrieval(cropped_images[item_name])
    
            # Extract URIs from the resulting_dict and assign them to the final_dict
            if resulting_dict and 'uris' in resulting_dict:
                # Flatten the list of URIs if they are nested
                uris = [uri for sublist in resulting_dict['uris'] for uri in sublist]
                final_dict[item_name] = uris

        index += 1  # Move to the next item in the list

    return final_dict



def process_images_and_map_ids(cropped_images, actual_list):
    """
    Process each cropped image, retrieve corresponding image IDs from results,
    and map them to the respective clothing items in the actual_list based on
    a distance threshold. Scale the number of results retrieved based on the
    number of items to ensure efficient processing.

    Parameters:
    cropped_images: Dictionary of cropped images with keys from actual_list.
    actual_list: List of clothing item names.

    Returns:
    final_dict: Dictionary mapping each clothing item to a list of image IDs where distance > 0.5.
    """
    final_dict = {}
    num_cropped_images = len(cropped_images)

    # Calculate the number of results to retrieve for each image retrieval
    max_total_results = 8  # Approximate maximum total results we want to handle
    results_per_image = max(1, max_total_results // max(num_cropped_images, 1))

    for item_name in actual_list:
        if item_name in cropped_images:
            # Adjust the retrieval to fetch an appropriate number of results
            resulting_dict = image_retrieval(cropped_images[item_name], results_per_image)
            filtered_ids = []

            if resulting_dict and 'ids' in resulting_dict and 'distances' in resulting_dict:
                for id_list, distance_list in zip(resulting_dict['ids'], resulting_dict['distances']):
                    filtered_ids.extend([id for id, distance in zip(id_list, distance_list) if distance > 0.3])
            
            final_dict[item_name] = filtered_ids
            print(f'Filtered IDs for {item_name}:', filtered_ids)

    return final_dict

# image_path="/home/taymur/Downloads/loose_twill_jacket_men_hnm-ezgif.com-webp-to-jpg-converter.jpg"
# historical_context='brothers wedding ceremony'
# # Example usage:


def call_vision_chain(image_path, historical_keyword_list, historical_context=None, historical_embeddings=False, call_retrieval=True, First=False):
    if historical_context is None:
        historical_context = historical_keyword_list
    
    # Detect objects and crop images based on these objects
    objects_info = localize_objects(image_path)
    detected_element_names = list(objects_info.keys())
    
    # Remove 'Person' from the detected elements if there are other elements present
    if len(detected_element_names) > 1 and 'Person' in detected_element_names:
        detected_element_names.remove('Person')

    cropped_images = crop_objects(image_path, objects_info, detected_element_names)  # Assume this returns a dict of image data
    print(detected_element_names)
    
    # Process the cropped images and map them to IDs with filtering logic
    final_dict = process_images_and_map_ids(cropped_images, detected_element_names)
    # print(final_dict)

    # Extract all values from final_dict and flatten them into a single list
    final_pin_list = [item_id for sublist in final_dict.values() for item_id in sublist]
    # print("Final pin list:", final_pin_list)

    return final_dict, detected_element_names, final_pin_list


def pin_image_received_chain(image_path,historical_context=None,call_retrieval=True):
    if historical_context==None:
        historical_context=""
    objects_info = localize_objects(image_path)
    print(objects_info)
    detected_element_names = list(objects_info.keys())
    print(detected_element_names)
    ## way too inconsistent to utilise the list parsing of detected objects , we will use a classifier here later
    # list_of_objects_to_crop=identify_labels_to_crop(detected_element_names,historical_context)
    # print(list_of_objects_to_crop)
    # print(type(list_of_objects_to_crop))
    # if type(list_of_objects_to_crop)==str:
    #     list_of_objects_to_crop = ast.literal_eval(list_of_objects_to_crop)
    #     print('changed type using ast')
    #     print(list_of_objects_to_crop)
    #     print(type(list_of_objects_to_crop))

    # print(cropped_image)
    cropped_images = crop_objects(image_path, objects_info, detected_element_names)  # Assume this returns a dict of image data
    if call_retrieval==False:
        return cropped_images,detected_element_names
    final_dict = process_images_and_map_ids(cropped_images, detected_element_names)
    print(final_dict)
    return final_dict


def call_chat_chain(message, historical_keyword_list, historical_chat, historical_embeddings, is_first_interaction):
    print("Starting call_chat_chain...")
    if is_first_interaction:
        response_35 = chat_question_no_keywords_no_history(message)
        print(f"First interaction: {response_35}")

        response_instruct = davinci_results_sentence(message)
        print(f"First interaction: Instructions: {response_instruct}")
    else:
        response_35 = basic_shopping_prompt(message, historical_keyword_list, historical_chat)
        print(f"Subsequent interaction: {response_35}")

        response_instruct = davinci_results_sentence(message)
        print(f"Subsequent interaction: Instructions: {response_instruct}")

    # Ensure response_instruct is a list
    if not isinstance(response_instruct, list):
        response_instruct=extract_list_from_string(response_instruct)
        # response_instruct = [response_instruct]  # Convert to list if not already
        print(f"Converted response_instruct to list: {response_instruct}")

    max_total_results = 5
    num_responses = len(response_instruct)
    results_per_response = max(1, max_total_results // max(num_responses, 1))
    print(f"Calculated number of results per response: {results_per_response}")

    final_dict = {}
    for instruction in response_instruct:
        print(f"Retrieving images for instruction: {instruction}")
        image_results = image_text_retrieval(instruction, results_per_response)
        print('image_results in chat chain',image_results)
        filtered_ids = []
        if image_results and 'ids' in image_results and 'distances' in image_results:
            for id_list, distance_list in zip(image_results['ids'], image_results['distances']):
                filtered_ids.extend([id for id, distance in zip(id_list, distance_list) if distance > 0.3])
        final_dict[instruction] = filtered_ids
        print(f"Filtered IDs for {instruction}: {filtered_ids}")

    final_pin_list = [item_id for sublist in final_dict.values() for item_id in sublist]
    print("Final pin list compiled:", final_pin_list)

    return response_35, response_instruct, final_dict, final_pin_list

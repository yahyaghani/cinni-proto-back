import urllib.request
import numpy as np
from PIL import Image

from fashion_clip.fashion_clip import FashionCLIP
from src.clotho.descriptions import clothing_descriptions

def load_fashion_clip_model():
    # Instantiate the FashionCLIP model
    # fclip = fashion_clip.FashionCLIP('fashion-clip')
    fclip = FashionCLIP('fashion-clip')

    return fclip

def preprocess_image(image_path):
    # Open and prepare the image
    image = Image.open(image_path)
    return image

def encode_image(fclip, image):
    # Create embeddings for the image
    image_embeddings = fclip.encode_images([image], batch_size=1)
    # Normalize the embeddings
    normalized_embeddings = image_embeddings / np.linalg.norm(image_embeddings, ord=2, axis=-1, keepdims=True)
    return normalized_embeddings

def encode_text(fclip, text):
    # Create embeddings for the text
    text_embeddings = fclip.encode_text([text], batch_size=1)
    # Normalize the embeddings
    normalized_embeddings = text_embeddings / np.linalg.norm(text_embeddings, ord=2, axis=-1, keepdims=True)
    return normalized_embeddings

def predict_similarity(image_embedding, text_embedding):
    # Calculate the dot product between image and text embeddings for similarity
    similarity = np.dot(image_embedding, text_embedding.T)
    return similarity


def load_image_from_url(url):
    # Retrieve and open image from URL
    with urllib.request.urlopen(url) as url_response:
        image = Image.open(url_response)
    return image

def process_query(fclip, query):
    # Determine if query is an image or text and encode appropriately
    if query.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):  # Check for common image file extensions
        if query.startswith('http'):
            image = load_image_from_url(query)
        else:
            image = preprocess_image(query)
        query_embedding = encode_image(fclip, image)
    else:
        query_embedding = encode_text(fclip, query)
    return query_embedding

def match_images(fclip, images_dict, query):
    # Process query to get the appropriate embedding
    query_embedding = process_query(fclip, query['query'])
    
    results = {}
    
    # Iterate through dictionary of images, process, and compare similarity
    for id, img_uri in images_dict.items():
        if img_uri.startswith('http'):
            image = load_image_from_url(img_uri)
        else:
            image = preprocess_image(img_uri)
        image_embedding = encode_image(fclip, image)
        
        similarity = predict_similarity(query_embedding, image_embedding)
        results[id] = similarity
        
    return results


def get_textual_description(image_path, fclip, text_embeddings):
    """
    Get textual description from an image using FashionCLIP embeddings.

    Args:
    image_path (str): Path to the image file.
    fclip (FashionCLIP): An instance of the FashionCLIP model.
    descriptions (list): List of pre-defined text descriptions.
    text_embeddings (np.array): Array of pre-computed text embeddings.

    Returns:
    str: The description that best matches the image.
    """
    descriptions=clothing_descriptions
    # Load the image
    image = Image.open(image_path)
    fclip = load_fashion_clip_model()
    # Encode the image to get its embedding
    image_embedding = fclip.encode_images([image], batch_size=1)
    image_embedding = image_embedding / np.linalg.norm(image_embedding, ord=2, axis=-1, keepdims=True)
    
    # Calculate dot products of the image embedding with all text embeddings
    similarities = np.dot(text_embeddings, image_embedding.T).squeeze()
    
    # Find the index of the highest similarity score
    best_match_idx = np.argmax(similarities)
    
    # Return the corresponding description
    return descriptions[best_match_idx]




# # Example usage
# if __name__ == "__main__":
#     fclip = load_fashion_clip_model()
#     ### single testing ## 

#     # query_image_path = "/home/taymur/Downloads/suitprint.webp"
#     # image = preprocess_image(query_image_path)
#     # # Encode the image
#     # image_embedding = encode_image(fclip, image)
#     # # Example text description
#     # # text = "A stylish red dress"
#     # text = "A brown printed suit"
#     # # Encode the text
#     # text_embedding = encode_text(fclip, text)
#     # # Predict similarity
#     # similarity_score = predict_similarity(image_embedding, text_embedding)
#     # print("Similarity Score:", similarity_score)


#     # Dictionary of images with their IDs
#     images_dict = {
#         '1': '/home/taymur/Downloads/suitprint.webp',
#         '2': '/home/taymur/Downloads/brownsuitprint3.webp',
#         '3': 'https://storage.yandexcloud.net/clothes-and-wildberries/clothes-parsing-dataset/shein/2022/03/21/16478435512fc0970d73701276e3bfec64a33320d2_thumbnail_600x.webp',

#     }
    
#     # Query can be text or an image URL or local path
#     query = {'query': 'A brown printed suit"'}  # Example text query
#     # query = {'query': '/path/to/query_image.jpg'}  # Example image query (local)
#     # query = {'query': 'http://example.com/query_image.jpg'}  # Example image query (URL)

#     # Match images and print results
#     similarity_results = match_images(fclip, images_dict, query)
#     print("Similarity Results:", similarity_results)

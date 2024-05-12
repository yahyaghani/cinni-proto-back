##

import json
import os
from PIL import Image

import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
###
###This module is our beta Indexing module

# Function to load the JSON data from a file
def load_json_data(file_path):
    print("Loading JSON data...")
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to convert WebP images to a compatible format (e.g., JPEG or PNG)
def convert_webp_to_compatible_format(image_path):
    image = Image.open(image_path)
    if image.format == "WEBP":
        # Convert WebP to JPEG or PNG
        image = image.convert("RGB")  # Convert to RGB format if necessary
        image_path_jpeg = image_path[:-5] + ".jpg"  # Change file extension to .jpg
        image.save(image_path_jpeg, "JPEG")
        return image_path_jpeg
    else:
        return image_path  # Return original path if not a WebP image
# Function to create and fill a Chroma collection with image embeddings
# Function to create and fill a Chroma collection with image embeddings
def create_and_fill_chroma_collection(client, image_folder, json_data, limit=3):
    print("Creating and filling Chroma collection...")
    embedding_function = OpenCLIPEmbeddingFunction()
    image_loader = ImageLoader()
    
    # Creating the collection
    collection = client.create_collection(
        name='multimodal_collection', 
        embedding_function=embedding_function, 
        data_loader=image_loader)

    # List all available images and prepare their URIs
    # available_images = sorted(os.listdir(image_folder))[:limit]  # Limit to first three images
    available_images = sorted(os.listdir(image_folder))  # Limit to first three images
    ids = [img.split('.')[0] for img in available_images if img.endswith('.jpg')]
    image_uris = [os.path.join(image_folder, f"{img_id}.jpg") for img_id in ids if f"{img_id}.jpg" in available_images]
    collection.add(ids=ids, uris=image_uris)
    retrieved = collection.query(query_texts=["carrier bag"], include=['data'], n_results=1)
    print(retrieved)

# Main function to process the JSON file and populate ChromaDB
def process_json_to_chroma_db(json_path, image_folder, chroma_client, image_limit):
    print("Processing JSON to ChromaDB...")
    json_data = load_json_data(json_path)
    create_and_fill_chroma_collection(chroma_client, image_folder, json_data, limit=image_limit)
    print("ChromaDB population complete.")

# Test usage:
if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join('/media/taymur/EXTERNAL_USB/LLMOps/cinni_image_set/', "products.json")
    image_folder = '/media/taymur/EXTERNAL_USB/LLMOps/cinni_image_set/images/'
    db_dir = os.path.join(current_dir, "chromadb_data")
    chroma_client = chromadb.PersistentClient(path=db_dir)
    process_json_to_chroma_db(json_path, image_folder, chroma_client, image_limit=15)


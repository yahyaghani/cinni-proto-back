import json
import os
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image

import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader

from src.chroma.initiate_chroma_client import chroma_client
from src.chroma.chroma_metadata_collection_index import openai_ef
from src.clotho.clip_module import analyze_image_with_text,analyze_image_with_images,predict_three_images
# from src.google_vision import call_vision_chain
from src.parser_helpers import convert_to_jpg_if_webp


def image_text_retrieval(input_query):
    embedding_function = OpenCLIPEmbeddingFunction()
    image_loader = ImageLoader()
    collection = chroma_client.get_or_create_collection(
    name='multimodal_collection', 
    embedding_function=embedding_function, 
    data_loader=image_loader)
    retrieved = collection.query(query_texts=input_query, include=['uris'], n_results=5)
    return retrieved

def image_retrieval(query_image):
    # Initialize embedding function and image loader
    embedding_function = OpenCLIPEmbeddingFunction()
    image_loader = ImageLoader()

    # Create or get the multimodal collection
    collection = chroma_client.get_or_create_collection(
        name='multimodal_collection',
        embedding_function=embedding_function,
        data_loader=image_loader
    )

    # Query the collection with the provided image
    retrieved = collection.query(query_images=[query_image], n_results=5)
    return retrieved


def query_by_embeddings(image):

    # Querying by a set of query_embeddings 
    embedding_function = OpenCLIPEmbeddingFunction()
    image_loader = ImageLoader()
    collection = chroma_client.get_or_create_collection(
    name='multimodal_collection', 
    embedding_function=embedding_function, 
    data_loader=image_loader)
    results = collection.query( 
        query_embeddings=[image], 
        n_results=1 
    ) 
    return results


# input_query='The suit is modern in style with a slim fit and tailored design. The color of the suit is navy blue, and it appears to be made of high-quality wool material. The man is standing confidently, wearing a white dress shirt underneath the suit jacket.'
# res=image_text_retrieval(input_query)
# print(res)

query_image_path = "/home/taymur/Downloads/suitprint.webp"
query_image_path2 = "/media/taymur/EXTERNAL_USB/LLMOps/cinni_image_set/images/sw2208023819893238.jpg"
query_image_path3 = "/home/taymur/Downloads/loose_twill_jacket_men_hnm-ezgif.com-webp-to-jpg-converter.jpg"

# # Load and preprocess the query image
jpg_path = convert_to_jpg_if_webp(query_image_path)
jpg_path2 = convert_to_jpg_if_webp(query_image_path2)
jpg_path3 = convert_to_jpg_if_webp(query_image_path3)

# query_image = np.array(Image.open(jpg_path))

# # Perform retrieval using the query image
# retrieved_results = image_retrieval(query_image)

# # Display the retrieved results
# print(retrieved_results)


# descriptions='red print suit'
# res=analyze_image_with_text(jpg_path,descriptions)

# rest=predict_three_images(jpg_path,jpg_path2,jpg_path3)
# print(rest)
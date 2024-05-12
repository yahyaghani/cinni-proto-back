import json
import os

import chromadb
import chromadb.utils.embedding_functions as embedding_functions

## Text meta data embeddings index module

api_key=os.getenv('OPENAI_API_KEY')
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key,
                model_name="text-embedding-3-small"
            )

client = chromadb.PersistentClient(path="test")

# Function to load the JSON data from a file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_and_fill_metadata_collection(client, json_data):
    collection = client.get_or_create_collection(
        name='metadata_collection_keys', 
        embedding_function=openai_ef  # Using OpenAI embedding function
    )

    for sku_id, data in json_data.items():
        meta = data["meta"]
        metadata_string = ','.join([meta.get(field, "") for field in ["Color"]])
        metadata_embedding = openai_ef(metadata_string)  # Embedding the metadata string using OpenAI model
        collection.add(ids=[sku_id], embeddings=[metadata_embedding])

    print("Metadata collection creation and filling complete.")

def process_json_to_chromadb(json_path, chroma_client):
    json_data = load_json_data(json_path)
    create_and_fill_metadata_collection(chroma_client, json_data)


def query_collection(collection, query, max_results):
    results = collection.query(query_texts=query, n_results=max_results, include=['distances']) 
    return results 

if __name__ == "__main__":
    # Ensure to create or retrieve collection before querying
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join('/media/taymur/EXTERNAL_USB/LLMOps/cinni_image_set/', "products.json")
    collection = client.get_or_create_collection(
        name='metadata_collection_keys', 
        embedding_function=openai_ef
    )
    # process_json_to_chromadb(json_path, client)

    query = 'brown'
    test_results = query_collection(collection, query, 3)    
    print(test_results)

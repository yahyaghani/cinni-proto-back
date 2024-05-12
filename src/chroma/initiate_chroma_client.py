import os 
import chromadb




current_dir = os.path.dirname(__file__)
db_dir = os.path.join(current_dir, "chromadb_data")
chroma_client = chromadb.PersistentClient(path=db_dir)

import chromadb
import os

FILE_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(FILE_PATH)

save_path = DIR_PATH + "\\save"
chroma_client = chromadb.PersistentClient(path=save_path)

collection = chroma_client.get_collection(name="my_collection")
results = collection.query(
    query_texts=["This is a query document about hawaii"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(results)
import chromadb
import os

FILE_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(FILE_PATH)

save_path = DIR_PATH + "\\save"
chroma_client = chromadb.PersistentClient(path=save_path)
collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents=[
        "This is a document about notebook",
        "This is a document about Japan"
    ],
    ids=["id1", "id2"]
)

results = collection.query(
    query_texts=["This is a query document about hawaii"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(results)
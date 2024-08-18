import chromadb
chroma_client = chromadb.Client()


# 名前を付けてcollectuionを作成する
# collectuionは、埋め込み、ドキュメント、追加のメタデータを格納 
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
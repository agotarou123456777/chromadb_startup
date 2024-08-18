# Getting Started
https://docs.trychroma.com/getting-started


ChromaはAIネイティブのオープンソースベクターデータベースです。必要なすべてが組み込まれており、あなたのマシンで動作します。ホスティング版も近日登場予定です！

1. **インストール**

コマンドライン

```bash
pip install chromadb
```

2. **Chromaクライアントを作成する**

Python

```python
import chromadb
chroma_client = chromadb.Client()
```

3. **コレクションを作成する**

コレクションは、埋め込み、ドキュメント、および追加のメタデータを保存する場所です。名前を指定してコレクションを作成できます。

Python

```python
collection = chroma_client.create_collection(name="my_collection")
```

4. **コレクションにテキストドキュメントを追加する**

Chromaはテキストを保存し、埋め込みとインデックス作成を自動的に処理します。埋め込みモデルのカスタマイズも可能です。

Python

```python
collection.add(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=["id1", "id2"]
)
```

5. **コレクションをクエリする**

クエリテキストのリストでコレクションをクエリすると、Chromaは最も類似した結果をn個返します。とても簡単です！

Python

```python
results = collection.query(
    query_texts=["This is a query document about hawaii"],  # Chromaがこれを埋め込みます
    n_results=2  # 返す結果の数
)
print(results)
```

6. **結果を確認する**

上記のクエリから、ハワイに関するクエリがパイナップルに関する文書と意味的に最も類似していることがわかります。直感的にも納得がいきます！

JavaScript

```javascript
{
  'documents': [[
      'This is a document about pineapple',
      'This is a document about oranges'
  ]],
  'ids': [['id1', 'id2']],
  'distances': [[1.0404009819030762, 1.243080496788025]],
  'uris': None,
  'data': None,
  'metadatas': [[None, None]],
  'embeddings': None,
}
```

7. **自分で試してみましょう**

例えば、「This is a document about florida」でクエリを実行したらどうなるでしょうか？

```python
import chromadb
chroma_client = chromadb.Client()
# 毎回新しいコレクションを作成しないように、`create_collection`を`get_or_create_collection`に切り替えます
collection = chroma_client.get_or_create_collection(name="my_collection")
# 毎回同じドキュメントを追加しないように、`add`を`upsert`に切り替えます
collection.upsert(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=["id1", "id2"]
)
results = collection.query(
    query_texts=["This is a query document about florida"],  # Chromaがこれを埋め込みます
    n_results=2  # 返す結果の数
)
print(results)
```

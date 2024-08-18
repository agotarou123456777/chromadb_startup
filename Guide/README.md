# 永続的なChromaクライアントの初期化

```python
import chromadb
```

Chromaを構成して、データベースをローカルマシンに保存および読み込むように設定できます。データは自動的に永続化され、起動時に（存在する場合は）読み込まれます。

```python
client = chromadb.PersistentClient(path="/path/to/save/to")
```

`path` は、Chromaがデータベースファイルをディスクに保存し、起動時に読み込む場所です。

`client` オブジェクトには、いくつか便利なメソッドがあります。

```python
client.heartbeat()  # ナノ秒のハートビートを返します。クライアントが接続されたままであることを確認するのに便利です。
client.reset()  # データベースを空にして完全にリセットします。⚠️ これは破壊的であり、元に戻せません。
```

### クライアント/サーバーモードでChromaを実行

Chromaはクライアント/サーバーモードでも実行できます。このモードでは、Chromaクライアントは別のプロセスで実行されているChromaサーバーに接続します。

Chromaサーバーを起動するには、次のコマンドを実行します：

コマンドライン

```bash
chroma run --path /db_path
```

その後、Chroma HTTPクライアントを使用してサーバーに接続します：

```python
import chromadb
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
```

これで完了です！ この変更だけで、ChromaのAPIはクライアントサーバーモードで動作します。

Chromaは非同期HTTPクライアントも提供しています。動作やメソッドシグネチャは同期クライアントと同じですが、ブロックする可能性のあるすべてのメソッドが非同期になります。使用するには、`AsyncHttpClient`を呼び出します：

```python
import asyncio
import chromadb

async def main():
    client = await chromadb.AsyncHttpClient()
    collection = await client.create_collection(name="my_collection")
    await collection.add(
        documents=["hello world"],
        ids=["id1"]
    )

asyncio.run(main())
```

### PythonのHTTPのみのクライアントを使用

クライアントサーバーモードでChromaを実行している場合、フルChromaライブラリは必要ないかもしれません。その代わりに、軽量のクライアント専用ライブラリを使用できます。この場合、`chromadb-client`パッケージをインストールできます。このパッケージは、最小限の依存関係でサーバー用の軽量HTTPクライアントです。

```bash
pip install chromadb-client
```

```python
import chromadb

# クライアントを設定してChromaサーバーに接続する例
client = chromadb.HttpClient(host='localhost', port=8000)

# または非同期使用の場合:
async def main():
    client = await chromadb.AsyncHttpClient(host='localhost', port=8000)
```

注意点として、`chromadb-client`パッケージはフルChromaライブラリのサブセットであり、すべての依存関係が含まれているわけではありません。フルChromaライブラリを使用したい場合は、代わりに `chromadb` パッケージをインストールできます。最も重要なのは、デフォルトの埋め込み関数がないことです。埋め込みなしで `add()` ドキュメントを追加する場合、埋め込み関数を手動で指定し、その依存関係をインストールする必要があります。

以下が日本語への翻訳です。

---

**コレクションの使用**

Chromaでは、コレクションプリミティブを使用して埋め込みのコレクションを管理できます。

**コレクションの作成、確認、および削除**

ChromaはURL内でコレクション名を使用するため、名前を付ける際にはいくつかの制約があります：

- 名前の長さは3〜63文字である必要があります。
- 名前は小文字のアルファベットまたは数字で始まり、終わる必要があり、間にはピリオド、ダッシュ、アンダースコアを含むことができます。
- 2つの連続したピリオドを含んではいけません。
- 名前は有効なIPアドレスではない必要があります。

Chromaのコレクションは、名前とオプションの埋め込み関数で作成されます。埋め込み関数を指定する場合、コレクションを取得するたびにそれを指定する必要があります。

Python

```python
collection = client.create_collection(name="my_collection", embedding_function=emb_fn)
collection = client.get_collection(name="my_collection", embedding_function=emb_fn)
```

後で`get_collection`を呼び出す場合は、コレクション作成時に指定した埋め込み関数を必ず指定してください。

埋め込み関数はテキストを入力として受け取り、トークン化と埋め込みを行います。埋め込み関数が指定されない場合、ChromaはデフォルトでSentence Transformerを使用します。

🧬 [埋め込み関数について詳しく知り、自分で作成する方法を学べます。](#)

既存のコレクションは名前で取得できます（`.get_collection`）、削除するには`.delete_collection`を使用します。また、`.get_or_create_collection`を使用して、存在する場合はコレクションを取得し、存在しない場合は作成できます。

Python

```python
collection = client.get_collection(name="test")  # 既存のコレクションから名前でコレクションオブジェクトを取得します。見つからない場合は例外が発生します。
collection = client.get_or_create_collection(name="test")  # 既存のコレクションから名前でコレクションオブジェクトを取得します。存在しない場合は作成します。
client.delete_collection(name="my_collection")  # コレクションと関連するすべての埋め込み、ドキュメント、およびメタデータを削除します。⚠️ これは破壊的で元に戻せません
```

コレクションには、いくつかの便利なメソッドがあります。

Python

```python
collection.peek()  # コレクション内の最初の10項目のリストを返します
collection.count()  # コレクション内の項目数を返します
collection.modify(name="new_name")  # コレクションの名前を変更します
```

**距離関数の変更**

`create_collection`は、オプションのメタデータ引数を受け取り、`hnsw:space`の値を設定して埋め込み空間の距離メソッドをカスタマイズできます。

Python

```python
collection = client.create_collection(
    name="collection_name",
    metadata={"hnsw:space": "cosine"}  # デフォルトはl2です
)
```

`hnsw:space`の有効なオプションは「l2」、「ip」、「cosine」です。デフォルトは「l2」で、これは二乗L2ノルムです。

| 距離関数           | パラメータ    | 方程式                        |
| ---------         | ----------    | -----------------------------|
| Squared L2        | l2            | d=∑(Ai−Bi)²                  |
| Inner product     | ip            | d=1.0−∑(Ai×Bi)               |
| Cosine similarity | cosine        | d=1.0−∑(Ai×Bi)/√(∑Ai²×∑Bi²)  |

**データをコレクションに追加する**

データをChromaに追加するには、`.add`を使用します。

```python
collection.add(
    documents=["lorem ipsum...", "doc2", "doc3", ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    ids=["id1", "id2", "id3", ...]
)
```

Chromaにドキュメントのリストが渡されると、それらを自動的にトークン化し、コレクションの埋め込み関数で埋め込みます（作成時に指定されていない場合はデフォルトが使用されます）。また、ドキュメント自体も保存します。選択した埋め込み関数を使用して埋め込むにはドキュメントが大きすぎる場合、例外が発生します。

各ドキュメントには一意のIDが関連付けられている必要があります。同じIDを2回追加しようとすると、最初の値のみが保存されます。各ドキュメントに追加情報を保存し、フィルタリングを可能にするためのメタデータ辞書のリストをオプションで指定できます。

別の方法として、ドキュメントに関連する埋め込みのリストを直接提供し、Chromaがそれらのドキュメントを自分で埋め込むことなく保存することもできます。

```python
collection.add(
    documents=["doc1", "doc2", "doc3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    ids=["id1", "id2", "id3", ...]
)
```

提供された埋め込みがコレクションと同じ次元でない場合、例外が発生します。

また、ドキュメントを別の場所に保存し、埋め込みとメタデータのリストのみをChromaに提供することもできます。IDを使用して、他の場所に保存されているドキュメントと埋め込みを関連付けることができます。


```python
collection.add(
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    ids=["id1", "id2", "id3", ...]
)
```

以下が日本語への翻訳です。

---

**コレクションのクエリ**

Chromaコレクションは、`.query` メソッドを使用してさまざまな方法でクエリできます。

クエリ埋め込みのセットを使用してクエリできます。

Python

```python
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1], [1.1, 2.3, 3.2], ...],
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains": "search_string"}
)
```

クエリは、各クエリ埋め込みに対して最も近い `n_results` 個の一致を順番に返します。オプションの `where` フィルタ辞書を指定することで、各ドキュメントに関連付けられたメタデータでフィルタリングできます。また、オプションの `where_document` フィルタ辞書を指定することで、ドキュメントの内容でフィルタリングすることも可能です。

指定されたクエリ埋め込みがコレクションと同じ次元でない場合、例外が発生します。

クエリテキストのセットを使用してクエリすることもできます。Chromaは最初にコレクションの埋め込み関数で各クエリテキストを埋め込み、その後生成された埋め込みでクエリを実行します。

Python

```python
collection.query(
    query_texts=["doc10", "thus spake zarathustra", ...],
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains": "search_string"}
)
```

また、`.get` を使用してIDでコレクションからアイテムを取得することもできます。

```python
collection.get(
    ids=["id1", "id2", "id3", ...],
    where={"style": "style1"}
)
```

`.get` も `where` および `where_document` フィルタをサポートしています。IDが指定されていない場合、`where` および `where_document` フィルタに一致するコレクション内のすべてのアイテムが返されます。

**返されるデータの選択**

`get` または `query` を使用するときに、`include` パラメータを使用して、返されるデータを指定できます。埋め込み、ドキュメント、メタデータ、および `query` の場合は距離のいずれかを指定できます。デフォルトでは、Chromaはドキュメント、メタデータ、および `query` の場合は結果の距離を返します。パフォーマンスのために埋め込みはデフォルトで除外され、IDは常に返されます。`query` または `get` メソッドの `include` パラメータに含めるフィールド名の配列を渡すことで、これらのうちどれを返すかを指定できます。


```javascript
# ドキュメントとIDのみを取得する
collection.get(
    include=["documents"]
)
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1], [1.1, 2.3, 3.2], ...],
    include=["documents"]
)
```

**Whereフィルタの使用**

Chromaは、メタデータおよびドキュメント内容でクエリをフィルタリングすることをサポートしています。`where` フィルタはメタデータでフィルタリングするために使用され、`where_document` フィルタはドキュメント内容でフィルタリングするために使用されます。

**メタデータによるフィルタリング**

メタデータでフィルタリングするには、クエリに `where` フィルタ辞書を指定する必要があります。この辞書は以下の構造を持っている必要があります：

```python
{
    "metadata_field": {
        <Operator>: <Value>
    }
}
```

メタデータフィルタリングでは、以下のオペレーターをサポートしています：

- `$eq` - 等しい（文字列、整数、浮動小数点数）
- `$ne` - 等しくない（文字列、整数、浮動小数点数）
- `$gt` - より大きい（整数、浮動小数点数）
- `$gte` - 以上（整数、浮動小数点数）
- `$lt` - より小さい（整数、浮動小数点数）
- `$lte` - 以下（整数、浮動小数点数）

`$eq` オペレーターを使用することは、`where` フィルタを使用することと同じです。

```python
{
    "metadata_field": "search_string"
}
# は次と同じです
{
    "metadata_field": {
        "$eq": "search_string"
    }
}
```

`Where` フィルタはキーが存在する埋め込みのみを検索します。例えば、`where={"version": {"$ne": 1}}` の場合、キー `version` を持たないメタデータは返されません。

**ドキュメント内容によるフィルタリング**

ドキュメント内容でフィルタリングするには、クエリに `where_document` フィルタ辞書を指定する必要があります。2つのフィルタリングキー `$contains` と `$not_contains` をサポートしています。辞書の構造は以下の通りです：

```python
# 検索文字列でフィルタリング
{
    "$contains": "search_string"
}
```

```python
# 含まないフィルタリング
{
    "$not_contains": "search_string"
}
```

**論理演算子の使用**

また、論理演算子 `$and` と `$or` を使用して複数のフィルタを組み合わせることもできます。

`$and` 演算子は、リスト内のすべてのフィルタに一致する結果を返します。

Python

```python
{
    "$and": [
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        },
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        }
    ]
}
```

`$or` 演算子は、リスト内のいずれかのフィルタに一致する結果を返します。

Python

```python
{
    "$or": [
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        },
        {
            "metadata_field": {
                <Operator>: <Value>
            }
        }
    ]
}
```

**包含演算子の使用（$in および $nin）**

以下の包含演算子がサポートされています：

- `$in` - 値が事前定義されたリスト内にある（文字列、整数、浮動小数点数、ブール値）
- `$nin` - 値が事前定義されたリスト内にない（文字列、整数、浮動小数点数、ブール値）

`$in` 演算子は、メタデータ属性が提供されたリストの一部である結果を返します：

JSON

```json
{
  "metadata_field": {
    "$in": ["value1", "value2", "value3"]
  }
}
```

`$nin` 演算子は、メタデータ属性が提供されたリストの一部ではない結果を返します：

JSON

```json
{
  "metadata_field": {
    "$nin": ["value1", "value2", "value3"]
  }
}
```

**実践的な例**

包含演算子の使用方法とデモの追加例については、ここに提供されているノートブックを参照してください。

**コレクション内のデータの更新**

コレクション内のアイテムの任意のプロパティは、`.update` を使用して更新できます。

```python
collection.update(
    ids=["id1", "id2", "id3", ...],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
    documents=["doc1", "doc2", "doc3", ...],
)
```

IDがコレクションに存在しない場合、エラーが記録され、更新は無視されます


# 埋め込み（Embeddings）

埋め込みは、あらゆるデータをAIネイティブに表現する方法であり、さまざまなAIを活用したツールやアルゴリズムと連携することができる
テキスト、画像、そして将来的には音声や動画を表現することができる

埋め込みを作成する方法は多数ある:
- ローカルでインストールされたライブラリを使用する
- API呼び出し

Chromaは、人気のある埋め込みプロバイダーを簡単に利用できる軽量なラッパーを提供
Chromaコレクションを作成する際に埋め込み関数を設定することができる
→　この設定により、埋め込みAPIは自動的に使用できる
直接呼び出して使用することも可能

| プロバイダー                   | Python | JS   |
|---------------------------- |--------|------|
| OpenAI                      | ✅     | ✅   |
| Google Generative AI        | ✅     | ✅   |
| Cohere                      | ✅     | ✅   |
| Hugging Face                | ✅     | ➖   |
| Instructor                  | ✅     | ➖   |
| Hugging Face Embedding Server | ✅     | ✅   |
| Jina AI                     | ✅     | ✅   |


### デフォルト：all-MiniLM-L6-v2

Chromaはデフォルトで、Sentence Transformersの`all-MiniLM-L6-v2`モデルを使用して埋め込みを作成する
この埋め込みモデルは、さまざまなタスクに使用できるsentenceやドキュメントの埋め込みを作成できる
この埋め込み関数はローカルマシンで実行され、モデルファイルのダウンロードが必要（自動的に行われる）

```python
from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()
```

埋め込み関数はコレクションにリンクして、`add`、`update`、`upsert`、`query`の呼び出し時に使用できる
直接使用でデバッグに利用することもできる

```python
val = default_ef(["foo"])

# [[0.05035809800028801, 0.0626462921500206, -0.061827320605516434...]]
```

### Sentence Transformers

任意のモデルを使用して埋め込みを作成することもできる

```python
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
```

`model_name`引数を指定することで、使用するSentence Transformersモデルを選択
デフォルトでは、Chromaは`all-MiniLM-L6-v2`を使用
[モデルのリスト](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)

### カスタム埋め込み関数

Chromaで使用するカスタム埋め込み関数を作成することもできる
この関数は`EmbeddingFunction`を継承する必要がある

```python
from chromadb import Documents, EmbeddingFunction, Embeddings
class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # ドキュメントを何らかの方法で埋め込む
        return embeddings
```

# マルチモーダル

Chromaはマルチモーダルコレクションをサポートしている

### マルチモーダル埋め込み関数

Chromaはマルチモーダル埋め込み関数をサポート
→　複数のモダリティからのデータを単一の埋め込み空間に埋め込むことができる
Chromaにはテキストと画像の両方をサポートするOpenCLIP埋め込み関数が組み込まれている

```python
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
embedding_function = OpenCLIPEmbeddingFunction()
```

### データローダー

Chromaはデータローダーをサポートしており、URIを介してChroma自体の外部に保存されたデータを保存およびクエリできる
Chromaはこのデータを保存しない
→　ただし、URIを保存し、必要に応じてURIからデータをロードする
Chromaには、ファイルシステムから画像をロードするためのデータローダーが組み込まれている

```python
from chromadb.utils.data_loaders import ImageLoader
data_loader = ImageLoader()
```

### マルチモーダルコレクション

マルチモーダル埋め込み関数を渡すことで、マルチモーダルコレクションを作成できる
→　URIからデータをロードするには、データローダーも渡す必要がある

```python
import chromadb
client = chromadb.Client()
collection = client.create_collection(
    name='multimodal_collection',
    embedding_function=embedding_function,
    data_loader=data_loader)
```

### データの追加

データモダリティを指定することで、マルチモーダルコレクションにデータを追加できます。
現在、画像がサポートされています。

```python
collection.add(
    ids=['id1', 'id2', 'id3'],
    images=[...] # 画像を表すnumpy配列のリスト
)
```

Chromaはデータを保存しないため、IDからデータへのマッピングを自分で管理する必要があります。

しかし、URI経由で他の場所に保存されているデータを追加することで、Chromaを利用することも可能です。これには、コレクションを作成するときにデータローダーを指定する必要があります。

```python
collection.add(
    ids=['id1', 'id2', 'id3'],
    uris=[...] # データのURIを表す文字列のリスト
)
```

埋め込み関数がマルチモーダルであるため、同じコレクションにテキストも追加できる

```python
collection.add(
    ids=['id4', 'id5', 'id6'],
    texts=["This is a document", "This is another document", "This is a third document"]
)
```

### クエリ

サポートされているモダリティのいずれかを使用して、マルチモーダルコレクションをクエリできます。
→　以下のように画像でクエリを実行できる

```python
results = collection.query(
    query_images=[...] # 画像を表すnumpy配列のリスト
)
```

テキストでクエリを実行することもできる

```python
results = collection.query(
    query_texts=["This is a query document", "This is another query document"]
)
```

データローダーがコレクションに設定されている場合、サポートされているモダリティのデータが他の場所に保存されているURIでクエリを実行することもできます。

```python
results = collection.query(
    query_uris=[...] # データのURIを表す文字列のリスト
)
```

さらに、コレクションにデータローダーが設定されていて、URIが利用可能である場合、結果にデータを含めることができます。

```python
results = collection.query(
    query_images=[...], # 画像を表すnumpy配列のリスト
    includes=['data']
)
```

これにより、利用可能なURIに対して自動的にデータローダーが呼び出され、結果にデータが含まれます。URIも`includes`フィールドとして利用可能です。

### 更新

`add`と同様に、データモダリティを指定することで、マルチモーダルコレクションを更新できます。現在、画像がサポートされています。

```python
collection.update(
    ids=['id1', 'id2', 'id3'],
    images=[...] # 画像を表すnumpy配列のリスト
)
```

特定のIDを持つエントリには、同時に1つのモダリティしか関連付けることができないことに注意してください。更新は既存のモダリティを上書きするため、例えば、最初にテキストが関連付けられていたエントリが画像で更新された場合、そのテキストは更新後には保持されません。

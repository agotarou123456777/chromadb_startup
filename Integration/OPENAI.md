# OpenAI

Chromaは、OpenAIの埋め込みAPIを簡単に利用できるラッパーを提供している
この埋め込み機能は、OpenAIのサーバー上でリモートで実行され、APIキーが必要
APIキーは、OpenAIのアカウントにサインアップすることで取得できる

対応しているOpenAI埋め込みモデルは以下の通り：

1. text-embedding-ada-002
2. text-embedding-3-small
3. text-embedding-3-large

### 詳細情報

詳細については、OpenAIの埋め込みドキュメントを参照
この埋め込み機能は、`openai` Pythonパッケージに依存しており、`pip install openai` でインストールできる
任意の `model_name` 引数を渡すことで、使用するOpenAI埋め込みモデルを選択できる
デフォルトでは、Chromaは `text-embedding-ada-002` を使用する

```python
import chromadb.utils.embedding_functions as embedding_functions
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key="YOUR_API_KEY",
                model_name="text-embedding-3-small"
            )
```

他のプラットフォーム（例えばAzureなど）でOpenAI埋め込みモデルを使用するには、`api_base` および `api_type` パラメータを使用できる

```python
import chromadb.utils.embedding_functions as embedding_functions
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key="YOUR_API_KEY",
                api_base="YOUR_API_BASE_PATH",
                api_type="azure",
                api_version="YOUR_API_VERSION",
                model_name="text-embedding-3-small"
            )
```

---
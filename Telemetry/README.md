# Telemetry

telemetryページ和訳
ref : https://docs.trychroma.com/telemetry

## 概要
・chromadbにはテレメトリ機能がある

[収集されるデータ]
Chromaのバージョンおよび環境の詳細（OS、Pythonバージョン、コンテナ内での実行か、Jupyter Notebookでの実行かなど）
Chromaに付属している埋め込み関数の使用状況およびカスタム埋め込みの集計使用状況（カスタム埋め込み自体に関する情報は収集しません）
コレクションコマンド
コレクションの匿名化されたUUIDおよびアイテム数
個人を特定できる情報や機密情報は収集しない
テレメトリデータの保存および可視化にはPosthogを使用


## テレメトリ機能のオプトアウト（無効化）

1. コード内で anonymized_telemetry を False に設定する

``` python
from chromadb.config import Settings
client = chromadb.Client(Settings(anonymized_telemetry=False))
# or if using PersistentClient
client = chromadb.PersistentClient(path="/path/to/save/to", settings=Settings(anonymized_telemetry=False))
```

1. 環境変数を使用してオプトアウト
ANONYMIZED_TELEMETRYをFalseに設定

```
ANONYMIZED_TELEMETRY=False
```
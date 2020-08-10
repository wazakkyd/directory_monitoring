
特定のフォルダを決められた時間間隔で監視して、変更についてレポートするpythonのプログラムです。

# 使い方

```bash
python directory_monitoring.py [監視したいディレクトリパス]
```

- デフォルトでは10分（600秒）ごとにディレクトリを監視します。
  監視間隔を変えたい場合は `--monitoring_interval` オプションで変更できます。

  ```bash
  python directory_monitoring.py [監視したいディレクトリパス] --monitoring_interval 300
  ```

- ファイルの変更については下記の3種について通知および記録します。
  - 追加
  - 削除
  - 変更
- スクリプトを実行すると下記の二つのファイルが生成されます。
  - `[監視対象ディレクトリ名]_checklist`
  - `YYYY-MM-DD_[監視対象ディレクトリ名].log`

# 必要ライブラリ

- `plyer`
  windowsの通知を表示するために必要です。
  `pip install plyer` でインストールしてください。




# ビルド手順

この文書は、`ptaorg/jp` に置いた元データから、確認用HTML、学校別実態調査票、Mermaid図ソースを生成するための手順です。

## 生成対象

`python scripts/build.py` を実行すると、現在の設計では `dist/` に次の成果物を生成します。

- `pta-school-separation-guideline.html`
- `pta-school-separation-notice-template.html`
- `pta-school-separation-school-survey-form.html`
- `pta-school-separation-school-survey.xlsx`  
  ただし、`artifact_tool` が利用できる環境のみ生成されます。
- `diagrams/chain.mmd`
- `diagrams/before-after.mmd`
- `diagrams/scope.mmd`
- `build-report.txt`

## 実行コマンド

```bash
python scripts/build.py
```

## 注意

このスクリプトは、現段階では次のことを行いません。

- PDF生成
- Mermaid図のSVG化
- `ptaorg.com` 又は `ptaorg.github.io` 本体サイトへの反映
- `dist/` 生成物の自動コミット

`dist/` は生成物置き場であり、`.gitignore` により通常はGit管理しません。

## Excel生成について

学校別実態調査票のExcel生成には `artifact_tool` を使います。

ChatGPTの実行環境では利用できる場合がありますが、一般のローカルPCやGitHub Actionsでは利用できない可能性があります。その場合、`scripts/build.py` はExcel生成だけをスキップし、HTML生成、CSV検証、Mermaid図コピーは続行します。

Excel生成がスキップされた場合、`dist/build-report.txt` に次のような行が出ます。

```text
SKIP xlsx: artifact_tool is not installed in this environment
```

## CSV検証

`build.py` は、次のCSVのヘッダーを検証します。

- `sources/primary-sources.csv`
- `data/separation-checklist.csv`

ヘッダーが想定と異なる場合、`build-report.txt` に `NG csv` と表示されます。

## 今後追加する予定の処理

今後、必要に応じて次の処理を追加します。

1. Mermaid図のSVG生成
2. ガイドライン本文のPDF生成
3. 通知ひな形のPDF生成
4. 学校別実態調査票のPDF版生成
5. 本体サイト掲載用HTMLへの整形

ただし、本体サイトへの反映は、本文・根拠資料・図表・チェックシートの内容が固まってから行います。

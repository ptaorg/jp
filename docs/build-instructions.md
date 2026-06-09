# ビルド手順

この文書は、`ptaorg/jp` に置いた元データから、確認用HTML、学校別実態調査票、Mermaid図ソース、必要に応じてMermaid図SVG、PDFを生成するための手順です。

## 1. 通常ビルド

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

実行コマンド:

```bash
python scripts/build.py
```

## 2. Mermaid図のSVG化

Mermaid図をSVGに変換する場合は、Node.js と Mermaid CLI が必要です。

初回のみ次を実行します。

```bash
npm install
```

その後、次のコマンドでSVGを生成します。

```bash
python scripts/render_diagrams.py
```

又は、次でも実行できます。

```bash
npm run render:diagrams
```

生成されるファイル:

- `dist/diagrams-svg/chain.svg`
- `dist/diagrams-svg/before-after.svg`
- `dist/diagrams-svg/scope.svg`
- `dist/diagram-render-report.txt`

Mermaid CLI が見つからない場合、スクリプトは失敗扱いにせず、`SKIP svg` として終了します。

## 3. PDF生成

PDF生成は、通常ビルドで作成した `dist/*.html` を変換する方式です。

実行コマンド:

```bash
python scripts/build_pdf.py
```

生成されるファイル:

- `dist/pdf/pta-school-separation-guideline.pdf`
- `dist/pdf/pta-school-separation-notice-template.pdf`
- `dist/pdf/pta-school-separation-school-survey-form.pdf`
- `dist/pdf-build-report.txt`

`dist/*.html` が未生成の場合、`scripts/build_pdf.py` は先に `scripts/build.py` を実行します。

PDF変換エンジンは、次の順に探します。

1. WeasyPrint Python module
2. `wkhtmltopdf`
3. Google Chrome / Chromium の headless PDF出力

いずれも見つからない場合、スクリプトは失敗扱いにせず、`SKIP pdf` として終了します。

## 4. 注意

現段階では、次のことを行いません。

- PDFのレンダリング画像検証
- `ptaorg.com` 又は `ptaorg.github.io` 本体サイトへの反映
- `dist/` 生成物の自動コミット

`dist/` は生成物置き場であり、`.gitignore` により通常はGit管理しません。

## 5. Excel生成について

学校別実態調査票のExcel生成には `artifact_tool` を使います。

ChatGPTの実行環境では利用できる場合がありますが、一般のローカルPCやGitHub Actionsでは利用できない可能性があります。その場合、`scripts/build.py` はExcel生成だけをスキップし、HTML生成、CSV検証、Mermaid図コピーは続行します。

Excel生成がスキップされた場合、`dist/build-report.txt` に次のような行が出ます。

```text
SKIP xlsx: artifact_tool is not installed in this environment
```

## 6. CSV検証

`build.py` は、次のCSVのヘッダーを検証します。

- `sources/primary-sources.csv`
- `data/separation-checklist.csv`

ヘッダーが想定と異なる場合、`build-report.txt` に `NG csv` と表示されます。

## 7. 今後追加する予定の処理

今後、必要に応じて次の処理を追加します。

1. PDFレンダリング検証
2. PDF用CSSの調整
3. 本体サイト掲載用HTMLへの整形

ただし、本体サイトへの反映は、本文・根拠資料・図表・チェックシートの内容が固まってから行います。

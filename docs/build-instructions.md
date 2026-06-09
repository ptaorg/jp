# ビルド手順

この文書は、`ptaorg/jp` に置いた元データから、確認用HTML、学校別実態調査票、Mermaid図ソース、必要に応じてMermaid図SVG、PDF、公開用成果物を生成するための手順です。

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

## 2. 標準ライブラリ版XLSX生成

GitHub Actionsなど、`artifact_tool` が使えない環境では、標準ライブラリ版のXLSX生成を使います。

```bash
python scripts/build_plain_xlsx.py
```

生成されるファイル:

- `dist/pta-school-separation-school-survey.xlsx`

## 3. Mermaid図のSVG化

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

GitHub Actions上では、`mermaid-puppeteer-config.json` によりChromiumのサンドボックス設定を調整します。Mermaid CLI が見つからない場合、スクリプトは失敗扱いにせず、`SKIP svg` として終了します。

## 4. PDF生成

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

## 5. 公開用成果物の配置

公開ページから直接リンクする成果物は、`public/` に配置します。

```bash
python scripts/publish_public.py
```

配置先:

- `public/pdf/`
- `public/xlsx/`
- `public/img/`

GitHub Actions の `Build public materials` も同じ処理を実行します。

## 6. 注意

現段階では、次のことを行いません。

- PDFのレンダリング画像検証
- 大元サイト `ptaorg.com` 側の編集

`dist/` は生成物置き場であり、`.gitignore` により通常はGit管理しません。公開に必要な成果物だけを `public/` に配置します。

## 7. Excel生成について

学校別実態調査票のExcel生成には、通常は `scripts/build_plain_xlsx.py` を使います。これは標準ライブラリだけで動作するため、GitHub Actionsでも扱いやすい方式です。

ChatGPT実行環境では `artifact_tool` 版のExcel生成も使えますが、公開用生成では標準ライブラリ版を優先します。

## 8. CSV検証

`build.py` は、次のCSVのヘッダーを検証します。

- `sources/primary-sources.csv`
- `data/separation-checklist.csv`

ヘッダーが想定と異なる場合、`build-report.txt` に `NG csv` と表示されます。

## 9. 今後追加する予定の処理

今後、必要に応じて次の処理を追加します。

1. PDFレンダリング検証
2. PDF用CSSの調整
3. 公開ページ上のリンク確認

ただし、大元サイトへの反映は行わず、まずは `ptaorg/jp` 内で完結させます。

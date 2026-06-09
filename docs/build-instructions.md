# ビルド手順

この文書は、`ptaorg/jp` に置いた元データから、確認用HTML、学校別実態調査票、SVG図表、PDF、公開用成果物を生成するための手順です。

公開ページそのものには、制作手順や内部生成ファイルへの導線を出しません。公開ページで読者に見せるダウンロード導線は、実務で使うPDFとExcelを中心にします。

## 1. 通常ビルド

`python scripts/build.py` を実行すると、`dist/` に次の成果物を生成・検証します。

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

通常ビルドで生成するHTMLは、PDF変換の元にもなります。公開PDFに内部制作メモが混入しないよう、生成HTML末尾には作業用注記を入れません。

## 2. 標準ライブラリ版XLSX生成

GitHub Actionsなど、`artifact_tool` が使えない環境では、標準ライブラリ版のXLSX生成を使います。

```bash
python scripts/build_plain_xlsx.py
```

生成されるファイル:

- `dist/pta-school-separation-school-survey.xlsx`

公開用XLSXの「根拠資料」シートには、一次資料台帳の `引用箇所` 列を含めます。教育委員会が調査票を読む際、単なる資料名ではなく、その資料のどの論点を参照しているのか確認できるようにするためです。

## 3. SVG図表生成

公開ページ本文中の図表は、Mermaidの自動レイアウトではなく、行政資料向けに固定レイアウトで生成します。

```bash
python scripts/render_diagrams.py
```

生成されるファイル:

- `dist/diagrams-svg/chain.svg`
- `dist/diagrams-svg/before-after.svg`
- `dist/diagrams-svg/scope.svg`
- `dist/diagram-render-report.txt`

図表の元データとして `diagrams/*.mmd` は残しますが、公開用SVGは `scripts/render_diagrams.py` が直接生成します。これにより、箱が散らばるだけの図ではなく、行政資料として読みやすい比較図・連鎖図・範囲図にします。

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

## 6. 公開リンク確認

`index.html` の相対リンクと、`public/` に必要な公開成果物が存在するかを確認します。

```bash
python scripts/check_public_links.py
```

公開URLまで確認する場合は、次のように実行します。

```bash
python scripts/check_public_links.py --base-url https://ptaorg.com/jp/
```

出力:

- `public/link-check-report.txt`

GitHub Actions の `Build public materials` では、ローカル存在確認を自動実行します。

## 7. 現在の確認対象

現時点で重視する確認対象は次のとおりです。

1. `docs/guideline.md`、`docs/notice-template.md`、`docs/school-survey-form.md` がPDFへ反映されていること。
2. `data/separation-checklist.csv` が31項目として検証され、Excelへ反映されていること。
3. 公開ページのリンクがPDF・Excel・一次資料台帳・調査票CSVに限定され、Markdown原稿やMermaidソースへの読者向け導線が出ていないこと。
4. 生成PDFに内部制作メモが混入していないこと。
5. PDFの余白、見出し、本文行間が行政資料として読める状態であること。
6. PDFで見出しだけがページ末尾に孤立しないこと。
7. 公開用XLSXの「根拠資料」シートに `引用箇所` 列が含まれていること。
8. 公開ページ本文中のSVG図表が、Mermaid任せの粗い箱図ではなく、行政資料として読みやすい固定レイアウトになっていること。

## 8. 注意

現段階では、次のことは別途確認が必要です。

- PDFのレンダリング画像検証
- 公開URL `https://ptaorg.com/jp/` のブラウザ実表示確認
- 公開URL上のHTTPリンク確認
- 大元サイト `ptaorg.com` 側の編集

`dist/` は生成物置き場であり、`.gitignore` により通常はGit管理しません。公開に必要な成果物だけを `public/` に配置します。

## 9. Excel生成について

学校別実態調査票のExcel生成には、通常は `scripts/build_plain_xlsx.py` を使います。これは標準ライブラリだけで動作するため、GitHub Actionsでも扱いやすい方式です。

ChatGPT実行環境では `artifact_tool` 版のExcel生成も使えますが、公開用生成では標準ライブラリ版を優先します。

## 10. CSV検証

`build.py` は、次のCSVのヘッダーを検証します。

- `sources/primary-sources.csv`
- `data/separation-checklist.csv`

ヘッダーが想定と異なる場合、`build-report.txt` に `NG csv` と表示されます。

## 11. 今後追加する予定の処理

今後、必要に応じて次の処理を追加します。

1. PDFレンダリング検証
2. PDF用CSSの調整
3. 公開URL上のリンク確認結果の精査

ただし、大元サイトへの反映は行わず、まずは `ptaorg/jp` 内で完結させます。

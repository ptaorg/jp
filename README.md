# PTAと学校の分離資料制作リポジトリ

このリポジトリは、教育委員会・学校管理職向けに、PTAと学校の分離原則を説明するための資料を作成・管理し、公開するためのリポジトリです。

## 目的

PTAは、学校の補助機関ではなく、任意加入の社会教育関係団体です。ところが、全国の学校現場では、入会申込記録が確認できないまま会員扱いがなされ、学校徴収金とPTA会費が一体処理され、学校名簿・学校連絡ツール・学校施設・教職員の事務負担を通じて、PTA運営が学校運営と混在している例が見られます。

本リポジトリでは、そうした混在運用を整理し、教育委員会が学校運営上の課題として分離措置を取るための資料を、この `ptaorg/jp` 内で完結する形で作成します。

大元サイト `https://ptaorg.com/` は、PTA適正化推進委員会全体の活動・資料・論考への補助導線として扱います。本リポジトリの本文、根拠資料、図表、調査票は、原則としてこのリポジトリ内で管理します。

## 公開用ページ

- `index.html`  
  教育委員会・学校管理職向けの公開用トップページです。カード型ポータルではなく、本文中心の説明ページとして構成しています。

- `assets/site.css`  
  公開用ページのスタイルです。

## 公開用生成物

公開用成果物は `public/` に配置します。

- `public/pdf/`  
  PDF版のガイドライン、通知ひな形、学校別実態調査票説明を配置します。

- `public/xlsx/`  
  学校別実態調査票のExcelファイルを配置します。

- `public/img/`  
  Mermaid図から生成したSVGを配置します。

`dist/` は作業用生成物置き場です。公開に使う成果物だけを `public/` にコピーします。

## 現在の主要ファイル

- `docs/guideline.md`  
  教育委員会向けPDF本編の元原稿です。

- `docs/notice-template.md`  
  教育委員会通知ひな形の元原稿です。

- `docs/school-survey-form.md`  
  学校別実態調査票の説明文です。

- `docs/build-instructions.md`  
  ローカル又は対応環境でのビルド手順です。

- `sources/primary-sources.csv`  
  法令、通知、一次資料、自治体回答等を管理するための一次資料台帳です。

- `sources/source-notes.md`  
  一次資料の確認状況を記録するメモです。

- `data/separation-checklist.csv`  
  学校別実態調査票の元データです。

- `diagrams/chain.mmd`  
  入会申込記録の欠落から広がる違法・不適切運用の連鎖図です。

- `diagrams/before-after.mmd`  
  現在の混在運用と分離後の運用を比較する図です。

- `diagrams/scope.mmd`  
  学校が関与できる範囲・関与すべきでない範囲を整理する図です。

- `scripts/build.py`  
  Markdown、CSV、Mermaid図を確認・変換し、対応環境ではExcel調査票も生成する最小ビルドスクリプトです。

- `scripts/build_plain_xlsx.py`  
  標準ライブラリだけで学校別実態調査票XLSXを生成する補助スクリプトです。

- `scripts/render_diagrams.py`  
  Mermaid CLI が利用できる環境で、Mermaid図をSVG化する補助スクリプトです。

- `scripts/build_pdf.py`  
  確認用HTMLからPDFを生成する補助スクリプトです。

- `scripts/publish_public.py`  
  生成できたPDF、XLSX、SVGを `public/` に配置する公開用ビルドスクリプトです。

- `.github/workflows/build-public.yml`  
  GitHub Actionsで公開用生成物を作成し、`public/` を更新するワークフローです。

- `package.json`  
  Mermaid CLI を導入するためのNode.js設定です。

## 実行コマンド

通常ビルド:

```bash
python scripts/build.py
```

標準ライブラリ版XLSX生成:

```bash
python scripts/build_plain_xlsx.py
```

Mermaid図のSVG化:

```bash
npm install
python scripts/render_diagrams.py
```

PDF生成:

```bash
python scripts/build_pdf.py
```

公開用生成物の配置:

```bash
python scripts/publish_public.py
```

詳細は `docs/build-instructions.md` を参照してください。

## 現段階で行っていないこと

- GitHub Pages の公開設定確認はまだ行っていません。
- GitHub Actions の実行結果確認はまだ行っていません。
- 横浜市通知、仙台市回答、広島市回答は、正式URL又は本文確認が未了のため、断定引用していません。

## 今後の作業方針

1. GitHub Pages の公開設定を確認する。
2. GitHub Actions `Build public materials` を実行し、`public/` 生成物がコミットされるか確認する。
3. `sources/primary-sources.csv` の未確認資料を精査する。
4. `docs/guideline.md` の本文を一次資料に基づいてさらに補強する。
5. 公開ページ上のPDF・XLSX・SVGリンクを確認する。

## 編集上の注意

- 本リポジトリは、カード型ポータルを作るためではなく、教育委員会が内部共有できる論理資料を整備するためのものです。
- 本文を薄くしてリンク集化しないでください。
- 確認していないURL、資料、法令、判例を断定しないでください。
- 大元サイトへのリンクは補助導線であり、このリポジトリの本文や根拠資料の代替ではありません。

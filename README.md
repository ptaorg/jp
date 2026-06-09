# PTAと学校の分離資料制作リポジトリ

このリポジトリは、教育委員会・学校管理職向けに、PTAと学校の分離原則を説明するための資料を作成・管理するための作業用リポジトリです。

## 目的

PTAは、学校の補助機関ではなく、任意加入の社会教育関係団体です。ところが、全国の学校現場では、入会申込記録が確認できないまま会員扱いがなされ、学校徴収金とPTA会費が一体処理され、学校名簿・学校連絡ツール・学校施設・教職員の事務負担を通じて、PTA運営が学校運営と混在している例が見られます。

本リポジトリでは、そうした混在運用を整理し、教育委員会が学校運営上の課題として分離措置を取るための資料を作成します。

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

- `scripts/render_diagrams.py`  
  Mermaid CLI が利用できる環境で、Mermaid図をSVG化する補助スクリプトです。

- `scripts/build_pdf.py`  
  確認用HTMLからPDFを生成する補助スクリプトです。

- `package.json`  
  Mermaid CLI を導入するためのNode.js設定です。

## 実行コマンド

通常ビルド:

```bash
python scripts/build.py
```

Mermaid図のSVG化:

```bash
npm install
python scripts/render_diagrams.py
```

又は、次でも実行できます。

```bash
npm run render:diagrams
```

PDF生成:

```bash
python scripts/build_pdf.py
```

詳細は `docs/build-instructions.md` を参照してください。

## 現段階で行っていないこと

- PDFのレンダリング画像検証はまだ行っていません。
- `ptaorg.com` または `ptaorg.github.io` 本体サイトへの反映はまだ行っていません。
- `dist/` 生成物の自動コミットは行っていません。
- 横浜市通知、仙台市回答、広島市回答は、正式URL又は本文確認が未了のため、断定引用していません。

## 今後の作業方針

1. `sources/primary-sources.csv` の未確認資料を精査する。
2. `docs/guideline.md` の本文を一次資料に基づいてさらに補強する。
3. Mermaid図のSVG出力結果を確認する。
4. PDF出力結果をレンダリング画像で検証する。
5. 完成物のみを本体サイトへ反映する。

## 編集上の注意

- 本リポジトリは、カード型ポータルを作るためではなく、教育委員会が内部共有できる論理資料を整備するためのものです。
- 本文を薄くしてリンク集化しないでください。
- 確認していないURL、資料、法令、判例を断定しないでください。
- 本体サイトへの反映は、生成物と本文構成が固まってから行います。

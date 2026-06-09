# public

このディレクトリは、`ptaorg/jp` 内で生成した公開用成果物を配置する場所です。

## 配置予定

- `pdf/`  
  教育委員会向けガイドライン、通知ひな形、学校別実態調査票説明のPDFを配置します。

- `xlsx/`  
  学校別実態調査票のExcelファイルを配置します。

- `img/`  
  Mermaid図から生成したSVGを配置します。

## 生成方法

次を実行すると、生成できた成果物だけが `public/` にコピーされます。

```bash
python scripts/publish_public.py
```

GitHub Actions からも同じ処理を実行する予定です。

## 注意

`dist/` は作業用生成物置き場です。公開に使う成果物は、必要なものだけ `public/` に配置します。

#!/usr/bin/env python3
"""
PTAと学校の分離資料を生成・検証する最小ビルドスクリプト。

役割:
- docs/*.md を dist/*.html に変換する
- data/*.csv / sources/*.csv のヘッダーを検証する
- diagrams/*.mmd を dist/ にコピーする
- artifact_tool が利用できる環境では学校別実態調査票 .xlsx を生成する
- dist/build-report.txt を出力する

このスクリプト単体では PDF / SVG / public 配置までは行わない。
公開用生成物の配置は scripts/publish_public.py が担当する。
"""

from __future__ import annotations

import csv
import html
import shutil
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

EXPECTED_CSV_HEADERS = {
    ROOT / "sources" / "primary-sources.csv": [
        "id",
        "資料種別",
        "資料名",
        "発行主体",
        "発出日",
        "確認日",
        "URL",
        "関連論点",
        "引用箇所",
        "掲載先",
        "備考",
    ],
    ROOT / "data" / "separation-checklist.csv": [
        "調査番号",
        "分類",
        "学校への確認事項",
        "回答方式",
        "添付を求める資料",
        "判定",
        "問題がある場合のリスク",
        "教育委員会が取るべき措置",
        "根拠資料ID",
        "備考",
    ],
}

DOCS = [
    (ROOT / "docs" / "guideline.md", DIST / "pta-school-separation-guideline.html", "PTAと学校の分離に関する教育委員会向けガイドライン"),
    (ROOT / "docs" / "notice-template.md", DIST / "pta-school-separation-notice-template.html", "PTAの任意加入及び学校関与の分離について（通知）"),
    (ROOT / "docs" / "school-survey-form.md", DIST / "pta-school-separation-school-survey-form.html", "PTAと学校の関係に関する学校別実態調査票"),
]

DIAGRAMS = [
    ROOT / "diagrams" / "chain.mmd",
    ROOT / "diagrams" / "before-after.mmd",
    ROOT / "diagrams" / "scope.mmd",
]

CSS = """
@page {
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
}
:root {
  color-scheme: light;
  --ink: #172033;
  --muted: #5f6b7a;
  --line: #d8dee8;
  --accent: #0b3a67;
  --paper: #ffffff;
  --soft: #f6f8fb;
}
* { box-sizing: border-box; }
html { background: #ffffff; }
body {
  margin: 0;
  background: #ffffff;
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans JP", "Hiragino Sans", Meiryo, sans-serif;
  font-size: 10.5pt;
  line-height: 1.78;
}
main {
  max-width: none;
  margin: 0;
  padding: 0;
  background: var(--paper);
  min-height: 0;
}
h1 {
  margin: 0 0 14mm;
  padding: 0 0 7mm;
  border-bottom: 4px solid var(--accent);
  font-size: 21pt;
  line-height: 1.35;
  letter-spacing: 0.02em;
  page-break-after: avoid;
  break-after: avoid;
}
h1::before {
  content: "PTA適正化推進委員会 / 教育委員会・学校管理職向け資料";
  display: block;
  margin-bottom: 8mm;
  padding: 3mm 4mm;
  background: var(--accent);
  color: #ffffff;
  font-size: 9.5pt;
  font-weight: 600;
  letter-spacing: 0.04em;
}
h2 {
  margin: 12mm 0 4mm;
  padding: 2.5mm 0 2.5mm 4mm;
  border-left: 6px solid var(--accent);
  border-bottom: 1px solid var(--line);
  font-size: 14.5pt;
  line-height: 1.45;
  page-break-after: avoid;
  break-after: avoid;
  page-break-inside: avoid;
  break-inside: avoid;
}
h3 {
  margin: 8mm 0 3mm;
  font-size: 11.6pt;
  color: var(--accent);
  page-break-after: avoid;
  break-after: avoid;
}
p {
  margin: 0 0 3.8mm;
  orphans: 2;
  widows: 2;
}
ul, ol {
  padding-left: 1.5em;
  margin: 0 0 4mm;
}
li {
  margin: 0 0 1.8mm;
  page-break-inside: avoid;
  break-inside: avoid;
}
code {
  padding: 0.1em 0.35em;
  border-radius: 4px;
  background: #eef2f6;
  font-family: "Noto Sans Mono CJK JP", monospace;
}
hr { border: none; border-top: 1px solid var(--line); margin: 8mm 0; }
.note {
  margin-top: 8mm;
  padding: 4mm 5mm;
  background: #f2f6fa;
  border-left: 5px solid var(--accent);
  color: var(--muted);
  font-size: 9.5pt;
  page-break-inside: avoid;
  break-inside: avoid;
}
@media screen {
  body { background: var(--soft); }
  main { max-width: 920px; margin: 0 auto; padding: 48px 28px 72px; min-height: 100vh; }
}
""".strip()


@dataclass
class CsvCheckResult:
    path: Path
    ok: bool
    message: str
    rows: int = 0


def convert_inline(text: str) -> str:
    """最小限のインライン変換。現段階では安全性重視でHTMLエスケープを優先する。"""
    return html.escape(text, quote=False)


def markdown_to_html(markdown: str, title: str) -> str:
    """この資料用の簡易Markdown変換。依存ライブラリを増やさないため、基本構文だけ処理する。"""
    lines = markdown.splitlines()
    body: list[str] = []
    paragraph: list[str] = []
    in_ul = False
    in_ol = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            body.append(f"<p>{convert_inline(' '.join(paragraph))}</p>")
            paragraph = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            body.append("</ul>")
            in_ul = False
        if in_ol:
            body.append("</ol>")
            in_ol = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            close_lists()
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            close_lists()
            body.append(f"<h1>{convert_inline(stripped[2:].strip())}</h1>")
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            close_lists()
            body.append(f"<h2>{convert_inline(stripped[3:].strip())}</h2>")
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            close_lists()
            body.append(f"<h3>{convert_inline(stripped[4:].strip())}</h3>")
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if in_ol:
                body.append("</ol>")
                in_ol = False
            if not in_ul:
                body.append("<ul>")
                in_ul = True
            body.append(f"<li>{convert_inline(stripped[2:].strip())}</li>")
            continue

        if len(stripped) > 3 and stripped[0].isdigit() and ". " in stripped[:4]:
            flush_paragraph()
            if in_ul:
                body.append("</ul>")
                in_ul = False
            if not in_ol:
                body.append("<ol>")
                in_ol = True
            item = stripped.split(". ", 1)[1]
            body.append(f"<li>{convert_inline(item.strip())}</li>")
            continue

        close_lists()
        paragraph.append(stripped)

    flush_paragraph()
    close_lists()
    body_html = "\n    ".join(body)

    return f"""<!doctype html>
<html lang=\"ja\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <main>
    {body_html}
  </main>
</body>
</html>
"""


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def validate_csv(path: Path, expected_header: list[str]) -> CsvCheckResult:
    if not path.exists():
        return CsvCheckResult(path, False, "missing file")

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return CsvCheckResult(path, False, "empty file")
        rows = sum(1 for _ in reader)

    if header != expected_header:
        return CsvCheckResult(
            path,
            False,
            "header mismatch: expected " + repr(expected_header) + " / actual " + repr(header),
            rows,
        )

    return CsvCheckResult(path, True, "ok", rows)


def build_docs(report: list[str]) -> None:
    for src, dst, title in DOCS:
        if not src.exists():
            report.append(f"NG docs: {src.relative_to(ROOT)} not found")
            continue
        html_text = markdown_to_html(src.read_text(encoding="utf-8"), title)
        dst.write_text(html_text, encoding="utf-8")
        report.append(f"OK docs: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def build_csv_checks(report: list[str]) -> None:
    for path, expected_header in EXPECTED_CSV_HEADERS.items():
        result = validate_csv(path, expected_header)
        status = "OK" if result.ok else "NG"
        report.append(f"{status} csv: {path.relative_to(ROOT)} rows={result.rows} message={result.message}")


def copy_diagrams(report: list[str]) -> None:
    target_dir = DIST / "diagrams"
    target_dir.mkdir(parents=True, exist_ok=True)
    for src in DIAGRAMS:
        if not src.exists():
            report.append(f"NG diagram: {src.relative_to(ROOT)} not found")
            continue
        dst = target_dir / src.name
        shutil.copyfile(src, dst)
        report.append(f"OK diagram: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def build_survey_xlsx(report: list[str]) -> None:
    """artifact_tool が利用できる環境だけで、学校別実態調査票 XLSX を生成する。"""
    try:
        from artifact_tool import SpreadsheetFile, Workbook
    except ImportError:
        report.append("SKIP xlsx: artifact_tool is not installed in this environment")
        return

    survey_path = ROOT / "data" / "separation-checklist.csv"
    sources_path = ROOT / "sources" / "primary-sources.csv"
    if not survey_path.exists() or not sources_path.exists():
        report.append("NG xlsx: required CSV files not found")
        return

    try:
        survey_rows = read_csv_dicts(survey_path)
        source_rows = read_csv_dicts(sources_path)

        wb = Workbook.create()
        survey_sheet = wb.worksheets.add("調査票")
        guide_sheet = wb.worksheets.add("回答区分")
        sources_sheet = wb.worksheets.add("根拠資料")

        survey_headers = [
            "調査番号",
            "分類",
            "学校への確認事項",
            "回答方式",
            "学校回答",
            "補足説明",
            "添付資料名",
            "教育委員会判定",
            "対応状況",
            "根拠資料ID",
            "問題がある場合のリスク",
            "教育委員会が取るべき措置",
            "添付を求める資料",
            "備考",
        ]
        survey_values = [survey_headers]
        for row in survey_rows:
            survey_values.append([
                row.get("調査番号", ""),
                row.get("分類", ""),
                row.get("学校への確認事項", ""),
                row.get("回答方式", ""),
                "",
                "",
                "",
                "",
                "",
                row.get("根拠資料ID", ""),
                row.get("問題がある場合のリスク", ""),
                row.get("教育委員会が取るべき措置", ""),
                row.get("添付を求める資料", ""),
                row.get("備考", ""),
            ])
        survey_end_row = len(survey_values)
        survey_sheet.get_range(f"A1:N{survey_end_row}").values = survey_values
        survey_sheet.freeze_panes.freeze_rows(1)
        survey_sheet.get_range("A1:N1").format = {
            "fill": "#0B3A67",
            "font": {"bold": True, "color": "#FFFFFF"},
            "horizontal_alignment": "center",
            "vertical_alignment": "center",
        }
        survey_sheet.get_range(f"A2:N{survey_end_row}").format.wrap_text = True
        survey_sheet.get_range("A:A").format.column_width = 10
        survey_sheet.get_range("B:B").format.column_width = 14
        survey_sheet.get_range("C:C").format.column_width = 42
        survey_sheet.get_range("D:D").format.column_width = 20
        survey_sheet.get_range("E:E").format.column_width = 18
        survey_sheet.get_range("F:G").format.column_width = 22
        survey_sheet.get_range("H:I").format.column_width = 18
        survey_sheet.get_range("J:J").format.column_width = 20
        survey_sheet.get_range("K:M").format.column_width = 34
        survey_sheet.get_range("N:N").format.column_width = 20
        survey_sheet.tables.add(f"A1:N{survey_end_row}", True, "SchoolSurveyTable")

        survey_sheet.get_range(f"H2:H{survey_end_row}").data_validation = {
            "rule": {"type": "list", "values": ["要是正", "要精査", "要確認", "概ね適正", "該当なし"]}
        }
        survey_sheet.get_range(f"I2:I{survey_end_row}").data_validation = {
            "rule": {"type": "list", "values": ["未着手", "確認中", "学校へ差戻し", "PTA協議中", "是正済み", "対象外"]}
        }

        guide_values = [
            ["区分", "選択肢"],
            ["教育委員会判定", "要是正／要精査／要確認／概ね適正／該当なし"],
            ["対応状況", "未着手／確認中／学校へ差戻し／PTA協議中／是正済み／対象外"],
            ["注意", "学校回答欄は各項目の回答方式に沿って記入する。必要に応じて補足説明と添付資料名を記入する。"],
        ]
        guide_sheet.get_range("A1:B4").values = guide_values
        guide_sheet.get_range("A1:B1").format = {
            "fill": "#0B3A67",
            "font": {"bold": True, "color": "#FFFFFF"},
            "horizontal_alignment": "center",
        }
        guide_sheet.get_range("A:B").format.column_width = 38
        guide_sheet.get_range("A1:B4").format.wrap_text = True

        source_headers = ["id", "資料種別", "資料名", "発行主体", "発出日", "確認日", "URL", "関連論点", "引用箇所", "掲載先", "備考"]
        source_values = [source_headers]
        for row in source_rows:
            source_values.append([row.get(header, "") for header in source_headers])
        sources_end_row = len(source_values)
        sources_sheet.get_range(f"A1:K{sources_end_row}").values = source_values
        sources_sheet.freeze_panes.freeze_rows(1)
        sources_sheet.get_range("A1:K1").format = {
            "fill": "#0B3A67",
            "font": {"bold": True, "color": "#FFFFFF"},
            "horizontal_alignment": "center",
        }
        sources_sheet.get_range(f"A2:K{sources_end_row}").format.wrap_text = True
        sources_sheet.get_range("A:A").format.column_width = 12
        sources_sheet.get_range("B:B").format.column_width = 16
        sources_sheet.get_range("C:C").format.column_width = 36
        sources_sheet.get_range("D:F").format.column_width = 16
        sources_sheet.get_range("G:G").format.column_width = 42
        sources_sheet.get_range("H:K").format.column_width = 28
        sources_sheet.tables.add(f"A1:K{sources_end_row}", True, "SourcesTable")

        output_path = DIST / "pta-school-separation-school-survey.xlsx"
        SpreadsheetFile.export_xlsx(wb).save(str(output_path))
        report.append(f"OK xlsx: {output_path.relative_to(ROOT)}")
    except Exception as exc:  # noqa: BLE001 - build report should capture generation failures
        report.append(f"NG xlsx: {type(exc).__name__}: {exc}")


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    report: list[str] = []
    report.append("PTA school separation materials build report")
    report.append("================================================")
    report.append("This normal build prepares HTML, checks CSV files, and stages diagram sources.")
    report.append("")

    build_docs(report)
    build_csv_checks(report)
    copy_diagrams(report)
    build_survey_xlsx(report)

    report_text = "\n".join(report) + "\n"
    (DIST / "build-report.txt").write_text(report_text, encoding="utf-8")
    print(report_text)

    return 1 if any(line.startswith("NG") for line in report) else 0


if __name__ == "__main__":
    raise SystemExit(main())

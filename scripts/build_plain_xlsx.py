#!/usr/bin/env python3
"""
標準ライブラリだけで学校別実態調査票の簡易XLSXを生成する。

目的:
- GitHub Actions 等で artifact_tool が使えない場合でも、公開用XLSXを生成できるようにする。
- 高度な書式より、閲覧・編集できるXLSXを確実に生成することを優先する。

出力:
- dist/pta-school-separation-school-survey.xlsx
"""

from __future__ import annotations

import csv
import html
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

SURVEY_CSV = ROOT / "data" / "separation-checklist.csv"
SOURCES_CSV = ROOT / "sources" / "primary-sources.csv"
OUTPUT = DIST / "pta-school-separation-school-survey.xlsx"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def col_name(index: int) -> str:
    name = ""
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def sheet_xml(rows: list[list[str]], widths: list[int] | None = None, freeze_top: bool = True) -> str:
    cols = ""
    if widths:
        parts = []
        for idx, width in enumerate(widths, start=1):
            parts.append(f'<col min="{idx}" max="{idx}" width="{width}" customWidth="1"/>')
        cols = "<cols>" + "".join(parts) + "</cols>"

    sheet_views = ""
    if freeze_top:
        sheet_views = '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'

    row_xml = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, value in enumerate(row, start=1):
            ref = f"{col_name(c_idx)}{r_idx}"
            style = ' s="1"' if r_idx == 1 else ""
            cells.append(f'<c r="{ref}" t="inlineStr"{style}><is><t>{esc(value)}</t></is></c>')
        row_xml.append(f'<row r="{r_idx}">' + "".join(cells) + "</row>")

    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
%s
%s
<sheetData>%s</sheetData>
</worksheet>
""" % (sheet_views, cols, "".join(row_xml))


def workbook_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="調査票" sheetId="1" r:id="rId1"/>
    <sheet name="回答区分" sheetId="2" r:id="rId2"/>
    <sheet name="根拠資料" sheetId="3" r:id="rId3"/>
  </sheets>
</workbook>
"""


def workbook_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""


def root_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"""


def content_types() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"""


def styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Yu Gothic"/></font>
    <font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Yu Gothic"/></font>
  </fonts>
  <fills count="2">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF0B3A67"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="2">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
    <xf numFmtId="0" fontId="1" fillId="1" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
  </cellXfs>
</styleSheet>
"""


def build() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    survey_rows = read_rows(SURVEY_CSV)
    source_rows = read_rows(SOURCES_CSV)

    survey_headers = [
        "調査番号", "分類", "学校への確認事項", "回答方式", "学校回答", "補足説明", "添付資料名",
        "教育委員会判定", "対応状況", "根拠資料ID", "問題がある場合のリスク", "教育委員会が取るべき措置", "添付を求める資料", "備考",
    ]
    survey_values = [survey_headers]
    for row in survey_rows:
        survey_values.append([
            row.get("調査番号", ""), row.get("分類", ""), row.get("学校への確認事項", ""), row.get("回答方式", ""), "", "", "", "", "",
            row.get("根拠資料ID", ""), row.get("問題がある場合のリスク", ""), row.get("教育委員会が取るべき措置", ""), row.get("添付を求める資料", ""), row.get("備考", ""),
        ])

    guide_values = [
        ["区分", "選択肢・説明"],
        ["教育委員会判定", "要是正／要精査／要確認／概ね適正／該当なし"],
        ["対応状況", "未着手／確認中／学校へ差戻し／PTA協議中／是正済み／対象外"],
        ["回答方法", "学校回答欄は各項目の回答方式に沿って記入し、必要に応じて補足説明と添付資料名を記入する。"],
    ]

    source_headers = ["id", "資料種別", "資料名", "発行主体", "発出日", "確認日", "URL", "関連論点", "掲載先", "備考"]
    source_values = [source_headers]
    for row in source_rows:
        source_values.append([row.get(header, "") for header in source_headers])

    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types())
        zf.writestr("_rels/.rels", root_rels())
        zf.writestr("xl/workbook.xml", workbook_xml())
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels())
        zf.writestr("xl/styles.xml", styles_xml())
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml(survey_values, [10, 14, 42, 20, 18, 24, 22, 18, 18, 20, 36, 38, 32, 18]))
        zf.writestr("xl/worksheets/sheet2.xml", sheet_xml(guide_values, [26, 70]))
        zf.writestr("xl/worksheets/sheet3.xml", sheet_xml(source_values, [10, 16, 40, 18, 14, 14, 46, 24, 24, 42]))

    print(f"OK xlsx: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()

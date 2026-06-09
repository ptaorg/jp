#!/usr/bin/env python3
"""
PTAと学校の分離資料を生成・検証する最小ビルドスクリプト。

現段階の役割:
- docs/*.md を dist/*.html に変換する
- data/*.csv / sources/*.csv のヘッダーを検証する
- diagrams/*.mmd を dist/ にコピーする
- dist/build-report.txt を出力する

現段階で行わないこと:
- PDF生成
- Excel生成
- ptaorg.com / ptaorg.github.io への反映
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
    (ROOT / "docs" / "notice-template.md", DIST / "pta-school-separation-notice-template.html", "PTAの任意加入及び学校関与の適正化について（通知）"),
    (ROOT / "docs" / "school-survey-form.md", DIST / "pta-school-separation-school-survey-form.html", "PTAと学校の関係に関する学校別実態調査票"),
]

DIAGRAMS = [
    ROOT / "diagrams" / "chain.mmd",
    ROOT / "diagrams" / "before-after.mmd",
    ROOT / "diagrams" / "scope.mmd",
]

CSS = """
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
body {
  margin: 0;
  background: var(--soft);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans JP", "Hiragino Sans", Meiryo, sans-serif;
  line-height: 1.85;
}
main {
  max-width: 920px;
  margin: 0 auto;
  padding: 48px 28px 72px;
  background: var(--paper);
  min-height: 100vh;
}
h1 {
  margin: 0 0 28px;
  padding-bottom: 18px;
  border-bottom: 4px solid var(--accent);
  font-size: 2rem;
  line-height: 1.35;
  letter-spacing: 0.02em;
}
h2 {
  margin-top: 44px;
  padding: 10px 0 10px 16px;
  border-left: 6px solid var(--accent);
  border-bottom: 1px solid var(--line);
  font-size: 1.35rem;
  line-height: 1.5;
}
h3 {
  margin-top: 32px;
  font-size: 1.12rem;
  color: var(--accent);
}
p { margin: 1em 0; }
ul, ol { padding-left: 1.5em; }
li { margin: 0.35em 0; }
code {
  padding: 0.1em 0.35em;
  border-radius: 4px;
  background: #eef2f6;
}
hr { border: none; border-top: 1px solid var(--line); margin: 32px 0; }
.note {
  margin-top: 40px;
  padding: 14px 18px;
  background: #f2f6fa;
  border-left: 5px solid var(--accent);
  color: var(--muted);
  font-size: 0.95rem;
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
    {'\n    '.join(body)}
    <div class=\"note\">このHTMLは作業確認用です。PDF生成・本体サイト反映はまだ行っていません。</div>
  </main>
</body>
</html>
"""


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


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    report: list[str] = []
    report.append("PTA school separation materials build report")
    report.append("================================================")
    report.append("This build does not generate PDF, Excel, or publish to ptaorg.com.")
    report.append("")

    build_docs(report)
    build_csv_checks(report)
    copy_diagrams(report)

    report_text = "\n".join(report) + "\n"
    (DIST / "build-report.txt").write_text(report_text, encoding="utf-8")
    print(report_text)

    return 1 if any(line.startswith("NG") for line in report) else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
公開ページ本文中に表示するSVG図表を生成する。

Mermaidの自動レイアウトでは、行政資料としての読みやすさ、余白、見出し、文字量の制御が難しいため、
このスクリプトでは固定レイアウトのSVGを直接生成する。

出力:
- dist/diagrams-svg/chain.svg
- dist/diagrams-svg/before-after.svg
- dist/diagrams-svg/scope.svg
- dist/diagram-render-report.txt
"""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT_DIR = DIST / "diagrams-svg"

INK = "#172033"
MUTED = "#5f6b7a"
ACCENT = "#0b3a67"
ACCENT_LIGHT = "#e9f1f8"
LINE = "#cfd8e6"
PAPER = "#ffffff"
SOFT = "#f6f8fb"
WARN = "#fff7df"
WARN_LINE = "#d4a72c"
OK = "#eef7f0"
OK_LINE = "#3b7f4b"
NG = "#fff1f1"
NG_LINE = "#b34b4b"
PURPLE = "#f1eefb"
PURPLE_LINE = "#8a75c9"

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans JP','Hiragino Sans',Meiryo,sans-serif"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def text_block(x: int, y: int, lines: list[str], size: int = 22, weight: int = 400, fill: str = INK, leading: int | None = None, anchor: str = "start") -> str:
    if leading is None:
        leading = int(size * 1.45)
    parts = [f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" font-family="{FONT}">']
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else leading
        parts.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    parts.append('</text>')
    return "".join(parts)


def rounded_rect(x: int, y: int, w: int, h: int, fill: str, stroke: str = LINE, sw: int = 2, rx: int = 14) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arrow(x1: int, y1: int, x2: int, y2: int, color: str = ACCENT, width: int = 3) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"/>'


def svg_wrap(width: int, height: int, title: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">PTAと学校の分離原則を説明する行政資料向け図表</desc>
  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M2,2 L10,6 L2,10 Z" fill="{ACCENT}"/>
    </marker>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.08"/>
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="{PAPER}"/>
  {body}
</svg>
'''


def render_chain() -> str:
    w, h = 1280, 460
    body: list[str] = []
    body.append(f'<rect x="34" y="28" width="1212" height="404" rx="18" fill="{SOFT}" stroke="{LINE}" stroke-width="2"/>')
    body.append(f'<rect x="34" y="28" width="1212" height="70" rx="18" fill="{ACCENT}"/>')
    body.append(text_block(64, 73, ["入会申込記録の欠落から広がる違法・不適切運用の連鎖"], 28, 700, "#ffffff"))
    body.append(text_block(64, 128, ["最初の書類不備が、会費・役員・名簿・教職員関与へ連鎖する"], 20, 500, MUTED))

    steps = [
        ("1", ["入会申込", "記録がない"], WARN, WARN_LINE),
        ("2", ["会員根拠が", "確認できない"], WARN, WARN_LINE),
        ("3", ["会費請求・役員選出", "名簿作成が不安定化"], NG, NG_LINE),
        ("4", ["学校名簿・徴収金", "連絡ツールへ依存"], NG, NG_LINE),
        ("5", ["個人情報・職専義務", "施設利用と衝突"], PURPLE, PURPLE_LINE),
        ("6", ["教育委員会の", "分離措置が必要"], ACCENT_LIGHT, ACCENT),
    ]
    x0, y, bw, bh, gap = 64, 188, 168, 118, 35
    centers: list[tuple[int, int]] = []
    for idx, (num, lines, fill, stroke) in enumerate(steps):
        x = x0 + idx * (bw + gap)
        centers.append((x + bw // 2, y + bh // 2))
        body.append(rounded_rect(x, y, bw, bh, fill, stroke, 3, 16))
        body.append(f'<circle cx="{x+30}" cy="{y+30}" r="18" fill="{stroke}"/>')
        body.append(text_block(x+30, y+37, [num], 20, 700, "#ffffff", anchor="middle"))
        body.append(text_block(x+18, y+70, lines, 19, 600, INK, 27))
    for (x1, y1), (x2, y2) in zip(centers, centers[1:]):
        body.append(arrow(x1 + bw // 2 - 4, y1, x2 - bw // 2 + 4, y2))

    body.append(rounded_rect(184, 340, 912, 54, "#ffffff", ACCENT, 2, 12))
    body.append(text_block(640, 374, ["学校がPTAの本来事務を補うほど、公私分離の問題として教育委員会の確認対象になる"], 21, 700, ACCENT, anchor="middle"))
    return svg_wrap(w, h, "入会申込記録の欠落から広がる連鎖", "\n  ".join(body))


def render_before_after() -> str:
    w, h = 1280, 520
    body: list[str] = []
    body.append(f'<rect x="34" y="28" width="1212" height="464" rx="18" fill="{SOFT}" stroke="{LINE}" stroke-width="2"/>')
    body.append(text_block(64, 74, ["混在運用から分離運用へ"], 30, 700, ACCENT))
    body.append(text_block(64, 110, ["学校手続に埋め込まれたPTA事務を、PTA自身の手続へ戻す"], 20, 500, MUTED))

    left_x, right_x, top = 70, 720, 145
    panel_w, panel_h = 490, 285
    body.append(rounded_rect(left_x, top, panel_w, panel_h, NG, NG_LINE, 3, 18))
    body.append(rounded_rect(right_x, top, panel_w, panel_h, OK, OK_LINE, 3, 18))
    body.append(f'<rect x="{left_x}" y="{top}" width="{panel_w}" height="54" rx="18" fill="{NG_LINE}"/>')
    body.append(f'<rect x="{right_x}" y="{top}" width="{panel_w}" height="54" rx="18" fill="{OK_LINE}"/>')
    body.append(text_block(left_x+245, top+36, ["現在の混在運用"], 23, 700, "#ffffff", anchor="middle"))
    body.append(text_block(right_x+245, top+36, ["分離後の適正運用"], 23, 700, "#ffffff", anchor="middle"))

    left_rows = ["入学式・学校説明会にPTA手続が混在", "入会申込記録が不十分", "学校徴収金とPTA会費を一体処理", "学校名簿・学校連絡ツールに依存", "教職員がPTA本来事務を処理"]
    right_rows = ["学校手続とPTA手続を明確に分離", "PTA名義で任意加入を確認", "PTA会費はPTAが独自に請求・管理", "学校情報とPTA会員情報を分離", "学校関与は連絡調整に限定"]
    for i, row in enumerate(left_rows):
        yy = top + 86 + i * 38
        body.append(f'<circle cx="{left_x+28}" cy="{yy-7}" r="6" fill="{NG_LINE}"/>')
        body.append(text_block(left_x+48, yy, [row], 18, 500, INK))
    for i, row in enumerate(right_rows):
        yy = top + 86 + i * 38
        body.append(f'<circle cx="{right_x+28}" cy="{yy-7}" r="6" fill="{OK_LINE}"/>')
        body.append(text_block(right_x+48, yy, [row], 18, 500, INK))

    body.append(arrow(590, 285, 690, 285, ACCENT, 5))
    body.append(text_block(640, 257, ["分離"], 22, 700, ACCENT, anchor="middle"))
    body.append(rounded_rect(214, 452, 852, 38, "#ffffff", ACCENT, 2, 10))
    body.append(text_block(640, 477, ["PTAを学校補助団体ではなく、会員の意思に基づく社会教育関係団体へ戻す"], 20, 700, ACCENT, anchor="middle"))
    return svg_wrap(w, h, "現在の混在運用と分離後の適正運用", "\n  ".join(body))


def render_scope() -> str:
    w, h = 1280, 620
    body: list[str] = []
    body.append(f'<rect x="34" y="28" width="1212" height="564" rx="18" fill="{SOFT}" stroke="{LINE}" stroke-width="2"/>')
    body.append(text_block(64, 74, ["学校が関与できる範囲・関与すべきでない範囲"], 30, 700, ACCENT))
    body.append(text_block(64, 110, ["学校が担えるのは連絡調整と条件確認。PTAの入会・会費・名簿・役員・会計はPTA自身が担う。"], 19, 500, MUTED))

    left_x, right_x, top = 70, 665, 150
    panel_w, panel_h = 545, 330
    body.append(rounded_rect(left_x, top, panel_w, panel_h, OK, OK_LINE, 3, 18))
    body.append(rounded_rect(right_x, top, panel_w, panel_h, WARN, WARN_LINE, 3, 18))
    body.append(f'<rect x="{left_x}" y="{top}" width="{panel_w}" height="58" rx="18" fill="{OK_LINE}"/>')
    body.append(f'<rect x="{right_x}" y="{top}" width="{panel_w}" height="58" rx="18" fill="{WARN_LINE}"/>')
    body.append(text_block(left_x+272, top+38, ["学校が関与できる範囲"], 23, 700, "#ffffff", anchor="middle"))
    body.append(text_block(right_x+272, top+38, ["PTA自身が担う本来事務"], 23, 700, "#ffffff", anchor="middle"))

    left_rows = [
        ["学校とPTAの連絡調整"],
        ["学校教育上必要な範囲での協議"],
        ["施設利用許可に関する条件確認"],
        ["児童生徒に不利益が出ないようにする管理"],
        ["学校行事との日程調整"],
    ]
    right_rows = [
        ["入会意思確認の代行"],
        ["PTA会費の徴収・督促・会計処理"],
        ["役員選出・くじ引き・免除審査"],
        ["PTA会員名簿の作成"],
        ["学校連絡ツールによるPTA内部事務"],
        ["PTA内部文書の作成・配布・回収"],
    ]

    for i, row in enumerate(left_rows):
        yy = top + 92 + i * 45
        body.append(rounded_rect(left_x+28, yy-24, panel_w-56, 34, "#ffffff", "#c7dfce", 1, 8))
        body.append(text_block(left_x+48, yy, row, 18, 500, INK))
    for i, row in enumerate(right_rows):
        yy = top + 82 + i * 39
        body.append(rounded_rect(right_x+28, yy-24, panel_w-56, 32, "#ffffff", "#ead7a0", 1, 8))
        body.append(text_block(right_x+48, yy, row, 18, 500, INK))

    body.append(rounded_rect(236, 520, 808, 48, ACCENT_LIGHT, ACCENT, 2, 12))
    body.append(text_block(640, 551, ["結論：学校関与は連絡調整と条件確認に限定し、PTA本来事務はPTAへ戻す"], 21, 700, ACCENT, anchor="middle"))
    return svg_wrap(w, h, "学校が関与できる範囲と関与すべきでない範囲", "\n  ".join(body))


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    diagrams = {
        "chain.svg": render_chain(),
        "before-after.svg": render_before_after(),
        "scope.svg": render_scope(),
    }

    report: list[str] = []
    report.append("PTA school separation SVG render report")
    report.append("======================================")
    report.append("renderer: fixed-layout SVG generator")

    for filename, content in diagrams.items():
        path = OUTPUT_DIR / filename
        path.write_text(content, encoding="utf-8")
        report.append(f"OK svg: {path.relative_to(ROOT)}")

    report_text = "\n".join(report) + "\n"
    (DIST / "diagram-render-report.txt").write_text(report_text, encoding="utf-8")
    print(report_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

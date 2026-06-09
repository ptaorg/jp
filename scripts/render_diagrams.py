#!/usr/bin/env python3
"""
Mermaid図をSVGへ変換する補助スクリプト。

前提:
- Mermaid CLI (`mmdc`) が利用できる環境でのみSVGを生成する。
- `mmdc` が見つからない場合は失敗扱いにせず、SKIPとして終了する。

出力:
- dist/diagrams-svg/chain.svg
- dist/diagrams-svg/before-after.svg
- dist/diagrams-svg/scope.svg
- dist/diagram-render-report.txt
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT_DIR = DIST / "diagrams-svg"
PUPPETEER_CONFIG = ROOT / "mermaid-puppeteer-config.json"

DIAGRAMS = [
    ROOT / "diagrams" / "chain.mmd",
    ROOT / "diagrams" / "before-after.mmd",
    ROOT / "diagrams" / "scope.mmd",
]


def find_mmdc() -> str | None:
    """mmdc のパスを探す。グローバル、ローカルnode_modulesの順に確認する。"""
    global_cmd = shutil.which("mmdc")
    if global_cmd:
        return global_cmd

    local_cmd = ROOT / "node_modules" / ".bin" / "mmdc"
    if local_cmd.exists():
        return str(local_cmd)

    local_cmd_cmd = ROOT / "node_modules" / ".bin" / "mmdc.cmd"
    if local_cmd_cmd.exists():
        return str(local_cmd_cmd)

    return None


def render_one(mmdc: str, src: Path, dst: Path) -> str:
    if not src.exists():
        return f"NG svg: source not found: {src.relative_to(ROOT)}"

    cmd = [
        mmdc,
        "-i",
        str(src),
        "-o",
        str(dst),
        "-b",
        "transparent",
    ]
    if PUPPETEER_CONFIG.exists():
        cmd.extend(["-p", str(PUPPETEER_CONFIG)])

    result = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True, check=False)
    if result.returncode != 0:
        details = (result.stderr or result.stdout or "unknown error").strip().splitlines()
        tail = " | ".join(details[-5:]) if details else "unknown error"
        return f"NG svg: {src.relative_to(ROOT)} -> {tail}"

    return f"OK svg: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}"


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    report: list[str] = []
    report.append("PTA school separation Mermaid render report")
    report.append("================================================")

    mmdc = find_mmdc()
    if not mmdc:
        report.append("SKIP svg: Mermaid CLI `mmdc` was not found")
        report.append("Install with: npm install")
        report_text = "\n".join(report) + "\n"
        (DIST / "diagram-render-report.txt").write_text(report_text, encoding="utf-8")
        print(report_text)
        return 0

    report.append(f"mmdc: {mmdc}")
    if PUPPETEER_CONFIG.exists():
        report.append(f"puppeteer config: {PUPPETEER_CONFIG.relative_to(ROOT)}")

    for src in DIAGRAMS:
        dst = OUTPUT_DIR / f"{src.stem}.svg"
        report.append(render_one(mmdc, src, dst))

    report_text = "\n".join(report) + "\n"
    (DIST / "diagram-render-report.txt").write_text(report_text, encoding="utf-8")
    print(report_text)

    return 1 if any(line.startswith("NG") for line in report) else 0


if __name__ == "__main__":
    raise SystemExit(main())

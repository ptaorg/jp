#!/usr/bin/env python3
"""
生成物を public/ に配置するための公開用ビルドスクリプト。

役割:
- 通常ビルドを実行する
- artifact_tool がない環境でも標準ライブラリ版XLSXを生成する
- PDF生成を試みる
- Mermaid SVG生成を試みる
- 生成できたものだけ public/ にコピーする

出力先:
- public/pdf/
- public/xlsx/
- public/img/
- public/public-build-report.txt
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PUBLIC = ROOT / "public"

PUBLIC_PDF = PUBLIC / "pdf"
PUBLIC_XLSX = PUBLIC / "xlsx"
PUBLIC_IMG = PUBLIC / "img"


def run_step(name: str, command: list[str], report: list[str]) -> None:
    result = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, check=False)
    status = "OK" if result.returncode == 0 else "NG"
    report.append(f"{status} step: {name}")
    output = (result.stdout or "").strip()
    error = (result.stderr or "").strip()
    if output:
        report.append(output)
    if error:
        report.append(error)


def copy_if_exists(src: Path, dst: Path, report: list[str]) -> None:
    if not src.exists():
        report.append(f"SKIP public: source not found: {src.relative_to(ROOT)}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    report.append(f"OK public: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def main() -> int:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    PUBLIC_PDF.mkdir(parents=True, exist_ok=True)
    PUBLIC_XLSX.mkdir(parents=True, exist_ok=True)
    PUBLIC_IMG.mkdir(parents=True, exist_ok=True)

    report: list[str] = []
    report.append("PTA school separation public build report")
    report.append("=========================================")

    run_step("normal build", [sys.executable, "scripts/build.py"], report)

    # artifact_tool がない環境でも公開用XLSXを生成できるように、標準ライブラリ版を必ず試す。
    run_step("plain xlsx build", [sys.executable, "scripts/build_plain_xlsx.py"], report)

    run_step("pdf build", [sys.executable, "scripts/build_pdf.py"], report)
    run_step("svg render", [sys.executable, "scripts/render_diagrams.py"], report)

    copy_if_exists(DIST / "pdf" / "pta-school-separation-guideline.pdf", PUBLIC_PDF / "pta-school-separation-guideline.pdf", report)
    copy_if_exists(DIST / "pdf" / "pta-school-separation-notice-template.pdf", PUBLIC_PDF / "pta-school-separation-notice-template.pdf", report)
    copy_if_exists(DIST / "pdf" / "pta-school-separation-school-survey-form.pdf", PUBLIC_PDF / "pta-school-separation-school-survey-form.pdf", report)
    copy_if_exists(DIST / "pta-school-separation-school-survey.xlsx", PUBLIC_XLSX / "pta-school-separation-school-survey.xlsx", report)

    copy_if_exists(DIST / "diagrams-svg" / "chain.svg", PUBLIC_IMG / "chain.svg", report)
    copy_if_exists(DIST / "diagrams-svg" / "before-after.svg", PUBLIC_IMG / "before-after.svg", report)
    copy_if_exists(DIST / "diagrams-svg" / "scope.svg", PUBLIC_IMG / "scope.svg", report)

    report_text = "\n".join(report) + "\n"
    (PUBLIC / "public-build-report.txt").write_text(report_text, encoding="utf-8")
    print(report_text)

    # 生成失敗があっても、公開できたものがあれば0で終える。個別失敗はレポートで確認する。
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

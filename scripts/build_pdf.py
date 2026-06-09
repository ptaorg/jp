#!/usr/bin/env python3
"""
確認用HTMLからPDFを生成する補助スクリプト。

前提:
- まず `scripts/build.py` で dist/*.html を生成する。
- PDF変換ツールが利用できる環境でのみPDFを生成する。
- 変換ツールが見つからない場合は失敗扱いにせず、SKIPとして終了する。

優先順位:
1. WeasyPrint Python module
2. wkhtmltopdf command
3. Chrome / Chromium headless print-to-pdf

出力:
- dist/pdf/pta-school-separation-guideline.pdf
- dist/pdf/pta-school-separation-notice-template.pdf
- dist/pdf/pta-school-separation-school-survey-form.pdf
- dist/pdf-build-report.txt
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PDF_DIR = DIST / "pdf"

PDF_TARGETS = [
    (
        DIST / "pta-school-separation-guideline.html",
        PDF_DIR / "pta-school-separation-guideline.pdf",
    ),
    (
        DIST / "pta-school-separation-notice-template.html",
        PDF_DIR / "pta-school-separation-notice-template.pdf",
    ),
    (
        DIST / "pta-school-separation-school-survey-form.html",
        PDF_DIR / "pta-school-separation-school-survey-form.pdf",
    ),
]

CHROME_COMMANDS = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "msedge",
    "microsoft-edge",
]


def ensure_html_exists(report: list[str]) -> bool:
    """HTMLがなければ通常ビルドを試みる。"""
    missing = [src for src, _ in PDF_TARGETS if not src.exists()]
    if not missing:
        return True

    report.append("INFO pdf: source HTML not found; running scripts/build.py first")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build.py")],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        report.append("NG pdf: scripts/build.py failed before PDF generation")
        if result.stderr.strip():
            report.append(result.stderr.strip())
        return False

    still_missing = [src.relative_to(ROOT) for src, _ in PDF_TARGETS if not src.exists()]
    if still_missing:
        report.append("NG pdf: source HTML still missing: " + ", ".join(map(str, still_missing)))
        return False

    return True


def find_pdf_engine() -> tuple[str, str | None]:
    """利用可能なPDF変換エンジンを返す。"""
    try:
        import weasyprint  # type: ignore  # noqa: F401
        return "weasyprint", None
    except Exception:
        pass

    wkhtmltopdf = shutil.which("wkhtmltopdf")
    if wkhtmltopdf:
        return "wkhtmltopdf", wkhtmltopdf

    for command in CHROME_COMMANDS:
        path = shutil.which(command)
        if path:
            return "chrome", path

    return "none", None


def render_with_weasyprint(src: Path, dst: Path) -> tuple[bool, str]:
    try:
        from weasyprint import HTML  # type: ignore

        HTML(filename=str(src)).write_pdf(str(dst))
        return True, f"OK pdf: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}"
    except Exception as exc:  # noqa: BLE001
        return False, f"NG pdf: weasyprint failed for {src.relative_to(ROOT)}: {type(exc).__name__}: {exc}"


def render_with_wkhtmltopdf(command: str, src: Path, dst: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [command, "--encoding", "utf-8", str(src), str(dst)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return True, f"OK pdf: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}"
    message = (result.stderr or result.stdout or "unknown error").strip().splitlines()
    return False, f"NG pdf: wkhtmltopdf failed for {src.relative_to(ROOT)}: {message[-1] if message else 'unknown error'}"


def render_with_chrome(command: str, src: Path, dst: Path) -> tuple[bool, str]:
    file_url = src.resolve().as_uri()
    result = subprocess.run(
        [
            command,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--print-to-pdf={dst}",
            file_url,
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0 and dst.exists():
        return True, f"OK pdf: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}"
    message = (result.stderr or result.stdout or "unknown error").strip().splitlines()
    return False, f"NG pdf: chrome failed for {src.relative_to(ROOT)}: {message[-1] if message else 'unknown error'}"


def render_pdf(engine: str, command: str | None, src: Path, dst: Path) -> tuple[bool, str]:
    if engine == "weasyprint":
        return render_with_weasyprint(src, dst)
    if engine == "wkhtmltopdf" and command:
        return render_with_wkhtmltopdf(command, src, dst)
    if engine == "chrome" and command:
        return render_with_chrome(command, src, dst)
    return False, "NG pdf: no PDF engine available"


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    report: list[str] = []
    report.append("PTA school separation PDF build report")
    report.append("======================================")

    if not ensure_html_exists(report):
        report_text = "\n".join(report) + "\n"
        (DIST / "pdf-build-report.txt").write_text(report_text, encoding="utf-8")
        print(report_text)
        return 1

    engine, command = find_pdf_engine()
    if engine == "none":
        report.append("SKIP pdf: no PDF engine found")
        report.append("Install one of: WeasyPrint, wkhtmltopdf, Google Chrome, Chromium")
        report_text = "\n".join(report) + "\n"
        (DIST / "pdf-build-report.txt").write_text(report_text, encoding="utf-8")
        print(report_text)
        return 0

    report.append(f"PDF engine: {engine}{' (' + command + ')' if command else ''}")
    for src, dst in PDF_TARGETS:
        ok, message = render_pdf(engine, command, src, dst)
        report.append(message)
        if ok and dst.exists():
            size_kb = dst.stat().st_size // 1024
            report.append(f"INFO pdf: {dst.name} size={size_kb}KB")

    report_text = "\n".join(report) + "\n"
    (DIST / "pdf-build-report.txt").write_text(report_text, encoding="utf-8")
    print(report_text)

    return 1 if any(line.startswith("NG") for line in report) else 0


if __name__ == "__main__":
    raise SystemExit(main())

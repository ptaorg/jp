#!/usr/bin/env python3
"""
公開ページのリンク確認スクリプト。

役割:
- index.html 内の href/src を抽出する
- 外部URL、アンカー、mailto 等を除外する
- `ptaorg/jp` リポジトリ内の相対リンク先が存在するか確認する
- 必要に応じて公開URLへのHTTP確認も行う

出力:
- public/link-check-report.txt

使い方:
- ローカル存在確認のみ:
  python scripts/check_public_links.py

- 公開URLのHTTP確認も行う:
  python scripts/check_public_links.py --base-url https://ptaorg.com/jp/
"""

from __future__ import annotations

import argparse
import html.parser
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
INDEX = ROOT / "index.html"
REPORT = PUBLIC / "link-check-report.txt"

SKIP_PREFIXES = (
    "#",
    "mailto:",
    "tel:",
    "javascript:",
)

REQUIRED_PUBLIC_FILES = [
    "public/pdf/pta-school-separation-guideline.pdf",
    "public/pdf/pta-school-separation-notice-template.pdf",
    "public/pdf/pta-school-separation-school-survey-form.pdf",
    "public/xlsx/pta-school-separation-school-survey.xlsx",
    "public/img/chain.svg",
    "public/img/before-after.svg",
    "public/img/scope.svg",
]


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value for key, value in attrs if value}
        if tag == "a" and "href" in attr_map:
            self.links.append(("href", attr_map["href"] or ""))
        if tag in {"img", "script"} and "src" in attr_map:
            self.links.append(("src", attr_map["src"] or ""))
        if tag == "link" and "href" in attr_map:
            self.links.append(("href", attr_map["href"] or ""))


def is_external(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in {"http", "https"}


def should_skip(url: str) -> bool:
    return not url or url.startswith(SKIP_PREFIXES)


def local_path_for(url: str) -> Path:
    clean = url.split("#", 1)[0].split("?", 1)[0]
    return (ROOT / urllib.parse.unquote(clean)).resolve()


def is_inside_root(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
        return True
    except ValueError:
        return False


def check_local_links(report: list[str]) -> bool:
    if not INDEX.exists():
        report.append("NG local: index.html not found")
        return False

    parser = LinkParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))

    ok = True
    seen: set[str] = set()
    report.append("Local link check")
    report.append("----------------")

    for attr, url in parser.links:
        if url in seen:
            continue
        seen.add(url)

        if should_skip(url):
            continue
        if is_external(url):
            report.append(f"SKIP external: {url}")
            continue

        path = local_path_for(url)
        if not is_inside_root(path):
            report.append(f"NG local: {attr}={url} points outside repository")
            ok = False
            continue
        if path.exists():
            report.append(f"OK local: {url}")
        else:
            report.append(f"NG local: missing {url}")
            ok = False

    report.append("")
    report.append("Required public files")
    report.append("---------------------")
    for rel in REQUIRED_PUBLIC_FILES:
        path = ROOT / rel
        if path.exists():
            report.append(f"OK required: {rel}")
        else:
            report.append(f"NG required: missing {rel}")
            ok = False

    return ok


def http_status(url: str, timeout: int = 20) -> tuple[bool, str]:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "ptaorg-link-check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            code = response.getcode()
            return 200 <= code < 400, str(code)
    except urllib.error.HTTPError as exc:
        # Some hosts reject HEAD. Try GET before failing.
        if exc.code in {403, 405}:
            try:
                get_request = urllib.request.Request(url, method="GET", headers={"User-Agent": "ptaorg-link-check/1.0"})
                with urllib.request.urlopen(get_request, timeout=timeout) as response:
                    code = response.getcode()
                    return 200 <= code < 400, str(code)
            except Exception as get_exc:  # noqa: BLE001
                return False, f"{type(get_exc).__name__}: {get_exc}"
        return False, f"HTTPError: {exc.code}"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def check_public_urls(base_url: str, report: list[str]) -> bool:
    base = base_url.rstrip("/") + "/"
    ok = True
    report.append("")
    report.append("Public URL check")
    report.append("----------------")

    urls = ["", "robots.txt", "sitemap.xml", *REQUIRED_PUBLIC_FILES]
    for rel in urls:
        url = urllib.parse.urljoin(base, rel)
        success, status = http_status(url)
        if success:
            report.append(f"OK public: {url} status={status}")
        else:
            report.append(f"NG public: {url} status={status}")
            ok = False

    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", help="Optional public base URL, e.g. https://ptaorg.com/jp/")
    args = parser.parse_args()

    PUBLIC.mkdir(parents=True, exist_ok=True)
    report: list[str] = []
    report.append("PTA school separation public link check")
    report.append("======================================")

    local_ok = check_local_links(report)
    public_ok = True
    if args.base_url:
        public_ok = check_public_urls(args.base_url, report)

    report_text = "\n".join(report) + "\n"
    REPORT.write_text(report_text, encoding="utf-8")
    print(report_text)

    return 0 if local_ok and public_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

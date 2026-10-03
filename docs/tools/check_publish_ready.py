#!/usr/bin/env python3
"""
check_publish_ready.py - decide which site drafts can be published, based on their link dependencies.

Reads the page register (docs/templates/pages.csv), scans every registered HTML file in
docs/site-drafts, and reports for each page:
  - draft markers still in the file ([EDITOR], TODO, TBC, verify highlights, draft banners)
  - every internal link, the page it points to, and that page's status
  - missing #anchors (e.g. /compare-all-tets.html#ctet-accepted)
  - links to pages that are not in the register at all

A page is PUBLISHABLE only when its own status is READY, it has no draft markers, and every page
it links to is PUBLISHED, or is READY and ships in the same release ("publish together").

It also writes docs/templates/page-dependencies.csv (generated; do not edit by hand).

Usage:
    python docs/tools/check_publish_ready.py              # all pages
    python docs/tools/check_publish_ready.py P020         # one page
    python docs/tools/check_publish_ready.py --external   # also check external links over HTTP
"""
import csv
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

DOCS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(DOCS_DIR, "site-drafts")
REGISTER = os.path.join(DOCS_DIR, "templates", "pages.csv")
DEPS_OUT = os.path.join(DOCS_DIR, "templates", "page-dependencies.csv")
SITE_ORIGIN = "https://easyctet.com"

DRAFT_MARKERS = {
    "[EDITOR] note": re.compile(r"\[EDITOR"),
    "TODO": re.compile(r"\bTODO\b"),
    "TBC": re.compile(r"\bTBC\b"),
    "verify highlight": re.compile(r'class="[^"]*\bverify\b'),
    "draft banner": re.compile(r'class="[^"]*\b(draft|draft-banner)\b'),
}
OK_TARGET = {"PUBLISHED"}
SHIP_TOGETHER = {"READY"}


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])


def parse(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    p = LinkParser()
    p.feed(text)
    return text, p.hrefs, p.ids


def norm(url):
    """Comparable form of a URL: scheme-less host + path, no query or fragment, no index.html.
    For query-keyed endpoints (like play.google.com?id=...), keep the primary id."""
    s = urlsplit(url)
    path = re.sub(r"/index\.html$", "/", s.path or "/")
    host = s.netloc.lower() or urlsplit(SITE_ORIGIN).netloc
    if "play.google.com" in host:
        from urllib.parse import parse_qs
        qs = parse_qs(s.query)
        app_id = qs.get("id", [""])[0]
        if app_id:
            return f"{host}{path}?id={app_id}"
    return host + path


def http_status(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:
        code = f"ERR {type(e).__name__}"
    # Some government sites block Python's client or use legacy TLS; retry the way a browser would.
    if shutil.which("curl"):
        out = subprocess.run(["curl", "-s", "-o", os.devnull, "-L", "-m", "40", "-A",
                              "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "-w", "%{http_code}", url],
                             capture_output=True, text=True)
        if out.stdout.strip().isdigit():
            return int(out.stdout.strip())
    return code


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_external = "--external" in sys.argv

    with open(REGISTER, newline="", encoding="utf-8-sig") as f:
        pages = list(csv.DictReader(f))
    by_url = {norm(urljoin(SITE_ORIGIN, p["url"])): p for p in pages}
    parsed = {}
    for p in pages:
        if p["file"]:
            path = os.path.join(SITE_DIR, p["file"])
            parsed[p["page_id"]] = parse(path) if os.path.exists(path) else None

    dep_rows, ext_cache = [], {}
    targets = [p for p in pages if p["file"] and (not args or p["page_id"] in args)]

    for page in targets:
        pid, status = page["page_id"], page["status"]
        print(f"\n{pid}  {page['file']}  [{status}]")
        blockers, together = [], set()

        if status not in {"READY", "PUBLISHED"}:
            blockers.append(f"page status is {status}, not READY or PUBLISHED")
        if parsed[pid] is None:
            print("  ! file not found in site-drafts")
            continue
        text, hrefs, own_ids = parsed[pid]

        for name, rx in DRAFT_MARKERS.items():
            n = len(rx.findall(text))
            if n:
                blockers.append(f"{n} x {name} still in the file")

        page_abs = urljoin(SITE_ORIGIN, page["url"])
        for href in dict.fromkeys(hrefs):
            if href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            absolute = urljoin(page_abs, href)
            frag = urlsplit(absolute).fragment
            internal = urlsplit(absolute).netloc == urlsplit(SITE_ORIGIN).netloc
            target = by_url.get(norm(absolute))

            if target is None and not internal:
                if check_external:
                    if absolute not in ext_cache:
                        ext_cache[absolute] = http_status(absolute)
                    code = ext_cache[absolute]
                    ok = code == 200
                    print(f"  {'ok ' if ok else 'BAD'} external {code}  {href}")
                    if not ok:
                        blockers.append(f"external link returns {code}: {href}")
                continue

            if target is None:
                verdict = "BLOCK: not in register"
                blockers.append(f"links to {href}, which is not in pages.csv")
                tstatus, tid, anchor_ok = "", "", ""
            else:
                tid, tstatus = target["page_id"], target["status"]
                anchor_ok = ""
                if frag:
                    tparsed = own_ids if tid == pid else (parsed.get(tid) or (None, None, set()))[2]
                    anchor_ok = "yes" if tparsed and frag in tparsed else "NO"
                    if anchor_ok == "NO":
                        blockers.append(f"anchor #{frag} not found in {tid}")
                if tid == pid or tstatus in OK_TARGET:
                    verdict = "ok"
                elif tstatus in SHIP_TOGETHER:
                    verdict = "ship together"
                    together.add(tid)
                elif tstatus == "RETIRED":
                    verdict = f"BLOCK: retired, link to {target['redirect_to']} instead"
                    blockers.append(f"links to retired page {tid}")
                else:
                    verdict = f"BLOCK: target is {tstatus}"
                    blockers.append(f"links to {tid} ({target['title']}), which is {tstatus}")
            print(f"  {verdict:<34} {href}  ->  {tid or '?'} {tstatus}"
                  + (f"  anchor:{anchor_ok}" if anchor_ok else ""))
            dep_rows.append([pid, href, tid, tstatus, anchor_ok, verdict])

        if blockers:
            print("  => BLOCKED")
            for b in dict.fromkeys(blockers):
                print(f"     - {b}")
        else:
            extra = f" (publish together with {', '.join(sorted(together))})" if together else ""
            print(f"  => PUBLISHABLE{extra}")

    if not args:
        with open(DEPS_OUT, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["page_id", "link", "target_page_id", "target_status", "anchor_found", "verdict"])
            w.writerows(dep_rows)
        print(f"\nWrote {os.path.relpath(DEPS_OUT, DOCS_DIR)}")


if __name__ == "__main__":
    main()

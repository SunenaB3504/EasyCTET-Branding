#!/usr/bin/env python3
"""
collect_forum_titles.py - collect PUBLIC discussion titles about teacher-eligibility exams for keyword research.

READ THIS FIRST
  * Check the target site's terms of service and robots.txt BEFORE running. Many sites (for example Quora) forbid
    automated collection; others (for example Reddit) provide an official API you should use instead.
  * This script refuses to run unless you pass --confirm-terms-checked, and it stops if robots.txt disallows the URL.
  * It identifies itself honestly (User-Agent with your contact email), uses randomised delays, and STOPS (it never
    tries to bypass) if it meets a CAPTCHA, a rate-limit page or a block page.
  * It collects only titles, links and public counts. It does not collect usernames or any personal data.
  * Titles are not search queries. Treat the output as raw ideas, then confirm demand in Search Console.

USAGE
  1. Fill in the CONFIG block below (start URL, contact email, CSS selectors).
  2. python collect_forum_titles.py --confirm-terms-checked
  Other options:
     --url URL              override START_URL
     --output FILE          default aspirant_forum_titles.csv (use aspirant_queries.csv if you prefer that name)
     --max-scrolls N        --max-results N        --no-headless
     --from-html FILE       parse a page you saved by hand (no browser, no network)
     --selftest             run the cleaning/sorting logic on built-in sample data

REQUIRES  pip install selenium beautifulsoup4     (Selenium 4 downloads the browser driver by itself; Chrome needed)
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import json
import logging
import random
import re
import sys
import time
import unicodedata
import urllib.robotparser
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

# =====================================================================================================
# CONFIG - edit this block
# =====================================================================================================
PLACEHOLDER = "<<<INSERT"


@dataclass
class Config:
    # --- where to collect from ---------------------------------------------------------------------
    START_URL: str = "<<<INSERT the search-results or listing URL you are allowed to collect from>>>"
    SOURCE_NAME: str = "<<<INSERT short site name, e.g. 'example-forum'>>>"
    CONTACT_EMAIL: str = "<<<INSERT your contact email (sent in the User-Agent)>>>"

    # --- CSS selectors for the target site (open the page, right-click > Inspect, copy the selector) --
    # One selector that matches EACH result block (a thread/question card):
    ITEM_SELECTOR: str = "<<<INSERT CSS selector for each result block, e.g. 'div.result-card'>>>"
    # Inside a result block: the element holding the title text. Use "" if the block itself is the title.
    TITLE_SELECTOR: str = "<<<INSERT CSS selector for the title inside a block, e.g. 'a.title'>>>"
    # Inside a result block: the link element (its href is used). Use "" to reuse the title element.
    LINK_SELECTOR: str = ""
    # Optional (use "" if the site does not show them):
    DATE_SELECTOR: str = ""         # e.g. 'time' (the datetime attribute is preferred when present)
    SCORE_SELECTOR: str = ""        # e.g. 'span.votes' or 'span.answers'

    # --- behaviour -----------------------------------------------------------------------------------
    HEADLESS: bool = True
    MAX_SCROLLS: int = 15            # hard stop for infinite scroll
    MAX_RESULTS: int = 500
    STOP_AFTER_NO_NEW: int = 2       # stop after this many scrolls that add no new items
    PAGE_LOAD_TIMEOUT_S: int = 30
    SCROLL_PAUSE_S: tuple = (2.0, 4.5)   # random pause range between scrolls (be gentle)
    NEAR_DUPLICATE_RATIO: float = 0.92   # flag (not delete) titles at least this similar
    OUTPUT_CSV: str = "aspirant_forum_titles.csv"


CFG = Config()

# Words that appear on CAPTCHA / block pages. If any is seen the script stops; it never tries to get around it.
BLOCK_MARKERS = ("captcha", "unusual traffic", "are you a robot", "are you a human", "access denied",
                 "too many requests", "rate limit", "verify you are human", "temporarily blocked")

EXAMS = [
    ("CTET", r"\bctet\b"), ("UPTET", r"\bup\s?-?tet\b|\buptet\b"), ("REET", r"\breet\b"), ("HTET", r"\bhtet\b"),
    ("KTET", r"\bk\s?-?tet\b|\bktet\b"), ("MPTET", r"\bmp\s?-?tet\b|\bmptet\b"),
    ("BIHAR_STET", r"\bbihar\s?stet\b|\bbstet\b|\bstet\b"), ("SUPER_TET", r"\bsuper\s?tet\b"),
    ("KVS", r"\bkvs\b"), ("NVS", r"\bnvs\b"), ("EMRS", r"\bemrs\b"), ("PSTET", r"\bpstet\b"),
]
HINGLISH_WORDS = {"aur", "kya", "hai", "hain", "me", "mein", "ke", "ka", "ki", "ko", "kaise", "kaun", "nahi", "nahin",
                  "hota", "hoga", "kab", "kitna", "kitne", "tayari", "paper", "ya", "se", "par", "liye", "antar"}

log = logging.getLogger("collector")


# =====================================================================================================
# Helpers: guard rails
# =====================================================================================================
def user_agent(cfg: Config) -> str:
    return f"AspirantQueryResearch/1.0 (+mailto:{cfg.CONTACT_EMAIL}; keyword research, low rate)"


def require_configured(cfg: Config) -> None:
    missing = [k for k, v in vars(cfg).items() if isinstance(v, str) and v.startswith(PLACEHOLDER)]
    if missing:
        sys.exit("Fill in these CONFIG values first: " + ", ".join(missing))


def robots_allows(url: str, ua: str) -> bool:
    parts = urlparse(url)
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{parts.scheme}://{parts.netloc}/robots.txt")
    try:
        rp.read()
    except Exception as exc:  # network problem: be conservative
        log.warning("Could not read robots.txt (%s). Not proceeding.", exc)
        return False
    return rp.can_fetch(ua, url)


def looks_blocked(page_source: str) -> bool:
    low = page_source.lower()
    return any(m in low for m in BLOCK_MARKERS)


# =====================================================================================================
# Step 1: load the page with Selenium (explicit waits, bounded infinite scroll)
# =====================================================================================================
def load_and_scroll(cfg: Config) -> str:
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    opts = Options()
    if cfg.HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument(f"--user-agent={user_agent(cfg)}")
    opts.add_argument("--window-size=1280,1800")
    driver = None
    try:
        driver = webdriver.Chrome(options=opts)
        driver.set_page_load_timeout(cfg.PAGE_LOAD_TIMEOUT_S)
        log.info("Opening %s", cfg.START_URL)
        driver.get(cfg.START_URL)
        time.sleep(random.uniform(*cfg.SCROLL_PAUSE_S))
        if looks_blocked(driver.page_source):
            log.error("The site is showing a CAPTCHA or block page. Stopping (no bypass attempted).")
            return ""
        try:
            WebDriverWait(driver, cfg.PAGE_LOAD_TIMEOUT_S).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, cfg.ITEM_SELECTOR)))
        except TimeoutException:
            log.error("No element matched ITEM_SELECTOR within %ss. Check the selector or the page.", cfg.PAGE_LOAD_TIMEOUT_S)
            return driver.page_source

        seen, idle = 0, 0
        for i in range(1, cfg.MAX_SCROLLS + 1):
            count = len(driver.find_elements(By.CSS_SELECTOR, cfg.ITEM_SELECTOR))
            log.info("Scroll %d/%d: %d items on page", i, cfg.MAX_SCROLLS, count)
            if count >= cfg.MAX_RESULTS:
                log.info("Reached MAX_RESULTS (%d).", cfg.MAX_RESULTS)
                break
            idle = idle + 1 if count == seen else 0
            if idle >= cfg.STOP_AFTER_NO_NEW:
                log.info("No new items after %d scrolls; stopping.", idle)
                break
            seen = count
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(*cfg.SCROLL_PAUSE_S))
            if looks_blocked(driver.page_source):
                log.error("Block/CAPTCHA page appeared while scrolling. Stopping (no bypass attempted).")
                break
        return driver.page_source
    except WebDriverException as exc:
        log.error("Browser error: %s", exc)
        return ""
    finally:
        if driver is not None:
            driver.quit()


# =====================================================================================================
# Step 2: extract with BeautifulSoup (selectors come from CONFIG)
# =====================================================================================================
def extract(html: str, cfg: Config, base_url: str = "") -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for block in soup.select(cfg.ITEM_SELECTOR):
        try:
            t_el = block.select_one(cfg.TITLE_SELECTOR) if cfg.TITLE_SELECTOR else block
            if t_el is None:
                continue
            title = t_el.get_text(" ", strip=True)
            l_el = block.select_one(cfg.LINK_SELECTOR) if cfg.LINK_SELECTOR else t_el
            href = l_el.get("href", "") if l_el is not None else ""
            url = urljoin(base_url or cfg.START_URL, href) if href else ""
            date = ""
            if cfg.DATE_SELECTOR:
                d_el = block.select_one(cfg.DATE_SELECTOR)
                if d_el is not None:
                    date = d_el.get("datetime") or d_el.get_text(" ", strip=True)
            score = ""
            if cfg.SCORE_SELECTOR:
                s_el = block.select_one(cfg.SCORE_SELECTOR)
                if s_el is not None:
                    score = s_el.get_text(" ", strip=True)
            if title:
                out.append({"title": title, "url": url, "date_posted": date, "score_or_answers": score})
        except Exception as exc:  # one broken block must not stop the run
            log.warning("Skipped a block: %s", exc)
    log.info("Extracted %d raw titles", len(out))
    return out


# =====================================================================================================
# Step 3: clean, de-duplicate, flag near-duplicates, label, sort
# =====================================================================================================
def clean_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip()


def match_key(s: str) -> str:
    """Case-, punctuation- and spacing-insensitive key (keeps Devanagari letters and digits)."""
    s = clean_text(s).casefold()
    s = re.sub(r"[^\w\s]", "", s, flags=re.UNICODE).replace("_", "")
    return re.sub(r"\s+", " ", s).strip()


def detect_language(s: str) -> str:
    if re.search(r"[ऀ-ॿ]", s):
        return "hi"
    words = set(re.findall(r"[a-z]+", s.lower()))
    return "hinglish" if len(words & HINGLISH_WORDS) >= 2 else "en"


def exams_in(s: str) -> str:
    low = s.lower()
    return ";".join(name for name, pat in EXAMS if re.search(pat, low))


def process(rows: list[dict], cfg: Config, source: str) -> list[dict]:
    today = dt.date.today().isoformat()
    freq = Counter(match_key(r["title"]) for r in rows if match_key(r["title"]))
    first: dict[str, dict] = {}
    for r in rows:
        title = clean_text(r["title"])
        key = match_key(title)
        if not key or key in first:
            continue
        first[key] = {
            "title": title, "url": r.get("url", ""), "source": source,
            "date_posted": r.get("date_posted", ""), "score_or_answers": r.get("score_or_answers", ""),
            "language": detect_language(title), "exams_mentioned": exams_in(title),
            "times_seen": freq[key], "near_duplicate_of": "", "collected_on": today,
        }
    keys = list(first)
    for i, k in enumerate(keys):  # flag, do not delete, near-duplicates
        for k2 in keys[:i]:
            if abs(len(k) - len(k2)) < 12 and difflib.SequenceMatcher(None, k, k2).ratio() >= cfg.NEAR_DUPLICATE_RATIO:
                first[k]["near_duplicate_of"] = first[k2]["title"]
                break
    return sorted(first.values(), key=lambda r: (r["exams_mentioned"] == "", r["exams_mentioned"], -r["times_seen"], r["title"].casefold()))


# =====================================================================================================
# Step 4: export
# =====================================================================================================
COLUMNS = ["title", "url", "source", "date_posted", "score_or_answers", "language", "exams_mentioned",
           "times_seen", "near_duplicate_of", "collected_on"]


def export_csv(rows: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:  # BOM so Excel shows Hindi correctly
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    log.info("Wrote %d rows to %s", len(rows), path)


def checkpoint(rows: list[dict], path: str) -> None:
    Path(path + ".raw.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")


# =====================================================================================================
# Self-test and main
# =====================================================================================================
SAMPLE_HTML = """
<div class="card"><a class="t" href="/q/1">Is CTET preparation enough for REET level 1?</a><time datetime="2026-09-01"></time><span class="n">12</span></div>
<div class="card"><a class="t" href="/q/2">is  ctet preparation enough for  REET level 1</a></div>
<div class="card"><a class="t" href="/q/3">UPTET aur CTET ke syllabus me kya antar hai</a></div>
<div class="card"><a class="t" href="/q/4">क्या CTET पास करने से REET दे सकते हैं?</a></div>
<div class="card"><a class="t" href="/q/5">Is CTET preparation enough for REET level 2?</a></div>
<div class="card"><a class="t" href="/q/6">Best free app for pedagogy mock tests (CTET, UPTET, HTET)</a></div>
"""


def selftest() -> int:
    cfg = Config(START_URL="https://example.invalid/search", SOURCE_NAME="sample", CONTACT_EMAIL="you@example.com",
                 ITEM_SELECTOR="div.card", TITLE_SELECTOR="a.t", DATE_SELECTOR="time", SCORE_SELECTOR="span.n")
    rows = process(extract(SAMPLE_HTML, cfg), cfg, cfg.SOURCE_NAME)
    for r in rows:
        print(f"{r['exams_mentioned']:<24}{r['language']:<9}x{r['times_seen']} dup:{'Y' if r['near_duplicate_of'] else '-'}  {r['title']}")
    assert len(rows) == 5, "case/space duplicates should merge (6 titles -> 5)"
    assert sum(1 for r in rows if r["near_duplicate_of"]) == 1, "level 1 vs level 2 should be flagged as near-duplicates"
    print("selftest OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Collect public forum titles for keyword research (see the header).")
    ap.add_argument("--confirm-terms-checked", action="store_true", help="I have read the site's terms and robots.txt")
    ap.add_argument("--url"), ap.add_argument("--output"), ap.add_argument("--from-html")
    ap.add_argument("--max-scrolls", type=int), ap.add_argument("--max-results", type=int)
    ap.add_argument("--no-headless", action="store_true"), ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler("collector.log", encoding="utf-8")])
    if a.selftest:
        return selftest()
    cfg = CFG
    if a.url:
        cfg.START_URL = a.url
    if a.output:
        cfg.OUTPUT_CSV = a.output
    if a.max_scrolls:
        cfg.MAX_SCROLLS = a.max_scrolls
    if a.max_results:
        cfg.MAX_RESULTS = a.max_results
    if a.no_headless:
        cfg.HEADLESS = False
    require_configured(cfg)

    if a.from_html:  # parse a page you saved by hand: no browser, no network
        html = Path(a.from_html).read_text(encoding="utf-8", errors="ignore")
    else:
        if not a.confirm_terms_checked:
            sys.exit("Please read the site's terms of service and robots.txt, then re-run with --confirm-terms-checked.")
        if not robots_allows(cfg.START_URL, user_agent(cfg)):
            sys.exit("robots.txt does not allow this URL (or could not be read). Not collecting.")
        html = load_and_scroll(cfg)
    if not html:
        log.error("No page content collected.")
        return 1
    raw = extract(html, cfg)
    if not raw:
        log.error("0 titles extracted: check ITEM_SELECTOR / TITLE_SELECTOR against the page.")
        return 1
    checkpoint(raw, cfg.OUTPUT_CSV)
    rows = process(raw[: cfg.MAX_RESULTS], cfg, cfg.SOURCE_NAME)
    export_csv(rows, cfg.OUTPUT_CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())

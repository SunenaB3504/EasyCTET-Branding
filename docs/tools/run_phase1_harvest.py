"""
Phase 1 Master Harvester: Multi-Source All-India TET Keyword Ingestion.
Executes Engine 1 (Google Alphabet & Wildcards), Engine 2 (YouTube Suggest),
and Engine 3 (Job Recruitment Bridge Matrix).
Pipes directly into docs/tools/db_manager.py for automated deduplication and slugging.
"""

import sys
import os
import time
import random
import requests
from typing import List, Dict, Set

# Ensure tools directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from db_manager import insert_keyword, export_to_csv, get_stats, init_db

# Headers for browser emulation
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# 18 Target Exams
ALL_EXAMS = [
    # National
    "CTET",
    # South
    "KTET", "TNTET", "TS_TET", "AP_TET", "KARTET",
    # North & Central
    "UPTET", "REET", "HTET", "MPTET", "PSTET", "UTET",
    # West & East
    "MAHA_TET", "WBTET", "OTET", "CG_TET", "BTET", "ASSAM_TET"
]

# Exams with active Hindi-belt candidate bases
HINDI_BELT_EXAMS = {"CTET", "UPTET", "REET", "HTET", "MPTET", "BTET", "CG_TET", "UTET", "PSTET"}

def fetch_google_suggest(session: requests.Session, query: str, retries: int = 3) -> List[str]:
    """Queries Google Web Search suggest with exponential backoff on 429."""
    url = "https://suggestqueries.google.com/complete/search"
    params = {
        "client": "firefox",
        "gl": "in",
        "hl": "en",
        "q": query
    }
    for attempt in range(retries):
        try:
            resp = session.get(url, params=params, headers=HEADERS, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                return data[1] if len(data) > 1 else []
            elif resp.status_code == 429:
                wait_s = (attempt + 1) * 3
                print(f" [Rate-Limited 429] Backing off {wait_s}s...")
                time.sleep(wait_s)
        except requests.RequestException:
            time.sleep(1)
    return []

import json

def fetch_youtube_suggest(session: requests.Session, query: str, retries: int = 3) -> List[str]:
    """Queries YouTube video & voice suggest, parsing JSONP response."""
    url = "https://suggestqueries.google.com/complete/search"
    params = {
        "client": "youtube",
        "ds": "yt",
        "gl": "in",
        "hl": "en",
        "q": query
    }
    for attempt in range(retries):
        try:
            resp = session.get(url, params=params, headers=HEADERS, timeout=6)
            if resp.status_code == 200:
                text = resp.text.strip()
                if text.startswith("window.google.ac.h("):
                    text = text[len("window.google.ac.h("):-1]
                data = json.loads(text)
                results = []
                for item in data[1]:
                    if isinstance(item, list) and len(item) > 0:
                        results.append(str(item[0]))
                    elif isinstance(item, str):
                        results.append(item)
                return results
            elif resp.status_code == 429:
                wait_s = (attempt + 1) * 3
                print(f" [YouTube 429] Backing off {wait_s}s...")
                time.sleep(wait_s)
        except Exception:
            time.sleep(1)
    return []

def run_engine_1_google(session: requests.Session) -> int:
    """Engine 1: Google Alphabet Soup, Prefixes, Wildcards & Code-Mixing."""
    print("\n" + "=" * 65)
    print("ENGINE 1: GOOGLE ALPHABET SOUP, WILDCARDS & CODE-MIXING")
    print("=" * 65)

    alphabet = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    total_added = 0

    core_intents = [
        "passing marks",
        "cut off marks",
        "qualifying marks",
        "syllabus pdf",
        "eligibility criteria",
        "pedagogy questions",
        "previous year question paper",
        "paper 1 paper 2 difference"
    ]

    prefix_stems = [
        "can {exam}",
        "how {exam}",
        "is {exam}",
        "which {exam}",
        "difference between {exam}",
        "after {exam}"
    ]

    wildcard_stems = [
        "_ for {exam} paper 1",
        "_ for {exam} paper 2",
        "is _ eligible for {exam}",
        "{exam} passing marks for _"
    ]

    manglish_prompts = [
        "ktet cat 1 pass mark ethra",
        "ktet cat 2 pass mark ethra",
        "ktet cat 3 pass mark ethra",
        "ktet qualifying mark ethra",
        "ktet negative mark undo",
        "ktet b.ed eligible aano",
        "d.el.ed kazhinjavarkku ktet apply cheyyamo",
        "ktet previous year question paper download malayalam",
        "ktet coaching illathe pass aavumo",
        "ktet category 2 science syllabus malayalam"
    ]

    hinglish_prompts = [
        "{exam} me kitne number chahiye",
        "{exam} 82 marks pass ya fail",
        "kya b.ed wale {exam} paper 1 de sakte hai",
        "{exam} ki taiyari kaise kare",
        "{exam} certificate ki validity kitne saal hoti hai",
        "{exam} me passing marks kitna hota hai obc ke liye",
        "{exam} pass karne ke baad kya kare"
    ]

    for exam in ALL_EXAMS:
        exam_clean = exam.replace("_", " ")
        print(f"\n[Engine 1] Processing: {exam}...")

        # 1. Core Intent Suffix Alphabet Sweep
        for intent in core_intents:
            seed = f"{exam_clean} {intent}"
            results = fetch_google_suggest(session, seed)
            for r in results:
                if insert_keyword(r, exam, "GOOGLE_SUGGEST"):
                    total_added += 1

            # Suffix letter expansion: 'seed a' .. 'seed z'
            # (Sample 8 strategic letters per intent to optimize polite crawling: a, c, f, o, p, s, w, y)
            sample_letters = ['a', 'c', 'f', 'o', 'p', 's', 'w', 'y']
            for letter in sample_letters:
                expanded_query = f"{seed} {letter}"
                results = fetch_google_suggest(session, expanded_query)
                for r in results:
                    if insert_keyword(r, exam, "GOOGLE_SUGGEST"):
                        total_added += 1
                time.sleep(0.15)

        # 2. Prefix Exploration
        for prefix in prefix_stems:
            p_seed = prefix.format(exam=exam_clean)
            results = fetch_google_suggest(session, p_seed)
            for r in results:
                if insert_keyword(r, exam, "GOOGLE_SUGGEST"):
                    total_added += 1
            time.sleep(0.15)

        # 3. Wildcard Gap Fills
        for wc in wildcard_stems:
            wc_seed = wc.format(exam=exam_clean)
            results = fetch_google_suggest(session, wc_seed)
            for r in results:
                if insert_keyword(r, exam, "GOOGLE_SUGGEST"):
                    total_added += 1
            time.sleep(0.15)

        # 4. Hinglish Ingestion (for Hindi belt exams)
        if exam in HINDI_BELT_EXAMS:
            for hp in hinglish_prompts:
                h_seed = hp.format(exam=exam_clean)
                results = fetch_google_suggest(session, h_seed)
                for r in results:
                    if insert_keyword(r, exam, "GOOGLE_SUGGEST"):
                        total_added += 1
                time.sleep(0.15)

    # 5. KTET Specific Manglish Sweep
    print("\n[Engine 1] Executing Manglish Code-Mixed Harvest for KTET...")
    for mp in manglish_prompts:
        results = fetch_google_suggest(session, mp)
        for r in results:
            if insert_keyword(r, "KTET", "GOOGLE_SUGGEST"):
                total_added += 1
        time.sleep(0.15)

    print(f"\n[Engine 1 Complete] Added {total_added} unique queries from Google.")
    return total_added

def run_engine_2_youtube(session: requests.Session) -> int:
    """Engine 2: YouTube Search & Voice Suggest."""
    print("\n" + "=" * 65)
    print("ENGINE 2: YOUTUBE SEARCH & VOICE SUGGEST HARVEST")
    print("=" * 65)

    theorists_and_topics = [
        "vygotsky questions",
        "piaget cognitive development",
        "kohlberg moral development",
        "thorndike trial and error",
        "inclusive education questions",
        "cce questions with answers",
        "cdp marathon class",
        "pedagogy tricks in hindi",
        "maths pedagogy questions",
        "evs pedagogy repeated questions",
        "previous year question paper solved"
    ]

    total_added = 0
    for exam in ALL_EXAMS:
        exam_clean = exam.replace("_", " ")
        print(f"[Engine 2] YouTube Search Harvest for: {exam}...")
        for topic in theorists_and_topics:
            yt_query = f"{exam_clean} {topic}"
            results = fetch_youtube_suggest(session, yt_query)
            for r in results:
                if insert_keyword(r, exam, "YOUTUBE_SUGGEST"):
                    total_added += 1
            time.sleep(0.2)

    print(f"\n[Engine 2 Complete] Added {total_added} unique queries from YouTube.")
    return total_added

def run_engine_3_job_recruitment(session: requests.Session) -> int:
    """Engine 3: Recruitment & Career Bridge Siphon."""
    print("\n" + "=" * 65)
    print("ENGINE 3: JOB RECRUITMENT & CAREER BRIDGE HARVEST")
    print("=" * 65)

    job_bridges = [
        # Central Jobs
        ("CTET", ["ctet kvs", "ctet nvs", "ctet dsssb", "ctet emrs"]),
        # Bihar BPSC Jobs
        ("CTET", ["ctet bpsc", "bpsc ctet", "ctet bihar teacher", "bpsc tre ctet passing marks"]),
        ("BTET", ["btet bpsc", "bihar stet paper 1", "btet teacher vacancy"]),
        # UP Jobs
        ("CTET", ["ctet super tet", "ctet up prt", "super tet ctet marks"]),
        ("UPTET", ["uptet super tet", "uptet up prt", "uptet vacancy"]),
        # Rajasthan Jobs
        ("REET", ["reet 3rd grade", "reet rpsc", "reet mains level 1", "reet level 2 vacancy"]),
        # Kerala Jobs
        ("KTET", ["ktet kpsc", "ktet lpsa", "ktet upsa", "ktet hsa", "kpsc ktet category 3"]),
        # Haryana Jobs
        ("HTET", ["htet prt vacancy", "htet tgt screening", "hssc htet"]),
        # Andhra & Telangana Jobs
        ("TS_TET", ["ts tet dsc", "ts tet trt", "ts dsc notification"]),
        ("AP_TET", ["ap tet dsc", "ap dsc notification", "ap tet trt"]),
        # Maharashtra Jobs
        ("MAHA_TET", ["maha tet pavitra portal", "maha tet shikshak bharti"])
    ]

    total_added = 0
    for exam, queries in job_bridges:
        print(f"[Engine 3] Recruitment Bridge for: {exam}...")
        for q in queries:
            results = fetch_google_suggest(session, q)
            entity_tag = q.split()[-1].upper()
            for r in results:
                if insert_keyword(r, exam, "JOB_GAZETTE", secondary_entity=entity_tag):
                    total_added += 1
            time.sleep(0.15)

    print(f"\n[Engine 3 Complete] Added {total_added} unique recruitment queries.")
    return total_added

def main():
    print("*" * 65)
    print("PHASE 1 ALL-INDIA TET KEYWORD HARVEST: COMMENCING")
    print("*" * 65)

    init_db()

    with requests.Session() as session:
        # Run Engine 1: Google Web & Alphabet
        e1_count = run_engine_1_google(session)

        # Run Engine 2: YouTube Search
        e2_count = run_engine_2_youtube(session)

        # Run Engine 3: Job Recruitment Gazette
        e3_count = run_engine_3_job_recruitment(session)

    # Export to Excel-compatible CSV
    total_exported = export_to_csv()

    # Final Statistics
    stats = get_stats()

    print("\n" + "=" * 65)
    print("PHASE 1 HARVEST COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f"Total Unique Queries Stored in SQLite: {stats['total_keywords']}")
    print(f"Exported to CSV: {total_exported} rows")
    print("\nBreakdown by Language:")
    for lang, count in stats['by_language'].items():
        print(f"  - {lang}: {count}")
    print("\nTop Exams by Query Volume:")
    for exam, count in list(stats['by_exam'].items())[:10]:
        print(f"  - {exam}: {count}")
    print("=" * 65)
    print("Phase 1 Data Foundation Ready for Phase 2 (Clustering & Routing).")

if __name__ == "__main__":
    main()

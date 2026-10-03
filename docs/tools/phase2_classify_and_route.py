"""
Phase 2 Engine: Semantic Intent Clustering, Priority Scoring & Content Format Routing.
Strictly adheres to:
- docs/Software_Specification_Document_Keyword_Pipeline.md
- docs/Master_Project_Plan_Execution_Roadmap.md
- docs/Pattern_Based_Content_Strategy.md
"""

import os
import sys
import sqlite3
import re
from typing import Tuple, Dict, Any

# Ensure tools directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from db_manager import DB_PATH, CSV_PATH, clean_slug, export_to_csv

# Regex for Language Markers
MANGLISH_PATTERN = re.compile(
    r'\b(ethra|aano|aavumo|ezhuthamo|undo|engane|kazhinjal|cheyyamo|padikkanam|kittumo|validaano|malayalam)\b',
    re.IGNORECASE
)
HINGLISH_PATTERN = re.compile(
    r'\b(kitne|kitna|chahiye|pass ya fail|kya|kaise|kab tak|wale|de sakte|kare|hoga|bhi|mein)\b',
    re.IGNORECASE
)

# Pillar 5 CDP & Theorists Keywords
PILLAR_5_TERMS = {
    "pedagogy", "vygotsky", "piaget", "kohlberg", "thorndike", "skinner",
    "pavlov", "inclusive", "cce", "child development", "theorist", "cdp",
    "psychology", "bloom", "scaffolding", "assimilation", "accommodation",
    "intelligence", "learning theory", "growth and development"
}

# Pillar 3 Recruitment & Job Bridge Keywords
PILLAR_3_TERMS = {
    "bpsc", "super tet", "kvs", "dsssb", "nvs", "emrs", "kpsc", "lpsa",
    "upsa", "hsa", "dsc", "trt", "3rd grade", "rpsc", "shikshak bharti",
    "pavitra portal", "valid in", "job", "recruitment", "vacancy", "after ctet",
    "after ktet", "after uptet", "validity", "certificate valid", "all states"
}

# Pillar 1 Cutoff & Marks Keywords
PILLAR_1_TERMS = {
    "pass", "mark", "cut off", "cutoff", "qualifying", "82", "90", "fail",
    "ethra", "kitne number", "score", "percentage", "general category",
    "obc", "sc st", "sc/st", "reservation"
}

# Pillar 2 Legal Eligibility & Qualification Keywords
PILLAR_2_TERMS = {
    "b.ed", "b ed", "bed", "d.el.ed", "deled", "dled", "btc", "eligib",
    "qualification", "criteria", "age limit", "fees", "last date", "form",
    "apply", "appearing", "supreme court", "verdict", "ezhuthamo", "cheyyamo",
    "graduation", "percentage required", "can apply", "eligible"
}

# Pillar 4 Syllabus, Paper Overlap & Question Paper Keywords
PILLAR_4_TERMS = {
    "syllabus", "difference", "paper 1", "paper 2", "cat 1", "cat 2",
    "category 1", "category 2", "scert", "ncert", "pattern", "subject",
    "books", "question paper", "previous year", "sample paper", "answer key",
    "solved paper", "pyq", "download", "pdf"
}

def migrate_schema(db_path: str = DB_PATH):
    """Adds hit_count, best_rank, and priority_score columns if not present."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("PRAGMA table_info(tet_keyword_master);")
    cols = {r[1] for r in c.fetchall()}

    if "hit_count" not in cols:
        print("[MIGRATE] Adding hit_count column...")
        c.execute("ALTER TABLE tet_keyword_master ADD COLUMN hit_count INTEGER NOT NULL DEFAULT 1;")
    if "best_rank" not in cols:
        print("[MIGRATE] Adding best_rank column...")
        c.execute("ALTER TABLE tet_keyword_master ADD COLUMN best_rank INTEGER NOT NULL DEFAULT 10;")
    if "priority_score" not in cols:
        print("[MIGRATE] Adding priority_score column...")
        c.execute("ALTER TABLE tet_keyword_master ADD COLUMN priority_score INTEGER NOT NULL DEFAULT 1;")

    # Add indices for priority querying
    c.execute("CREATE INDEX IF NOT EXISTS idx_priority_score ON tet_keyword_master(priority_score);")
    conn.commit()
    conn.close()

def classify_query(raw_query: str, target_exam: str) -> Tuple[str, str, str, int, str]:
    """
    Classifies a raw query into:
    (language_mix, intent_cluster, content_format, priority_score, video_hook)
    """
    q_lower = raw_query.lower()

    # 1. Language Classification
    if MANGLISH_PATTERN.search(q_lower):
        lang = "MANGLISH"
    elif HINGLISH_PATTERN.search(q_lower):
        lang = "HINGLISH"
    else:
        lang = "ENGLISH"

    # 2. Semantic Pillar Classification (Order matters: CDP -> Recruitment -> Cutoffs -> Eligibility -> Syllabus)
    if any(t in q_lower for t in PILLAR_5_TERMS):
        pillar = "PILLAR_5_CDP_PEDAGOGY"
        fmt = "REMOTION_SHORT"
        hook = f"90% of {target_exam} aspirants miss this pedagogy concept! Let's solve it."
    elif any(t in q_lower for t in PILLAR_3_TERMS):
        pillar = "PILLAR_3_RECRUITMENT_BRIDGE"
        fmt = "PILLAR_HUB"
        hook = f"Will your {target_exam} score qualify you for teaching recruitment? Official rule."
    elif any(t in q_lower for t in PILLAR_1_TERMS):
        pillar = "PILLAR_1_CUTOFF"
        fmt = "STATIC_HTML"
        hook = f"82 or 90? The official {target_exam} qualifying passing marks explained."
    elif any(t in q_lower for t in PILLAR_2_TERMS):
        pillar = "PILLAR_2_ELIGIBILITY"
        fmt = "STATIC_HTML"
        hook = f"Are you legally eligible for {target_exam}? Supreme Court and NCTE guidelines."
    elif any(t in q_lower for t in PILLAR_4_TERMS):
        pillar = "PILLAR_4_SYLLABUS_OVERLAP"
        # If looking for papers or downloads, route to printable PDF cheat sheet; else static HTML
        if any(w in q_lower for w in ["pdf", "paper", "download", "previous year", "answer key"]):
            fmt = "PDF_CHEAT_SHEET"
        else:
            fmt = "STATIC_HTML"
        hook = f"Master the complete {target_exam} syllabus topic breakdown offline."
    else:
        # Fallback to Syllabus & Curriculum
        pillar = "PILLAR_4_SYLLABUS_OVERLAP"
        fmt = "STATIC_HTML"
        hook = f"Everything you need to know about {target_exam} preparation."

    # 3. Calculate Deterministic Priority Score
    # Base: 20 points
    score = 20

    # Short, broad head queries get higher base search volume bonus
    if len(raw_query) < 25:
        score += 25
    elif len(raw_query) < 35:
        score += 15

    # High-converting pillars get bonus
    if pillar == "PILLAR_1_CUTOFF":
        score += 25
    elif pillar == "PILLAR_3_RECRUITMENT_BRIDGE":
        score += 20
    elif pillar == "PILLAR_5_CDP_PEDAGOGY":
        score += 15

    # Core national exams get priority weight
    if target_exam in {"CTET", "UPTET", "KTET", "REET"}:
        score += 15

    return lang, pillar, fmt, score, hook

def run_phase_2(db_path: str = DB_PATH):
    print("=" * 65)
    print("PHASE 2: CLASSIFICATION, PRIORITY SCORING & CONTENT ROUTING")
    print("=" * 65)

    migrate_schema(db_path)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT keyword_id, raw_query, target_exam, clean_slug FROM tet_keyword_master;")
    records = c.fetchall()
    total = len(records)
    print(f"Ingesting & Classifying {total} records from database...")

    updates = []
    for kwd_id, raw_query, target_exam, slug in records:
        lang, pillar, fmt, priority, hook = classify_query(raw_query, target_exam)
        url = f"/{target_exam.lower()}/{slug}/"

        updates.append((
            lang, pillar, fmt, priority, url, hook, 'FORMAT_ASSIGNED', kwd_id
        ))

    c.executemany("""
    UPDATE tet_keyword_master
    SET language_mix = ?,
        intent_cluster = ?,
        content_format = ?,
        priority_score = ?,
        target_url = ?,
        video_hook = ?,
        lifecycle_status = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE keyword_id = ?;
    """, updates)

    conn.commit()

    # Query statistics
    c.execute("SELECT intent_cluster, COUNT(*) FROM tet_keyword_master GROUP BY intent_cluster ORDER BY COUNT(*) DESC;")
    by_pillar = dict(c.fetchall())

    c.execute("SELECT content_format, COUNT(*) FROM tet_keyword_master GROUP BY content_format ORDER BY COUNT(*) DESC;")
    by_format = dict(c.fetchall())

    c.execute("SELECT language_mix, COUNT(*) FROM tet_keyword_master GROUP BY language_mix;")
    by_lang = dict(c.fetchall())

    c.execute("SELECT COUNT(*) FROM tet_keyword_master WHERE lifecycle_status = 'FORMAT_ASSIGNED';")
    assigned_count = c.fetchone()[0]

    # Fetch Top 10 High Priority Keywords
    c.execute("""
    SELECT raw_query, target_exam, intent_cluster, priority_score, content_format
    FROM tet_keyword_master
    ORDER BY priority_score DESC, target_exam ASC
    LIMIT 10;
    """)
    top_10 = c.fetchall()

    conn.close()

    # Re-export CSV mirror
    exported_csv = export_to_csv()

    print("\n" + "=" * 65)
    print("PHASE 2 CLASSIFICATION COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f"Total Records Formatted & Assigned: {assigned_count} of {total} (100%)")
    print(f"Exported to CSV: {exported_csv} rows sorted by priority in {CSV_PATH}")

    print("\nBreakdown by Pattern Pillar:")
    for pillar, cnt in by_pillar.items():
        print(f"  - {pillar}: {cnt} keywords ({cnt/total*100:.1f}%)")

    print("\nBreakdown by Media Content Format:")
    for fmt, cnt in by_format.items():
        print(f"  - {fmt}: {cnt} assets ({cnt/total*100:.1f}%)")

    print("\nBreakdown by Language:")
    for lang, cnt in by_lang.items():
        print(f"  - {lang}: {cnt}")

    print("\n" + "=" * 65)
    print("TOP 10 HIGHEST-PRIORITY TARGET KEYWORDS (IMMEDIATE PRODUCTION FOCUS):")
    print("=" * 65)
    for r in top_10:
        print(f" [Score: {r[3]}] [{r[1]}] '{r[0]}' -> {r[2]} ({r[4]})")
    print("=" * 65)
    print("Phase 2 Definition of Done (DoD) Achieved. Staged for Phase 3 Manufacturing.")

if __name__ == "__main__":
    run_phase_2()

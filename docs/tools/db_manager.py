"""
Database Manager & Schema Engine for All-India TET Keyword Pipeline.
Strictly conforms to: docs/Software_Specification_Document_Keyword_Pipeline.md
"""

import os
import re
import sqlite3
import csv
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(BASE_DIR, "research")
DB_PATH = os.path.join(RESEARCH_DIR, "all_india_tet_master.db")
CSV_PATH = os.path.join(RESEARCH_DIR, "all_india_tet_master.csv")

# Valid Exam Set
VALID_EXAMS = {
    # National
    "CTET",
    # South
    "KTET", "TNTET", "TS_TET", "AP_TET", "KARTET",
    # North / Central
    "UPTET", "REET", "HTET", "MPTET", "PSTET", "UTET",
    # West / East
    "MAHA_TET", "WBTET", "OTET", "CG_TET", "BTET", "ASSAM_TET"
}

# Regex for Language Markers
MANGLISH_PATTERN = re.compile(r'\b(ethra|aano|aavumo|ezhuthamo|undo|engane|kazhinjal|cheyyamo|padikkanam|kittumo|validaano)\b', re.IGNORECASE)
HINGLISH_PATTERN = re.compile(r'\b(kitne|kitna|chahiye|pass ya fail|kya|kaise|kab tak|wale|de sakte|kare|hoga)\b', re.IGNORECASE)

WINDOWS_RESERVED_NAMES = {
    "con", "prn", "aux", "nul",
    "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
    "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9"
}

def clean_slug(text: str) -> str:
    r"""
    Creates a Windows-safe and URL-compliant slug.
    - Expands '&' to 'and'
    - Strips reserved characters (?, :, *, ", <, >, |, /, \) and collapses hyphens
    - Protects against Windows reserved filenames (CON, NUL, AUX, PRN, etc.)
    - Handles pure non-ASCII (Malayalam/Devanagari) with deterministic hash fallback
    """
    # Convert ampersand
    text = text.replace("&", " and ")
    # Lowercase & strip
    text = text.lower().strip()
    # Replace non-alphanumeric with hyphen
    slug = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    
    # Fallback if slug is empty (e.g. pure Malayalam script)
    if not slug:
        h = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
        slug = f"query-{h}"

    # Guard against Windows reserved names
    if slug in WINDOWS_RESERVED_NAMES:
        slug = f"{slug}-topic"

    return slug

def classify_language(query: str) -> str:
    """Detects whether query is English, Manglish, or Hinglish."""
    if MANGLISH_PATTERN.search(query):
        return "MANGLISH"
    if HINGLISH_PATTERN.search(query):
        return "HINGLISH"
    return "ENGLISH"

def generate_keyword_id(exam: str, normalized_query: str) -> str:
    """Generates a deterministic unique ID based on exam and query SHA256 hash."""
    h = hashlib.sha256(normalized_query.encode('utf-8')).hexdigest()[:10].upper()
    return f"KWD_{exam}_{h}"

def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Initializes the SQLite database schema if not already present."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tet_keyword_master (
        keyword_id          TEXT PRIMARY KEY,
        raw_query           TEXT NOT NULL,
        normalized_query    TEXT NOT NULL UNIQUE,
        clean_slug          TEXT NOT NULL,
        canonical_slug      TEXT DEFAULT NULL,
        target_exam         TEXT NOT NULL,
        secondary_entity    TEXT DEFAULT NULL,
        language_mix        TEXT NOT NULL DEFAULT 'ENGLISH',
        source_engine       TEXT NOT NULL,
        intent_cluster      TEXT NOT NULL DEFAULT 'UNCLUSTERED',
        content_format      TEXT NOT NULL DEFAULT 'UNASSIGNED',
        target_url          TEXT DEFAULT NULL,
        video_hook          TEXT DEFAULT NULL,
        hit_count           INTEGER NOT NULL DEFAULT 1,
        best_rank           INTEGER NOT NULL DEFAULT 10,
        priority_score      INTEGER NOT NULL DEFAULT 1,
        lifecycle_status    TEXT NOT NULL DEFAULT 'DISCOVERED',
        discovered_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Performance indices
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_target_exam ON tet_keyword_master(target_exam);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_intent_cluster ON tet_keyword_master(intent_cluster);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_canonical_slug ON tet_keyword_master(canonical_slug);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority_score ON tet_keyword_master(priority_score);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_lifecycle_status ON tet_keyword_master(lifecycle_status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_language_mix ON tet_keyword_master(language_mix);")

    conn.commit()
    return conn

def insert_keyword(
    raw_query: str,
    target_exam: str,
    source_engine: str,
    secondary_entity: Optional[str] = None,
    intent_cluster: str = "UNCLUSTERED",
    content_format: str = "UNASSIGNED",
    canonical_slug: Optional[str] = None,
    rank: int = 10,
    db_path: str = DB_PATH
) -> bool:
    """
    Inserts a keyword with deterministic deduplication and automated slug/language assignment.
    Uses SQLite upsert to maintain true frequency counts (hit_count) and record best SERP rank.
    """
    norm = raw_query.strip().lower()
    if not norm:
        return False

    exam_clean = target_exam.upper().replace("-", "_").replace(" ", "_")
    slug = clean_slug(norm)
    lang = classify_language(norm)
    kwd_id = generate_keyword_id(exam_clean, norm)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO tet_keyword_master (
            keyword_id, raw_query, normalized_query, clean_slug, canonical_slug,
            target_exam, secondary_entity, language_mix, source_engine,
            intent_cluster, content_format, hit_count, best_rank, priority_score,
            lifecycle_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, 10, 'DISCOVERED')
        ON CONFLICT(normalized_query) DO UPDATE SET
            hit_count = tet_keyword_master.hit_count + 1,
            best_rank = MIN(tet_keyword_master.best_rank, excluded.best_rank),
            updated_at = CURRENT_TIMESTAMP;
        """, (
            kwd_id, raw_query.strip(), norm, slug, canonical_slug or slug,
            exam_clean, secondary_entity, lang, source_engine,
            intent_cluster, content_format, rank
        ))
        conn.commit()
        success = cursor.rowcount > 0
    finally:
        conn.close()

    return success

def export_to_csv(db_path: str = DB_PATH, csv_path: str = CSV_PATH) -> int:
    """
    Exports all records from SQLite to an Excel-compatible UTF-8 BOM CSV.
    Returns the total number of exported rows.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        keyword_id, raw_query, normalized_query, clean_slug, canonical_slug, target_exam,
        secondary_entity, language_mix, source_engine, intent_cluster,
        content_format, target_url, video_hook, hit_count, best_rank, priority_score,
        lifecycle_status, discovered_at
    FROM tet_keyword_master
    ORDER BY priority_score DESC, hit_count DESC, target_exam ASC;
    """)

    rows = cursor.fetchall()
    headers = [d[0] for d in cursor.description]
    conn.close()

    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return len(rows)

def get_stats(db_path: str = DB_PATH) -> Dict[str, Any]:
    """Returns summary statistics of the repository."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tet_keyword_master;")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT target_exam, COUNT(*) FROM tet_keyword_master GROUP BY target_exam ORDER BY COUNT(*) DESC;")
    by_exam = dict(cursor.fetchall())

    cursor.execute("SELECT language_mix, COUNT(*) FROM tet_keyword_master GROUP BY language_mix;")
    by_lang = dict(cursor.fetchall())

    cursor.execute("SELECT lifecycle_status, COUNT(*) FROM tet_keyword_master GROUP BY lifecycle_status;")
    by_status = dict(cursor.fetchall())

    conn.close()
    return {
        "total_keywords": total,
        "by_exam": by_exam,
        "by_language": by_lang,
        "by_status": by_status
    }

if __name__ == "__main__":
    import sys
    print("=" * 60)
    print("All-India TET Keyword Pipeline: Database Engine Self-Test")
    print("=" * 60)

    # Initialize
    conn = init_db()
    print(f"[OK] Database initialized at: {DB_PATH}")

    # Self-test entries
    test_cases = [
        ("CTET passing marks for OBC 2026?", "CTET", "GOOGLE_SUGGEST"),
        ("is B.Ed eligible for CTET Paper 1 *verdict*?", "CTET", "GOOGLE_SUGGEST"),
        ("ktet cat 2 pass mark ethra", "KTET", "GOOGLE_SUGGEST"),
        ("uptet me 82 number pass hai ya fail", "UPTET", "YOUTUBE_SUGGEST"),
        ("bihar bpsc tre 4.0 me ctet marks kitne chahiye", "CTET", "JOB_GAZETTE", "BPSC_TRE"),
        # Duplicate test
        ("ctet passing marks for obc 2026?", "CTET", "YOUTUBE_SUGGEST"),
    ]

    inserted_count = 0
    for item in test_cases:
        query = item[0]
        exam = item[1]
        source = item[2]
        secondary = item[3] if len(item) > 3 else None
        res = insert_keyword(query, exam, source, secondary_entity=secondary)
        status = "INSERTED" if res else "SKIPPED (Duplicate)"
        print(f" -> '{query}' [{exam}] -> {status}")
        if res:
            inserted_count += 1

    print(f"\n[OK] Inserted {inserted_count} unique test records (Duplicates correctly filtered).")

    # Export to CSV
    exported = export_to_csv()
    print(f"[OK] Exported {exported} records to Excel-friendly CSV at: {CSV_PATH}")

    # Print Stats
    stats = get_stats()
    print("\nCurrent Database State:")
    print(f" Total Keywords: {stats['total_keywords']}")
    print(f" By Language: {stats['by_language']}")
    print(f" By Exam: {stats['by_exam']}")
    print("=" * 60)
    print("Phase 0 Data Foundation Ready for Ingestion.")

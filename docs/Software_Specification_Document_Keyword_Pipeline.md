# Software Specification Document (SSD)
## System: All-India TET Keyword Intelligence & Content Generation Pipeline
**Document Version:** 1.0  
**Status:** Approved Architecture Draft  
**Target Environment:** Local Workstation (Windows 10/11, Python 3.10+, SQLite 3)  
**Parent System:** EasyCTET / EasyKTET Digital Strategy  

---

## 1. System Purpose & Objectives

### 1.1 Purpose
This document establishes the formal software architecture, data contracts, and interface specifications for the **All-India TET Keyword Intelligence & Content Generation Pipeline**. 

The system acts as the central data nervous system for EasyCTET. It discovers, normalizes, deduplicates, classifies, and routes real-world search queries across 18 Central and State Teacher Eligibility Tests into automated production pipelines for static web pages, short-form videos, and community cheat sheets.

### 1.2 Core Architectural Principles
1. **Zero Data Swamp:** Every query entering the system must conform to a strict relational schema before storage.
2. **Deterministic Deduplication:** Ingestion engines must automatically discard identical queries regardless of source.
3. **OS & Filesystem Safety:** All URL slugs and filenames must be strictly sanitized against Windows filesystem reserved characters (`?`, `:`, `*`, `"`, `<`, `>`, `|`, `/`, `\`).
4. **Zero-Cloud Dependency:** The database runs on a local, zero-maintenance SQLite engine requiring no external servers, cloud subscriptions, or database daemon configurations.
5. **Loose Coupling:** Ingestion scrapers, clustering logic, and content generators interact strictly via the centralized SQLite database and standard CSV/JSON contracts.

---

## 2. System Architecture Overview

The system is organized into four discrete operational tiers:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 TIER 1: INGESTION                                      │
├────────────────────┬────────────────────┬────────────────────┬─────────────────────────┤
│ Google Suggest API │ YouTube Suggest API│ Competitor Sitemaps│ Recruitment Gazette Map │
└─────────┬──────────┴─────────┬──────────┴─────────┬──────────┴────────────┬────────────┘
          │                    │                    │                       │
          ▼                    ▼                    ▼                       ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TIER 2: NORMALIZATION & INGESTION CONTRACT                      │
│   - Lowercase & strip whitespace                                                       │
│   - Regex slugification (Windows & URL compliant)                                      │
│   - Language classification (English, Hinglish, Manglish)                              │
│   - Unique constraint enforcement via SQLite INSERT OR IGNORE                          │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         TIER 3: CENTRAL STORAGE & CLUSTERING                           │
│   Database: docs/research/all_india_tet_master.db (SQLite)                             │
│   - Intent Clustering (Cutoff, Eligibility, Pedagogy, PYQ, Recruitment)                │
│   - Media Format Mapping (Static HTML, Remotion Video, PDF Cheat Sheet)                │
│   - State Lifecycle: DISCOVERED -> CLUSTERED -> ASSIGNED -> GENERATED -> PUBLISHED     │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              TIER 4: OUTPUT INTERFACES                                 │
├─────────────────────────┬───────────────────────────┬──────────────────────────────────┤
│ Static HTML Generator   │ Remotion Video Automation │ PDF Cheat Sheet Compiler         │
│ (Target: EasyCTET.com)  │ (Target: @easyctetofficial)│ (Target: WhatsApp/Telegram)      │
└─────────────────────────┴───────────────────────────┴──────────────────────────────────┘
```

---

## 3. Data Dictionary & Storage Contract

### 3.1 Database Engine
* **Engine:** SQLite 3.
* **Storage Location:** `docs/research/all_india_tet_master.db`.
* **Export Mirror:** `docs/research/all_india_tet_master.csv` (Encoded with `utf-8-sig` for Microsoft Excel compatibility on Windows).

### 3.2 Master Relational Table: `tet_keyword_master`

| Column Name | Data Type | Nullable | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `keyword_id` | `TEXT` | No | `PRIMARY KEY` | Unique hash/ID (e.g., `KWD_CTET_00842`). |
| `raw_query` | `TEXT` | No | None | Original unedited search string as extracted. |
| `normalized_query` | `TEXT` | No | `UNIQUE` | Lowercase, whitespace-trimmed version for deduplication. |
| `clean_slug` | `TEXT` | No | None | Windows/URL-safe slug for HTML filenames and web routes. |
| `target_exam` | `TEXT` | No | `CHECK (target_exam IN (...))` | Primary exam entity (e.g., `CTET`, `KTET`, `UPTET`, etc.). |
| `secondary_entity` | `TEXT` | Yes | `DEFAULT NULL` | Downstream recruitment exam (e.g., `BPSC_TRE`, `SUPER_TET`). |
| `language_mix` | `TEXT` | No | `DEFAULT 'ENGLISH'` | Classified language (`ENGLISH`, `MANGLISH`, `HINGLISH`). |
| `source_engine` | `TEXT` | No | None | Source (`GOOGLE_SUGGEST`, `YOUTUBE_SUGGEST`, `SITEMAP`, `PAA`). |
| `intent_cluster` | `TEXT` | No | `DEFAULT 'UNCLUSTERED'` | Target intent bucket (`CUTOFF`, `ELIGIBILITY`, `CDP_PEDAGOGY`, `PYQ_SYLLABUS`, `RECRUITMENT_BRIDGE`). |
| `content_format` | `TEXT` | No | `DEFAULT 'UNASSIGNED'` | Recommended format (`STATIC_HTML`, `REMOTION_SHORT`, `PDF_CHEAT_SHEET`, `PILLAR_HUB`). |
| `target_url` | `TEXT` | Yes | `DEFAULT NULL` | Relative URL on `EasyCTET.com` (e.g., `/ctet/passing-marks-for-obc/`). |
| `video_hook` | `TEXT` | Yes | `DEFAULT NULL` | 3-second visual/voice hook for Remotion Shorts. |
| `lifecycle_status` | `TEXT` | No | `DEFAULT 'DISCOVERED'` | Current stage (`DISCOVERED`, `PLANNED`, `GENERATED`, `PUBLISHED`). |
| `discovered_at` | `DATETIME` | No | `DEFAULT CURRENT_TIMESTAMP`| Timestamp of ingestion. |
| `updated_at` | `DATETIME` | No | `DEFAULT CURRENT_TIMESTAMP`| Timestamp of last state modification. |

### 3.3 Target Exam Enumeration Set
The `target_exam` field is strictly validated against the official 18 Indian teacher eligibility examinations:
* **National:** `CTET`
* **South:** `KTET`, `TNTET`, `TS_TET`, `AP_TET`, `KARTET`
* **North / Central:** `UPTET`, `REET`, `HTET`, `MPTET`, `PSTET`, `UTET`
* **West / East:** `MAHA_TET`, `WBTET`, `OTET`, `CG_TET`, `BTET`, `ASSAM_TET`

---

## 4. Processing & Business Logic Rules

### 4.1 Slug Sanitization Rule (Windows & Web Safe)
All `clean_slug` values must be generated via the following strict deterministic transformation:
1. Convert string to lowercase.
2. Replace all ampersands (`&`) with the word `and`.
3. Replace all non-alphanumeric characters (including spaces, slashes, punctuation, dots, quotes, question marks) with a single hyphen (`-`).
4. Collapse multiple consecutive hyphens into a single hyphen (`--` $\rightarrow$ `-`).
5. Strip leading and trailing hyphens.

**Regex Implementation Standard:**
```python
slug = re.sub(r'[^a-z0-9]+', '-', text.lower().strip())
clean_slug = slug.strip('-')
```

### 4.2 Ingestion Deduplication Rule
The database layer enforces idempotency. When any scraper inserts a query:
```sql
INSERT OR IGNORE INTO tet_keyword_master (
    keyword_id, raw_query, normalized_query, clean_slug, target_exam, source_engine, language_mix
) VALUES (?, ?, ?, ?, ?, ?, ?);
```
If `normalized_query` already exists, the record is discarded without error, ensuring repeated crawler runs never inflate the dataset.

### 4.3 Language Classification Logic
During ingestion, the system automatically assigns the `language_mix` attribute based on regular expression lexical markers:
* **`MANGLISH`:** Matches patterns containing `ethra`, `aano`, `aavumo`, `ezhuthamo`, `undo`, `engane`, `kazhinjal`, `cheyyamo`, `padikkanam`.
* **`HINGLISH`:** Matches patterns containing `kitne`, `kitna`, `chahiye`, `pass ya fail`, `kya`, `kaise`, `kab tak`, `wale`, `de sakte`.
* **`ENGLISH`:** Default classification for queries without vernacular markers.

---

## 5. Subsystem Module Specifications

### Module 5.1: Ingestion Scrapers (`tools/ingest_*.py`)
1. **`ingest_google_alphabet.py`:** Executes recursive alphabet expansion (seeds $\times$ `[a-z]` $\times$ `[a-z]`) with a 0.25s rate-limit pause and `requests.Session()` connection pooling.
2. **`ingest_youtube_suggest.py`:** Queries YouTube's video autocomplete engine (`client=youtube&ds=yt`) to extract voice and pedagogy-heavy queries.
3. **`ingest_job_gazettes.py`:** Cross-multiplies TET exams with recruitment examinations (`BPSC TRE`, `Super TET`, `KPSC LPSA/UPSA`, `KVS`, `DSSSB`).
4. **`ingest_competitor_sitemaps.py`:** Parses public XML sitemaps of educational incumbents (Testbook, Adda247) to extract historical URL slugs.

### Module 5.2: Content Routing Engine (`tools/classify_and_route.py`)
Applies semantic intent rules to update `intent_cluster` and `content_format`:
* **`STATIC_HTML`:** Assigned to queries containing `passing marks`, `cut off`, `qualifying marks`, `syllabus`, `eligibility criteria`, `difference between`.
* **`REMOTION_SHORT`:** Assigned to queries containing `questions with answers`, `pedagogy questions`, `important questions`, `repeated questions`, `vygotsky`, `piaget`, `kohlberg`.
* **`PDF_CHEAT_SHEET`:** Assigned to queries containing `pdf download`, `previous year question paper`, `answer key pdf`, `notes pdf`.

---

## 6. Output & Export Interfaces

### 6.1 Programmatic Static HTML Generator Interface
The static generator consumes records where `content_format = 'STATIC_HTML'` and outputs static HTML files adhering to the design specifications established in `compare-all-tets.html`:
* Pure HTML/CSS (under 35 KB).
* Embedded JSON-LD `FAQPage` schema.
* Dedicated Call-to-Action (CTA) card linking to the offline EasyCTET/EasyKTET Google Play Store listing.

### 6.2 Remotion Video Pipeline Interface
The video automation pipeline queries records where `content_format = 'REMOTION_SHORT'` and generates a structured JSON payload:
```json
{
  "keyword_id": "KWD_CTET_00412",
  "exam": "CTET",
  "hook_title": "99% Fail This Vygotsky Pedagogy Question",
  "question_text": "According to Lev Vygotsky, the zone of proximal development refers to:",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "B",
  "tts_voice": "en-IN-NeerjaNeural",
  "cta_text": "Practice 2,000+ more offline on EasyCTET"
}
```

### 6.3 Spreadsheet Export Interface
A command-line utility (`tools/export_to_csv.py`) exports all database records into `docs/research/all_india_tet_master.csv` formatted with `utf-8-sig` encoding, ensuring seamless opening in Microsoft Excel without character corruption.

---

## 7. Operational Safety, Scalability & Lifecycle

1. **HTTP Rate-Limiting Protocol:** All network requests to Google and YouTube suggest endpoints must implement an exponential backoff retry loop on `HTTP 429` (wait 3s, 6s, 12s) to prevent IP blocking.
2. **Database Version Control:** The SQLite database file (`all_india_tet_master.db`) and its CSV mirror are stored locally in `docs/research/` within the repository.
3. **Execution State Transition:**
   $$\text{DISCOVERED} \longrightarrow \text{CLUSTERED} \longrightarrow \text{FORMAT\_ASSIGNED} \longrightarrow \text{PUBLISHED}$$
   No content may be generated for a record until its state reaches `FORMAT_ASSIGNED`.

---

## 8. Document Sign-off

This Software Specification Document serves as the authoritative technical baseline. All subsequent scripts, scrapers, database initialization routines, and content generators must strictly comply with the contracts defined herein.

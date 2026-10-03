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
| `keyword_id` | `TEXT` | No | `PRIMARY KEY` | Deterministic SHA256 hash (e.g., `KWD_CTET_A1B2C3D4E5`). |
| `raw_query` | `TEXT` | No | None | Original unedited search string as extracted. |
| `normalized_query` | `TEXT` | No | `UNIQUE` | Lowercase, whitespace-trimmed version for deduplication. |
| `clean_slug` | `TEXT` | No | None | Windows/URL-safe slug for specific query matching. |
| `canonical_slug` | `TEXT` | Yes | `DEFAULT NULL` | Many-to-One Intent Hub slug (prevents Scaled Content Abuse). |
| `target_exam` | `TEXT` | No | `CHECK (target_exam IN (...))` | Primary exam entity (e.g., `CTET`, `KTET`, `UPTET`, etc.). |
| `secondary_entity` | `TEXT` | Yes | `DEFAULT NULL` | Downstream recruitment exam (e.g., `BPSC_TRE`, `SUPER_TET`). |
| `language_mix` | `TEXT` | No | `DEFAULT 'ENGLISH'` | Classified language (`ENGLISH`, `MANGLISH`, `HINGLISH`). |
| `source_engine` | `TEXT` | No | None | Source (`GOOGLE_SUGGEST`, `YOUTUBE_SUGGEST`, `JOB_GAZETTE`, `SITEMAP`). |
| `intent_cluster` | `TEXT` | No | `DEFAULT 'UNCLUSTERED'` | Target pattern pillar (`PILLAR_1_CUTOFF`, `PILLAR_2_ELIGIBILITY`, `PILLAR_3_RECRUITMENT_BRIDGE`, `PILLAR_4_SYLLABUS_OVERLAP`, `PILLAR_5_CDP_PEDAGOGY`). |
| `content_format` | `TEXT` | No | `DEFAULT 'UNASSIGNED'` | Recommended format (`STATIC_HTML`, `REMOTION_SHORT`, `PDF_CHEAT_SHEET`, `PILLAR_HUB`). |
| `hit_count` | `INTEGER` | No | `DEFAULT 1` | Cumulative multi-seed search frequency counter via upsert. |
| `best_rank` | `INTEGER` | No | `DEFAULT 10` | Highest autocomplete suggestion position (1 to 10). |
| `priority_score` | `INTEGER` | No | `DEFAULT 1` | Calculated priority metric: `(hit_count * 10) + (11 - best_rank)`. |
| `target_url` | `TEXT` | Yes | `DEFAULT NULL` | Relative canonical URL on `EasyCTET.com` (e.g., `/ctet/ctet-passing-marks-for-obc/`). |
| `video_hook` | `TEXT` | Yes | `DEFAULT NULL` | Calm pedagogical voice hook for Remotion Shorts. |
| `lifecycle_status` | `TEXT` | No | `DEFAULT 'DISCOVERED'` | Stage: `DISCOVERED`, `CLUSTERED`, `FORMAT_ASSIGNED`, `GENERATED`, `REVIEWED`, `PUBLISHED`. |
| `discovered_at` | `DATETIME` | No | `DEFAULT CURRENT_TIMESTAMP`| Timestamp of ingestion. |
| `updated_at` | `DATETIME` | No | `DEFAULT CURRENT_TIMESTAMP`| Timestamp of last state modification. |

### 3.3 Target Exam Enumeration Set
The `target_exam` field is validated against 18 central and state teacher eligibility examinations:
* **National:** `CTET`
* **South:** `KTET`, `TNTET`, `TS_TET`, `AP_TET`, `KARTET`
* **North / Central:** `UPTET` *(Note: Inactive since 2021; monitored for UP Education Commission)*, `REET`, `HTET`, `MPTET`, `PSTET`, `UTET`
* **West / East:** `MAHA_TET`, `WBTET`, `OTET`, `CG_TET`, `BTET` *(Note: Subsumed by Bihar STET / BPSC TRE)*, `ASSAM_TET`

---

## 4. Processing & Business Logic Rules

### 4.1 Slug Sanitization Rule (Windows & Web Safe)
All `clean_slug` and `canonical_slug` values must conform to strict filesystem safety:
1. Convert string to lowercase and strip whitespace.
2. Expand ampersands (`&` $\rightarrow$ ` and `).
3. Replace all non-alphanumeric characters with hyphens.
4. Collapse consecutive hyphens and strip leading/trailing hyphens.
5. **Non-ASCII Fallback:** If query is in non-Latin script (Malayalam/Devanagari) producing an empty string, generate a deterministic hash slug (`query-{md5[:8]}`).
6. **Windows Reserved Word Guard:** Protect against reserved device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`-`COM9`, `LPT1`-`LPT9`) by appending `-topic`.

### 4.2 Ingestion Upsert Rule (Deduplication + Frequency Counter)
To prevent search volume loss and primary key collisions, scrapers execute an atomic SQLite **upsert**:
```sql
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
```
This guarantees that repeated discovery across multiple seeds increments `hit_count`, records the best SERP rank, and never creates duplicate records or silent data loss.

### 4.3 Intent Clustering & Anti-Scaled Content Abuse Architecture
To avoid Google's March 2024 "Scaled Content Abuse" penalties for mass-generated thin pages:
* **Many-to-One Mapping:** Distinct long-tail keyword variations (e.g., *"ctet passing marks obc"*, *"ctet cutoff 2026 obc"*, *"ctet qualifying marks for obc category"*) are grouped under a single parent `canonical_slug` (`ctet-passing-marks-for-obc`).
* **Authoritative Hubs:** The static generator compiles comprehensive, high-utility pillar pages that answer the parent intent completely with full comparison tables and FAQs, rather than generating hundreds of fragmented micro-pages.

### 4.4 Language Classification Logic
During ingestion, the system automatically assigns `language_mix` based on lexical markers:
* **`MANGLISH`:** Matches patterns containing `ethra`, `aano`, `aavumo`, `ezhuthamo`, `undo`, `engane`, `kazhinjal`, `cheyyamo`, `padikkanam`, `malayalam`.
* **`HINGLISH`:** Matches patterns containing `kitne`, `kitna`, `chahiye`, `pass ya fail`, `kya`, `kaise`, `kab tak`, `wale`, `de sakte`, `kare`, `hoga`.
* **`ENGLISH`:** Default classification for standard English queries.

---

## 5. Subsystem Module Specifications

### Module 5.1: Ingestion Scrapers (`tools/ingest_*.py`)
1. **`ingest_google_alphabet.py`:** Executes recursive alphabet expansion (seeds $\times$ `[a-z]` $\times$ `[a-z]`) with a 0.25s rate-limit pause and `requests.Session()` connection pooling.
2. **`ingest_youtube_suggest.py`:** Queries YouTube's video autocomplete engine (`client=youtube&ds=yt`) to extract voice and pedagogy-heavy queries.
3. **`ingest_job_gazettes.py`:** Cross-multiplies TET exams with recruitment examinations (`BPSC TRE`, `Super TET`, `KPSC LPSA/UPSA`, `KVS`, `DSSSB`).
4. **`ingest_competitor_sitemaps.py`:** Parses public XML sitemaps of educational incumbents (Testbook, Adda247) to extract historical URL slugs.

### Module 5.2: Content Routing Engine (`tools/classify_and_route.py`)
Applies deterministic semantic rules to assign `intent_cluster` to one of the 5 Pillars and map `content_format`:
* **`PILLAR_1_CUTOFF` (Format: `STATIC_HTML`):**
  * Matches queries containing `passing marks`, `cut off`, `qualifying marks`, `82 marks`, `pass ya fail`, `ethra`.
  * Outputs: Clean category breakdown tables with FAQ schema.
* **`PILLAR_2_ELIGIBILITY` (Format: `STATIC_HTML`):**
  * Matches queries containing `b.ed`, `d.el.ed`, `eligibility criteria`, `supreme court`, `appearing student`, `ezhuthamo`.
  * Outputs: Post-Supreme Court legal decision tree with verified NCTE citations.
* **`PILLAR_3_RECRUITMENT_BRIDGE` (Format: `PILLAR_HUB`):**
  * Matches queries containing `bpsc`, `super tet`, `kvs`, `dsssb`, `kpsc`, `lpsa`, `upsa`, `valid in all states`.
  * Outputs: State recruitment bridge pages cross-selling EasyCTET as the common pedagogy engine.
* **`PILLAR_4_SYLLABUS_OVERLAP` (Format: `PDF_CHEAT_SHEET`):**
  * Matches queries containing `paper 1 paper 2 difference`, `syllabus pdf`, `malayalam medium`, `notes download`.
  * Outputs: 2-page printable Trojan Horse PDF cheat sheets with offline app CTA footers.
* **`PILLAR_5_CDP_PEDAGOGY` (Format: `REMOTION_SHORT`):**
  * Matches queries containing `pedagogy questions`, `vygotsky`, `piaget`, `kohlberg`, `thorndike`, `inclusive education`.
  * Outputs: 15-second vertical countdown quiz drills with Azure Neural TTS voiceover.

---

## 6. Output & Export Interfaces

### 6.1 Programmatic Static HTML Generator Interface
The static generator consumes records where `content_format = 'STATIC_HTML'` and outputs static HTML files adhering to the design specifications established in `compare-all-tets.html`:
* Pure HTML/CSS (under 35 KB, zero client-side JavaScript bloat).
* Embedded JSON-LD `FAQPage` schema (provides structured semantic data for semantic search, without relying on deprecated SERP badge widgets).
* Dedicated Call-to-Action (CTA) card linking to the offline EasyCTET/EasyKTET Google Play Store listing with radical privacy messaging.

### 6.2 Remotion Video Pipeline Interface
The video automation pipeline queries records where `content_format = 'REMOTION_SHORT'` and generates a structured JSON payload with calm, pedagogical hooks (strictly no manufactured panic or fake statistics):
```json
{
  "keyword_id": "KWD_CTET_00412",
  "exam": "CTET",
  "hook_title": "A Vygotsky question that frequently trips up candidates. Try it yourself.",
  "question_text": "According to Lev Vygotsky, the zone of proximal development refers to:",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "B",
  "tts_voice": "en-IN-NeerjaNeural",
  "cta_text": "Practice 2,000+ official questions 100% offline on EasyCTET"
}
```

### 6.3 Spreadsheet Export Interface
A command-line utility (`tools/export_to_csv.py`) exports all database records into `docs/research/all_india_tet_master.csv` formatted with `utf-8-sig` encoding, ensuring seamless opening in Microsoft Excel without character corruption.

---

## 7. Operational Safety, Scalability & Lifecycle

1. **HTTP Rate-Limiting Protocol:** All network requests to Google and YouTube suggest endpoints must implement an exponential backoff retry loop on `HTTP 429` (wait 3s, 6s, 12s) to prevent IP blocking.
2. **Database Version Control:** The SQLite database file (`all_india_tet_master.db`) and its CSV mirror are stored locally in `docs/research/` within the repository.
3. **Execution State Transition (6-Stage Governance):**
   $$\text{DISCOVERED} \longrightarrow \text{CLUSTERED} \longrightarrow \text{FORMAT\_ASSIGNED} \longrightarrow \text{GENERATED} \longrightarrow \text{REVIEWED} \longrightarrow \text{PUBLISHED}$$
   - `DISCOVERED`: Ingested into SQLite with raw and normalized text.
   - `CLUSTERED`: Semantic intent pillar and language mix assigned.
   - `FORMAT_ASSIGNED`: Target media format and priority score calculated.
   - `GENERATED`: Static HTML, Remotion JSON, or PDF compiled by script.
   - `REVIEWED`: Factual accuracy, official notification citations, and formatting signed off by human auditor.
   - `PUBLISHED`: Deployed to production web server, YouTube channel, or distribution channel.

---

## 8. Document Sign-off

This Software Specification Document serves as the authoritative technical baseline. All subsequent scripts, scrapers, database initialization routines, and content generators must strictly comply with the contracts defined herein.

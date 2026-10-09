# Software Specification Document (SSD)
## System: All-India TET Keyword Intelligence & Content Generation Pipeline
**Document Version:** 1.1 (8 October 2026)  
**Status:** Approved architecture, with as-built notes and refinement backlog  
**Target Environment:** Local Workstation (Windows 10/11, Python 3.10+, SQLite 3)  
**Parent System:** EasyCTET / EasyKTET Digital Strategy  

### Change log
| Version | Date | Changes |
| :--- | :--- | :--- |
| 1.0 | 2026-10-03 | Upsert ingestion, hashed IDs, canonical slugs, page and sources registers, publish checker, 6-stage lifecycle. |
| 1.1 | 2026-10-08 | Added **as-built notes** wherever the engines differ from this spec; module names corrected to the real scripts; new **Module 5.4 Syllabus Overlap Engine** and **Module 5.5 Content Verification Protocol**; publish checker rules updated to current behaviour; new **Section 8 Refinement Backlog** (GAP-01 to GAP-14) for engine work. |

> **How to read this document.** Normal text is the target specification. Blocks marked **As-built (8 Oct 2026)** describe what the code and data actually do today. Where the two differ, the gap is listed in Section 8 with an ID, so engine refinement can work through it item by item.

---

## 1. System Purpose & Objectives

### 1.1 Purpose
This document establishes the formal software architecture, data contracts, and interface specifications for the **All-India TET Keyword Intelligence & Content Generation Pipeline**. 

The system acts as the central data nervous system for EasyCTET. It discovers, normalizes, deduplicates, classifies, and routes real-world search queries across 18 Central and State Teacher Eligibility Tests into production pipelines for static web pages, short-form videos, and community cheat sheets. A second engine (Module 5.4) maps the CTET syllabus against state TET syllabi and feeds the comparison pages.

### 1.2 Core Architectural Principles
1. **Zero Data Swamp:** Every query entering the system must conform to a strict relational schema before storage.
2. **Deterministic Deduplication:** Ingestion engines must automatically merge identical queries regardless of source.
3. **OS & Filesystem Safety:** All URL slugs and filenames must be strictly sanitized against Windows filesystem reserved characters (`?`, `:`, `*`, `"`, `<`, `>`, `|`, `/`, `\`).
4. **Zero-Cloud Dependency:** The database runs on a local, zero-maintenance SQLite engine requiring no external servers, cloud subscriptions, or database daemon configurations.
5. **Loose Coupling:** Ingestion scrapers, clustering logic, and content generators interact strictly via the centralized SQLite database and standard CSV/JSON contracts.
6. **Single Source of Truth per Artefact:** Every published file has exactly one place where it is edited: either a build script (generated pages and generated data) or the HTML file itself (hand-written pages). Edits are never made to a generated output. See Section 6.4.
7. **Primary Sources Only for Facts:** No fact reaches a page unless it is traced to an entry in `sources.csv`. See Module 5.5.

---

## 2. System Architecture Overview

The system is organized into four discrete operational tiers, plus a parallel syllabus engine:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 TIER 1: INGESTION                                      │
├────────────────────┬────────────────────┬────────────────────┬─────────────────────────┤
│ Google Suggest API │ YouTube Suggest API│ Competitor Sitemaps│ Recruitment Gazette Map │
│                    │                    │ (not built: GAP-01)│                         │
└─────────┬──────────┴─────────┬──────────┴─────────┬──────────┴────────────┬────────────┘
          │      + manual discovery: forum / Quora titles (collect_forum_titles.py,      │
          │        merge_titles.py → docs/research/aspirant_questions_merged.csv)        │
          ▼                    ▼                    ▼                       ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TIER 2: NORMALIZATION & INGESTION CONTRACT                      │
│   - Lowercase & strip whitespace                                                       │
│   - Regex slugification (Windows & URL compliant)                                      │
│   - Language classification (English, Hinglish, Manglish)                              │
│   - Upsert on normalized_query (hit_count / best_rank)                                 │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         TIER 3: CENTRAL STORAGE & CLUSTERING                           │
│   Database: docs/research/all_india_tet_master.db (SQLite)                             │
│   - Intent Clustering (Cutoff, Eligibility, Recruitment, Syllabus, Pedagogy)           │
│   - Media Format Mapping (Static HTML, Pillar Hub, Remotion Video, PDF Cheat Sheet)    │
│   - Lifecycle: DISCOVERED → CLUSTERED → FORMAT_ASSIGNED → GENERATED → REVIEWED →        │
│     PUBLISHED                                                                          │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              TIER 4: OUTPUT INTERFACES                                 │
├─────────────────────────┬───────────────────────────┬──────────────────────────────────┤
│ Static HTML Generator   │ Remotion Video Automation │ PDF Cheat Sheet Compiler         │
│ (Target: EasyCTET.com)  │ (Target: @easyctetofficial)│ (Target: WhatsApp/Telegram)     │
└────────────┬────────────┴───────────────────────────┴──────────────────────────────────┘
             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  RELEASE GATE: pages.csv + sources.csv + check_publish_ready.py (Module 5.3, 5.5)      │
└────────────────────────────────────────────────────────────────────────────────────────┘

  PARALLEL: SYLLABUS OVERLAP ENGINE (Module 5.4)
  official syllabi (docs/syllabi) → master-topics.csv → build_page_hub.py / build_page_ctet_ktet.py
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
| `keyword_id` | `TEXT` | No | `PRIMARY KEY` | Deterministic SHA256 hash of `normalized_query` (e.g., `KWD_CTET_A1B2C3D4E5`). |
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
| `target_url` | `TEXT` | Yes | `DEFAULT NULL` | Relative canonical URL of the page that answers this query's intent (must exist in `pages.csv`). |
| `video_hook` | `TEXT` | Yes | `DEFAULT NULL` | Calm pedagogical voice hook for Remotion Shorts. |
| `lifecycle_status` | `TEXT` | No | `DEFAULT 'DISCOVERED'` | Stage: `DISCOVERED`, `CLUSTERED`, `FORMAT_ASSIGNED`, `GENERATED`, `REVIEWED`, `PUBLISHED`. |
| `discovered_at` | `DATETIME` | No | `DEFAULT CURRENT_TIMESTAMP`| Timestamp of ingestion. |
| `updated_at` | `DATETIME` | No | `DEFAULT CURRENT_TIMESTAMP`| Timestamp of last state modification. |

> **As-built (8 Oct 2026)**, live database: 2,422 rows (Google Suggest 1,892; YouTube 294; Job Gazette 236).
> * No `CHECK` constraint on `target_exam` exists in the live table (GAP-02).
> * `canonical_slug` is filled for every row, but it is a copy of `clean_slug` (2,409 distinct values for 2,422 rows; 13 rows hold an empty string). Many-to-one grouping is **not implemented** (GAP-03).
> * `target_url` is set one per keyword as `/{exam}/{clean_slug}/` and does not point to real pages in `pages.csv` (GAP-04).
> * `priority_score` is computed with a different formula from the one above (see 5.2 as-built; GAP-05).
> * No row has `hit_count > 1` (GAP-06).
> * `lifecycle_status`: 2,420 `FORMAT_ASSIGNED`, 2 `GENERATED`; no row is `REVIEWED` or `PUBLISHED`, although 10 pages are live (GAP-07).

### 3.3 Target Exam Enumeration Set
The `target_exam` field is validated against 18 central and state teacher eligibility examinations:
* **National:** `CTET`
* **South:** `KTET`, `TNTET`, `TS_TET`, `AP_TET`, `KARTET`
* **North / Central:** `UPTET` *(re-check status: UPESSC has published a 2026 exam calendar for UPTET; verify against an official UPESSC notice before relying on "inactive")*, `REET`, `HTET`, `MPTET`, `PSTET`, `UTET`
* **West / East:** `MAHA_TET`, `WBTET`, `OTET`, `CG_TET`, `BTET` *(Note: Subsumed by Bihar STET / BPSC TRE)*, `ASSAM_TET`

### 3.4 Content Data Files (outside the database)
These CSV files in `docs/templates/` are part of the data contract and are read by the release gate and the page builders:

| File | Owner (where it is edited) | Purpose |
| :--- | :--- | :--- |
| `pages.csv` | Hand-edited | Page register: `page_id, file, url, title, status, last_verified, source_ids, redirect_to, notes`. `P0xx` = site pages, `X0xx` = external dependencies (Play Store listings). |
| `sources.csv` | Hand-edited | Sources register `S001`–`S035`: `source_id, exam, document_title, publisher, url, publication_or_notification_date, retrieved_on, official_or_non_official, local_file_name, used_for`. |
| `page-dependencies.csv` | **Generated** by `check_publish_ready.py` | Every link on every page, its target and verdict. Never edit by hand. |
| `master-topics.csv` | **Generated** by `build_ctet_topics.py` + `map_*.py` (Module 5.4) | 182 topic rows × exam columns with `Same / Similar / Different / Not found`. Corrections must be made in the `map_*.py` scripts, not in the CSV. |
| `exam-facts.csv` | Hand-edited | Structural facts per exam (questions, marks, negative marking, pass marks, validity) with source and `VERIFIED/UNVERIFIED` status. |
| `queries.csv`, `coverage-by-topic.csv`, `question-bank-tags.csv` | Hand-edited | Templates for Search Console queries, app coverage and question tagging. Currently empty or near-empty (GAP-13). |
| `legend.md` | Hand-edited | Label definitions used on every page and sheet (overlap labels, page statuses, publish rule). |

---

## 4. Processing & Business Logic Rules

### 4.1 Slug Sanitization Rule (Windows & Web Safe)
All `clean_slug` and `canonical_slug` values must conform to strict filesystem safety:
1. Convert string to lowercase and strip whitespace.
2. Expand ampersands (`&` → ` and `).
3. Replace all non-alphanumeric characters with hyphens.
4. Collapse consecutive hyphens and strip leading/trailing hyphens.
5. **Non-ASCII Fallback:** If query is in non-Latin script (Malayalam/Devanagari) producing an empty string, generate a deterministic hash slug (`query-{md5[:8]}`).
6. **Windows Reserved Word Guard:** Protect against reserved device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`-`COM9`, `LPT1`-`LPT9`) by appending `-topic`.

> **As-built:** implemented as specified in `db_manager.clean_slug()`.

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

> **As-built:** the upsert is implemented in `db_manager.insert_keyword()`. Yet no row in the live database has `hit_count > 1`. Either each harvest run sees every query only once, or duplicates are filtered before insertion. Until this is fixed, `hit_count` carries no demand signal (GAP-06).

### 4.3 Intent Clustering & Anti-Scaled Content Abuse Architecture
To avoid Google's "Scaled Content Abuse" penalties for mass-generated thin pages:
* **Many-to-One Mapping:** Distinct long-tail keyword variations (e.g., *"ctet passing marks obc"*, *"ctet cutoff 2026 obc"*, *"ctet qualifying marks for obc category"*) are grouped under a single parent `canonical_slug` that corresponds to one real page, e.g. `passing-marks` → `/ctet/passing-marks/` (`P020`).
* **Authoritative Hubs:** Pages answer the parent intent completely, with full comparison tables and FAQs, rather than hundreds of fragmented micro-pages.
* **Link to the page register:** `canonical_slug` → `target_url` → `pages.csv.url`. A keyword is "covered" only when its `target_url` resolves to a `PUBLISHED` page.

> **As-built:** not implemented. `canonical_slug` mirrors `clean_slug` (GAP-03), and `target_url` is per keyword (GAP-04). The live pages were built by intent by hand, not from this mapping.

### 4.4 Language Classification Logic
During ingestion, the system automatically assigns `language_mix` based on lexical markers (word-boundary regex):
* **`MANGLISH`:** `ethra`, `aano`, `aavumo`, `ezhuthamo`, `undo`, `engane`, `kazhinjal`, `cheyyamo`, `padikkanam`, `kittumo`, `validaano`, `malayalam`.
* **`HINGLISH`:** `kitne`, `kitna`, `chahiye`, `pass ya fail`, `kya`, `kaise`, `kab tak`, `wale`, `de sakte`, `kare`, `hoga`, `bhi`, `mein`.
* **`ENGLISH`:** Default classification for standard English queries.

> **As-built:** marker lists above match `phase2_classify_and_route.py`. Result in the live database: 2,345 English, 61 Hinglish, 16 Manglish. `undo` and `malayalam` are weak markers: "undo" is an English word, and "malayalam" also appears in English queries (GAP-08).

---

## 5. Subsystem Module Specifications

### Module 5.1: Ingestion Engines
**Target design:** one engine per source, each writing through `db_manager.insert_keyword()`:
1. **Google alphabet expansion:** seeds × `[a-z]` × `[a-z]`, 0.25s pause, `requests.Session()` pooling, exponential backoff on HTTP 429.
2. **YouTube Suggest:** `client=youtube&ds=yt` for pedagogy-heavy and voice-style queries.
3. **Recruitment bridge matrix:** TET exams × recruitment exams (`BPSC TRE`, `Super TET`, `KPSC LPSA/UPSA`, `KVS`, `DSSSB`).
4. **Competitor sitemap parser:** public XML sitemaps (Testbook, Adda247) for topic discovery. Sitemaps show which topics competitors cover; they do **not** show traffic.

> **As-built:** engines 1–3 are combined in **`tools/run_phase1_harvest.py`** (`run_engine_1_google`, `run_engine_2_youtube`, `run_engine_3_job_recruitment`). Engine 4 (sitemaps) is **not built** (GAP-01). Manual discovery tools also exist: **`tools/collect_forum_titles.py`** (public forum and Quora titles, with robots.txt checks) and **`tools/merge_titles.py`** (merges hand-copied titles into `docs/research/aspirant_questions_merged.csv`). That merged file is not yet loaded into the database (GAP-12). Storage and export live in **`tools/db_manager.py`**.

### Module 5.2: Content Routing Engine
Applies deterministic rules to assign `intent_cluster` and `content_format`. Target rules:
* Match on **whole words or phrases**, not substrings.
* Rules are evaluated in a fixed precedence order, and the order is documented.
* Queries that match no rule, or that express an intent outside the five pillars (admit card, result, application dates, notifications), go to `intent_cluster = 'OTHER'` and `lifecycle_status = 'CLUSTERED'` for human review, rather than being forced into a pillar.
* `video_hook` text follows Section 6.2: calm, no invented statistics.
* `priority_score = (hit_count * 10) + (11 - best_rank)`, computed in a view or at query time, so it never goes stale.

> **As-built (`tools/phase2_classify_and_route.py`):**
> * **Precedence:** Pillar 5 (CDP) → Pillar 3 (Recruitment) → Pillar 1 (Cutoff) → Pillar 2 (Eligibility) → Pillar 4 (Syllabus) → **fallback to Pillar 4**. There is no `OTHER` bucket, so 100% of rows are "mapped" by construction (GAP-09).
> * **Substring matching:** e.g. `"pass"` matches "passage", `"90"` matches "1990", `"bed"` matches any word containing "bed". Pillar 2 also catches administrative intents (`fees`, `last date`, `form`, `apply`) (GAP-10).
> * **Live distribution:** Pillar 1: 506 · Pillar 2: 238 · Pillar 3: 217 · Pillar 4: 1,126 · Pillar 5: 335. Formats: STATIC_HTML 999 · PDF_CHEAT_SHEET 871 · REMOTION_SHORT 335 · PILLAR_HUB 217.
> * **Priority score** is a heuristic: base 20, plus 25 if the query is under 25 characters (15 if under 35), plus a pillar bonus (Cutoff 25, Recruitment 20, CDP 15), plus 15 for CTET/UPTET/KTET/REET. It does not use `hit_count` or `best_rank` (GAP-05).
> * **Video hooks** include *"90% of {exam} aspirants miss this pedagogy concept!"*. That is an invented statistic and breaks Section 6.2 (GAP-11).

### Module 5.3: Page Registry & Publish Readiness Verifier (`tools/check_publish_ready.py`)
Enforces release discipline, link integrity, and source traceability across all web properties.
1. **Page Register (`docs/templates/pages.csv`):** inventory of all web assets.
   * **Statuses:** `PLANNED` (no file yet) · `DRAFT` (being written or fact-checked) · `READY` (final, waiting to go live) · `PUBLISHED` (live) · `RETIRED` (never publish; `redirect_to` gives the replacement URL).
   * `X0xx` rows register external dependencies, such as Play Store listings. An `X` row may be `PUBLISHED` only after its URL returns HTTP 200.
2. **Sources Register (`docs/templates/sources.csv`):** see Module 5.5.
3. **Checks per page:**
   * Draft markers: `[EDITOR`, `TODO`, `TBC`, `class="verify"`, draft banners (`class="draft"` / `draft-banner`).
   * Every `<a href>`: resolves relative links against the page URL, looks the target up in `pages.csv` (scheme-less host + path; query and fragment ignored), and reports links to unregistered pages.
   * Anchors: `#fragment` must exist as an `id` in the target file (or the same file).
   * `--external`: HTTP-checks every external link, **including registered `X` targets marked `PUBLISHED`**. It uses Python's client first, then falls back to `curl` with a browser user agent, because some government sites block Python clients or use legacy TLS.
4. **Publish Rule:** a page is **PUBLISHABLE** only if its own status is `READY` or `PUBLISHED`, it has no draft markers, and every internal target is `PUBLISHED`, or `READY` and released in the same batch ("ship together"). Links to `PLANNED`, `DRAFT` or `RETIRED` targets block, as does any external link returning non-200 under `--external`.
5. **Output:** `docs/templates/page-dependencies.csv` (generated on a full run).

```
python docs/tools/check_publish_ready.py               # all pages
python docs/tools/check_publish_ready.py P020          # one page
python docs/tools/check_publish_ready.py --external    # include live HTTP checks
```

### Module 5.4: Syllabus Overlap Engine (new in v1.1)
Builds the topic-by-topic comparison between CTET and state TETs that feeds the comparison pages.

**Pipeline (run in this order, from `docs/templates/`):**
1. `build_ctet_topics.py`: rebuilds the CTET rows of `master-topics.csv` from CTET Sep 2026 bulletin Appendix I (182 topic rows across CDP, languages, maths, EVS, science, social studies).
2. `map_ktet.py` → `map_reet.py` → `map_mptet.py` → `map_uptet.py` → `map_htet.py`: each fills its exam columns with `Same / Similar / Different / Not found` from the official syllabus files in `docs/syllabi/`. Exam-only topics are added as `KTET-*`, `REET-*` and similar rows.
3. `build_page_hub.py` (with `patch_hub_final.py` already applied) → `docs/site-drafts/compare-all-tets.html` (P010).
4. `build_page_ctet_ktet.py` (with `patch_ktet_final.py` already applied) → `docs/site-drafts/ctet-vs-ktet.html` (P011).

**Scoring formulas:**
* **Hub labels** (`share`): (Same + Similar) / assessed CTET topics for the paper. Very high ≥ 0.85 · High ≥ 0.65 · Partial ≥ 0.40 · Low below that.
* **Hub percentages** (`wshare`): (Same × 1 + Similar × 0.5) / (matched CTET topics + exam-only topics), rounded to the nearest 5. Shown only if at least 60% of the topics are assessed.
* **CTET vs KTET page:** (Same + Similar) / number of CTET topics for the paper (Paper 1 vs Cat 1: 79 topics, 92%; Paper 2 vs Cat 2: 124 topics, 73%).

**Rules:**
* `master-topics.csv` is a **generated file**. Corrections go into the relevant `map_*.py` script with a dated comment, then the chain is re-run. A full rebuild on 8 Oct 2026 reproduced the published labels with 0 differences.
* Exams without an official topic list (HTET) are labelled **"Likely"** on pages, never as a measured result.
* Text in legacy Hindi/Malayalam fonts (Kruti Dev and similar) does not extract correctly. Those PDFs must be read visually page by page (Module 5.5).

**Verification status of `master-topics.csv` (8 Oct 2026):**

| Exam column | Checked against official syllabus | Status |
| :--- | :--- | :--- |
| `ktet_c2` | All 124 Paper 2 rows (CDP, languages, maths, science, social studies) | **Verified**; 3 labels corrected |
| `ktet_c1` | All CDP rows, all maths and EVS rows | **Verified** (languages not re-checked) |
| `uptet` (Paper 1) | All CDP rows | **Verified**; other subjects first-pass |
| `reet_l1` | All CDP rows | **Verified** (1 borderline call) |
| `uptet` (Paper 2), `reet_l2`, `mptet`, `ktet_c3`, `ktet_c4` | Not re-checked | First-pass, unverified |
| `htet` | No official topic list exists | Low confidence; "Likely" on pages |

> The `verified_by_me` column is still `N` on every row. The verification above is recorded here and in the `notes` column, not in that flag (GAP-14).

### Module 5.5: Content Verification Protocol (new in v1.1)
Every fact on a page must pass these rules before the page can be `READY`:
1. **Official source first.** Use the issuing body's own document: CBSE bulletin or FAQ, NCTE, Kerala Pareeksha Bhavan, Kerala PSC, UPESSC, BPSC, DSSSB, KVS/NVS notifications, PIB, or Supreme Court judgments. Coaching and news sites may be used to *find* a document, never as the citation. If the official PDF cannot be reached, the fact is marked as confirmed via secondary sources in `sources.csv`, and the page links the board's home page.
2. **Register it.** Every cited document gets an `S0xx` row in `sources.csv` with its URL, date, retrieval date and `official_or_non_official`. Every page lists its `source_ids` in `pages.csv`.
3. **Cite precisely on the page:** document title, number and date, and clause or page where possible (e.g., "K-TET Sept 2026 notification, page 16"). Never invent clause numbers, G.O. numbers or chapter names. *(Example found in review: "G.O.(Ms) No. 145/2021" and "Chapter VII of the prospectus" did not exist in any source and were removed.)*
4. **Read the actual text.** Legacy-font PDFs (UPESSC, REET, BPSC scans, KTET Malayalam notification) must be read as images. Scanned PDFs with no text layer must be read visually.
5. **Numbers:** state percentages and marks as the source states them. 55% of 150 is 82.5, so a "55%" rule means **83** unless the source itself says 82 (KTET's notification does say 82).
6. **Never overclaim.** Eligibility is not appointment. "Accepted in place of" is not "gets you the job". Do not say "nationwide" unless every state accepts it.
7. **Product claims** (question counts, features) must match the app's own documentation. Store links appear only when the listing returns HTTP 200; otherwise show a non-clickable "Google Play (Coming Soon)" label.
8. **Page template contract:** author "EasyCTET Research Team"; "Last checked" date; canonical URL; one home link in the header; `lang="ml"` on Malayalam blocks; FAQ JSON-LD identical to the visible FAQs (question and answer text); a linked sources list in the footer; "independent study aid" disclaimer.
9. **Re-verification triggers:** a new notification or bulletin for the exam, a court order, or 12 months since `last_verified`.

---

## 6. Output & Export Interfaces

### 6.1 Programmatic Static HTML Generator Interface
The static generator consumes records where `content_format = 'STATIC_HTML'` and outputs static HTML files adhering to the design specifications established in `compare-all-tets.html`:
* Pure HTML/CSS (target under 35 KB, zero client-side JavaScript).
* Embedded JSON-LD `FAQPage` schema matching the visible FAQs exactly (structured data for search; FAQ rich results are not expected for this site category).
* Call-to-action card for the EasyCTET/EasyKTET Play Store listing, following Module 5.5 rule 7.

> **As-built:** `tools/build_programmatic_pages.py` writes only to `docs/site-drafts/programmatic/`. All live pages were built either by the Module 5.4 builders (P010, P011) or by hand (P000, P001, P012, P020, P022, P024, P025). Page sizes: `compare-all-tets.html` 37.1 KB and `ctet-vs-ktet.html` 35.9 KB exceed the 35 KB target. The other pages are 16–31 KB.

### 6.2 Remotion Video Pipeline Interface
The video automation pipeline queries records where `content_format = 'REMOTION_SHORT'` and generates a structured JSON payload with calm, pedagogical hooks (strictly no manufactured panic or invented statistics):
```json
{
  "keyword_id": "KWD_CTET_A1B2C3D4E5",
  "exam": "CTET",
  "hook_title": "A Vygotsky question that often trips people up. Try it yourself.",
  "question_text": "According to Lev Vygotsky, the zone of proximal development refers to:",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "B",
  "tts_voice": "en-IN-NeerjaNeural",
  "cta_text": "Practise 1,800 questions offline on EasyCTET"
}
```

> **As-built:** the Remotion pipeline is not built. The `video_hook` values in the database break this section (GAP-11).

### 6.3 Spreadsheet Export Interface
All database records are exported to `docs/research/all_india_tet_master.csv` with `utf-8-sig` encoding for Microsoft Excel.

> **As-built:** implemented as `export_to_csv()` in `tools/db_manager.py`, also called at the end of Phase 2. There is no separate `tools/export_to_csv.py`.

### 6.4 Directory Separation, Source of Truth & Anti-Overwrite Safeguards
To protect human-verified editorial content from automated overwrites:
* **Editorial drafts directory (`docs/site-drafts/`):** final and published pages.
* **Programmatic scratch directory (`docs/site-drafts/programmatic/`):** the only place bulk compilers may write.
* **Prohibition:** scripts must never overwrite files in the root of `docs/site-drafts/`, and must never regenerate pages marked `RETIRED`.
* **Source of truth per page:**

| Page | Edited in |
| :--- | :--- |
| P010 `compare-all-tets.html` | `templates/build_page_hub.py` (+ `patch_hub_final.py`), data from `master-topics.csv` |
| P011 `ctet-vs-ktet.html` | `templates/build_page_ctet_ktet.py` (+ `patch_ktet_final.py`), data from `master-topics.csv` |
| P012, P020, P022, P024, P025 | The HTML file itself |
| P000, P001 | `EasyCTET-Branding/website/` (deploy repository) |

* **Deploy copy:** the live site is served from `EasyCTET-Branding/website/` (GitHub Pages). Files finalised in `docs/site-drafts/` must be copied there to go live. There is no sync check between the two folders yet (GAP-07).

---

## 7. Operational Safety, Scalability & Lifecycle

1. **HTTP Rate-Limiting Protocol:** All network requests to Google and YouTube suggest endpoints must implement an exponential backoff retry loop on `HTTP 429` (wait 3s, 6s, 12s) to prevent IP blocking.
2. **Database Version Control:** The SQLite database file (`all_india_tet_master.db`) and its CSV mirror are stored locally in `docs/research/`. Commit the CSV mirror, not the binary `.db`, to avoid merge conflicts.
3. **Execution State Transition (6-Stage Governance):**
   $$\text{DISCOVERED} \longrightarrow \text{CLUSTERED} \longrightarrow \text{FORMAT\_ASSIGNED} \longrightarrow \text{GENERATED} \longrightarrow \text{REVIEWED} \longrightarrow \text{PUBLISHED}$$
   - `DISCOVERED`: Ingested into SQLite with raw and normalized text.
   - `CLUSTERED`: Semantic intent pillar and language mix assigned (or `OTHER` for review).
   - `FORMAT_ASSIGNED`: Target media format, canonical slug and target page assigned.
   - `GENERATED`: Asset compiled by script into the sandbox.
   - `REVIEWED`: The target page passed Module 5.5 verification and is `READY` in `pages.csv`.
   - `PUBLISHED`: The target page is `PUBLISHED` in `pages.csv` and live.
4. **Sync rule:** a keyword's `lifecycle_status` for `REVIEWED`/`PUBLISHED` is derived from the status of the page its `target_url` points to. Not implemented (GAP-07).

---

## 8. Refinement Backlog (Spec vs Engines)

Prioritised for engine refinement. P1 = affects data quality or published pages; P2 = needed before scaling content; P3 = housekeeping.

| ID | Pri | Area | Gap (as-built vs spec) | Where to fix | Suggested refinement |
| :--- | :---: | :--- | :--- | :--- | :--- |
| GAP-03 | P1 | Clustering | `canonical_slug` = `clean_slug`; no many-to-one grouping | `phase2_classify_and_route.py` | Add an intent map (pattern → canonical slug → page_id), e.g. all OBC/cutoff variants → `passing-marks` (P020). Unmatched → `OTHER`. |
| GAP-04 | P1 | Clustering | `target_url` per keyword, not linked to `pages.csv` | same | Set `target_url` from the intent map to a real `pages.csv` URL; leave NULL if no page exists (that is a content gap). |
| GAP-09 | P1 | Routing | Fallback forces unmatched queries into Pillar 4; no review bucket | same | Add `OTHER` / `UNCLUSTERED`; report count per run; replace the Phase 2 DoD "100% mapped" with "≤10% OTHER after review". |
| GAP-10 | P1 | Routing | Substring matching (`pass`→passage, `90`→1990, `bed`); admin intents in Pillar 2 | same | Word-boundary regex; separate `ADMIN` intent (dates, fees, admit card, result). Add a unit-test file of 50 labelled queries. |
| GAP-11 | P1 | Hooks | `video_hook` uses invented statistics ("90% of aspirants…") | same | Replace the templates with calm hooks per Section 6.2; re-run Phase 2. |
| GAP-05 | P2 | Scoring | Heuristic priority score instead of `(hit_count*10)+(11-best_rank)` | same | Compute in a SQL view from real signals; later blend in Search Console impressions (`queries.csv`). |
| GAP-06 | P2 | Ingestion | `hit_count` never > 1 | `run_phase1_harvest.py`, `db_manager.py` | Check whether the harvester dedupes before insert; pass the suggestion position as `rank`; re-harvest a seed twice in a test. |
| GAP-07 | P2 | Lifecycle | DB lifecycle not synced with `pages.csv`; no sync between `site-drafts/` and the deploy folder | new `tools/sync_lifecycle.py`; extend `check_publish_ready.py` | Derive REVIEWED/PUBLISHED from `pages.csv`; add a check that the live copy in `EasyCTET-Branding/website/` matches `site-drafts/` for every PUBLISHED page. |
| GAP-01 | P2 | Ingestion | Sitemap engine not built | new engine | Build only for topic discovery; treat its output as topics, not demand. |
| GAP-12 | P2 | Ingestion | `aspirant_questions_merged.csv` (forum/Quora titles) not loaded | `merge_titles.py` → `db_manager` | Load with `source_engine='FORUM'` (add to the enum). |
| GAP-02 | P3 | Schema | No CHECK constraint on `target_exam` | `db_manager.init_db()` + migration | Add the constraint, or validate in `insert_keyword()`. |
| GAP-08 | P3 | Language | Weak markers (`undo`, `malayalam`) | `phase2_classify_and_route.py` | Require two markers, or drop the ambiguous ones. |
| GAP-13 | P3 | Data | `queries.csv`, `coverage-by-topic.csv`, `question-bank-tags.csv` empty | — | Fill from Search Console and the app's question bank once both are available. |
| GAP-14 | P3 | Syllabus engine | `verified_by_me` flag unused; verification recorded only in notes | `map_*.py` | Add a `verified_on` column per exam column, or set the flag per verified row, so pages can show verification coverage. |

---

## 9. Document Sign-off

This Software Specification Document serves as the authoritative technical baseline. All subsequent scripts, scrapers, database initialization routines, and content generators must comply with the contracts defined herein. Where the as-built notes differ, the gap is tracked in Section 8 until it is closed or the spec is formally changed.

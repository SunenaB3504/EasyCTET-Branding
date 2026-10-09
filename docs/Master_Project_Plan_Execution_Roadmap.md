# Master Project Plan (MPP) & Execution Roadmap
## All-India TET Keyword Intelligence & Content Distribution Engine
**Document Version:** 1.1 (8 October 2026)  
**Project Lead:** Systems Architect & Project Manager  
**Field Strategist:** Medical Representative & Field Specialist  
**Technical Workbench:** Artificial Intelligence Execution Layer  
**Target Horizon:** 90-Day Compounding Rollout (Zero-Ad Spend, Bootstrapped)  
**Companion spec:** `Software_Specification_Document_Keyword_Pipeline.md` v1.1 (gap IDs `GAP-xx` refer to its Section 8)

### Change log
| Version | Date | Changes |
| :--- | :--- | :--- |
| 1.0 | 2026-10-03 | Financial milestones, RACI, phases 0–5, launch cluster, risk register RSK-01 to RSK-09, pre-flight checklist. |
| 1.1 | 2026-10-08 | Added **Section 2: Status as of 8 Oct 2026** (phase gates, live pages, deviations); updated Phase 2 counts to the live database; added **WBS 3.7 content verification**, **WBS 4.5 redeploy queue** and **Phase R: Engine Refinement Sprint**; new risks RSK-10 to RSK-14; KPI notes. |

---

## 1. Executive Summary & Strategic Objectives

### 1.1 Financial Architecture & Milestones
* **Near-Term Bootstrap Milestone (Year 1):** Acquire 5,000 to 10,000 paid qualifying teachers across CTET & KTET at ₹950 flat. Netting ~₹680 per sale (after 18% GST and Google Play's 15% tier), this generates **₹34,00,000 to ₹68,00,000 net profit** with zero external capital, zero debt, and negligible server overhead.
* **Long-Term Compounding Vision:** $1M (~₹8.3 Crore) annual revenue at a 60%+ net profit margin across multi-exam offerings (18 Indian Central & State TETs) and subsequent quiet, offline K-12 learning companion tools.

### 1.2 Core Pillars of Execution
1. **Asymmetric Organic Distribution:** Compete where venture-backed competitors cannot look: code-mixed long-tail search queries, teacher WhatsApp sharing with admin permission, and a small number of authoritative hub pages.
2. **Zero-Data Privacy Standard:** We collect zero personal data, require no login or phone number, and store nothing remotely. We run no telemetry tracking.
3. **Teacher-Centric Organic Goodwill:** Secure lifelong teacher trust through **EasyCTET** and **EasyKTET**. Educators who cleared their exams distraction-free naturally recommend our quiet utilities to peers and parents.
4. **Systems Discipline:** Maintain a strictly defined relational schema and primary-source verification (SSD Module 5.5) before publishing any content or code.

---

## 2. Status as of 8 October 2026

### 2.1 Phase gate status

| Phase | Gate (DoD) | Status | Evidence / deviation |
| :--- | :--- | :---: | :--- |
| 0 Data setup | DB, slugifier, CSV export | **Met** | `db_manager.py`: upsert, hashed IDs, slug guards, `utf-8-sig` export. |
| 1 Ingestion | 5,000+ unique queries; 4 engines | **Not met** | 2,422 queries (Google 1,892 · YouTube 294 · Job Gazette 236). Sitemap engine not built (GAP-01). Forum/Quora titles collected but not loaded (GAP-12). `hit_count` never > 1 (GAP-06). |
| 2 Routing | 100% mapped; ranked; FORMAT_ASSIGNED | **Met on paper** | 2,420 rows FORMAT_ASSIGNED. "100% mapped" holds only because unmatched queries fall back to Pillar 4 (GAP-09). Many-to-one clustering and target pages not implemented (GAP-03, GAP-04). |
| 3 Manufacturing | Flagship pages verified and READY | **Met for web** | 8 content pages verified against primary sources (below). PDFs and Shorts not started. App billing status not tracked here. |
| 4 Distribution | Launch cluster live, zero 404s, app listing live | **Partly met** | Cluster is live, but **the EasyCTET Play listing (X001) is not live**. The **EasyKTET listing (X002) returns 404 although it is marked PUBLISHED**. Pages show "Coming Soon" labels instead of store links. |
| 5 Conversion | Search → site → install → ₹950 pass | **Blocked** | Depends on X001/X002 going live. |

### 2.2 Page register (`docs/templates/pages.csv`)

| ID | Page | Status | Built from | Verified |
| :--- | :--- | :--- | :--- | :--- |
| P000 | `/` home | PUBLISHED | deploy repo | not reviewed in this cycle |
| P001 | `/ctet/` hub | PUBLISHED | deploy repo | not reviewed in this cycle |
| P010 | `/compare-all-tets.html` | PUBLISHED | `build_page_hub.py` | 3 Oct: spot-check + official recruitment notices |
| P011 | `/ctet-vs-ktet.html` | PUBLISHED | `build_page_ctet_ktet.py` | 3 Oct: all Cat 2 rows verified; **redeploy pending** (73% figure) |
| P012 | `/ctet-vs-uptet.html` | PUBLISHED | hand-written | **not reviewed** |
| P020 | `/ctet/passing-marks/` | PUBLISHED | hand-written | 3 Oct: KVS/NVS, DSSSB, BPSC notices |
| P021 | old OBC keyword page | RETIRED → `/ctet/passing-marks/` | — | wrong "82 = pass" claim |
| P022 | `/ktet/ktet-cat-2-pass-mark-ethra/` | PUBLISHED | hand-written | 3 Oct: corrected; **redeploy pending** |
| P023 | old Bihar BPSC page | RETIRED → `/ctet/passing-marks/` | — | — |
| P024 | `/ctet/is-b-ed-eligible-for-ctet-paper-1/` | PUBLISHED | hand-written | 3 Oct: SC judgment and order, CBSE FAQ, NCTE |
| P025 | `/ktet/kerala-psc-lpst-upst-qualification/` | PUBLISHED | hand-written | 3 Oct: corrected; **redeploy pending** |
| X001 | EasyCTET on Google Play | PLANNED | — | listing returns 404 |
| X002 | EasyKTET on Google Play | PUBLISHED (register) | — | **listing returns 404 (checked 8 Oct)**; register status is wrong |

Sources register: S001–S035, with official documents preferred. Two recruitment rules (Rajasthan RSSB, Haryana HSSC) are confirmed only via secondary coverage (S027, S029).

### 2.3 Key lessons from the verification cycle
* AI-drafted pages contained **plausible but non-existent citations** (e.g., "G.O.(Ms) No. 145/2021", "Chapter VII of the prospectus"), invented history ("landmark 2024 order amended the RTE Rules"; the CTET rule actually dates from a 2018 circular), and wrong counts (CTET offers 27 languages, not 20). All were caught only by reading the primary document. Module 5.5 verification is therefore a hard gate, not a nice-to-have.
* Several government PDFs (UPESSC, REET, BPSC, KTET Malayalam) use legacy fonts or are scans, and must be read visually.
* Generated data must be corrected at its source script. A direct CSV edit would have been lost on the next rebuild (fixed: corrections now live in `map_ktet.py`).

---

## 3. RACI Governance Matrix

| Workstream / Function | Systems Architect & PM (You) | Field Strategist (Brother) | AI Technical Workbench |
| :--- | :---: | :---: | :---: |
| **Architectural Specifications & SSD** | **Accountable (A)** | Consulted (C) | Responsible (R - Drafting) |
| **Database & Schema Integrity** | **Accountable (A)** | Informed (I) | Responsible (R - Code) |
| **App Engineering & Offline Engine** | **Accountable (A)** | Consulted (C) | Responsible (R - Architecture) |
| **Vernacular Phrasing & Local Tone** | Consulted (C) | **Accountable (A)** | Responsible (R - Extraction) |
| **Scraper & Ingestion Automation** | **Accountable (A)** | Informed (I) | Responsible (R - Execution) |
| **Content Quality & Primary-Source Verification** | **Accountable (A)** | Consulted (C) | Responsible (R - Research & Drafting) |
| **Community Distribution & Ground Outreach** | Consulted (C) | **Accountable (A)** | Responsible (R - Assets) |
| **Conversion & In-App Paywall UX** | **Accountable (A)** | Consulted (C) | Responsible (R - Code) |

* **Accountable (A):** The single decision maker who owns the outcome (strictly 1 Accountable per workstream).
* **Responsible (R):** The worker who executes the technical implementation.
* **Consulted (C):** The advisor providing domain wisdom and ground feedback.
* **Informed (I):** Kept up to date on milestones.

---

## 4. Work Breakdown Structure (WBS) & 90-Day Execution Roadmap

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 90-DAY PHASE GATES                                      │
├───────────────┬───────────────┬───────────────┬───────────────┬───────────────┬─────────┤
│   PHASE 0     │   PHASE 1     │   PHASE 2     │   PHASE 3     │   PHASE 4     │ PHASE 5 │
│ Data Setup    │ Multi-Source  │ Clustering &  │ Content       │ Organic       │ Convert │
│ & Environment │ Ingestion     │ Format Routing│ Manufacturing │ Distribution  │ & Scale │
│ (Days 1–3)    │ (Days 4–10)   │ (Days 11–14)  │ (Days 15–30)  │ (Days 31–60)  │(Days 61+)
└───────────────┴───────────────┴───────────────┴───────────────┴───────────────┴─────────┘
            PHASE R: Engine Refinement Sprint (runs alongside Phase 4; see 4.7)
```

---

### Phase 0: Data Infrastructure & Storage Setup (Days 1–3) — *Met*
**Objective:** Lock down the data contracts, initialize the SQLite repository, and verify OS filesystem sanitization rules.

* **WBS 0.1:** Initialize the local SQLite database (`docs/research/all_india_tet_master.db`) strictly conforming to the SSD.
* **WBS 0.2:** Build and test the deterministic Regex Slugifier module (`clean_slug`) to prevent Windows reserved character errors (`?`, `:`, `*`, `"`, `<`, `>`, `|`).
* **WBS 0.3:** Build the Excel-compatible CSV export mirror script (`utf-8-sig`).
* **Phase Gate 0 Definition of Done (DoD):**
  * Database file created with all tables and unique constraints active.
  * Unit test verifies that inserting a query with `?` or `&` produces a valid, safe Windows slug and URL path.
  * Automated CSV export opens in Microsoft Excel without character distortion.

---

### Phase 1: Exhaustive Multi-Source Ingestion (Days 4–10) — *Not met (2,422 of 5,000)*
**Objective:** Ingest 5,000 to 10,000 raw candidate search queries across all 18 Indian TET exams.

* **WBS 1.1: Google Recursive Alphabet Sweep** (`run_phase1_harvest.py`, engine 1). Done.
* **WBS 1.2: YouTube Suggest Ingestion** (engine 2). Done.
* **WBS 1.3: Recruitment & Job Bridge Matrix** (engine 3). Done.
* **WBS 1.4: Competitor Public XML Sitemap Parser.** Not built (GAP-01). Output is topic coverage, not traffic.
* **WBS 1.5 (new): Load forum/Quora titles** from `aspirant_questions_merged.csv` as `source_engine='FORUM'` (GAP-12).
* **Phase Gate 1 Definition of Done (DoD):**
  * Database contains **5,000+ unique, deduplicated queries**.
  * Zero database lock or constraint violation crashes.
  * 100% of rows have `source_engine`, `raw_query`, and `clean_slug` populated.
  * **(new)** A repeat-harvest test shows `hit_count` increasing for re-seen queries (GAP-06).

---

### Phase 2: Classification, Priority Scoring & Content Routing (Days 11–14) — *Met on paper; refinement needed*
**Objective:** Transform raw query strings into prioritized, pillar-mapped content tickets that point at real pages.

* **WBS 2.1: Automated Language Tagging:** `ENGLISH` / `MANGLISH` / `HINGLISH` (live: 2,345 / 16 / 61).
* **WBS 2.2: Pattern Pillar Semantic Clustering.** Live counts (8 Oct 2026, 2,422 rows):
    * `PILLAR_1_CUTOFF`: 506
    * `PILLAR_2_ELIGIBILITY`: 238
    * `PILLAR_3_RECRUITMENT_BRIDGE`: 217
    * `PILLAR_4_SYLLABUS_OVERLAP`: 1,126 *(inflated by the fallback rule; GAP-09)*
    * `PILLAR_5_CDP_PEDAGOGY`: 335
* **WBS 2.3: Priority Scoring:** target `priority_score = (hit_count * 10) + (11 - best_rank)`. The engine currently uses a heuristic (GAP-05).
* **WBS 2.4: Content Format Routing:** `STATIC_HTML` 999 · `PDF_CHEAT_SHEET` 871 · `REMOTION_SHORT` 335 · `PILLAR_HUB` 217.
* **WBS 2.5: App Architecture & Offline Question Engine:**
  * Finalize local Android SQLite schema for storing past official exam questions (app documentation: 1,800 questions, 53 audio masterclasses).
  * Zero-telemetry verification: app functions 100% offline with zero external network requests.
* **WBS 2.6 (new): Intent map to real pages:** group keywords many-to-one under `canonical_slug` and set `target_url` to a `pages.csv` URL (GAP-03, GAP-04).
* **Phase Gate 2 Definition of Done (DoD), revised:**
  * Every record has a pillar **or** `OTHER`, and `OTHER` is ≤ 10% after human review (replaces "100% mapped").
  * Every Pillar 1–3 record has a `target_url` that exists in `pages.csv`, or is listed as a content gap.
  * Status transitions to `lifecycle_status = 'FORMAT_ASSIGNED'`.

---

### Phase 3: Content Manufacturing & App Hardening (Days 15–30) — *Web pages met; PDFs, Shorts, app open*
**Objective:** Assemble the initial verified batch of web, video, and PDF assets and harden the offline mobile application.

* **WBS 3.1: Pillar 1 & 2 pages.** Done: P020 (CTET passing marks by employer), P022 (KTET pass marks), P024 (B.Ed eligibility).
* **WBS 3.2: Pillar 3 recruitment bridge hubs.** Done: P010 (comparison hub with "Does CTET count here?"), P025 (Kerala PSC LPST/UPST). Open: Bihar BPSC TRE and UP Super TET sub-pages; the Supreme Court Sept 2025 in-service teacher TET mandate.
* **WBS 3.3: Pillar 4 printable cheat sheets** (5). Not started.
* **WBS 3.4: Pillar 5 pedagogical Shorts** (10). Not started. Requires GAP-11 fixed first (calm hooks).
* **WBS 3.5: Mobile App Billing & Offline Security:** Google Play In-App Billing for the ₹950 lifetime pass; offline license persistence and "Restore Purchase".
* **WBS 3.6: Publication Readiness & Link Dependency Verification:** `check_publish_ready.py --external` against all candidate pages; no draft markers; anchors valid; registered externals return 200.
* **WBS 3.7 (new): Content verification (SSD Module 5.5).**
  * 3.7.1 Review P012 (`ctet-vs-uptet.html`), P000 and P001 against primary sources; they have not been reviewed.
  * 3.7.2 Finish syllabus verification: `uptet` Paper 2, `reet_l2`, `mptet`, `ktet_c3/c4`, `ktet_c1` languages (SSD 5.4 table).
  * 3.7.3 Replace secondary-only sources S027 (RSSB) and S029 (HSSC) with the official PDFs.
  * 3.7.4 Bring P010 and P011 under 35 KB, or accept and document the exception.
* **Phase Gate 3 Definition of Done (DoD):**
  * Flagship pages fact-checked against primary sources (`REVIEWED`) and `READY` in `pages.csv`.
  * 5 printable PDF cheat sheets compiled and verified.
  * 10 pedagogical Shorts rendered and catalogued.
  * Android APK tested for 100% offline mock simulation and purchase restoration.

---

### Phase 4: Quiet Organic Distribution & Indexing (Days 31–60) — *In progress*
**Objective:** Launch distribution calmly across organic search, video search, and teacher communities.

* **WBS 4.0: Minimal Viable Launch Cluster (Synchronized Release).** Deployed with P000, P001, P010, P011, P020, plus P012, P022, P024 and P025. **Deviation:** item 6 (live Play Store listing, X001) was not met. Pages show "Coming Soon" labels, so there is no 404 for users, but there is also no conversion path.
* **WBS 4.1: Web Hub Deployment & Search Console:** deploy to GitHub Pages under `EasyCTET.com`; submit `sitemap.xml`; request indexing for cluster pages.
* **WBS 4.2: YouTube & Instagram Educational Cadence:** publish pedagogical Shorts at peak study hours (7:30 AM or 9:30 PM), grouped into theorist playlists.
* **WBS 4.3: Community Value Sharing:** share PDF cheat sheets in teacher WhatsApp/Telegram groups **with admin permission**.
* **WBS 4.4: Owned WhatsApp Channel Activation:** "Daily Offline Drills".
* **WBS 4.5 (new): Redeploy queue.** Copy from `docs/site-drafts/` to `EasyCTET-Branding/website/` and redeploy:
  1. `ctet-vs-ktet.html` (Category 2 overlap 74% → 73%; method note)
  2. `ktet-cat-2-pass-mark-ethra.html` → `/ktet/ktet-cat-2-pass-mark-ethra/`
  3. `kerala-psc-lpst-upst-ktet-ctet-qualification.html` → `/ktet/kerala-psc-lpst-upst-qualification/`
* **WBS 4.6 (new): Register hygiene.** Set X002 to `PLANNED` until `com.easyktet.app` returns HTTP 200; re-run `check_publish_ready.py --external` after every deploy.
* **Phase Gate 4 Definition of Done (DoD):**
  * Launch cluster live with 100% valid internal links and zero 404s (including store links).
  * First 25+ flagship URLs indexed on Google Search Console.
  * Initial batch of YouTube Shorts published.
  * First 250+ educators joined the Official WhatsApp Channel.

---

### Phase R: Engine Refinement Sprint (runs alongside Phase 4)
**Objective:** Close the spec-vs-engine gaps so the keyword engine drives page planning rather than producing unused rows. Work items map to SSD Section 8.

| Order | Work item | Gaps | Done when |
| :---: | :--- | :--- | :--- |
| R1 | Word-boundary rules, `ADMIN` and `OTHER` buckets, 50-query labelled test set | GAP-09, GAP-10 | Test set passes; `OTHER` + `ADMIN` reported per run. |
| R2 | Calm video hooks; re-run Phase 2 | GAP-11 | No hook contains a percentage or invented claim. |
| R3 | Intent map → `canonical_slug` → `pages.csv` URL | GAP-03, GAP-04 | Every Pillar 1–3 row points to a real page or is listed as a content gap. |
| R4 | Fix `hit_count` / `best_rank`; priority score as a SQL view | GAP-05, GAP-06 | Re-harvest test increments counts; ranking uses real signals. |
| R5 | Lifecycle sync with `pages.csv`; drafts-vs-deploy consistency check | GAP-07 | Live pages show `PUBLISHED` in the DB; checker flags any drift between `site-drafts/` and the deploy copy. |
| R6 | Load forum titles; sitemap topic engine | GAP-01, GAP-12 | Phase 1 gate (5,000+) re-assessed. |
| R7 | Schema and marker hygiene; verification flags in `master-topics.csv` | GAP-02, GAP-08, GAP-14 | Constraint added; weak markers removed; verification coverage visible per exam column. |

---

### Phase 5: Conversion Optimization & Scale (Days 61–90) — *Blocked on store listings*
**Objective:** Convert organic web and video traffic into active, paying users of the offline mobile applications.

* **WBS 5.1: The "Instant Win" Mobile Experience:** the APK opens instantly into a **100% free, full 150-question mock exam** with zero login, zero phone number, and zero network dependency. The ₹950 lifetime pass modal appears only on the scorecard.
* **WBS 5.2: In-App Billing & License Restoration:** verify the one-time purchase flow and the "Restore Purchase" button.
* **WBS 5.3: Search Console Intelligence Feedback Loop:** analyze queries with high impressions and record them in `queries.csv`; feed them back into Phase 1 and into the priority score (GAP-05, GAP-13).
* **WBS 5.4 (new): Swap "Coming Soon" labels for tagged store links** on every page once X001/X002 return 200 (the checker confirms).
* **Phase Gate 5 Definition of Done (DoD):**
  * End-to-end user path operational: Search query → `EasyCTET.com` → Google Play Store install → Free test → ₹950 Lifetime Pass conversion.

---

## 5. Risk Management Register & Mitigation Protocols

| Risk ID | Identified Risk Event | Probability | Impact | Mitigation Strategy |
| :--- | :--- | :---: | :---: | :--- |
| **RSK-01** | Google/YouTube API `HTTP 429` Rate Limiting during deep scraping. | High | Medium | Persistent `requests.Session()`, 0.3s jitter pauses, exponential backoff (3s, 6s, 12s). |
| **RSK-02** | Google "Scaled Content Abuse" penalty against thin programmatic pages. | Medium | High | Many-to-one intent clustering (GAP-03): 20–50 queries per authoritative hub page; programmatic output stays in the sandbox. |
| **RSK-03** | Aspirant disputes answer keys leading to negative Play Store reviews. | High | Low | Cite official final answer key bulletins (CBSE/Pareeksha Bhavan) in every explanation. |
| **RSK-04** | Telegram/WhatsApp group admins ban account for link sharing. | High | Medium | Share only with admin permission; useful content with a footer link; grow the owned WhatsApp Channel. |
| **RSK-05** | User changes phones and fears loss of ₹950 purchase without an account. | Medium | High | Native Google Play In-App Billing with an on-device "Restore Purchase" button, stated in the app FAQ. |
| **RSK-06** | Factual inaccuracies in reservation or eligibility advice cause candidate harm. | Medium | High | SSD Module 5.5: primary sources, precise citations, "Last checked" date, employer notices supersede general rules, human sign-off (`REVIEWED`). |
| **RSK-07** | Founder bandwidth bottleneck due to full-time field commitments. | High | High | Batches of ~10 verified pages per cycle rather than mass unverified output. |
| **RSK-08** | Broken internal links or premature deployment of pages with draft dependencies. | High | High | `check_publish_ready.py --external` before every deploy. |
| **RSK-09** | Compilers overwrite verified editorial pages or recreate retired URLs. | Medium | High | Compiler output isolated in `site-drafts/programmatic/`; `RETIRED` status blocks deprecated files. |
| **RSK-10** *(new)* | **Fabricated citations in AI-drafted content** (non-existent G.O. numbers, clause numbers, history). | High | High | Every citation must resolve to an `S0xx` source that was actually opened and read; reviewers check the cited page or clause, not just the topic. |
| **RSK-11** *(new)* | **Pages promote an app that is not live** (X001 PLANNED; X002 returns 404 but is marked PUBLISHED). | High | High | Store links only when the listing returns 200 (checker enforces this); "Coming Soon" labels until then; keep register statuses honest. |
| **RSK-12** *(new)* | **Draft and live copies drift apart** (corrected pages in `docs/site-drafts/` not redeployed; duplicate `docs/` trees in the workspace and in the deploy repository). | High | Medium | WBS 4.5 redeploy queue; GAP-07 consistency check; treat `docs/` as the single editing location and mirror deliberately. |
| **RSK-13** *(new)* | **Generated data edited in place and lost on rebuild** (`master-topics.csv`, hub and comparison pages). | Medium | High | SSD 6.4 source-of-truth table; corrections only in the builder scripts; rebuild-and-diff before deploy. |
| **RSK-14** *(new)* | **Keyword engine output misleads planning** (forced fallback to Pillar 4, substring matches, flat `hit_count`). | High | Medium | Phase R items R1–R4 before using pillar counts or priority scores for decisions. |

---

## 6. Success Metrics & Key Performance Indicators (KPIs)

1. **Anonymous App Store Metrics (Google Play Console):**
   * Monthly App Installs and Active Installs by Device.
   * Play Store Rating: Maintain ≥ 4.7 stars with zero complaints regarding data theft or ad intrusion.
   * 30-Day Refund Rate: < 1.5%.
2. **Paid Conversions & Unit Economics:**
   * Milestone 1 Target: 5,000 paid qualifying teachers at ₹950 (~₹34 Lakhs net profit).
3. **Web Performance & Search Health:**
   * 100/100 Lighthouse score; page size < 35 KB (currently exceeded by P010 at 37.1 KB and P011 at 35.9 KB; WBS 3.7.4); 0 ms JavaScript blocking.
   * Organic clicks on Google Search Console for eligibility and relaxation clusters, recorded in `queries.csv`.
4. **Content Quality (new):**
   * 100% of PUBLISHED pages have `source_ids` in `pages.csv` and a "Last checked" date within 12 months.
   * 0 citations without an `S0xx` source; 0 external links failing `--external`.
   * Syllabus verification coverage per exam column (SSD 5.4 table) reported each cycle.
5. **Content Production Cadence:**
   * 10 fully verified pillar pages, 5 community cheat sheets, and 10 calm Shorts per release cycle.

---

## 7. Pre-Flight & Launch Checklist for High SERP Placement

Every release must pass this three-tier gate:

### Tier A: Pre-Flight Static Quality & Link Audit
- [ ] **Automated audit:** `python docs/tools/check_publish_ready.py --external` reports **PUBLISHABLE** for every page in the release: 0 draft markers, 0 dead anchors, 0 links to `PLANNED`/`DRAFT`/`RETIRED` targets, 0 failing external links (including store listings).
- [ ] **Primary-source audit (Module 5.5):** every fact traced to an `S0xx` source; citations name the document, number, date and clause or page.
- [ ] **Rebuild-and-diff:** for generated pages (P010, P011), re-run the builder chain; the output must match the file being deployed.
- [ ] **Core Web Vitals:** Lighthouse 100/100 mobile; page < 35 KB; 0 ms JS blocking.
- [ ] **Schema.org Validation:** valid JSON-LD `@graph` (`Article`, `BreadcrumbList`, `FAQPage`); FAQ schema text identical to the visible FAQs.
- [ ] **Meta & Canonical Hygiene:** canonical matches the route; title and description match real candidate queries.

### Tier B: Production Deployment & Search Engine Ingestion
- [ ] **Copy to deploy repository:** files from `docs/site-drafts/` copied to `EasyCTET-Branding/website/` at their route paths.
- [ ] **Domain & SSL:** live on `https://easyctet.com` with `robots.txt` (`Allow: /`).
- [ ] **Sitemap Submission:** `https://easyctet.com/sitemap.xml` submitted to Google Search Console.
- [ ] **URL Inspection → Request Indexing** for changed pages.
- [ ] **Store listing check:** X001/X002 return 200 before any page links to them.

### Tier C: Community Seeding & Feedback
- [ ] **Curated Community Seeding:** share useful comparison tables in 5–10 teacher WhatsApp/Telegram groups with admin permission.
- [ ] **Video reinforcement:** matching calm Shorts with pinned comments pointing to the website table.
- [ ] **Search Console Monitoring:** average position and CTR; new phrases recorded in `queries.csv`.

---

## 8. Document Sign-off & Execution Readiness

This Master Project Plan connects our corporate philosophy, technical specification, and daily operational steps into a unified system. As of 8 October 2026, execution is in **Phase 4** for the web, with **Phase R (Engine Refinement)** as the next engineering focus and **Phase 5** blocked on the store listings.

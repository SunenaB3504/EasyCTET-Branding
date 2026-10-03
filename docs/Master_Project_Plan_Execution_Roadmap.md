# Master Project Plan (MPP) & Execution Roadmap
## All-India TET Keyword Intelligence & Content Distribution Engine
**Document Version:** 1.0  
**Project Lead:** Systems Architect & Project Manager  
**Field Strategist:** Medical Representative & Field Specialist  
**Technical Workbench:** Artificial Intelligence Execution Layer  
**Target Horizon:** 90-Day Compounding Rollout (Stealth, Zero-Ad Spend, Bootstrapped)  

---

## 1. Executive Summary & Strategic Objectives

### 1.1 Financial Architecture & Milestones
* **Near-Term Bootstrap Milestone (Year 1):** Acquire 5,000 to 10,000 paid qualifying teachers across CTET & KTET at ₹950 flat. Netting ~₹680 per sale (after 18% GST and Google Play's 15% tier), this generates **₹34,00,000 to ₹68,00,000 net profit** with zero external capital, zero debt, and negligible server overhead.
* **Long-Term Compounding Vision:** $1M (~₹8.3 Crore) annual revenue at a 60%+ net profit margin across multi-exam offerings (18 Indian Central & State TETs) and subsequent quiet, offline K-12 learning companion tools.

### 1.2 Core Pillars of Execution
1. **Asymmetric Organic Distribution:** Compete where venture-backed competitors cannot look: code-mixed long-tail search queries, dark-social teacher WhatsApp sharing, and lean programmatic SEO hubs.
2. **Zero-Data Privacy Standard:** We collect zero personal data, require no login or phone number, and store nothing remotely. We run no telemetry tracking.
3. **Teacher-Centric Organic Goodwill:** Secure lifelong teacher trust through **EasyCTET** and **EasyKTET**. Educators who cleared their exams distraction-free naturally recommend our quiet utilities to peers and parents.
4. **Systems Discipline:** Maintain a strictly defined relational schema and primary-source verification process before publishing any content or code.

---

## 2. RACI Governance Matrix

| Workstream / Function | Systems Architect & PM (You) | Field Strategist (Brother) | AI Technical Workbench |
| :--- | :---: | :---: | :---: |
| **Architectural Specifications & SSD** | **Accountable (A)** | Consulted (C) | Responsible (R - Drafting) |
| **Database & Schema Integrity** | **Accountable (A)** | Informed (I) | Responsible (R - Code) |
| **App Engineering & Offline Engine** | **Accountable (A)** | Consulted (C) | Responsible (R - Architecture) |
| **Vernacular Phrasing & Local Tone** | Consulted (C) | **Accountable (A)** | Responsible (R - Extraction) |
| **Scraper & Ingestion Automation** | **Accountable (A)** | Informed (I) | Responsible (R - Execution) |
| **Content Quality & Pedagogy Verification** | **Accountable (A)** | Consulted (C) | Responsible (R - Generation) |
| **Community Distribution & Ground Outreach** | Consulted (C) | **Accountable (A)** | Responsible (R - Assets) |
| **Conversion & In-App Paywall UX** | **Accountable (A)** | Consulted (C) | Responsible (R - Code) |

* **Accountable (A):** The single decision maker who owns the outcome (strictly 1 Accountable per workstream).
* **Responsible (R):** The worker who executes the technical implementation.
* **Consulted (C):** The advisor providing domain wisdom and ground feedback.
* **Informed (I):** Kept up to date on milestones.

---

## 3. Work Breakdown Structure (WBS) & 90-Day Execution Roadmap

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 90-DAY PHASE GATES                                      │
├───────────────┬───────────────┬───────────────┬───────────────┬───────────────┬─────────┤
│   PHASE 0     │   PHASE 1     │   PHASE 2     │   PHASE 3     │   PHASE 4     │ PHASE 5 │
│ Data Setup    │ Multi-Source  │ Clustering &  │ Content       │ Stealth       │ Convert │
│ & Environment │ Ingestion     │ Format Routing│ Manufacturing │ Distribution  │ & Scale │
│ (Days 1–3)    │ (Days 4–10)   │ (Days 11–14)  │ (Days 15–30)  │ (Days 31–60)  │(Days 61+)
└───────────────┴───────────────┴───────────────┴───────────────┴───────────────┴─────────┘
```

---

### Phase 0: Data Infrastructure & Storage Setup (Days 1–3)
**Objective:** Lock down the data contracts, initialize the SQLite repository, and verify OS filesystem sanitization rules.

* **WBS 0.1:** Initialize the local SQLite database (`docs/research/all_india_tet_master.db`) strictly conforming to `Software_Specification_Document_Keyword_Pipeline.md`.
* **WBS 0.2:** Build and test the deterministic Regex Slugifier module (`clean_slug`) to prevent Windows reserved character errors (`?`, `:`, `*`, `"`, `<`, `>`, `|`).
* **WBS 0.3:** Build the Excel-compatible CSV export mirror script (`utf-8-sig`) with automated sync triggers.
* **Phase Gate 0 Definition of Done (DoD):**
  * Database file created with all tables and unique constraints active.
  * Unit test verifies that inserting a query with `?` or `&` produces a valid, safe Windows slug and URL path.
  * Automated CSV export opens seamlessly in Microsoft Excel without character distortion.

---

### Phase 1: Exhaustive Multi-Source Ingestion (Days 4–10)
**Objective:** Ingest 5,000 to 10,000 raw candidate search queries across all 18 Indian TET exams from 5 discrete data engines.

* **WBS 1.1: Google Recursive Alphabet Soup Sweep:**
  * Execute recursive A–Z and prefix letter expansion across all 18 exams using `requests.Session()` with connection pooling.
  * Implement exponential backoff for `HTTP 429` rate-limit resilience.
* **WBS 1.2: YouTube Video & Voice Suggest Ingestion:**
  * Query YouTube’s dedicated autocomplete endpoint (`client=youtube&ds=yt`) for pedagogical, theorist, and chapter-specific queries.
* **WBS 1.3: Recruitment & Job Bridge Gazette Siphon:**
  * Cross-multiply all 18 exams against downstream job recruitment boards (`BPSC TRE`, `Super TET`, `KPSC LPSA/UPSA`, `KVS`, `DSSSB`).
* **WBS 1.4: Competitor Public XML Sitemap Parser:**
  * Parse public sitemaps of incumbents (Testbook, Adda247, Shiksha) to extract verified historical high-traffic URL slugs.
* **Phase Gate 1 Definition of Done (DoD):**
  * Database contains **5,000+ unique, deduplicated queries**.
  * Zero database lock or constraint violation crashes.
  * 100% of rows have `source_engine`, `raw_query`, and `clean_slug` populated.

---

### Phase 2: Classification, Priority Scoring & Content Routing (Days 11–14)
**Objective:** Transform raw query strings into mathematically prioritized, pillar-mapped content tickets.

* **WBS 2.1: Automated Language Tagging:**
  * Tag queries as `ENGLISH`, `MANGLISH` (containing `ethra`, `aano`, `ezhuthamo`), or `HINGLISH` (containing `kitne`, `pass ya fail`, `kya b.ed`).
* **WBS 2.2: Pattern Pillar Semantic Clustering:**
  * Categorize every query into one of our 5 empirical patterns:
    * `PILLAR_1_CUTOFF` (394 queries: 82 vs 90 marks, category relaxations)
    * `PILLAR_2_ELIGIBILITY` (160 queries: B.Ed vs D.El.Ed, Supreme Court rulings)
    * `PILLAR_3_RECRUITMENT_BRIDGE` (63 queries: BPSC, Super TET, KPSC, KVS validity)
    * `PILLAR_4_SYLLABUS_OVERLAP` (587 queries: Paper 1 vs Paper 2 differences, syllabus PDFs)
    * `PILLAR_5_CDP_PEDAGOGY` (270 queries: Theorists, Piaget, Vygotsky, Kohlberg)
* **WBS 2.3: Search Frequency & Priority Scoring:**
  * Calculate `priority_score = (hit_count * 10) + (11 - best_rank)` to rank high-focus keywords for production.
* **WBS 2.4: Content Format Routing:**
  * Assign each record its optimal production medium: `STATIC_HTML`, `REMOTION_SHORT`, `PDF_CHEAT_SHEET`, or `PILLAR_HUB`.
* **WBS 2.5: App Architecture & Offline Question Engine:**
  * Finalize local Android SQLite schema for storing 2,000+ past official exam questions.
  * Implement zero-telemetry verification: app functions 100% offline with zero external network requests.
* **Phase Gate 2 Definition of Done (DoD):**
  * 100% of records mapped to a Pattern Pillar.
  * Records ranked by `priority_score` in `all_india_tet_master.csv`.
  * Status transitions to `lifecycle_status = 'FORMAT_ASSIGNED'`.

---

### Phase 3: Automated Content Manufacturing & App Hardening (Days 15–30)
**Objective:** Assemble the initial verified batch of web, video, and PDF assets and harden the offline mobile application.

* **WBS 3.1: Pillar 1 & 2 Static HTML Production (`EasyCTET.com`):**
  * Generate category-wise cutoff tables (Pillar 1) highlighting the CBSE 60% rule vs state relaxation matrix.
  * Generate B.Ed/D.El.Ed decision trees (Pillar 2) citing Supreme Court & NCTE notifications.
  * Embed JSON-LD `FAQPage` schema and calm offline app CTA badges (under 35 KB page payload).
* **WBS 3.2: Pillar 3 State Recruitment Bridge Hubs:**
  * Deploy `compare-all-tets.html` and state sub-hubs (Bihar BPSC TRE, UP Super TET, Kerala KPSC).
  * Address the Supreme Court Sept 2025 in-service teacher TET mandate.
* **WBS 3.3: Pillar 4 High-Utility Printable Cheat Sheets:**
  * Generate 5 printable 2-page syllabus difference sheets for WhatsApp/Telegram distribution with quiet offline footers.
* **WBS 3.4: Pillar 5 Pedagogical Shorts (`@easyctetofficial`):**
  * Render 10 vertical question drills (Vygotsky, Piaget, Kohlberg) using calm, thoughtful hooks and Azure Neural TTS voiceover. Strictly zero manufactured panic or heartbeat timers.
* **WBS 3.5: Mobile App Billing & Offline Security:**
  * Integrate Google Play In-App Billing for the single ₹950 lifetime pass.
  * Verify offline license persistence and "Restore Purchase" functionality.
* **WBS 3.6: Publication Readiness & Link Dependency Verification:**
  * Execute `docs/tools/check_publish_ready.py` against all candidate drafts.
  * Eliminate all editor markers (`[EDITOR]`, `TODO`, `TBC`, draft banners).
  * Validate anchor targets (e.g. `#ctet-accepted`) and verify linked pages in `docs/templates/pages.csv`.
* **Phase Gate 3 Definition of Done (DoD):**
  * Initial wave of flagship Intent Hub pages compiled and fact-checked against primary bulletins (`lifecycle_status = 'REVIEWED'`).
  * Pages pass static validation and transition to `status = 'READY'` in `pages.csv`.
  * 5 printable PDF cheat sheets compiled and verified.
  * 10 pedagogical shorts rendered and cataloged.
  * Android APK tested for 100% offline mock simulation and purchase restoration.

---

### Phase 4: Quiet Organic Distribution & Indexing (Days 31–60)
**Objective:** Launch distribution calmly across organic search, video search, and teacher communities.

* **WBS 4.0: Minimal Viable Launch Cluster (Synchronized Release):**
  * Prevent broken navigation and orphan pages by deploying the interdependent flagship cluster simultaneously:
    1. **Home Page (`P000`, `/`):** Navigation root and primary brand anchor.
    2. **CTET Section Hub (`P001`, `/ctet/`):** Breadcrumb and category hub.
    3. **All-India Comparison Hub (`P010`, `/compare-all-tets.html`):** Resolved editor notes and verified state anchors (`#ctet-accepted`).
    4. **CTET vs KTET Comparison (`P011`, `/ctet-vs-ktet.html`):** Verified syllabus difference matrix.
    5. **CTET Passing Marks Guide (`P020`, `/ctet/passing-marks/`):** Fully unblocked and publishable.
    6. **Active Google Play Store Listing (`X001`):** Verified live app URL.
  * Mandatory pre-flight condition: `python docs/tools/check_publish_ready.py` returns `PUBLISHABLE` for all release pages.
* **WBS 4.1: Web Hub Deployment & Search Console:**
  * Deploy verified static HTML cluster to GitHub Pages under `EasyCTET.com`.
  * Submit XML sitemaps to Google Search Console; verify mobile-friendly indexing.
* **WBS 4.2: YouTube & Instagram Educational Cadence:**
  * Publish pedagogical shorts consistently at peak study hours (7:30 AM or 9:30 PM).
  * Group videos into theorist playlists for calm, focused revision.
* **WBS 4.3: Community Value Sharing:**
  * Share high-value PDF cheat sheets in active WhatsApp and Telegram teacher study groups with admin permission.
* **WBS 4.4: Owned WhatsApp Channel Activation:**
  * Launch the **Official EasyCTET/EasyKTET WhatsApp Channel** for *"Daily Offline Drills"*, migrating community members into an owned broadcast audience.
* **Phase Gate 4 Definition of Done (DoD):**
  * Minimal Viable Launch Cluster live with 100% valid internal links and zero 404s.
  * First 25+ flagship URLs indexed on Google Search Console.
  * Initial batch of YouTube Shorts published with clean Play Store links.
  * First 250+ educators joined the Official WhatsApp Channel.

---

### Phase 5: Conversion Optimization & Scale (Days 61–90)
**Objective:** Convert organic web and video traffic into active, paying users of the offline mobile applications.

* **WBS 5.1: The "Instant Win" Mobile Experience:**
  * Android APK opens instantly into a **100% free, full 150-question mock exam** with zero login, zero phone number, and zero network dependency.
  * Display the single ₹950 lifetime pass modal only upon scorecard completion.
* **WBS 5.2: In-App Billing & License Restoration:**
  * Verify Google Play Billing API one-time purchase flow and the "Restore Purchase" one-click button for device migration.
* **WBS 5.3: Search Console Intelligence Feedback Loop:**
  * Analyze Search Console search queries generating high impressions to expand the programmatic library.
* **Phase Gate 5 Definition of Done (DoD):**
  * End-to-end user path operational: Search query $\rightarrow$ `EasyCTET.com` $\rightarrow$ Google Play Store install $\rightarrow$ Free test $\rightarrow$ ₹950 Lifetime Pass conversion.

---

## 4. Risk Management Register & Mitigation Protocols

| Risk ID | Identified Risk Event | Probability | Impact | Mitigation Strategy |
| :--- | :--- | :---: | :---: | :--- |
| **RSK-01** | Google/YouTube API `HTTP 429` Rate Limiting during deep scraping. | High | Medium | Implement persistent `requests.Session()`, 0.3s jitter pauses, and exponential backoff retry loops (3s, 6s, 12s). |
| **RSK-02** | Google "Scaled Content Abuse" penalty against thin programmatic pages. | Medium | High | Many-to-One Intent Clustering: group 20–50 long-tail queries under single authoritative hub pages with comprehensive data tables. |
| **RSK-03** | Aspirant disputes answer keys leading to negative Play Store reviews. | High | Low | Explicitly cite official government final answer key bulletins (CBSE/Pareeksha Bhavan) in every explanation. |
| **RSK-04** | Telegram/WhatsApp group admins ban account for link sharing. | High | Medium | Use printable cheat sheets with zero promotional body copy; app links reside strictly in academic footers. Pull traffic into our owned WhatsApp Channel. |
| **RSK-05** | User changes phones and fears loss of ₹950 purchase without an account. | Medium | High | Utilize native Google Play In-App Billing with a prominent on-device "Restore Purchase" button. State this clearly in the app FAQ. |
| **RSK-06** | Factual inaccuracies in state reservation or eligibility advice cause candidate harm. | Medium | High | Every page must cite specific official gazettes/bulletins, display a "Last Verified" date-stamp, and clarify that employer notices supersede CTET marksheets. Mandatory human sign-off (`REVIEWED`). |
| **RSK-07** | Founder bandwidth bottleneck due to full-time field commitments. | High | High | Keep content manufacturing in manageable batches (10 pages per cycle) rather than mass unverified dumps. |
| **RSK-08** | Broken internal links or premature deployment of orphan pages with draft dependencies. | High | High | Enforce pre-flight verification via `check_publish_ready.py`. No page may be published unless all linked targets are `READY` or `PUBLISHED`. |
| **RSK-09** | Programmatic compilers accidentally overwrite verified editorial pages or recreate retired URLs. | Medium | High | Isolate compiler outputs into `docs/site-drafts/programmatic/`. Enforce `RETIRED` status in `pages.csv` to permanently block deprecated keyword files. |

---

## 5. Success Metrics & Key Performance Indicators (KPIs)

1. **Anonymous App Store Metrics (Google Play Console):**
   * Monthly App Installs and Active Installs by Device.
   * Play Store Rating: Maintain $\ge 4.7$ stars with zero complaints regarding data theft or ad intrusion.
   * 30-Day Refund Rate: $< 1.5\%$.
2. **Paid Conversions & Unit Economics:**
   * Milestone 1 Target: 5,000 paid qualifying teachers at ₹950 (generating ~₹34 Lakhs net profit).
3. **Web Performance & Search Health:**
   * 100/100 Google Lighthouse score on `EasyCTET.com`, page size $< 35\text{ KB}$, $0\text{ms}$ JavaScript blocking time.
   * Increasing organic clicks on Google Search Console for state relaxation and eligibility intent clusters.
4. **Content Production Cadence:**
   * 10 fully verified pillar pages, 5 community cheat sheets, and 10 calm shorts published per release cycle.

---

## 6. Pre-Flight & Launch Checklist for High SERP Placement

To guarantee that real candidates searching on Google discover our pages ahead of bloated commercial portals, every release must pass this three-tier gate:

### Tier A: Pre-Flight Static Quality & Link Audit
- [ ] **Automated Static Audit (`check_publish_ready.py`):** 0 unresolved `[EDITOR]` or `TODO` tags, 0 dead `#anchor` fragments, and 0 links pointing to `PLANNED` or `DRAFT` assets.
- [ ] **100/100 Core Web Vitals:** Mobile Lighthouse performance score of 100/100; total page weight $< 35\text{ KB}$; 0ms JavaScript execution blocking.
- [ ] **Schema.org Validation:** Valid JSON-LD `@graph` (`Article`, `BreadcrumbList`, and `FAQPage`) tested on Google's Rich Results Testing tool.
- [ ] **Meta & Canonical Hygiene:** `<link rel="canonical">` matches the exact route; `<title>` and `<meta name="description">` match real candidate long-tail queries.

### Tier B: Production Deployment & Search Engine Ingestion
- [ ] **Domain & SSL Deployment:** Production site live under HTTPS on `https://easyctet.com` with clean `robots.txt` (`Allow: /`).
- [ ] **Sitemap Submission:** Generate and submit `https://easyctet.com/sitemap.xml` directly to Google Search Console.
- [ ] **Accelerated URL Inspection Crawl:** Execute **URL Inspection $\rightarrow$ "Request Indexing"** in Google Search Console for all cluster pages to trigger immediate crawling.
- [ ] **Active App Store URL Verification:** Confirm Google Play Store URL (`X001`) with UTM campaign tags is live and functional.

### Tier C: Dark Social Seeding & Dwell-Time Flywheel
- [ ] **Curated Community Seeding:** Share clean, helpful comparison tables in 5–10 active teacher WhatsApp/Telegram groups with admin permission.
- [ ] **Video Algorithmic Reinforcement:** Publish matching calm Shorts on YouTube with pinned comments pointing back to the website table.
- [ ] **Search Console Monitoring:** Monitor average position and CTR in GSC Performance reports to capture emerging search phrases.

---

## 7. Document Sign-off & Execution Readiness

This Master Project Plan connects our corporate philosophy, technical specification, and daily operational steps into a unified system. 

Execution commences at **Phase 0: Infrastructure & Data Foundation Setup**.

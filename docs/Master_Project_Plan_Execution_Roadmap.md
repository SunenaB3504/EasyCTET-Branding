# Master Project Plan (MPP) & Execution Roadmap
## All-India TET Keyword Intelligence & Content Distribution Engine
**Document Version:** 1.0  
**Project Lead:** Systems Architect & Project Manager  
**Field Strategist:** Medical Representative & Field Specialist  
**Technical Workbench:** Artificial Intelligence Execution Layer  
**Target Horizon:** 90-Day Compounding Rollout (Stealth, Zero-Ad Spend, Bootstrapped)  

---

## 1. Executive Summary & Strategic Objectives

### 1.1 The Strategic Objective
To build an unshakeable, profitable, bootstrapped software and digital presence across India that captures teacher trust organically—generating **$1M annual revenue at a 60%+ net profit margin** with zero external venture capital, zero debt, and zero tele-sales harassment.

### 1.2 Core Pillars of Execution
1. **Stealth & Asymmetric Distribution:** Compete where venture-backed competitors cannot look (code-mixed long-tail queries, Dark Social WhatsApp sharing, and automated programmatic SEO).
2. **Offline-First & Zero-Telemetry:** Leverage the Digital Personal Data Protection (DPDP) Act 2023 as an unassailable moral and technical moat.
3. **The Teacher Trojan Horse:** Secure the lifelong trust of qualifying teachers through **EasyCTET** and **EasyKTET**, turning them into the primary unpaid distribution gatekeepers for future K-12 student applications.
4. **Systems Discipline:** Maintain a strictly defined, relational data contract before touching scrapers or content generators.

---

## 2. RACI Governance Matrix

| Workstream / Function | Systems Architect & PM (You) | Field Strategist (Brother) | AI Technical Workbench |
| :--- | :---: | :---: | :---: |
| **Architectural Specifications & SSD** | **Accountable (A)** | Consulted (C) | Responsible (R - Drafting) |
| **Database & Schema Integrity** | **Accountable (A)** | Informed (I) | Responsible (R - Code) |
| **Vernacular Phrasing & Empathy Review** | Consulted (C) | **Accountable (A)** | Responsible (R - Extraction) |
| **Scraper & Ingestion Automation** | **Accountable (A)** | Informed (I) | Responsible (R - Execution) |
| **Content Quality & Pedagogy Verification** | Accountable (A) | **Accountable (A)** | Responsible (R - Generation) |
| **Dark Social & Community Infiltration** | Consulted (C) | **Accountable (A)** | Responsible (R - Assets) |
| **Conversion & In-App Paywall UX** | **Accountable (A)** | Consulted (C) | Responsible (R - Code) |

* **Accountable (A):** The decision maker who owns the outcome.
* **Responsible (R):** The worker who executes the technical implementation.
* **Consulted (C):** The advisor providing domain wisdom and feedback.
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

### Phase 2: Classification, Language Tagging & Content Routing (Days 11–14)
**Objective:** Transform raw query strings into structured, actionable content tickets.

* **WBS 2.1: Automated Language Tagging:**
  * Tag queries as `ENGLISH`, `MANGLISH` (containing `ethra`, `aano`, `ezhuthamo`), or `HINGLISH` (containing `kitne`, `pass ya fail`, `kya b.ed`).
* **WBS 2.2: Semantic Intent Clustering:**
  * Run rule-based pattern matching to categorize every query into:
    * `CLUSTER_A_CUTOFF` (Passing marks, qualifying rules)
    * `CLUSTER_B_ELIGIBILITY` (B.Ed vs D.El.Ed, degree requirements)
    * `CLUSTER_C_CDP_PEDAGOGY` (Theorists, child development, learning)
    * `CLUSTER_D_PYQ_SYLLABUS` (Past papers, official answer keys)
    * `CLUSTER_E_RECRUITMENT` (Job eligibility, state validity)
* **WBS 2.3: Content Format Routing:**
  * Assign each record its target production medium: `STATIC_HTML`, `REMOTION_SHORT`, `PDF_CHEAT_SHEET`, or `PILLAR_HUB`.
* **Phase Gate 2 Definition of Done (DoD):**
  * Zero records remain in `UNCLUSTERED` or `UNASSIGNED` status.
  * 100% of records transition to `lifecycle_status = 'FORMAT_ASSIGNED'`.

---

### Phase 3: Automated Content Manufacturing (Days 15–30)
**Objective:** Assemble the web, video, and PDF assets using automated, zero-marginal-cost software pipelines.

* **WBS 3.1: Programmatic Static HTML Assembly (`EasyCTET.com`):**
  * Build the Python template generator feeding off `STATIC_HTML` records.
  * Ensure every generated page includes:
    * Under 35 KB total payload (zero framework JavaScript).
    * Structured JSON-LD `FAQPage` schema.
    * High-contrast CTA card driving to Google Play.
    * Parent hub breadcrumb navigation.
* **WBS 3.2: Automated Remotion Video Pipeline (`@easyctetofficial`):**
  * Set up React/Remotion 9:16 templates with animated countdown timers and karaoke subtitles.
  * Connect Azure Neural Speech TTS (Hindi/Malayalam) for automated voiceover rendering.
  * Batch-render the first 30 daily vertical shorts.
* **WBS 3.3: Trojan Horse PDF Cheat Sheets:**
  * Generate 10 beautifully styled 2-page PDF revision sheets with embedded QR codes and offline app footers.
* **Phase Gate 3 Definition of Done (DoD):**
  * 100+ static HTML pages generated and tested locally.
  * 30 vertical Remotion MP4 video files rendered and cataloged.
  * 10 PDF cheat sheets compiled and verified.

---

### Phase 4: Stealth Multi-Channel Distribution & Indexing (Days 31–60)
**Objective:** Launch distribution silently across organic search, social algorithms, and community dark social.

* **WBS 4.1: Web Hub Deployment & Search Console:**
  * Push static HTML directory to GitHub Pages under `EasyCTET.com`.
  * Submit XML sitemaps to Google Search Console; verify mobile-friendly indexing.
* **WBS 4.2: YouTube & Instagram Cadence:**
  * Publish 1 Remotion short per day at peak commute hours (7:30 AM) or pre-sleep hours (9:30 PM).
  * Structure videos into topic-specific playlists for algorithmic bingeing.
* **WBS 4.3: Dark Social Community Seeding:**
  * Distribute high-value PDF cheat sheets into 30–50 active WhatsApp and Telegram teacher study groups.
  * Monitor footer-link clickthrough rates.
* **WBS 4.4: Owned WhatsApp Channel Activation:**
  * Launch the **Official EasyCTET/EasyKTET WhatsApp Channel** for *"Daily Offline Drills"*, migrating borrowed community members into an owned broadcast audience.
* **Phase Gate 4 Definition of Done (DoD):**
  * First 50+ URLs indexed on Google Search Console.
  * 30 consecutive days of YouTube Shorts published with active Play Store links in comments.
  * Initial 500+ members joined the Official WhatsApp Channel.

---

### Phase 5: Conversion Optimization, Play Store Linking & Scaling (Days 61–90)
**Objective:** Convert organic web and video traffic into active, paying users of the offline mobile applications.

* **WBS 5.1: The "Instant Win" Mobile Experience:**
  * Ensure the EasyCTET / EasyKTET Android APK opens instantly into a **100% free, full 150-question mock exam** with zero login, zero phone number, and zero network dependency.
  * Trigger the single ₹950 lifetime pass modal only upon scorecard completion.
* **WBS 5.2: In-App Billing & License Restoration:**
  * Verify Google Play Billing API one-time purchase flow and the "Restore Purchase" one-click button for device migration.
* **WBS 5.3: Search Console Intelligence Feedback Loop:**
  * Analyze Search Console search queries generating high impressions but low clicks.
  * Feed new high-performing search phrases back into Step 1 to expand the programmatic library.
* **Phase Gate 5 Definition of Done (DoD):**
  * End-to-end user path operational: Search query $\rightarrow$ `EasyCTET.com` $\rightarrow$ Google Play Store install $\rightarrow$ Free test $\rightarrow$ ₹950 Lifetime Pass conversion.

---

## 4. Risk Management Register & Mitigation Protocols

| Risk ID | Identified Risk Event | Probability | Impact | Mitigation Strategy |
| :--- | :--- | :---: | :---: | :--- |
| **RSK-01** | Google/YouTube API `HTTP 429` Rate Limiting during deep scraping. | High | Medium | Implement persistent `requests.Session()`, 0.3s jitter pauses, and exponential backoff retry loops (3s, 6s, 12s). |
| **RSK-02** | Google "Scaled Content Abuse" penalty against thin programmatic pages. | Medium | High | Guarantee that every page includes a unique data table (cutoff marks breakdown), rich `FAQPage` schema, and links back to the pillar hub. |
| **RSK-03** | Aspirant disputes answer keys leading to negative Play Store reviews. | High | Low | Explicitly cite official government final answer key bulletins (CBSE/Pareeksha Bhavan) in every explanation. |
| **RSK-04** | Telegram/WhatsApp group admins ban account for link sharing. | High | Medium | Use "Trojan Horse PDFs" containing zero promotional body copy; app links reside strictly in academic footers. Pull traffic into our own owned WhatsApp Channel. |
| **RSK-05** | User changes phones and fears loss of ₹950 purchase without an account. | Medium | High | Utilize native Google Play In-App Billing with a prominent on-device "Restore Purchase" button. State this clearly in the app FAQ. |

---

## 5. Success Metrics & Key Performance Indicators (KPIs)

1. **Data Completeness:** $\ge 5,000$ unique, verified queries across all 18 Indian TET exams stored in `all_india_tet_master.db`.
2. **Web Performance:** 100/100 Google Lighthouse score on `EasyCTET.com`, page size $< 35\text{ KB}$, $0\text{ms}$ JavaScript blocking time.
3. **Organic Search Visibility:** $\ge 25,000$ monthly organic search impressions on Google Search Console within 60 days of sitemap submission.
4. **Video Output:** 30 shorts published per month with zero manual video editing overhead.
5. **Conversion Rate:** $3\%\text{ to }5\%$ of active app test-takers converting to the ₹950 Lifetime Pass.

---

## 6. Document Sign-off & Execution Readiness

This Master Project Plan connects our corporate philosophy, technical specification, and daily operational steps into a unified system. 

Execution commences at **Phase 0: Infrastructure & Data Foundation Setup**.

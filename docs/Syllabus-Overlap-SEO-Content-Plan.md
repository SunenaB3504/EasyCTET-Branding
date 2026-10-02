# Web Content, Syllabus Overlap and SEO Plan (easyctet.com)

Status: v2, 1 October 2026 · Owner: EasyCTET / EasyKTET developer · Review cycle: monthly
This is the single tracking document for everything web-related: research data, pages, SEO, conversion, community answers and measurement.

---

## 1. Purpose and scope

Help teachers answer "Is my CTET preparation enough for my state TET?" with verified information, and turn the readers who find it useful into EasyCTET / EasyKTET users, openly and without tricks.

- **Primary exams:** CTET and KTET.
- **Secondary (compared, not campaigned for):** UPTET, REET, MPTET (2026 in-service test), HTET. Bihar STET is excluded (secondary level, classes 9-12).
- **The message:** most TET marks are pedagogy that carries across exams; the pedagogy and child-development part is the hard part; we show exactly what is covered and what to add.
- **Out of scope for now:** state-specific ad campaigns, claims of full state-syllabus coverage, any score or pass guarantee.

### Goals (first 90 days)

| Goal | Target |
|---|---|
| Hub + five exam pages live (English) | Week 6 |
| Hindi/Hinglish hub live | Week 8 |
| Spot-check of the overlap mapping finished (about 10% of rows) | Before anything is published |
| Search Console impressions on comparison pages | Baseline week 4, then +50% by day 90 |
| Installs attributed to the site (tagged links) | Baseline week 4, then track monthly |
| Factual errors on live pages | 0 known; every page shows "last verified" |

## 2. Principles

1. **Accuracy over speed.** Facts come from the exam board's own documents. Anything from a coaching site or an AI summary is marked unverified and kept off public pages.
2. **Honest coverage.** Every page says what the app covers, what to add, and what has not been compared.
3. **Lead with the answer.** Verdict first, tables second, method last.
4. **Transparent promotion.** Soft calls to action beside genuinely useful content. Disclose that we make the app wherever we mention it. No fake accounts, no hidden promotion, no outcome guarantees.
5. **Privacy-consistent.** No sign-up and no personal data on the site, matching the app's promise.
6. **Own words.** Write our own comparisons and explanations. Check each board's terms before hosting any question paper.
7. **One exam at a time**, with the same template.

## 3. Evidence base (what we verified, from official documents)

| Exam | Official documents read | Topic-level mapping |
|---|---|---|
| CTET | Sept 2026 Information Bulletin (Appendix I syllabus) | Base list: 153 topic rows with stable IDs |
| KTET | Sept 2026 notification (read as page images), 2012 SCERT syllabus for Cat I-IV | Done |
| REET | REET-2024 notification, syllabus files dated 2016 (CDP, Maths, EVS, Social Studies, Level 2 Maths/Science) | Done; language syllabi not read |
| MPTET | 2026 rulebook for in-service teachers (primary chapter) | Done for primary; middle chapter and EVS list not read |
| UPTET | UPESSC syllabus PDFs (Primary, Upper Primary), supplied by the owner | Done; cutoffs and validity not in the PDFs |
| HTET | HTET-2025 Information Bulletin (structure, marks, pass marks, validity); three 2023 sample papers (one read, Q1-60) | Indicative only: no official topic list exists |

Files: `docs/syllabi/` (documents), `docs/templates/` (data and scripts), `docs/Gemini-Result-Review.md` (what the AI research got right and wrong).

### Key findings to carry into the web copy

- 90 of 150 marks in CTET Paper 1 (80 in Paper 2) are pedagogy. Source: CTET bulletin Appendix I question counts.
- The CTET bulletin states only a 60% pass mark; the "55% (82)" reserved-category figure is not in it. KTET's 60/55/50% scheme is official.
- CDP is the hardest area for 14 of 20 KTET teachers surveyed (small sample; not for public claims without approval).
- The state exams name more learning theorists than CTET does (Thorndike, Pavlov, Skinner, Kohler, Gagne, Sternberg, motivation theorists). HTET's past paper is heavy on them.
- HTET language marks are pure grammar and vocabulary in the paper we read; UPTET Language II (English/Urdu) lists content only.
- REET: wrong answers carry no penalty, but a question with no option marked loses 1/3 mark (tick option E to skip).
- MPTET 2026 is only for in-service teachers and its result is not valid for fresh recruitment.
- Survey (n=20): wanted timed mocks, explained previous-year questions, trend alerts; offline access mattered less than expected. Stated prices: medians of 600 / 1,000 / 1,500 rupees for one / two / all categories.

## 4. Web content architecture (three layers)

1. **Layer 1, hub (people read this):** "Is CTET preparation enough for your state TET?" Verdict, pedagogy-first percentages, exam-by-exam heatmap, 150-mark bars, three-step strip.
2. **Layer 2, one short page per exam:** verdict, what carries over, what to add, facts table, FAQ.
3. **Layer 3, reference tables:** full topic-by-topic tables, collapsed or on their own pages, with the counting method and "last verified" date.

Visual rules: colour and a word in every cell (accessible); percentages rounded to the nearest 5 and described as syllabus overlap, never a score prediction; plain HTML and inline SVG, no libraries; works in dark mode and on a phone.

## 5. Tracker: every web deliverable

Status: Done / Draft / Ready to start / Blocked / Not started.

| ID | Deliverable | Layer | Status | Depends on | Next action |
|---|---|---|---|---|---|
| W01 | Hub page "Is CTET enough for your state TET?" | 1 | Draft v4 (`site-drafts/compare-all-tets.html`) | Spot-check; app coverage counts | Review wording; verify HTET data; fill app coverage placeholders |
| W02 | CTET vs KTET detail page | 3 | Draft v1 (`site-drafts/ctet-vs-ktet.html`) | Spot-check; KTET certificate validity | Shorten into a Layer 2 page; keep tables as reference |
| W03 | CTET vs UPTET page | 2 | Ready to start | Data ready | Write verdict, add-ons (grammar, UP content), FAQ |
| W04 | CTET vs REET page | 2 | Ready to start | REET language syllabi not read | Write; mark languages "not compared yet"; include the blank-answer rule |
| W05 | CTET vs MPTET page (in-service test) | 2 | Ready to start | Middle chapter not read | Write with clear "in-service only" notice |
| W06 | CTET vs HTET page | 2 | Blocked | Official topic list absent; Level 1 paper | Use "indicative" labels, or read more sample papers first |
| W07 | KTET Category 3 and 4 page (adolescent psychology, subject content) | 2 | Not started | Content plan for EasyKTET | Separate message; no CTET-overlap claim |
| W08 | Hindi and Hinglish hub ("UPTET aur CTET ke syllabus me kya antar hai") | 1 | Not started | English hub approved | Translate with a native reviewer |
| W09 | "Which is tougher, CTET or UPTET?" page | 2 | Not started | Evidence per section | Base on grammar load and CDP depth findings |
| W10 | "10 days to prepare for CTET Paper 1" plan | 2 | Not started | Official weightage (done) | Draft day-by-day plan |
| W11 | "Where to find previous-year papers" page | 2 | Not started | Board terms on reuse | Link to official archives; add own explanations for a few questions |
| W12 | TET family overview ("what other exams can I give") | 2 | Not started | Only verified exams | List verified exams; link to hub |
| W13 | One-page comparison PDF (download) | 3 | Not started | W01 approved | Generate from the data, with a branded footer |
| W14 | CDP "named theorists" cheat sheet (PDF) | 3 | Not started | Theorist list verified | Build from the official lists |
| W15 | Readiness checker (5-question web quiz) | 2 | Not started | Tagged question bank; free sample | Build after tagging |
| W16 | Shareable exam cards for WhatsApp/Telegram | 3 | Not started | W01 approved | One image per exam; no tracking |
| W17 | FAQ blocks and structured data on all pages | 2 | Not started | Pages exist | Use the exact question wording from searches |
| W18 | Play Store listing aligned with search wording | - | Not started | W01 | Titles and short description with CTET/UPTET/REET mock-test phrasing |
| W19 | Search Console, privacy-friendly analytics, tagged links | - | Not started | Site access | Set up before launch to get a baseline |
| W20 | Community answers (Quora, Reddit, forums) | - | Not started | W01-W05 live | Disclosed, helpful answers; a few per week |
| W21 | Forum-title collector for keyword ideas (`tools/collect_forum_titles.py`) | - | Script ready, not run | Site terms and robots.txt checked; selectors filled in | Prefer an official API or manual collection; run only where allowed; confirm demand in Search Console |
| W22 | Manual question research (Quora, Google, Bing) merged with `tools/merge_titles.py` into `research/aspirant_questions_merged.csv` | - | In progress: CTET search merged (125 titles); other exams and pairs still to collect | Browser console copy or manual paste per search | Run the seed searches for uptet, reet, htet, ktet, mptet, bihar stet, super tet, state tet and the pairs; paste under `SEARCH: <query>` |
| W23 | Volume pages from keyword research: CTET previous-year questions explained by topic (links to the official papers), mock tests by paper and subject, regional-language paper pages | 2 | Idea (from the 885-phrase Google suggestion list) | Board terms on papers; tagged question bank; keyword volumes from Keyword Planner | Confirm volumes, then pick 3 pages; avoid competitor brand names in titles |

### 5A. Content readiness board (update at every change)

Readiness levels: **R0** not started · **R1** official sources read · **R2** facts verified and topics mapped, not spot-checked · **R3** spot-checked and approved · **R4** page drafted from that data · **R5** published and monitored.
A page cannot go live until every exam it mentions is at R3 or higher.

| Exam | Official sources | Facts table (marks, pass marks, validity) | Topic mapping | Spot-check | Page draft | Open gaps | Readiness |
|---|---|---|---|---|---|---|---|
| CTET | Sept 2026 bulletin | Verified (60% pass mark; lifetime validity) | Base list, 153 rows | Not done | In hub | Reserved-category cutoff not in the bulletin (do not publish 82 marks) | **R2** |
| KTET | Sept 2026 notification, 2012 syllabus | Verified; certificate validity not seen | Cat 1-2 mapped; Cat 3-4 skimmed | Not done | W02 draft | Certificate validity; Cat 2 science and social rows; the 2012 syllabus may have been revised | **R2 / R4 draft** |
| UPTET | UPESSC syllabus PDFs (user-supplied) | Structure verified; pass marks and validity not in the PDFs | Mapped | Not done | Not started | Official notification for cutoffs, validity, dates | **R2** |
| REET | 2024 notification; syllabus files dated 2016 | Verified (pattern, pass marks, blank-answer rule, validity) | Mapped without languages | Not done | Not started | Language syllabi not read; confirm 2016 files are still current | **R2** |
| MPTET | 2026 rulebook (in-service test) | Verified for the primary exam | Primary mapped | Not done | Not started | EVS list and middle-level chapter not read; validity not stated | **R2** |
| HTET | 2025 bulletin; one 2023 sample paper read | Structure and pass marks verified | Indicative only (no official topic list) | Not done | In hub (indicative) | Level 1 paper; General Studies section; Social Studies and Science papers unread | **R1 / R2 indicative** |
| Bihar STET | Not read | - | Excluded (secondary level) | - | - | - | n/a |

| Cross-cutting item | Status |
|---|---|
| Spot-check of the mapping | **Not done** (the main gate for publishing) |
| App coverage counts per topic (question bank tagged) | **Not done** |
| Free-sample policy decided | **Open** |
| Hindi / Hinglish copy and native review | **Not started** |
| Search Console, analytics and tagged links | **Not set up** |
| Survey citation approval | **Open** |

Current publishable pages: **none yet** (hub and CTET vs KTET are drafts at R4; the spot-check and app counts are the blockers).

## 6. Query-to-page map

| Searcher's question (examples) | Page |
|---|---|
| CTET vs UPTET / REET / HTET syllabus, overlap, difference | W01, W03-W06 |
| Is CTET preparation enough for REET Level 1? | W04 (exact question as the heading) |
| UPTET aur CTET ke syllabus me kya antar hai | W08 |
| Which is tougher, CTET or UPTET? | W09 |
| Previous-year papers for CTET, REET, UPTET | W11 |
| 10 days preparation strategy for CTET Paper 1 | W10 |
| Best free app for pedagogy mock tests | W15 and a pedagogy practice page with free samples |
| What other government exams can I give (UPTET, HTET, KVS, NVS) | W12 |
| CTET vs UPTET syllabus 2026 PDF download | W13 |

## 7. On-page SEO checklist (every page)

- Heading uses the searcher's wording; the answer is in the first two lines (about 50 words).
- Title and description include the exam names and 2026.
- FAQ block with the real questions; structured data only where the content is accurate.
- "Last verified" date and links to the official documents used.
- Internal links: hub, exam pages, reference tables.
- Hindi and Hinglish versions for the top pages.
- Static, fast pages; mobile layout checked.

## 8. Conversion plan (gentle and open)

1. **Soft call to action beside the answer**, one line: "Practise this offline in the app, no sign-up."
2. **Readiness checker (W15):** a few CDP questions in the browser, a short result ("weak spot: motivation theorists"), then a clear next step into the app.
3. **Topic-level links:** each topic row can link to practice for that topic (needs the question bank tagged by topic ID).
4. **Useful downloads (W13, W14)** with a branded footer that says who made them.
5. **Honest price wording:** the app is a paid ₹950 pass; offer free sample questions and say exactly how many.
6. **Play Store alignment (W18)** so search wording and the listing match.
7. **Messaging priorities** (from the survey and the exam analysis): explained answers (why each option is right or wrong, especially in child psychology), timed 150-question mocks, trend alerts for previous-year questions, a mistake ledger. Offline is a supporting benefit, not the lead.

## 9. Community plan (Quora, Reddit, forums)

- Answer real questions with the data from our pages, then link to the page for details.
- Always disclose: "I'm the developer of EasyCTET."
- Follow each community's self-promotion rules; a few answers a week, not bursts.
- No fake accounts or reviews; no competitor names or unverified claims about them.
- Keep a log of answers posted (date, platform, link) in this document or a sheet.

## 10. Data pipeline and files

| File | Purpose |
|---|---|
| `docs/templates/master-topics.csv` | 176 topic rows; columns for CTET, KTET (4 categories), UPTET, REET (2 levels), HTET, MPTET; confidence and verification flags |
| `docs/templates/exam-facts.csv` | Official facts per exam and paper, with status |
| `docs/templates/sources.csv` | Every document used: URL, date, official or not, local file |
| `docs/templates/coverage-by-topic.csv`, `question-bank-tags.csv`, `queries.csv`, `legend.md` | Templates for tagging the question bank and tracking queries |
| `docs/templates/build_ctet_topics.py`, `map_ktet.py`, `map_reet.py`, `map_mptet.py`, `map_uptet.py`, `map_htet.py` | Rebuild the master list in this order |
| `docs/templates/build_page_hub.py`, `build_page_ctet_ktet.py` | Generate the draft pages from the data |
| `docs/site-drafts/` | Draft HTML pages |
| `docs/syllabi/` | Downloaded official documents and text extracts |

## 11. Quality gates (before any page goes live)

1. Spot-check about 10% of mapped rows against the official PDFs, concentrating on the KTET Category 2 science and social studies rows and the REET and UPTET "Similar" ratings.
2. Re-run the scripts and review the hub numbers.
3. Remove all draft markers and [EDITOR] notes; fill in the real app coverage counts.
4. Confirm unverified items are off the page: HTET topic lists, UPTET pass marks and validity, KTET certificate validity.
5. Check each board's terms before showing any question paper content.
6. Read the page on a phone and in dark mode; confirm nothing relies on colour alone.
7. Log the verification date on the page and in `sources.csv`.

## 12. Measurement

- Search Console: queries, impressions and clicks by page, per week.
- Tagged links: installs and trial-to-purchase by page and button.
- Community answers: clicks and installs per answer.
- Accuracy: any reader correction recorded and fixed within one week.
- Review monthly; add a state only when its search data and installs justify it.

## 13. Timeline

| Weeks | Milestones |
|---|---|
| Done | Research, official documents, master topic list, five exam mappings, hub draft v4, CTET vs KTET draft |
| 1 | Spot-check; set up Search Console and tagged links (W19); review hub wording |
| 2-3 | Question bank tagged by topic; app coverage counts; finish W01; shorten W02 |
| 3-5 | W03, W04, W05 (UPTET, REET, MPTET pages); W17 FAQ blocks; W18 Play Store wording |
| 5-7 | W09, W10, W11, W13 (difficulty, 10-day plan, past papers, PDF) |
| 6-8 | W08 Hindi/Hinglish hub; W16 share cards |
| 7-10 | W15 readiness checker; W07 KTET Category 3/4 page |
| Ongoing | W20 community answers; monthly review |

## 14. Risks

| Risk | Mitigation |
|---|---|
| A wrong overlap claim damages trust | Official sources only; spot-check; dated verification; "indicative" labels where evidence is thin |
| Percentages read as a score promise | Rounded, labelled syllabus overlap, explicit "not a score prediction" |
| HTET and REET language data incomplete | Mark "not compared yet"; read more documents before showing numbers |
| Syllabi and rules change | Monthly review; "last verified" dates; change log |
| Copyright on question papers | Link to official archives; check terms; write our own explanations |
| Promotion seen as spam | Disclose the developer role; lead with useful answers; follow community rules |
| Too much work for one person | Build in the order above; reuse one template; CTET/KTET first |
| Survey is small (n=20) | Use internally; never present as a general statistic |

## 15. Open decisions

1. Cite the survey publicly (for example "14 of 20 teachers we surveyed")? Needs approval.
2. Can the app offer a free sample (how many questions per exam)? Needed for W15 and the pricing wording.
3. English first or Hindi/Hinglish first for the next pages?
4. Disclose the developer in forum answers (recommended)?
5. Pilot exam for the first full exam page: UPTET (data complete) or REET (rule explainer)?
6. Should KTET Category 3 get its own message and content plan in EasyKTET?
7. Keep or remove the HTET percentages until a Level 1 paper or an official topic list is found?

## 16. Change log

| Date | Change |
|---|---|
| 2026-10-01 | Plan v1 created (Phases 0-7, templates for topics, facts, sources, queries). |
| 2026-10-01 | Official documents read for CTET, KTET, REET, MPTET, UPTET (user-supplied), HTET; master topic list built (153 CTET rows plus exam-only rows); exam facts and sources recorded. |
| 2026-10-01 | Gemini research reviewed; errors found (CTET reserved cutoff, UPTET pedagogy claim, MPTET "Varg" framing, unverified HTET topics); notes in `Gemini-Result-Review.md`. |
| 2026-10-01 | CTET vs KTET draft page built (`site-drafts/ctet-vs-ktet.html`). |
| 2026-10-01 | Hub page drafted and revised to v4: pedagogy-first percentages, heatmap with cell percentages, 150-mark bars, KTET Category 3/4 box (`site-drafts/compare-all-tets.html`). |
| 2026-10-01 | HTET evidence added from the board's Level 2 sample paper (CDP theorist depth; languages are pure grammar); hub HTET rows filled and marked indicative. |
| 2026-10-01 | Plan v2: web deliverable tracker (W01-W20), query map, conversion and community plans, readiness board added. |
| 2026-10-01 | Added `tools/collect_forum_titles.py` (config-driven, robots.txt check, honest user agent, stops on CAPTCHA, self-test passes); not run against any site. |
| 2026-10-01 | Quora CTET search captured (125 unique question titles) and merged with `tools/merge_titles.py`; 24 unanswered; 16 multi-exam questions. |
| 2026-10-02 | Google suggestion list for 'ctet' saved (885 phrases, `research/google_suggestions_ctet_2026-10-02.txt`): 45% previous-year papers, 16% mock tests, 11% competitor brands, 0 comparison phrases with state exams, 1 pedagogy phrase, no phrase dated after 2023. |

When a status changes, update the tracker (section 5), the readiness board (5A) and add a dated line here.

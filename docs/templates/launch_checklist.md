# Pre-Flight & Launch Checklist for High SERP Placement
## EasyCTET / EasyKTET Organic Search Distribution Standard
**Parent Document:** [Master_Project_Plan_Execution_Roadmap.md](file:///c:/Users/Admin/Summs/EasyCTET-Branding/docs/Master_Project_Plan_Execution_Roadmap.md)  
**Target Domain:** `https://easyctet.com`  
**Standard:** 100/100 Core Web Vitals, Radical Truth, Zero-JS Bloat  

---

### Phase A: Pre-Flight Static Quality & Link Audit
- [ ] **1. Automated Link & Marker Verification:**
  - Execute `python docs/tools/check_publish_ready.py`.
  - Verify every release page returns **`PUBLISHABLE`** (Zero `[EDITOR]`, `TODO`, `TBC` markers; zero broken `#anchor` fragments).
  - Verify all linked targets in [pages.csv](file:///c:/Users/Admin/Summs/EasyCTET-Branding/docs/templates/pages.csv) have status `READY` or `PUBLISHED`.
- [ ] **2. Core Web Vitals & Performance Benchmark:**
  - Run Google Lighthouse Audit on mobile simulation.
  - Performance: `100/100` (First Contentful Paint < 0.8s, Largest Contentful Paint < 1.2s, Cumulative Layout Shift = 0.000).
  - Page payload strictly under 35 KB (pure semantic HTML and inline CSS; zero external JavaScript frameworks).
- [ ] **3. Structured Data Validation (Schema.org):**
  - Validate embedded JSON-LD graphs via [Google Rich Results Test](https://search.google.com/test/rich-results).
  - Confirm valid syntax for `@type: Article`, `@type: BreadcrumbList`, and `@type: FAQPage`.
- [ ] **4. Canonical URL & Meta Tag Hygiene:**
  - Confirm `<link rel="canonical">` matches the exact intended production route.
  - Verify `<meta name="description">` contains high-intent target keywords without keyword stuffing.
  - Verify OpenGraph (`og:title`, `og:description`, `og:url`) for dark social link previews.

---

### Phase B: Production Deployment & Technical Indexing
- [ ] **5. Domain & Host Deployment:**
  - Deploy verified HTML cluster to production hosting (`easyctet.com`).
  - Verify automated HTTPS redirection and valid SSL certificate.
  - Confirm `robots.txt` permits crawling (`User-agent: *`, `Allow: /`).
- [ ] **6. Sitemap Generation & Search Console Submission:**
  - Generate clean `sitemap.xml` containing only canonical URLs with ISO 8601 `<lastmod>` timestamps.
  - Submit `https://easyctet.com/sitemap.xml` directly to Google Search Console.
- [ ] **7. Accelerated Indexing Trigger (URL Inspection):**
  - Open Google Search Console -> **URL Inspection**.
  - Enter `https://easyctet.com/ctet/passing-marks/` (and all cluster URLs).
  - Click **"Test Live URL"** $\rightarrow$ **"Request Indexing"** to place the page in Google's high-priority crawl queue.
- [ ] **8. App Store Link Activation:**
  - Confirm Google Play Store URL is live and resolves properly with UTM campaign tracking (`referrer=utm_source%3Dweb%26utm_medium%3Dseo%26utm_campaign%3D...`).

---

### Phase C: Dark Social Seeding & RankBrain Engagement Flywheel
- [ ] **9. High-Value Community Seeding (WhatsApp & Telegram):**
  - Share the direct table/guide in 5–10 active teacher preparation groups with group admin knowledge.
  - Focus strictly on helpful answering of existing candidate queries (e.g. *"Can outside OBC candidates apply for Delhi DSSSB?"*).
- [ ] **10. Algorithmic Video Reinforcement:**
  - Release corresponding calm pedagogical YouTube Short on `@easyctetofficial`.
  - Pin comment directing aspirants to the comprehensive, unhurried comparison table on the website.
- [ ] **11. Post-Launch Search Console Monitoring (Week 1–2):**
  - Track **Total Impressions** and **Average Position** for long-tail query clusters in GSC Performance reports.
  - Monitor click-through rate (CTR) to refine title tags if impressions are high but clicks are lagging.

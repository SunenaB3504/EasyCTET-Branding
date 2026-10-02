"""Builds the DRAFT easyctet.com page 'CTET vs KTET syllabus comparison' from master-topics.csv.
Output: ../site-drafts/ctet-vs-ktet.html   (static HTML, no external assets)
Counts use the rule: share of CTET topic rows (for that paper) that appear in the KTET category as Same or Similar.
"""
import csv, html, os
from collections import OrderedDict

S, SIM, NF, DIFF = "Same", "Similar", "Not found", "Different"
rows = list(csv.DictReader(open("master-topics.csv", encoding="utf-8")))

FAMILIES = OrderedDict([
    ("Child Development and Pedagogy", lambda s: s.startswith("Child Development")),
    ("Language I", lambda s: s.startswith("Language I") and not s.startswith("Language II")),
    ("Language II", lambda s: s.startswith("Language II")),
    ("Mathematics", lambda s: s.startswith("Mathematics")),
    ("Environmental Studies", lambda s: s.startswith("Environmental")),
    ("Science", lambda s: s.startswith("Science")),
    ("Social Studies", lambda s: s.startswith("Social Studies")),
])


def family(subject):
    for name, fn in FAMILIES.items():
        if fn(subject):
            return name
    return None


def pair(ctet_col, ktet_col):
    base = [r for r in rows if r[ctet_col] and family(r["subject"])]
    by = OrderedDict((f, {"n": 0, S: 0, SIM: 0, NF: 0, DIFF: 0}) for f in FAMILIES)
    for r in base:
        d = by[family(r["subject"])]
        d["n"] += 1
        v = r[ktet_col] or NF
        d[v if v in (S, SIM, DIFF) else NF] += 1
    by = OrderedDict((k, v) for k, v in by.items() if v["n"])
    n = len(base)
    same = sum(v[S] for v in by.values())
    sim = sum(v[SIM] for v in by.values())
    return base, by, n, same, sim


def summary_table(by):
    h = "<table><thead><tr><th>Subject area</th><th>CTET topics</th><th>Same in KTET</th><th>Similar</th><th>Not in KTET</th></tr></thead><tbody>"
    for f, v in by.items():
        h += f"<tr><td>{html.escape(f)}</td><td>{v['n']}</td><td>{v[S]}</td><td>{v[SIM]}</td><td>{v[NF] + v[DIFF]}</td></tr>"
    return h + "</tbody></table>"


def detail_table(base, ktet_col):
    h = "<table><thead><tr><th>Topic</th><th>Area</th><th>In KTET?</th></tr></thead><tbody>"
    for r in base:
        v = r[ktet_col] or NF
        cls = {"Same": "same", "Similar": "sim"}.get(v, "none")
        label = {"Same": "Same", "Similar": "Similar", "Different": "Different level"}.get(v, "Not found")
        h += (f"<tr><td>{html.escape(r['topic'])}</td><td>{html.escape(family(r['subject']) or '')}</td>"
              f"<td class='{cls}'>{label}</td></tr>")
    return h + "</tbody></table>"


b1, by1, n1, s1, m1 = pair("ctet_p1", "ktet_c1")
b2, by2, n2, s2, m2 = pair("ctet_p2", "ktet_c2")
pct = lambda a, b: round(100 * a / b)

ktet_only = [r for r in rows if r["topic_id"].startswith("KTET-") and r["ktet_c1"] in (S, SIM) or
             r["topic_id"].startswith("KTET-") and r["ktet_c2"] in (S, SIM)]

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>CTET vs KTET Syllabus Comparison (2026): What Overlaps</title>
<meta name="description" content="Topic-by-topic comparison of the CTET and KTET syllabi, built from the official CBSE and Kerala Pareeksha Bhavan documents. Last verified 1 October 2026.">
<style>
:root{{--bg:#fff;--fg:#1c1c1e;--mut:#5b6068;--line:#dde1e6;--ok:#e6f4ea;--sim:#fff6d9;--no:#f3f4f6;--acc:#0b57d0}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#ececee;--mut:#a3a8b0;--line:#363a41;--ok:#16301f;--sim:#3a3217;--no:#23262b;--acc:#8ab4f8}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:860px;margin:0 auto;padding:24px 16px 64px}}
h1{{font-size:1.7rem;line-height:1.25}} h2{{margin-top:2.2rem;font-size:1.25rem}}
table{{border-collapse:collapse;width:100%;font-size:.93rem;margin:12px 0}}
th,td{{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}}
th{{background:var(--no)}} td.same{{background:var(--ok)}} td.sim{{background:var(--sim)}} td.none{{background:var(--no);color:var(--mut)}}
.box{{border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:var(--no)}}
.note{{color:var(--mut);font-size:.9rem}} a{{color:var(--acc)}}
.draft{{border:2px dashed #c0392b;border-radius:8px;padding:10px 14px;margin-bottom:20px;font-size:.9rem}}
details{{margin:12px 0}} summary{{cursor:pointer;font-weight:600}}
.scroll{{overflow-x:auto}}
</style></head><body><main>

<div class="draft"><strong>DRAFT, not for publishing.</strong> Overlap labels are a first-pass judgement from the official syllabi and have not been spot-checked. Remove this box and the bracketed [EDITOR] notes before publishing.</div>

<h1>CTET vs KTET Syllabus Comparison (2026)</h1>
<p class="note">Last verified: 1 October 2026 · Sources: CBSE CTET Information Bulletin (September 2026), Kerala K-TET Notification (September 2026) and the official K-TET syllabus documents.</p>

<div class="box">
<strong>Short answer.</strong> About <strong>{pct(s1+m1, n1)}%</strong> of the topics in CTET Paper 1 also appear in KTET Category 1 ({n1} CTET topics compared: {s1} the same, {m1} similar).
For CTET Paper 2 and KTET Category 2 it is about <strong>{pct(s2+m2, n2)}%</strong> ({n2} topics: {s2} the same, {m2} similar; the count covers the maths, science and social studies streams together, and a candidate takes only one stream).
KTET Categories 3 and 4 are a different kind of exam and overlap very little.
</div>

<h2>How we counted</h2>
<p>We listed every topic in the official CTET syllabus for each paper, then checked whether the KTET category's official syllabus covers it. A topic counts as <em>Same</em> if the syllabus wording and scope match, and <em>Similar</em> if the topic appears with a different focus or depth. The percentage above is (Same + Similar) divided by the number of CTET topics for that paper. It tells you how much of the CTET syllabus also helps for KTET, not the other way round. [EDITOR: confirm the numbers again after the spot-check.]</p>

<h2>Exam facts side by side</h2>
<div class="scroll"><table>
<thead><tr><th></th><th>CTET</th><th>KTET</th></tr></thead><tbody>
<tr><td>Conducted by</td><td>CBSE</td><td>Kerala Pareeksha Bhavan</td></tr>
<tr><td>Papers / categories</td><td>Paper 1 (classes 1–5), Paper 2 (classes 6–8)</td><td>Category 1 (classes 1–5), 2 (classes 6–8), 3 (high school), 4 (language and specialist teachers)</td></tr>
<tr><td>Questions and marks</td><td>150 MCQs, 150 marks</td><td>150 MCQs, 150 marks</td></tr>
<tr><td>Duration</td><td>2½ hours</td><td>2½ hours</td></tr>
<tr><td>Negative marking</td><td>No</td><td>No</td></tr>
<tr><td>Paper language</td><td>Bilingual Hindi/English; Language I and II chosen from a list</td><td>Malayalam, English, Kannada, Tamil (Category 3 in English only, except language subjects)</td></tr>
<tr><td>Pass mark</td><td>60% (90 marks). The bulletin leaves any concession for reserved categories to each school's policy.</td><td>General 60% (90); SC/ST/OBC/OEC 55% (82); persons with disabilities 50% (75), as stated in the notification</td></tr>
<tr><td>Certificate validity</td><td>Lifetime</td><td>[EDITOR: not confirmed on the notification pages we read. Check before stating.]</td></tr>
<tr><td>Next exam</td><td>See the CTET website for the current schedule</td><td>14–15 November 2026 (September 2026 notification)</td></tr>
</tbody></table></div>
<p class="note">Eligibility rules differ by exam and change over time. Always read the official bulletin before applying.</p>

<h2>Paper 1 and KTET Category 1 (classes 1–5)</h2>
{summary_table(by1)}
<details><summary>Show all {n1} topics</summary><div class="scroll">{detail_table(b1, "ktet_c1")}</div></details>

<h2>Paper 2 and KTET Category 2 (classes 6–8)</h2>
{summary_table(by2)}
<details><summary>Show all {n2} topics</summary><div class="scroll">{detail_table(b2, "ktet_c2")}</div></details>

<h2>What is in KTET but not in CTET</h2>
<ul>
<li>Kerala-specific content, including Kerala history, geography and economy in the Category 2 social science paper.</li>
<li>Economics as a topic in Category 2 social science (growth, five-year plans, money and banking, globalisation).</li>
<li>Learning theories and personality in more detail than CTET lists, and methods of studying child behaviour.</li>
<li>Mother-tongue papers in Malayalam, Tamil or Kannada, with Kerala literature and culture.</li>
<li>Category 3: adolescent psychology, learning theories and teaching aptitude (40 marks) plus 80 marks of subject content for classes 8–10.</li>
<li>Category 4: specialist and language-teacher content, including physical education and arts.</li>
</ul>

<h2>Which should you prepare for?</h2>
<ul>
<li><strong>Aiming for primary classes (1–5):</strong> CTET Paper 1 and KTET Category 1 share most of the child development and pedagogy material, so one study plan covers both. Add the Kerala-specific parts for KTET.</li>
<li><strong>Aiming for classes 6–8:</strong> CTET Paper 2 and KTET Category 2 overlap well in pedagogy and in maths and science content; the social science sections overlap only in part.</li>
<li><strong>High school or specialist teachers:</strong> KTET Categories 3 and 4 need subject-level study that CTET does not cover.</li>
</ul>

<h2>Practise offline</h2>
<p>[EDITOR: add the honest app description here once the question bank is tagged by topic, for example "EasyCTET covers X of these topics with Y questions". Link to the Play Store with a tagged URL.]</p>

<h2>Frequently asked questions</h2>
<details><summary>Is the CTET syllabus enough for KTET?</summary><p>Only partly. The child development, pedagogy and language-pedagogy sections overlap well, but KTET adds Kerala-specific content, a mother-tongue paper, and in some categories subject content that CTET does not test. Use the tables above to see exactly what is missing.</p></details>
<details><summary>Do both exams have negative marking?</summary><p>No. Both state that there is no negative marking.</p></details>
<details><summary>What is the pass mark?</summary><p>CTET: 60% (90 of 150). KTET: 60% for General, 55% for SC/ST/OBC/OEC and 50% for persons with disabilities, per the September 2026 notification. [EDITOR: re-check before each exam cycle.]</p></details>

<h2>Sources</h2>
<ul class="note">
<li>CBSE, CTET September 2026 Information Bulletin (ctet.nic.in), Appendix I.</li>
<li>Kerala Pareeksha Bhavan, K-TET September 2026 Notification and the Category I–IV syllabus documents (ktet.kerala.gov.in; syllabus files dated 2012 on the site).</li>
</ul>
<p class="note">This comparison is an independent study aid. It is not issued by CBSE or the Kerala Pareeksha Bhavan.</p>
</main></body></html>"""

os.makedirs("../site-drafts", exist_ok=True)
open("../site-drafts/ctet-vs-ktet.html", "w", encoding="utf-8").write(page)
print(f"P1 vs Cat1: n={n1} same={s1} similar={m1} -> {pct(s1+m1,n1)}%")
print(f"P2 vs Cat2: n={n2} same={s2} similar={m2} -> {pct(s2+m2,n2)}%")

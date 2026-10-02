"""Builds the DRAFT hub page 'Can CTET preparation help for state TETs?' (layer 1) from master-topics.csv.
Output: ../site-drafts/compare-all-tets.html.  Labels (not percentages) are derived per exam from the mapped columns."""
import csv, html, os

S, SIM = "Same", "Similar"
rows = list(csv.DictReader(open("master-topics.csv", encoding="utf-8")))
LANG_ROW = lambda r: r["topic_id"].startswith("LANG-")
core = [r for r in rows if not r["topic_id"].startswith(("KTET-", "REET-", "MPTET-", "UPTET-", "HTET-"))]


def share(paper_col, exam_col):
    base = [r for r in core if r[paper_col]]
    assessed = [r for r in base if r[exam_col]]
    if not assessed:
        return None, 0, 0
    ok = sum(1 for r in assessed if r[exam_col] in (S, SIM))
    return ok / len(assessed), len(assessed), len(base)


def label(x):
    if x is None:
        return "Structure only"
    return "Very high" if x >= .85 else "High" if x >= .65 else "Partial" if x >= .40 else "Low"


exams = [
    ("KTET", "ktet_c1", "ktet_c2", "KTET Cat 1 / Cat 2"),
    ("UPTET", "uptet", "uptet", "UPTET Paper 1 / 2"),
    ("REET", "reet_l1", "reet_l2", "REET Level 1 / 2"),
    ("MPTET", "mptet", None, "MPTET primary (in-service)"),
    ("HTET", "htet", None, "HTET Level 1 / 2"),
]
lab = {}
for name, c1, c2, _ in exams:
    p1 = share("ctet_p1", c1)[0] if c1 else None
    p2 = share("ctet_p2", c2)[0] if c2 else None
    lab[name] = (label(p1), label(p2) if c2 else ("n/a" if name == "MPTET" else "Structure only"))
    print(name, lab[name], [round(v, 2) if v is not None else None for v in (p1, p2)])


# ---------- section-level statuses (drive the bars and the heatmap) ----------
COV, LIK, PAR, ADD, UNK = "Covered", "Likely", "Partly", "Add-on", "Not compared"
FAM = {"cdp": ["Child Development and Pedagogy"], "l1": ["Language I"], "l2": ["Language II"], "math": ["Mathematics"],
       "evs": ["Environmental Studies"], "msci": ["Mathematics", "Science"]}


def fam_of(subject):
    for key, names in (("Child Development and Pedagogy", "Child Development"), ("Language II", "Language II"),
                       ("Language I", "Language I"), ("Mathematics", "Mathematics"),
                       ("Environmental Studies", "Environmental"), ("Science", "Science"), ("Social Studies", "Social Studies")):
        if subject.startswith(names):
            return key
    return None


def computed(col, pflag, key):
    x, _ = sec_pct(col, pflag, key)
    if x is None:
        return UNK
    return COV if x >= .80 else PAR if x >= .55 else ADD


P1 = [("cdp", "Child dev. & pedagogy", 30), ("l1", "Language I", 30), ("l2", "Language II", 30), ("math", "Maths", 30), ("evs", "EVS", 30)]
P2 = [("cdp", "Child dev. & pedagogy", 30), ("l1", "Language I", 30), ("l2", "Language II", 30), ("msci", "Maths + Science (or Social Studies)", 60)]
HT1 = [("cdp", "Child dev. & pedagogy", 30), ("l1", "Languages (Hindi 15, English 15)", 30), ("gs", "General Studies", 30), ("math", "Maths", 30), ("evs", "EVS", 30)]
HT2 = [("cdp", "Child dev. & pedagogy", 30), ("l1", "Languages (Hindi 15, English 15)", 30), ("gs", "General Studies", 30), ("sub", "Subject-specific", 60)]

K1, K2 = "KTET Cat 1 (classes 1-5)", "KTET Cat 2 (classes 6-8)"
U1, U2 = "UPTET Paper 1 (classes 1-5)", "UPTET Paper 2 (classes 6-8)"
R1, R2 = "REET Level 1 (classes 1-5)", "REET Level 2 (classes 6-8)"
M1 = "MPTET primary (in-service)"
H1, H2 = "HTET Level 1 (classes 1-5)", "HTET Level 2 (classes 6-8)"
PAPERS = [
    ("KTET", K1, P1, "ktet_c1", "ctet_p1"), ("KTET", K2, P2, "ktet_c2", "ctet_p2"),
    ("UPTET", U1, P1, "uptet", "ctet_p1"), ("UPTET", U2, P2, "uptet", "ctet_p2"),
    ("REET", R1, P1, "reet_l1", "ctet_p1"), ("REET", R2, P2, "reet_l2", "ctet_p2"),
    ("MPTET", M1, P1, "mptet", "ctet_p1"),
    ("HTET", H1, HT1, "htet", "ctet_p1"), ("HTET", H2, HT2, "htet", "ctet_p2"),
]
OVR = {
    (K1, "l1"): (PAR, "mother-tongue literature"), (K2, "l1"): (PAR, "mother-tongue literature"),
    (K2, "msci"): (PAR, "science content broader"),
    (U1, "l1"): (PAR, "heavy Hindi grammar"), (U2, "l1"): (PAR, "heavy Hindi grammar"),
    (U1, "l2"): (ADD, "grammar-based"), (U2, "l2"): (ADD, "grammar-based"),
    (R1, "l1"): (UNK, "languages not compared yet"), (R1, "l2"): (UNK, "languages not compared yet"),
    (R2, "l1"): (UNK, "languages not compared yet"), (R2, "l2"): (UNK, "languages not compared yet"),
    (R1, "evs"): (PAR, "Rajasthan content"), (R2, "msci"): (PAR, "broader science, Rajasthan social studies"),
    (M1, "evs"): (UNK, "rulebook incomplete"),
    (H1, "cdp"): (PAR, "named-theorist depth"), (H1, "math"): (LIK, "NCERT-based, no topic list"),
    (H1, "evs"): (LIK, "NCERT-based, no topic list"), (H1, "l1"): (ADD, "grammar and vocabulary"),
    (H1, "gs"): (ADD, "aptitude, reasoning, Haryana GK"),
    (H2, "cdp"): (PAR, "named-theorist depth"), (H2, "l1"): (ADD, "grammar and vocabulary"),
    (H2, "gs"): (ADD, "aptitude, reasoning, Haryana GK"), (H2, "sub"): (UNK, "no topic list"),
}
CSS_CLASS = {COV: "s-cov", LIK: "s-lik", PAR: "s-par", ADD: "s-add", UNK: "s-unk"}


def sec_status(label, key, col, pflag):
    if (label, key) in OVR:
        return OVR[(label, key)]
    if col:
        return computed(col, pflag, key), ""
    return UNK, ""


def bar(label, secs, col, pflag):
    h = f'<div class="bar-title">{html.escape(label)} <span class="note">150 marks</span></div><div class="bar">'
    for key, name, marks in secs:
        st, note = sec_status(label, key, col, pflag)
        extra = (" · " + html.escape(note)) if note else ""
        h += (f'<div class="blk {CSS_CLASS[st]}" style="flex:{marks} 1 {marks * 3}px" title="{html.escape(name)}: {st}">'
              f'<b>{html.escape(name)}</b><span>{marks} marks</span><em>{st}{extra}</em></div>')
    return h + "</div>" + marks_line(label, secs, col, pflag)


def heatmap():
    cols = [("cdp", "Child dev."), ("l1", "Language I"), ("l2", "Language II"), ("math", "Maths"),
            ("last", "EVS / Science / Social"), ("gs", "Extra")]
    h = "<div class='scroll'><table class='heat'><thead><tr><th>Exam paper</th>" + "".join(f"<th>{c[1]}</th>" for c in cols) + "</tr></thead><tbody>"
    for exam, label, secs, col, pflag in PAPERS:
        keys = {k for k, n, m in secs}
        h += f"<tr><th>{html.escape(label)}</th>"
        for ck, _ in cols:
            if ck == "last":
                k2 = "evs" if "evs" in keys else "msci" if "msci" in keys else "sub" if "sub" in keys else None
            else:
                k2 = ck if ck in keys else None
            if not k2:
                h += "<td class='s-none'>&ndash;</td>"
                continue
            st, note = sec_status(label, k2, col, pflag)
            pc = sec_pct(col, pflag, k2) if col else (None, False)
            sub = (f"<small>{pct_txt(pc)}</small>" if pc[0] is not None and (label, k2) not in OVR else '')
            h += f"<td class='{CSS_CLASS[st]}' title='{html.escape(note)}'>{st}{sub}</td>"
        h += "</tr>"
    return h + "</tbody></table></div>"


def legend():
    items = [(COV, "Covered: CTET practice matches"), (LIK, "Likely: board describes it like CTET, no topic list"),
             (PAR, "Partly: add a little"), (ADD, "Add-on needed"), (UNK, "Not compared yet")]
    return '<div class="legend">' + "".join(f'<span><i class="{CSS_CLASS[k]}"></i>{html.escape(t)}</span>' for k, t in items) + "</div>"



# ---------- v4: percentages (topic-based, Same = 1, Similar = 0.5, rounded to nearest 5) ----------
def is_cdp(r):
    return "CDP-" in r["topic_id"]


def is_ped(r):
    return is_cdp(r) or "-PED-" in r["topic_id"]


extras_all = [r for r in rows if r["topic_id"].startswith(("KTET-", "REET-", "MPTET-", "UPTET-", "HTET-"))]


def extra_in_paper(r, pflag):
    sub = r["subject"]
    if "(Paper 2)" in sub or "(Level 2)" in sub or "(Cat II)" in sub:
        return pflag == "ctet_p2"
    if sub.startswith("Environmental"):
        return pflag == "ctet_p1"
    return True


def wshare(col, pflag, pred):
    """Share of the EXAM's own topics that CTET practice covers: (Same + 0.5 Similar) / (matched topics + exam-only topics)."""
    rows_ = [r for r in core if r[pflag] and pred(r)]
    assessed = [r for r in rows_ if r[col]]
    if not rows_ or len(assessed) / len(rows_) < .6:
        return None, False
    matched = [r for r in assessed if r[col] in (S, SIM)]
    extra = [r for r in extras_all if r[col] in (S, SIM) and pred(r) and extra_in_paper(r, pflag)]
    den = len(matched) + len(extra)
    if not den:
        return None, False
    x = sum(1 if r[col] == S else .5 for r in matched) / den
    return x, len(assessed) < len(rows_)


def r5(x):
    return int(5 * round(100 * x / 5))


def pct_txt(res):
    x, partial = res
    return "n/a" if x is None else f"~{r5(x)}%" + ("*" if partial else "")


def sec_pct(col, pflag, key):
    if key not in FAM:
        return None, False
    names = FAM[key]
    return wshare(col, pflag, lambda r: fam_of(r["subject"]) in names)


def marks_line(label, secs, col, pflag):
    tot = {COV: 0, LIK: 0, PAR: 0, ADD: 0, UNK: 0}
    for key, name, marks in secs:
        tot[sec_status(label, key, col, pflag)[0]] += marks
    parts = []
    if tot[COV]:
        parts.append(f"<b>{tot[COV]}</b> marks in sections CTET practice covers well")
    if tot[LIK]:
        parts.append(f"<b>{tot[LIK]}</b> likely covered (no topic list)")
    if tot[PAR]:
        parts.append(f"<b>{tot[PAR]}</b> partly covered")
    if tot[ADD]:
        parts.append(f"<b>{tot[ADD]}</b> need an add-on")
    if tot[UNK]:
        parts.append(f"<b>{tot[UNK]}</b> not compared yet")
    return '<p class="mline">' + " &middot; ".join(parts) + " (of 150)</p>"


def meter(res):
    x, partial = res
    if x is None:
        return '<div class="meter"><span class="na">n/a</span></div>'
    return (f'<div class="meter"><div class="fill" style="width:{r5(x)}%"></div><span>{pct_txt(res)}</span></div>')


def pedagogy_panel():
    h = ('<div class="scroll"><table class="ped"><thead><tr><th>Exam paper</th>'
         '<th>Child development &amp; learning (CDP)</th><th>Subject pedagogy (languages, maths, EVS, science, social)</th>'
         '<th>Content topics shared with CTET</th></tr></thead><tbody>')
    for exam, label, secs, col, pflag in PAPERS:
        if not col:
            h += f"<tr><th>{html.escape(label)}</th><td colspan='3' class='s-unk'>Structure only: the board publishes no topic list</td></tr>"
            continue
        a = wshare(col, pflag, is_cdp)
        b = wshare(col, pflag, lambda r: is_ped(r) and not is_cdp(r))
        c = wshare(col, pflag, lambda r: not is_ped(r))
        h += f"<tr><th>{html.escape(label)}</th><td>{meter(a)}</td><td>{meter(b)}</td><td>{meter(c)}</td></tr>"
    return h + "</tbody></table></div>"


def bars_for(exam):
    return "".join(bar(l, sc, c, pf) for e, l, sc, c, pf in PAPERS if e == exam)


facts = {
    "CTET": ("Paper 1 (classes 1–5), Paper 2 (6–8)", "No", "60%", "Lifetime", "See ctet.nic.in"),
    "KTET": ("Categories 1–4 (Cat 1: 1–5, Cat 2: 6–8, Cat 3: high school, Cat 4: language/specialist)", "No",
             "60% General; 55% reserved categories; 50% disability", "Check the notification", "14–15 Nov 2026"),
    "UPTET": ("Paper 1 (1–5), Paper 2 (6–8)", "No", "See the notification", "See the notification", "See upessc.up.gov.in"),
    "REET": ("Level 1 (1–5), Level 2 (6–8)", "Wrong answers: no penalty. A question left with no option marked loses ⅓ mark (tick option E to skip)",
             "60% General; 55% SC/OBC/MBC/EWS", "Lifetime", "Per REET-2024 notification"),
    "MPTET": ("2026 test for in-service teachers (primary and middle)", "No", "60% others; 50% SC/ST/OBC/PwD/EWS",
              "Check the rulebook", "12 Oct 2026. Not valid for fresh recruitment"),
    "HTET": ("Level 1 (1–5), Level 2 (6–8), Level 3 (PGT)", "No", "60% General; 55% SC/disabled of Haryana",
             "Lifetime", "HTET-2026 announced, no dates yet"),
}
order = ["CTET", "KTET", "UPTET", "REET", "MPTET", "HTET"]


def li(items):
    return "".join(f"<li>{html.escape(i)}</li>" for i in items)


blocks = {
    "KTET": dict(
        verdict="Your CTET practice carries over well, especially for classes 1–8. Add the Kerala-specific parts.",
        covered=["Child development, learning and inclusive education", "Maths and EVS pedagogy", "English language pedagogy and comprehension"],
        add=["Mother-tongue paper (Malayalam, Tamil or Kannada)", "Kerala-specific curriculum questions", "Learning theories and personality in more detail", "Category 2: economics and Kerala history and geography"],
        notcov=["Category 3 and 4 subject papers (secondary level or specialist)"],
        link='<a href="ctet-vs-ktet.html">Full CTET vs KTET topic comparison</a>'),
    "UPTET": dict(
        verdict="The pedagogy you practise for CTET applies here too. UPTET adds heavy grammar, so budget extra time for it.",
        covered=["Child development, learning theories and inclusive education", "Hindi language pedagogy", "Maths and EVS content and pedagogy", "Paper 2: science and social studies pedagogy"],
        add=["Hindi and English grammar (sandhi, samas, alankar, tenses, voice...)", "Uttar Pradesh geography and civics", "Paper 2: home science, physical education, music and similar sections for those subject teachers"],
        notcov=["UPTET does not list assessment/CCE or intelligence, so skip those unless you also sit CTET"]),
    "REET": dict(
        verdict="Most of the pedagogy matches. Add Rajasthan-specific content and learn the blank-answer rule before exam day.",
        covered=["Child development and learning", "Maths and EVS pedagogy", "Level 2: science and social studies pedagogy"],
        add=["Rajasthan content in EVS and Level 2 social studies", "Applied arithmetic (profit and loss, interest, HCF/LCM)", "Personality, action research and RTE Act 2009"],
        notcov=["Language papers: we have not yet compared the Hindi, English and other language syllabi"],
        note="Exam-day tip from the REET-2024 notification: wrong answers carry no penalty, but a question with none of the five options marked loses ⅓ mark."),
    "MPTET": dict(
        verdict="The 2026 test is only for teachers already in service, and its result is not valid for fresh recruitment.",
        covered=["Child development, learning and inclusive education (almost the same text as CTET)", "Language II pedagogy", "Maths content and pedagogy"],
        add=["Mental health and behaviour problems, guidance and counselling, child delinquency"],
        notcov=["EVS details were not listed in full in the rulebook we read"]),
    "HTET": dict(
        verdict="The board publishes no topic list, but a past Level 2 paper shows what to expect: child-development questions lean on named theorists, and the language marks are pure grammar.",
        covered=["Child development and learning (30 marks): your CTET practice carries over", "Inclusive education and learning difficulties"],
        add=["Go deeper on named theories: intelligence tests, motivation theorists (Maslow, McClelland), Gagne, Sternberg, Thorndike's laws, Kohlberg's stages", "Hindi (15) and English (15) grammar and vocabulary", "General Studies (30 marks): quantitative aptitude, reasoning and Haryana GK, 10 marks each"],
        notcov=["Level 1 maths and EVS: no official topic list, so check the board's sample papers", "Level 2 and 3 subject papers (60 marks) need subject study"],
        note="Evidence: the board's 2023 sample paper for Level 2 (Mathematics, Set A). Level 1 papers were not available to us."),
}

cards = ""
for name in ["KTET", "UPTET", "REET", "MPTET", "HTET"]:
    b = blocks[name]
    p1, p2 = lab[name]
    cards += f"""<details class="card"{" open" if name == "UPTET" else ""}><summary><span>{name}</span><span class="tag">Overlap with CTET: {p1}{'' if p2 in ('n/a', 'Structure only') or p1 == p2 else ' / ' + p2}</span></summary>
<p class="verdict">{html.escape(b['verdict'])}</p>{bars_for(name)}
<div class="cols"><div><h4>Covered by CTET practice</h4><ul>{li(b['covered'])}</ul></div>
<div><h4>Add on top</h4><ul>{li(b['add'])}</ul></div>
<div><h4>Not covered / unknown</h4><ul>{li(b['notcov'])}</ul></div></div>
{('<p class="tip">' + html.escape(b['note']) + '</p>') if b.get('note') else ''}
{('<p>' + b['link'] + '</p>') if b.get('link') else ''}</details>"""

mrow = ""
for key, idx in (("Structure", 0), ("Negative marking", 1), ("Pass mark (General)", 2), ("Certificate validity", 3), ("Next exam", 4)):
    mrow += f"<tr><th>{key}</th>" + "".join(f"<td>{html.escape(facts[e][idx])}</td>" for e in order) + "</tr>"
overlap_row = "<tr><th>Syllabus carry-over from CTET</th><td>–</td>" + "".join(
    f"<td><strong>{lab[e][0]}</strong>{'' if lab[e][1] in ('n/a','Structure only') or lab[e][0]==lab[e][1] else ' / <strong>' + lab[e][1] + '</strong>'}</td>" for e in order[1:]) + "</tr>"

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Is CTET Preparation Enough for State TETs? Compared (2026)</title>
<meta name="description" content="How much of CTET preparation carries over to KTET, UPTET, REET, MPTET and HTET, and what to add. Built from the official bulletins. Last verified 1 October 2026.">
<style>
:root{{--bg:#fff;--fg:#1c1c1e;--mut:#5b6068;--line:#dde1e6;--soft:#f3f4f6;--acc:#0b57d0;--ok:#e6f4ea}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#ececee;--mut:#a3a8b0;--line:#363a41;--soft:#23262b;--acc:#8ab4f8;--ok:#16301f}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:900px;margin:0 auto;padding:20px 16px 64px}} h1{{font-size:1.65rem;line-height:1.25;margin:.2em 0}} h2{{font-size:1.2rem;margin-top:2rem}}
.lead{{font-size:1.05rem;border-left:4px solid var(--acc);padding:6px 14px;background:var(--soft);border-radius:0 8px 8px 0}}
.note{{color:var(--mut);font-size:.88rem}} .draft{{border:2px dashed #c0392b;border-radius:8px;padding:8px 12px;font-size:.88rem;margin-bottom:16px}}
.scroll{{overflow-x:auto}} table{{border-collapse:collapse;min-width:760px;width:100%;font-size:.9rem}}
th,td{{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}} thead th{{background:var(--soft)}} tbody th{{background:var(--soft);position:sticky;left:0;min-width:120px}}
.card{{border:1px solid var(--line);border-radius:10px;margin:10px 0;padding:0 14px}} .card summary{{cursor:pointer;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;padding:12px 0;font-weight:700}}
.tag{{font-weight:500;font-size:.85rem;background:var(--ok);padding:2px 10px;border-radius:99px}} .verdict{{margin:0 0 10px;font-weight:600}}
.cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}} h4{{margin:.3em 0;font-size:.92rem;color:var(--mut)}} ul{{margin:.2em 0;padding-left:1.1em}}
.tip{{background:var(--soft);padding:8px 12px;border-radius:8px;font-size:.92rem}} a{{color:var(--acc)}}
.big{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}} .stat{{background:var(--soft);border-radius:10px;padding:12px 14px}} .stat b{{font-size:1.6rem;display:block}}

.bar{{display:flex;flex-wrap:wrap;gap:4px;margin:4px 0 14px}}.bar-title{{font-weight:600;font-size:.9rem;margin-top:8px}}
.blk{{border-radius:6px;padding:6px 8px;min-width:105px;box-sizing:border-box;border:1px solid rgba(0,0,0,.18);font-size:.8rem;display:flex;flex-direction:column;gap:1px}}
.blk b{{font-size:.82rem}}.blk em{{font-style:normal;font-weight:600}}
.s-cov{{background:#cfe9d6;color:#14351f}}.s-lik{{background:repeating-linear-gradient(45deg,#cfe9d6,#cfe9d6 6px,#e9f5ec 6px,#e9f5ec 12px);color:#14351f}}
.s-par{{background:#ffe9a8;color:#3d2e00}}.s-add{{background:#ffc9a3;color:#4a1f00}}.s-unk{{background:#e3e5e8;color:#3a3f45}}.s-none{{background:transparent;color:var(--mut);text-align:center}}
.heat td{{text-align:center;font-weight:600;font-size:.82rem}}.heat th{{font-size:.82rem}}.heat{{min-width:640px}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.82rem;margin:8px 0}}.legend i{{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-2px;border:1px solid rgba(0,0,0,.2)}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;counter-reset:st}}.steps div{{background:var(--soft);border-radius:10px;padding:12px 14px;position:relative}}
.steps div b{{display:block;margin-bottom:4px}}.steps div:before{{counter-increment:st;content:counter(st);position:absolute;right:12px;top:6px;font-size:1.8rem;font-weight:800;opacity:.18}}

.mline{{margin:0 0 12px;font-size:.84rem;color:var(--mut)}}.mline b{{color:var(--fg)}}
.ped td,.ped th{{vertical-align:middle}}.ped{{min-width:620px}}
.meter{{position:relative;height:26px;background:var(--soft);border-radius:6px;overflow:hidden;min-width:140px}}
.meter .fill{{position:absolute;inset:0 auto 0 0;background:#8fd0a2}}.meter span{{position:relative;z-index:1;padding:0 8px;font-weight:700;font-size:.86rem;line-height:26px;color:#10301b}}
.meter .na{{color:var(--mut);font-weight:500}}
.heat small{{display:block;font-weight:500;font-size:.72rem;opacity:.85}}
.cat3{{border:1px solid var(--line);border-radius:10px;padding:12px 16px;background:var(--soft)}}
</style></head><body><main>
<div class="draft"><strong>DRAFT v4, not for publishing.</strong> The overlap labels come from a first-pass mapping that has not been spot-checked. Remove this box and the [EDITOR] notes before publishing.</div>

<h1>Is CTET preparation enough for your state TET?</h1>
<p class="note">Last verified: 1 October 2026 · From the official bulletins and syllabus documents of each exam board.</p>

<p class="lead"><strong>Short answer:</strong> mostly yes for the teaching part of the exam. A large share of every TET is pedagogy (how children learn and how to teach), and that is where CTET practice carries over. What you add is the state's own content: local language, local GK and grammar.</p>

<h2>Where CTET practice pays off most: the pedagogy marks</h2>
<p>Child development and pedagogy is the part most teachers find hardest, and it carries the most marks. This table shows how much of each exam's own topics your CTET practice already covers, split into the child-development part, the subject-pedagogy part and the content part.</p>
{pedagogy_panel()}
<p class="note">Each percentage is the share of the exam's topics that CTET practice also covers (a matching topic counts fully, a similar one counts half; topics only the exam has count as not covered), rounded to the nearest 5. They describe syllabus overlap, not the questions in the app and not a score prediction. * = some language sections not yet compared. HTET figures are indicative: they rest on one past Level 2 paper and an unverified syllabus summary, because the board publishes no topic list. [EDITOR: after the spot-check, re-run and re-check these numbers.]</p>
<p><strong>Theories and theorists:</strong> CTET lists Piaget, Kohlberg and Vygotsky. UPTET, MPTET and KTET also name the learning theorists Thorndike, Pavlov, Skinner and Kohler, and REET lists the theories of learning, so make sure your child-development practice includes those too. That is the main CDP gap between CTET and the state exams. [EDITOR: add the survey line here only if you decide to cite it, for example "14 of 20 KTET teachers we surveyed named CDP as their hardest area".]</p>

<h2>What CTET practice covers, exam by exam</h2>
{heatmap()}{legend()}
<p class="note">Each exam paper compared topic by topic with CTET, using the official syllabus. First-pass labels. Open an exam card below to see its sections as a 150-mark bar.</p>

<h2>How to use it</h2>
<div class="steps">
<div><b>Practise CTET pedagogy</b>Child development, learning, inclusive education and subject pedagogy carry the most marks and travel across exams.</div>
<div><b>Add your state's extras</b>Open your exam card below: grammar, local content and special rules are listed under "Add on top".</div>
<div><b>Take a mock for your exam</b>Check weak topics, fix them, repeat. No sign-up, works offline.</div>
</div>

<h2>Why CTET practice travels well</h2>
<div class="big">
<div class="stat"><b>90 of 150</b>marks in CTET Paper 1 are pedagogy: child development (30) plus 15 pedagogy questions each in two languages, maths and EVS.</div>
<div class="stat"><b>80 of 150</b>marks in CTET Paper 2 are pedagogy, whichever stream you take.</div>
<div class="stat"><b>Most</b>of that pedagogy appears in near-identical wording in KTET, UPTET, REET and MPTET. Exceptions are noted below.</div>
</div>
<p class="note">Counts from CTET September 2026 Information Bulletin, Appendix I. [EDITOR: re-check the "near-identical wording" claim after the spot-check.]</p>

<h2>All exams at a glance</h2>
<div class="scroll"><table><thead><tr><th></th>{''.join(f'<th>{e}</th>' for e in order)}</tr></thead><tbody>{overlap_row}{mrow}</tbody></table></div>
<p class="note">Syllabus carry-over compares the topics we checked (Very high, High, Partial, Low). Where a column says "Structure only", the board publishes no topic list. Eligibility rules differ by exam and change; read the official bulletin before you apply.</p>

<h2>What to do for each exam</h2>
{cards}

<h2>Practise this way with EasyCTET</h2>
<ol>
<li>Start with the pedagogy topics, since they count for the most marks and carry across exams.</li>
<li>Take a mock test offline and note your weak topics.</li>
<li>Add the state-specific items from the "Add on top" list for your exam.</li>
</ol>
<p>[EDITOR: add the real app coverage per exam here once the question bank is tagged, for example "EasyCTET covers X of Y topics for UPTET Paper 1". Add the Play Store link with a tagged URL. No sign-up, no phone number, works offline.]</p>

<h2>Preparing for KTET Category 3 or 4?</h2>
<div class="cat3"><p><strong>These are different exams.</strong> Category 3 (high school) has 40 marks of adolescent psychology, learning theories and teaching aptitude, 30 marks of language, and 80 marks of subject content for classes 8 to 10. Category 4 is for language and specialist teachers. CTET practice helps with the psychology and teaching-aptitude part, but not with the subject content, which needs its own study.</p></div>

<h2>Common questions</h2>
<details><summary>Can I use the CTET certificate for a state job?</summary><p>That depends on the state and the recruiting body. Each state decides which TET it accepts. Check the recruitment notice.</p></details>
<details><summary>How accurate is this comparison?</summary><p>We read the official syllabus and bulletin of each exam and compared them topic by topic. The comparison is an independent study aid, not issued by any exam board, and syllabi change, so check the board's website before each exam.</p></details>

<h2>Sources</h2>
<ul class="note"><li>CBSE, CTET September 2026 Information Bulletin.</li><li>Kerala Pareeksha Bhavan, K-TET September 2026 notification and Category I–IV syllabus documents.</li><li>UPESSC, UPTET syllabus documents (Primary and Upper Primary).</li><li>Board of Secondary Education Rajasthan, REET-2024 notification and syllabus files.</li><li>MP Employees Selection Board, 2026 eligibility test rulebook for in-service teachers.</li><li>Board of School Education Haryana, HTET-2025 Information Bulletin.</li></ul>
</main></body></html>"""
os.makedirs("../site-drafts", exist_ok=True)
open("../site-drafts/compare-all-tets.html", "w", encoding="utf-8").write(page)
print("written")

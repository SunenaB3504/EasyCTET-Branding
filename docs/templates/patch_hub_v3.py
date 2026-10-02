"""One-off patch: adds section-level statuses, 150-mark bars, a heatmap and a 3-step strip to build_page_hub.py."""
p = "build_page_hub.py"
s = open(p, encoding="utf-8").read()

MODEL = r'''
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
    names = FAM[key]
    base = [r for r in core if r[pflag] and fam_of(r["subject"]) in names]
    assessed = [r for r in base if r[col]]
    if not assessed:
        return UNK
    x = sum(1 for r in assessed if r[col] in (S, SIM)) / len(assessed)
    return COV if x >= .85 else PAR if x >= .60 else ADD


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
    ("HTET", H1, HT1, None, None), ("HTET", H2, HT2, None, None),
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
    (H1, "cdp"): (LIK, "board describes it like CTET"), (H1, "math"): (LIK, "NCERT-based, no topic list"),
    (H1, "evs"): (LIK, "NCERT-based, no topic list"), (H1, "l1"): (UNK, "no topic list"),
    (H1, "gs"): (ADD, "aptitude, reasoning, Haryana GK"),
    (H2, "cdp"): (LIK, "board describes it like CTET"), (H2, "l1"): (UNK, "no topic list"),
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
    return h + "</div>"


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
            h += f"<td class='{CSS_CLASS[st]}' title='{html.escape(note)}'>{st}</td>"
        h += "</tr>"
    return h + "</tbody></table></div>"


def legend():
    items = [(COV, "Covered: CTET practice matches"), (LIK, "Likely: board describes it like CTET, no topic list"),
             (PAR, "Partly: add a little"), (ADD, "Add-on needed"), (UNK, "Not compared yet")]
    return '<div class="legend">' + "".join(f'<span><i class="{CSS_CLASS[k]}"></i>{html.escape(t)}</span>' for k, t in items) + "</div>"


def bars_for(exam):
    return "".join(bar(l, sc, c, pf) for e, l, sc, c, pf in PAPERS if e == exam)

'''

CSS = """
.bar{display:flex;flex-wrap:wrap;gap:4px;margin:4px 0 14px}.bar-title{font-weight:600;font-size:.9rem;margin-top:8px}
.blk{border-radius:6px;padding:6px 8px;min-width:105px;box-sizing:border-box;border:1px solid rgba(0,0,0,.18);font-size:.8rem;display:flex;flex-direction:column;gap:1px}
.blk b{font-size:.82rem}.blk em{font-style:normal;font-weight:600}
.s-cov{background:#cfe9d6;color:#14351f}.s-lik{background:repeating-linear-gradient(45deg,#cfe9d6,#cfe9d6 6px,#e9f5ec 6px,#e9f5ec 12px);color:#14351f}
.s-par{background:#ffe9a8;color:#3d2e00}.s-add{background:#ffc9a3;color:#4a1f00}.s-unk{background:#e3e5e8;color:#3a3f45}.s-none{background:transparent;color:var(--mut);text-align:center}
.heat td{text-align:center;font-weight:600;font-size:.82rem}.heat th{font-size:.82rem}.heat{min-width:640px}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.82rem;margin:8px 0}.legend i{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-2px;border:1px solid rgba(0,0,0,.2)}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;counter-reset:st}.steps div{background:var(--soft);border-radius:10px;padding:12px 14px;position:relative}
.steps div b{display:block;margin-bottom:4px}.steps div:before{counter-increment:st;content:counter(st);position:absolute;right:12px;top:6px;font-size:1.8rem;font-weight:800;opacity:.18}
</style>"""

BODY = """<h2>What CTET practice covers, exam by exam</h2>
{heatmap()}{legend()}
<p class="note">Each exam paper compared topic by topic with CTET, using the official syllabus. First-pass labels. Open an exam card below to see its sections as a 150-mark bar.</p>

<h2>How to use it</h2>
<div class="steps">
<div><b>Practise CTET pedagogy</b>Child development, learning, inclusive education and subject pedagogy carry the most marks and travel across exams.</div>
<div><b>Add your state's extras</b>Open your exam card below: grammar, local content and special rules are listed under "Add on top".</div>
<div><b>Take a mock for your exam</b>Check weak topics, fix them, repeat. No sign-up, works offline.</div>
</div>

<h2>Why CTET practice travels well</h2>"""

assert "facts = {" in s and "<h2>Why CTET practice travels well</h2>" in s
s = s.replace("facts = {", MODEL + "\nfacts = {", 1)
s = s.replace("<p class=\"verdict\">{html.escape(b['verdict'])}</p>", "<p class=\"verdict\">{html.escape(b['verdict'])}</p>{bars_for(name)}", 1)
s = s.replace("</style>", CSS, 1)
s = s.replace("<h2>Why CTET practice travels well</h2>", BODY, 1)
open(p, "w", encoding="utf-8").write(s)
print("patched")

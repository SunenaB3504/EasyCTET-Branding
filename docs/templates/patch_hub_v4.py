"""Patch v4 for build_page_hub.py: pedagogy-first panel with rounded percentages, % in the heatmap cells,
a marks summary line on each bar, and a separate KTET Category 3/4 box."""
p = "build_page_hub.py"
s = open(p, encoding="utf-8").read()

HELPERS = r'''
# ---------- v4: percentages (topic-based, Same = 1, Similar = 0.5, rounded to nearest 5) ----------
def is_ped(r):
    t = r["topic_id"]
    return t.startswith("CDP-") or "-PED-" in t


def is_cdp(r):
    return r["topic_id"].startswith("CDP-")


def wshare(col, pflag, pred):
    rows_ = [r for r in core if r[pflag] and pred(r)]
    assessed = [r for r in rows_ if r[col]]
    if not rows_ or len(assessed) / len(rows_) < .6:
        return None, False
    x = sum(1 if r[col] == S else .5 if r[col] == SIM else 0 for r in assessed) / len(assessed)
    return x, len(assessed) < len(rows_)


def r5(x):
    return int(5 * round(100 * x / 5))


def pct_txt(res):
    x, partial = res
    return "n/a" if x is None else f"~{r5(x)}%" + ("*" if partial else "")


def sec_pct(col, pflag, key):
    names = FAM[key]
    return wshare(col, pflag, lambda r: fam_of(r["subject"]) in names)


def marks_line(label, secs, col, pflag):
    tot = {COV: 0, LIK: 0, PAR: 0, ADD: 0, UNK: 0}
    for key, name, marks in secs:
        tot[sec_status(label, key, col, pflag)[0]] += marks
    parts = []
    if tot[COV] + tot[LIK]:
        parts.append(f"<b>{tot[COV] + tot[LIK]}</b> marks in sections CTET practice covers well")
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

'''

assert "def bars_for(exam):" in s
s = s.replace("def bars_for(exam):", HELPERS + "\ndef bars_for(exam):", 1)

# % in heatmap cells
old_cell = "h += f\"<td class='{CSS_CLASS[st]}' title='{html.escape(note)}'>{st}</td>\""
assert old_cell in s
new_cell = ("pc = sec_pct(col, pflag, k2) if col else (None, False)\n"
            "            sub = (f\"<small>{pct_txt(pc)}</small>\" if pc[0] is not None else '')\n"
            "            h += f\"<td class='{CSS_CLASS[st]}' title='{html.escape(note)}'>{st}{sub}</td>\"")
s = s.replace(old_cell, new_cell, 1)

# marks summary under every bar group
old_bar_ret = "    return h + \"</div>\"\n\n\ndef heatmap():"
assert old_bar_ret in s
s = s.replace(old_bar_ret, "    return h + \"</div>\" + marks_line(label, secs, col, pflag)\n\n\ndef heatmap():", 1)

CSS = """
.mline{margin:0 0 12px;font-size:.84rem;color:var(--mut)}.mline b{color:var(--fg)}
.ped td,.ped th{vertical-align:middle}.ped{min-width:620px}
.meter{position:relative;height:26px;background:var(--soft);border-radius:6px;overflow:hidden;min-width:140px}
.meter .fill{position:absolute;inset:0 auto 0 0;background:#8fd0a2}.meter span{position:relative;z-index:1;padding:0 8px;font-weight:700;font-size:.86rem;line-height:26px;color:#10301b}
.meter .na{color:var(--mut);font-weight:500}
.heat small{display:block;font-weight:500;font-size:.72rem;opacity:.85}
.cat3{border:1px solid var(--line);border-radius:10px;padding:12px 16px;background:var(--soft)}
</style>"""
s = s.replace("</style>", CSS.replace("{", "{{").replace("}", "}}"), 1)

PANEL = """<h2>Where CTET practice pays off most: the pedagogy marks</h2>
<p>Child development and pedagogy is the part most teachers find hardest, and it carries the most marks. This table shows how much of CTET's pedagogy and content also appears in each exam, so you can see where your CTET practice does the most work.</p>
{pedagogy_panel()}
<p class="note">Percentages are the share of CTET topics that also appear in the exam (a matching topic counts fully, a similar one counts half), rounded to the nearest 5. They describe syllabus overlap, not the questions in the app and not a score prediction. * = some language sections not yet compared. [EDITOR: after the spot-check, re-run and re-check these numbers.]</p>
<p><strong>Theories and theorists</strong> (Piaget, Vygotsky, Kohlberg, Thorndike, Skinner and others) are listed in KTET, UPTET, REET and MPTET as well as CTET, so one set of explanations serves them all. [EDITOR: add the survey line here only if you decide to cite it, for example "14 of 20 KTET teachers we surveyed named CDP as their hardest area".]</p>

<h2>What CTET practice covers, exam by exam</h2>"""
assert "<h2>What CTET practice covers, exam by exam</h2>" in s
s = s.replace("<h2>What CTET practice covers, exam by exam</h2>", PANEL, 1)

CAT3 = """<h2>Preparing for KTET Category 3 or 4?</h2>
<div class="cat3"><p><strong>These are different exams.</strong> Category 3 (high school) has 40 marks of adolescent psychology, learning theories and teaching aptitude, 30 marks of language, and 80 marks of subject content for classes 8 to 10. Category 4 is for language and specialist teachers. CTET practice helps with the psychology and teaching-aptitude part, but not with the subject content, which needs its own study.</p></div>

<h2>Common questions</h2>"""
assert "<h2>Common questions</h2>" in s
s = s.replace("<h2>Common questions</h2>", CAT3, 1)

s = s.replace("DRAFT v2", "DRAFT v4")
open(p, "w", encoding="utf-8").write(s)
print("patched v4")

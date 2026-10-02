"""Fills the uptet column in master-topics.csv from the UPESSC UPTET syllabus PDFs supplied by the user
(docs/syllabi/UPTET_Primary_syllabus.pdf, UPTET_Upper_Primary_syllabus.pdf; created Jan 2026).
Paper 1 rows are judged against the Primary syllabus, Paper 2 rows against the Upper Primary syllabus.
Run after build_ctet_topics.py, map_ktet.py, map_reet.py and map_mptet.py.  First-pass judgement, unverified.
"""
import csv

S, SIM, NF = "Same", "Similar", "Not found"
rows = list(csv.DictReader(open("master-topics.csv", encoding="utf-8")))
hdr = list(rows[0].keys())

u = {
    # CDP (identical lists in Primary and Upper Primary)
    "CDP-DEV-CONCEPT": S, "CDP-DEV-PRINCIPLES": SIM, "CDP-DEV-HEREDITY-ENV": S, "CDP-DEV-SOCIALIZATION": SIM,
    "CDP-DEV-THEORISTS": SIM, "CDP-DEV-PROGRESSIVE-ED": NF, "CDP-DEV-INTELLIGENCE": NF, "CDP-DEV-MULTI-INTEL": NF,
    "CDP-DEV-LANG-THOUGHT": SIM, "CDP-DEV-GENDER": SIM, "CDP-DEV-INDIV-DIFF": SIM, "CDP-DEV-ASSESSMENT": NF,
    "CDP-DEV-QUESTIONING": NF, "CDP-INCL-DIVERSE": S, "CDP-INCL-LD-IMPAIR": S, "CDP-INCL-TALENTED": NF,
    "CDP-LRN-THINK-LEARN": S, "CDP-LRN-T-L-PROCESS": S, "CDP-LRN-PROBLEM-SOLVER": S, "CDP-LRN-ERRORS": S,
    "CDP-LRN-COG-EMO": SIM, "CDP-LRN-MOTIVATION": S, "CDP-LRN-FACTORS": S,
    "KTET-CDP-LEARNING-THEORIES": S, "KTET-CDP-PERSONALITY": NF,
    # Language I = Hindi: comprehension + a full pedagogy list; Language II (English/Urdu) lists content only
    "LANG-L1-COMP": S,
}
for k in ("ACQ", "PRINC", "LISTEN-SPEAK", "GRAMMAR", "DIVERSE", "SKILLS", "EVAL", "TLM", "REMEDIAL"):
    u[f"LANG-L1-PED-{k}"] = S
    u[f"LANG-L2-PED-{k}"] = NF
u["LANG-L2-COMP"] = S
# Maths
for k, v in {"GEOM": S, "SOLIDS": SIM, "NUM": S, "ADD-SUB": S, "MULT": S, "DIV": S, "MEAS": S, "DATA": S,
             "PATTERNS": NF, "MONEY": S}.items():
    u[f"MATH-P1-CONT-{k}"] = v
for k in ("NUMSYS", "ALGEBRA", "GEOM", "DATA"):
    u[f"MATH-P2-CONT-{k}"] = S
for k in ("NATURE", "PLACE", "LANGUAGE", "COMMUNITY", "EVAL", "PROBLEMS", "REMEDIAL"):
    u[f"MATH-PED-{k}"] = S
u["MATH-PED-ERROR"] = S  # Paper 1 lists error analysis; Paper 2 does not (handled below)
# EVS (Paper 1)
for k in ("FAMILY", "FOOD", "SHELTER", "WATER", "TRAVEL", "THINGS"):
    u[f"EVS-CONT-{k}"] = S
for k in ("CONCEPT", "SIGNIF", "EE", "PRINC", "RELATION", "APPROACH", "ACTIVITIES", "EXPT", "DISC", "CCE", "AIDS", "PROBLEMS"):
    u[f"EVS-PED-{k}"] = S
# Science (Paper 2)
for k, v in {"FOOD": S, "MATERIALS": S, "LIVING": S, "MOVING": S, "HOW": S, "NATURAL-PHEN": SIM, "NATURAL-RES": S}.items():
    u[f"SCI-CONT-{k}"] = v
for k in ("NATURE", "AIMS", "UNDERSTAND", "APPROACH", "METHOD", "INNOV", "AIDS", "EVAL", "PROBLEMS", "REMEDIAL"):
    u[f"SCI-PED-{k}"] = S
# Social studies (Paper 2)
hist = {1: SIM, 2: SIM, 3: SIM, 5: S, 6: S, 7: S, 9: SIM, 11: S, 12: S, 14: S, 17: S, 20: SIM, 21: SIM, 23: S, 24: S}
for i in range(1, 25):
    u[f"SST-HIST-{i:02d}"] = hist.get(i, NF)
geo = {2: S, 3: S, 4: S, 5: S, 6: S, 7: SIM, 8: S, 9: SIM}
for i in range(1, 10):
    u[f"SST-GEO-{i:02d}"] = geo.get(i, NF)
pol = {1: SIM, 2: S, 3: S, 5: S, 6: S, 9: S, 10: SIM, 11: SIM}
for i in range(1, 13):
    u[f"SST-POL-{i:02d}"] = pol.get(i, NF)
ped = {1: S, 2: S, 3: S, 4: S, 5: S, 7: S, 8: S}
for i in range(1, 9):
    u[f"SST-PED-{i:02d}"] = ped.get(i, NF)

note = "UPTET column: judged against UPESSC UPTET syllabus PDFs (Primary / Upper Primary, Jan 2026), unverified"
for r in rows:
    tid = r["topic_id"]
    if tid not in u:
        continue
    v = u[tid]
    p1, p2 = bool(r["ctet_p1"]), bool(r["ctet_p2"])
    if tid == "MATH-PED-ERROR" and not p1:
        v = NF
    # Language II pedagogy: not listed for English/Urdu; Sanskrit lists it, but English is the default Language II
    r["uptet"] = v
    r["notes"] = (r["notes"] + "; " if r["notes"] else "") + note

extra = [
    ("UPTET-LANG-HINDI-GRAMMAR", "Language I (Hindi)", "Hindi grammar and vocabulary: varnamala, matra, sandhi, samas, alankar, idioms, synonyms, punctuation", "Content"),
    ("UPTET-LANG-ENGLISH-GRAMMAR", "Language II (English)", "English grammar: parts of speech, tenses, articles, voice, narration, punctuation, word formation", "Content"),
    ("UPTET-EVS-UP-CIVICS", "Environmental Studies", "Uttar Pradesh and India geography, governance structure (panchayat to state), national symbols, fairs, sports", "Content"),
    ("UPTET-P2-MATH-COMMERCIAL", "Mathematics (Paper 2)", "Commercial maths (tax, banking, compound interest), graphs, probability, Cartesian plane, mensuration", "Content"),
    ("UPTET-P2-SST-OTHER-SUBJECTS", "Social Studies and others (Paper 2)", "Home science, physical education and sports, music, horticulture, disaster management, disability", "Content"),
]
for tid, subj, topic, sub in extra:
    row = {h: "" for h in hdr}
    row.update(topic_id=tid, subject=subj, topic=topic, subtopic=sub, uptet=S,
               source_ref="UPESSC UPTET syllabus PDFs (docs/syllabi)", confidence="Medium", verified_by_me="N",
               notes="UPTET-specific; not in the CTET syllabus (Same here means 'present in UPTET')")
    rows.append(row)

with open("master-topics.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    w.writerows(rows)

for label, base in (("UPTET Paper 1 vs CTET P1", [r for r in rows if r["ctet_p1"]]),
                    ("UPTET Paper 2 vs CTET P2", [r for r in rows if r["ctet_p2"]])):
    ok = sum(1 for r in base if r["uptet"] in (S, SIM))
    print(f"{label}: {ok}/{len(base)} matched ({sum(1 for r in base if r['uptet']==S)} Same)")

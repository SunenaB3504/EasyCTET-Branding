"""Fills ktet_c1..c4 in master-topics.csv from the KTET 2012 SCERT syllabus PDFs (docs/syllabi).

Values: Same / Similar / Different / Not found.  These are first-pass judgements, NOT verified.
Run build_ctet_topics.py first (it regenerates the CTET rows), then this script.
"""
import csv

S, SIM, NF = "Same", "Similar", "Not found"
src = list(csv.DictReader(open("master-topics.csv", encoding="utf-8")))
hdr = list(src[0].keys())

# (c1, c2, c3, c4) per topic_id (exact) or prefix
rules = {
    # --- CDP development
    "CDP-DEV-CONCEPT": (S, S, SIM, NF),
    "CDP-DEV-PRINCIPLES": (S, S, S, NF),
    "CDP-DEV-HEREDITY-ENV": (S, S, S, NF),
    "CDP-DEV-SOCIALIZATION": (NF, S, NF, NF),
    "CDP-DEV-THEORISTS": (S, S, SIM, NF),
    "CDP-DEV-PROGRESSIVE-ED": (S, S, NF, NF),
    "CDP-DEV-INTELLIGENCE": (S, S, SIM, NF),
    "CDP-DEV-MULTI-INTEL": (SIM, S, NF, NF),
    "CDP-DEV-LANG-THOUGHT": (S, S, NF, NF),
    "CDP-DEV-GENDER": (S, S, NF, NF),
    "CDP-DEV-INDIV-DIFF": (S, S, NF, NF),
    "CDP-DEV-ASSESSMENT": (S, S, SIM, NF),
    "CDP-DEV-QUESTIONING": (SIM, SIM, NF, NF),
    # --- inclusive
    "CDP-INCL-DIVERSE": (S, S, SIM, NF),
    "CDP-INCL-LD-IMPAIR": (S, S, SIM, NF),
    "CDP-INCL-TALENTED": (S, S, SIM, NF),
    # --- learning and pedagogy
    "CDP-LRN-THINK-LEARN": (S, SIM, SIM, NF),
    "CDP-LRN-T-L-PROCESS": (S, S, SIM, NF),
    "CDP-LRN-PROBLEM-SOLVER": (S, SIM, NF, NF),
    "CDP-LRN-ERRORS": (S, NF, NF, NF),
    "CDP-LRN-COG-EMO": (S, S, NF, NF),
    "CDP-LRN-MOTIVATION": (S, S, SIM, NF),
    "CDP-LRN-FACTORS": (S, S, SIM, NF),
    # --- Maths content
    "MATH-P1-CONT-GEOM": (SIM, NF, NF, NF),
    "MATH-P1-CONT-SOLIDS": (NF, NF, NF, NF),
    "MATH-P1-CONT-NUM": (S, NF, NF, NF),
    "MATH-P1-CONT-ADD-SUB": (S, NF, NF, NF),
    "MATH-P1-CONT-MULT": (S, NF, NF, NF),
    "MATH-P1-CONT-DIV": (S, NF, NF, NF),
    "MATH-P1-CONT-MEAS": (S, NF, NF, NF),
    "MATH-P1-CONT-DATA": (NF, NF, NF, NF),
    "MATH-P1-CONT-PATTERNS": (SIM, NF, NF, NF),
    "MATH-P1-CONT-MONEY": (S, NF, NF, NF),
    "MATH-P2-CONT-NUMSYS": (NF, SIM, NF, NF),
    "MATH-P2-CONT-ALGEBRA": (NF, SIM, NF, NF),
    "MATH-P2-CONT-GEOM": (NF, SIM, NF, NF),
    "MATH-P2-CONT-DATA": (NF, S, NF, NF),
    "MATH-PED-NATURE": (S, S, NF, NF),
    "MATH-PED-PLACE": (S, S, NF, NF),
    "MATH-PED-LANGUAGE": (S, S, NF, NF),
    "MATH-PED-COMMUNITY": (NF, NF, NF, NF),
    "MATH-PED-EVAL": (S, S, NF, NF),
    "MATH-PED-PROBLEMS": (SIM, NF, NF, NF),  # Cat II: verified 2026-10-03, no such topic in KTET Cat II maths pedagogy
    "MATH-PED-REMEDIAL": (S, S, NF, NF),
    "MATH-PED-ERROR": (S, S, NF, NF),
}
# EVS (Cat I "Environmental Science": content topics differ in wording; pedagogy is science-oriented)
for k in ("FAMILY", "FOOD", "WATER", "SHELTER"):
    rules[f"EVS-CONT-{k}"] = (S, NF, NF, NF)
rules["EVS-CONT-TRAVEL"] = (SIM, NF, NF, NF)  # 'Vehicles'
rules["EVS-CONT-THINGS"] = (SIM, NF, NF, NF)  # 'Jobs'/tools
for k in ("CONCEPT", "SIGNIF", "EE", "RELATION", "APPROACH", "ACTIVITIES", "EXPT", "CCE", "AIDS", "PROBLEMS", "PRINC", "DISC"):
    rules[f"EVS-PED-{k}"] = (SIM, NF, NF, NF)
# Science P2 vs Cat II science (content is broader / more advanced in KTET)
for k in ("FOOD", "MATERIALS", "LIVING", "MOVING", "HOW", "NATURAL-PHEN", "NATURAL-RES"):
    rules[f"SCI-CONT-{k}"] = (NF, SIM, NF, NF)
for k in ("NATURE", "AIMS", "UNDERSTAND", "APPROACH", "METHOD", "INNOV", "AIDS", "EVAL", "PROBLEMS", "REMEDIAL"):
    rules[f"SCI-PED-{k}"] = (NF, SIM, NF, NF)
# Language
for L in ("L1", "L2"):
    rules[f"LANG-{L}-COMP"] = (SIM, SIM, SIM, NF)
l2_ped_c2 = S  # Cat II Hindi/Language II pedagogy list mirrors the CTET list item by item
for k, c1, c3, c4 in (("ACQ", S, NF, SIM), ("PRINC", S, NF, SIM), ("LISTEN-SPEAK", SIM, NF, NF), ("GRAMMAR", NF, NF, SIM),
                      ("DIVERSE", SIM, NF, SIM), ("SKILLS", S, SIM, S), ("EVAL", S, NF, S), ("TLM", SIM, NF, S),
                      ("REMEDIAL", NF, NF, NF)):
    rules[f"LANG-L2-PED-{k}"] = (c1, l2_ped_c2, c3, c4)
    rules[f"LANG-L1-PED-{k}"] = (SIM, SIM, c3, c4)
# Refinements after reading Cat II social science, science and maths sections in full (c3 = Cat III covers
# these subjects at secondary level, so "Different")
D = "Different"
hist = {2: SIM,  # 1 (When, where and how) verified Not found in Cat II, 2026-10-03
         3: SIM, 4: SIM, 17: SIM, 18: SIM, 19: SIM, 20: S, 21: SIM, 22: SIM, 23: S}
for i in range(1, 25):
    rules[f"SST-HIST-{i:02d}"] = (NF, hist.get(i, NF), D, NF)
geo = {2: S, 3: S, 4: SIM, 5: SIM, 7: SIM, 8: SIM, 9: SIM}
for i in range(1, 10):
    rules[f"SST-GEO-{i:02d}"] = (NF, geo.get(i, NF), D, NF)
pol = {2: SIM, 3: S, 5: S, 6: S, 10: SIM}  # 10: Cat II lists election process/Election Commission (verified 2026-10-03)
for i in range(1, 13):
    rules[f"SST-POL-{i:02d}"] = (NF, pol.get(i, NF), D, NF)
ped = {1: S, 2: SIM, 8: S}
for i in range(1, 9):
    rules[f"SST-PED-{i:02d}"] = (NF, ped.get(i, NF), D, NF)
rules.update({
    "MATH-P2-CONT-NUMSYS": (NF, S, D, NF),
    "MATH-P2-CONT-ALGEBRA": (NF, S, D, NF),
    "MATH-P2-CONT-GEOM": (NF, SIM, D, NF),
    "MATH-P2-CONT-DATA": (NF, S, D, NF),
    "SCI-PED-NATURE": (NF, SIM, NF, NF), "SCI-PED-AIMS": (NF, S, NF, NF), "SCI-PED-UNDERSTAND": (NF, SIM, NF, NF),
    "SCI-PED-APPROACH": (NF, S, NF, NF), "SCI-PED-METHOD": (NF, S, NF, NF), "SCI-PED-INNOV": (NF, NF, NF, NF),
    "SCI-PED-AIDS": (NF, S, NF, NF), "SCI-PED-EVAL": (NF, S, NF, NF), "SCI-PED-PROBLEMS": (NF, SIM, NF, NF),
    "SCI-PED-REMEDIAL": (NF, NF, NF, NF),
})
for k in ("FOOD", "MATERIALS", "LIVING", "MOVING", "HOW", "NATURAL-PHEN", "NATURAL-RES"):
    rules[f"SCI-CONT-{k}"] = (NF, SIM, D, NF)

unmapped = []
for r in src:
    v = rules.get(r["topic_id"])
    if not v:
        unmapped.append(r["topic_id"])
        continue
    r["ktet_c1"], r["ktet_c2"], r["ktet_c3"], r["ktet_c4"] = v
    r["confidence"] = "Medium"
    r["notes"] = (r["notes"] + "; " if r["notes"] else "") + "KTET columns: first-pass mapping from 2012 SCERT syllabus PDFs, unverified"
if unmapped:
    print("UNMAPPED:", unmapped)

# KTET-only topics
extra = [
    ("KTET-CDP-STUDY-METHODS", "Child Development and Pedagogy", "Methods of studying child behaviour (observation, case study, interview, tests)", "Child Development", (S, NF, SIM, NF)),
    ("KTET-CDP-LEARNING-THEORIES", "Child Development and Pedagogy", "Basic learning theories (Pavlov, Skinner, Gestalt, Bruner)", "Child Development", (S, S, S, NF)),
    ("KTET-CDP-PERSONALITY", "Child Development and Pedagogy", "Personality development and adjustment mechanisms", "Child Development", (S, S, S, NF)),
    ("KTET-CDP-ADOLESCENT", "Adolescent Psychology (Cat III)", "Adolescence: characteristics, problems, developmental theories", "Child Development", (NF, SIM, S, NF)),
    ("KTET-CDP-TEACHING-APTITUDE", "Teaching Aptitude (Cat III)", "Teaching aptitude: teacher roles, methods, classroom management, NCF 2005 / KCF 2007 / RTE 2009", "Teaching", (NF, NF, S, NF)),
    ("KTET-LANG-MOTHER-TONGUE", "Language I (Malayalam/Tamil/Kannada)", "Mother-tongue literature, culture, functional grammar (Kerala language papers)", "Language", (S, S, S, NF)),
    ("KTET-SUBJECT-CAT3", "Subject-specific areas (Cat III)", "Subject content and pedagogy for classes VIII-X (80 questions)", "Subject", (NF, NF, S, NF)),
    ("KTET-SST-ECONOMICS", "Social Science (Cat II)", "Economics: growth, five year plans, money and banking, globalisation (8 questions)", "Economics", (NF, S, D, NF)),
    ("KTET-SST-KERALA", "Social Science (Cat II)", "Kerala-specific history, geography and economy", "Kerala", (NF, S, D, NF)),
    ("KTET-CAT4-SPECIALIST", "Category IV specialist", "Language teachers (Arabic, Urdu, Sanskrit, Hindi), art and physical education content", "Specialist", (NF, NF, NF, S)),
]
for tid, subj, topic, sub, v in extra:
    row = {h: "" for h in hdr}
    row.update(topic_id=tid, subject=subj, topic=topic, subtopic=sub, ktet_c1=v[0], ktet_c2=v[1], ktet_c3=v[2], ktet_c4=v[3],
               source_ref="KTET 2012 SCERT syllabus PDFs (docs/syllabi)", confidence="Medium", verified_by_me="N",
               notes="KTET-only or KTET-heavier topic; not in CTET syllabus")
    src.append(row)

with open("master-topics.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    w.writerows(src)

# summary: share of CTET topics with any KTET overlap per category
cats = ("ktet_c1", "ktet_c2", "ktet_c3", "ktet_c4")
ctet = [r for r in src if r["ctet_p1"] or r["ctet_p2"]]
for c in cats:
    hit = sum(1 for r in ctet if r[c] in (S, SIM))
    same = sum(1 for r in ctet if r[c] == S)
    print(c, f"{hit}/{len(ctet)} CTET topics found (Same or Similar); {same} Same")

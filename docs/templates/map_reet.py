"""Fills reet_l1 / reet_l2 in master-topics.csv from the REET syllabus files in docs/syllabi (2016 files on the
BSER site, English text on page 2 of each PDF).  Run after build_ctet_topics.py and map_ktet.py.

Values: Same / Similar / Different / Not found.  First-pass judgement, NOT verified.
Language I/II syllabi were not downloaded, so LANG-* rows are left blank for REET.
"""
import csv

S, SIM, NF = "Same", "Similar", "Not found"
rows = list(csv.DictReader(open("master-topics.csv", encoding="utf-8")))
hdr = list(rows[0].keys())

r = {}  # topic_id -> (l1, l2)
# CDP (L1 and L2 lists are almost identical; L2 adds named theorists)
for k, v in {
    "DEV-CONCEPT": (S, S), "DEV-PRINCIPLES": (S, S), "DEV-HEREDITY-ENV": (S, S), "DEV-SOCIALIZATION": (NF, NF),
    "DEV-THEORISTS": (SIM, SIM), "DEV-PROGRESSIVE-ED": (NF, NF), "DEV-INTELLIGENCE": (S, S), "DEV-MULTI-INTEL": (S, S),
    "DEV-LANG-THOUGHT": (NF, NF), "DEV-GENDER": (SIM, SIM), "DEV-INDIV-DIFF": (S, S), "DEV-ASSESSMENT": (S, S),
    "DEV-QUESTIONING": (SIM, SIM), "INCL-DIVERSE": (S, S), "INCL-LD-IMPAIR": (S, S), "INCL-TALENTED": (S, S),
    "LRN-THINK-LEARN": (S, S), "LRN-T-L-PROCESS": (SIM, SIM), "LRN-PROBLEM-SOLVER": (NF, SIM), "LRN-ERRORS": (NF, NF),
    "LRN-COG-EMO": (NF, NF), "LRN-MOTIVATION": (S, S), "LRN-FACTORS": (S, S),
}.items():
    r[f"CDP-{k}"] = v
# Maths Paper 1 content -> REET Level 1 only
for k, v in {"GEOM": SIM, "SOLIDS": SIM, "NUM": S, "ADD-SUB": S, "MULT": S, "DIV": S, "MEAS": S, "DATA": NF,
             "PATTERNS": NF, "MONEY": S}.items():
    r[f"MATH-P1-CONT-{k}"] = (v, NF)
# Maths Paper 2 content -> REET Level 2 only
for k, v in {"NUMSYS": SIM, "ALGEBRA": S, "GEOM": S, "DATA": S}.items():
    r[f"MATH-P2-CONT-{k}"] = (NF, v)
for k in ("NATURE", "PLACE", "LANGUAGE", "COMMUNITY", "EVAL", "PROBLEMS", "REMEDIAL"):
    r[f"MATH-PED-{k}"] = (S, S)
r["MATH-PED-ERROR"] = (S, NF)
# EVS -> Level 1 only
for k, v in {"FAMILY": SIM, "FOOD": SIM, "SHELTER": SIM, "WATER": SIM, "TRAVEL": S, "THINGS": SIM}.items():
    r[f"EVS-CONT-{k}"] = (v, NF)
for k in ("CONCEPT", "SIGNIF", "EE", "PRINC", "RELATION", "APPROACH", "ACTIVITIES", "EXPT", "DISC", "CCE", "AIDS", "PROBLEMS"):
    r[f"EVS-PED-{k}"] = (S, NF)
# Science -> Level 2 only
for k in ("FOOD", "MATERIALS", "LIVING", "MOVING", "HOW", "NATURAL-PHEN", "NATURAL-RES"):
    r[f"SCI-CONT-{k}"] = (NF, SIM)
for k in ("NATURE", "AIMS", "UNDERSTAND", "METHOD", "INNOV", "AIDS", "EVAL", "PROBLEMS", "REMEDIAL"):
    r[f"SCI-PED-{k}"] = (NF, S)
r["SCI-PED-APPROACH"] = (NF, SIM)
# Social studies -> Level 2 only
hist = {4: SIM, 7: SIM, 8: SIM, 10: SIM, 14: SIM, 17: SIM, 20: S, 21: SIM, 23: S}
for i in range(1, 25):
    r[f"SST-HIST-{i:02d}"] = (NF, hist.get(i, NF))
geo = {4: SIM, 5: SIM, 6: SIM, 7: SIM, 8: S, 9: S}
for i in range(1, 10):
    r[f"SST-GEO-{i:02d}"] = (NF, geo.get(i, NF))
pol = {2: S, 3: S, 5: S, 6: S, 8: SIM, 9: S, 10: S, 11: SIM, 12: S}
for i in range(1, 13):
    r[f"SST-POL-{i:02d}"] = (NF, pol.get(i, NF))
ped = {1: S, 2: S, 3: S, 4: S, 5: S, 6: SIM, 7: S, 8: S}
for i in range(1, 9):
    r[f"SST-PED-{i:02d}"] = (NF, ped.get(i, NF))
# KTET extras that REET also covers
r["KTET-CDP-LEARNING-THEORIES"] = (S, S)
r["KTET-CDP-PERSONALITY"] = (S, S)

note = "REET columns: first-pass mapping from 2016 BSER syllabus files (not the 2024 notification), unverified"
unmapped = []
for row in rows:
    tid = row["topic_id"]
    if tid in r:
        row["reet_l1"], row["reet_l2"] = r[tid]
        row["notes"] = (row["notes"] + "; " if row["notes"] else "") + note
    elif tid.startswith("LANG-") or tid.startswith("KTET-"):
        pass  # language syllabi not read; KTET-only rows not assessed for REET
    else:
        unmapped.append(tid)
if unmapped:
    print("UNMAPPED:", unmapped)

extra = [
    ("REET-CDP-ACTION-RESEARCH-RTE", "Child Development and Pedagogy", "Action research; Right to Education Act 2009 (role and responsibilities of teachers); adjustment", "Teaching", (S, S)),
    ("REET-MATH-ARITH-APPLIED", "Mathematics", "Fractions, prime numbers, LCM/HCF; unitary law, average, profit and loss, simple interest (Level 1); indices, square/cube roots, compound interest, percentage, partnership (Level 2)", "Content", (S, S)),
    ("REET-EVS-RAJASTHAN", "Environmental Studies", "Rajasthan-specific content: industries, culture, fairs, tourist places, renewable resources, state symbols", "Content", (S, NF)),
    ("REET-EVS-HEALTH-CIVICS", "Environmental Studies", "Public places and institutions, panchayat/assembly/parliament basics; personal hygiene, diseases, pulse polio", "Content", (S, NF)),
    ("REET-SST-RAJASTHAN-GEO", "Social Studies (Level 2)", "Geography and resources of Rajasthan", "Geography", (NF, S)),
    ("REET-SST-RAJASTHAN-HIST", "Social Studies (Level 2)", "History and culture of Rajasthan, freedom struggle, integration, heritage", "History", (NF, S)),
    ("REET-SCI-HEALTH-TECH", "Science (Level 2)", "Human body and health, adolescence, science and technology, structure of matter, chemical substances", "Content", (NF, S)),
]
for tid, subj, topic, sub, v in extra:
    row = {h: "" for h in hdr}
    row.update(topic_id=tid, subject=subj, topic=topic, subtopic=sub, reet_l1=v[0], reet_l2=v[1],
               source_ref="REET syllabus files from BSER site (2016), docs/syllabi", confidence="Medium", verified_by_me="N",
               notes="REET-specific or REET-heavier topic; not in the CTET syllabus (REET Same here means 'present in REET')")
    rows.append(row)

with open("master-topics.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    w.writerows(rows)

ctet1 = [x for x in rows if x["ctet_p1"]]
ctet2 = [x for x in rows if x["ctet_p2"]]
for label, base, col in (("REET L1 vs CTET P1", ctet1, "reet_l1"), ("REET L2 vs CTET P2", ctet2, "reet_l2")):
    ok = sum(1 for x in base if x[col] in (S, SIM))
    same = sum(1 for x in base if x[col] == S)
    scored = [x for x in base if x[col]]
    print(f"{label}: {ok}/{len(base)} CTET topics matched ({same} Same); language rows not assessed ({len(base) - len(scored)} blank)")

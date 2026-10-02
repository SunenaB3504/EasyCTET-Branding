"""Fills the mptet column in master-topics.csv from the MPESB 2026 rulebook for in-service teachers
(Primary-level exam, chapter 1, pp.7-13 read as images).  Only CTET Paper 1 rows are assessed; Paper 2 / middle-level
chapter (pp.14-29) was not read.  Run after build_ctet_topics.py, map_ktet.py and map_reet.py.
"""
import csv

S, SIM, NF = "Same", "Similar", "Not found"
rows = list(csv.DictReader(open("master-topics.csv", encoding="utf-8")))
hdr = list(rows[0].keys())

m = {}
for tid in [r["topic_id"] for r in rows if r["topic_id"].startswith("CDP-")]:
    m[tid] = S
m["CDP-DEV-THEORISTS"] = SIM  # Piaget, Pavlov, Kohler, Thorndike instead of Piaget, Kohlberg, Vygotsky
for k in ("COMP", "PED-ACQ", "PED-PRINC", "PED-LISTEN-SPEAK", "PED-GRAMMAR", "PED-DIVERSE", "PED-EVAL", "PED-TLM", "PED-REMEDIAL"):
    m[f"LANG-L1-{k}"] = S
    m[f"LANG-L2-{k}"] = S
m["LANG-L1-PED-SKILLS"] = SIM
m["LANG-L2-PED-SKILLS"] = S
m.update({
    "MATH-P1-CONT-GEOM": S, "MATH-P1-CONT-SOLIDS": SIM, "MATH-P1-CONT-NUM": S, "MATH-P1-CONT-ADD-SUB": S,
    "MATH-P1-CONT-MULT": S, "MATH-P1-CONT-DIV": S, "MATH-P1-CONT-MEAS": S, "MATH-P1-CONT-DATA": S,
    "MATH-P1-CONT-PATTERNS": S, "MATH-P1-CONT-MONEY": S,
    "MATH-PED-NATURE": SIM, "MATH-PED-PLACE": S, "MATH-PED-LANGUAGE": S, "MATH-PED-COMMUNITY": NF,
    "MATH-PED-EVAL": S, "MATH-PED-PROBLEMS": NF, "MATH-PED-REMEDIAL": S, "MATH-PED-ERROR": NF,
    "EVS-CONT-FAMILY": S, "EVS-CONT-SHELTER": S, "EVS-CONT-WATER": SIM, "EVS-CONT-THINGS": S,
})
note = "MPTET column: 2026 in-service eligibility test (primary), rulebook pp.7-13; EVS content/pedagogy listing incomplete in file"
for r in rows:
    if r["topic_id"] in m:
        r["mptet"] = m[r["topic_id"]]
        r["notes"] = (r["notes"] + "; " if r["notes"] else "") + note

row = {h: "" for h in hdr}
row.update(topic_id="MPTET-CDP-EXTRA", subject="Child Development and Pedagogy",
           topic="Mental health and behaviour problems of children; personality and its measurement; aptitude; memory and forgetting; guidance and counselling; child delinquency",
           subtopic="Child Development", mptet=S, source_ref="MPESB rulebook 2026 pp.8-9", confidence="Medium",
           verified_by_me="N", notes="MPTET-specific additions to the CDP list")
rows.append(row)

with open("master-topics.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    w.writerows(rows)

p1 = [r for r in rows if r["ctet_p1"]]
ok = sum(1 for r in p1 if r["mptet"] in (S, SIM))
print(f"MPTET primary vs CTET P1: {ok}/{len(p1)} matched ({sum(1 for r in p1 if r['mptet']==S)} Same); "
      f"{sum(1 for r in p1 if not r['mptet'])} blank (EVS items not read)")

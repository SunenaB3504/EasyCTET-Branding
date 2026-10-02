"""Fills the htet column in master-topics.csv from the HTET syllabus summary pasted by the user (source unknown).
The official HTET-2025 bulletin gives only the structure and sample questions, so every HTET value here is LOW confidence
and must be verified against a BSEH syllabus page before it is published.  Run last (after map_uptet.py)."""
import csv

S, SIM, NF = "Same", "Similar", "Not found"
rows = list(csv.DictReader(open("master-topics.csv", encoding="utf-8")))
hdr = list(rows[0].keys())

h = {
    # CDP (Level 1-3 share one description in the summary)
    "CDP-DEV-CONCEPT": S, "CDP-DEV-HEREDITY-ENV": S, "CDP-DEV-SOCIALIZATION": S, "CDP-DEV-THEORISTS": S,
    "CDP-DEV-ASSESSMENT": S,
    "CDP-INCL-DIVERSE": S, "CDP-INCL-TALENTED": S,
    "CDP-LRN-THINK-LEARN": S, "CDP-LRN-T-L-PROCESS": S, "CDP-LRN-PROBLEM-SOLVER": S, "CDP-LRN-COG-EMO": S,
    "CDP-LRN-MOTIVATION": S,
    "KTET-CDP-LEARNING-THEORIES": S,
    # Languages: Hindi 15 + English 15
    "LANG-L1-COMP": S, "LANG-L2-COMP": S,
    # Level 2 sample paper (Q31-60): Hindi and English are pure grammar/vocabulary, no language-pedagogy questions
    "LANG-L2-PED-ACQ": NF, "LANG-L2-PED-PRINC": NF, "LANG-L2-PED-SKILLS": NF, "LANG-L2-PED-REMEDIAL": NF,
    "LANG-L1-PED-ACQ": NF, "LANG-L1-PED-PRINC": NF,
    # CDP: confirmed in Level 2 sample paper Q1-30
    "CDP-DEV-INTELLIGENCE": S, "CDP-DEV-PROGRESSIVE-ED": S, "CDP-DEV-INDIV-DIFF": S, "CDP-DEV-PRINCIPLES": S,
    "CDP-INCL-LD-IMPAIR": S, "CDP-LRN-FACTORS": S, "KTET-CDP-ADOLESCENT": S,
    # Level 1 Maths and EVS (themes identical to CTET Paper 1 in the summary)
    "MATH-P1-CONT-GEOM": S, "MATH-P1-CONT-SOLIDS": S, "MATH-P1-CONT-NUM": S, "MATH-P1-CONT-ADD-SUB": S,
    "MATH-P1-CONT-MULT": S, "MATH-P1-CONT-DIV": S, "MATH-P1-CONT-MEAS": S, "MATH-P1-CONT-DATA": S,
    "MATH-P1-CONT-PATTERNS": S, "MATH-P1-CONT-MONEY": S,
    "MATH-PED-NATURE": S, "MATH-PED-ERROR": S, "MATH-PED-REMEDIAL": S,
    "EVS-CONT-FAMILY": S, "EVS-CONT-FOOD": S, "EVS-CONT-SHELTER": S, "EVS-CONT-WATER": S, "EVS-CONT-TRAVEL": S,
    "EVS-CONT-THINGS": S, "EVS-PED-SIGNIF": S, "EVS-PED-EXPT": S, "EVS-PED-CCE": S,
}
note = "HTET column: from a pasted summary of unknown source (official bulletin has structure and sample questions only); LOW confidence, verify"
for r in rows:
    if r["topic_id"] in h:
        r["htet"] = h[r["topic_id"]]
        r["confidence"] = "Low"
        r["notes"] = (r["notes"] + "; " if r["notes"] else "") + note

extra = [
    ("HTET-CDP-NAMED-THEORIES", "Child Development and Pedagogy", "Named-theory depth: laws of heredity, intelligence tests (Koh, Pass-along, Stanford-Binet), Sternberg triarchic theory, Thorndike laws, Pavlov conditioning, Kohlberg stages, motivation theorists (Atkinson, Maslow, Woodworth, McClelland), Gagne learning levels, adolescent development", "Child Development"),
    ("HTET-GS-QUANT", "General Studies (HTET)", "Quantitative aptitude (10 marks): number system, percentage, profit and loss, interest, average, time and work, algebra, mensuration", "General Studies"),
    ("HTET-GS-REASONING", "General Studies (HTET)", "Reasoning ability (10 marks): verbal and non-verbal reasoning, analogies, syllogism, blood relations, coding-decoding, Venn diagrams", "General Studies"),
    ("HTET-GS-HARYANA-GK", "General Studies (HTET)", "Haryana GK and awareness (10 marks): history, geography, culture, polity, economy, schemes, current affairs", "General Studies"),
    ("HTET-LANG-GRAMMAR", "Languages (HTET)", "Hindi and English grammar and vocabulary (15 + 15 marks)", "Content"),
    ("HTET-L2-L3-SUBJECT", "Subject-specific (HTET)", "Level 2 (classes 6-10 syllabus) and Level 3 (classes 9-12, up to post-graduate depth) concerned-subject content, 60 marks", "Subject"),
]
for tid, subj, topic, sub in extra:
    row = {h_: "" for h_ in hdr}
    row.update(topic_id=tid, subject=subj, topic=topic, subtopic=sub, htet=S, source_ref="HTET-2025 bulletin pp.13-16 (marks); Level 2 sample paper Q1-60 (CDP, languages); other topic lists from an unverified summary",
               confidence="Low", verified_by_me="N", notes="HTET-specific; the 30-mark General Studies block and the structure are verified in the bulletin, the topic lists are not")
    rows.append(row)

with open("master-topics.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    w.writerows(rows)
p1 = [r for r in rows if r["ctet_p1"] and not r["topic_id"].startswith(("KTET-", "REET-", "MPTET-", "UPTET-", "HTET-"))]
print("HTET Level 1 vs CTET P1: assessed", sum(1 for r in p1 if r["htet"]), "of", len(p1),
      "| matched", sum(1 for r in p1 if r["htet"] in (S, SIM)))

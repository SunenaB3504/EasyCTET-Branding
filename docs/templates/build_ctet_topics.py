"""Builds the CTET rows of master-topics.csv from CTET Sep 2026 bulletin, Appendix I."""
import csv

rows = []
A = "CTET Sep 2026 bulletin, Appendix I"


def add(tid, subj, topic, sub, p1, p2, note=""):
    rows.append([tid, subj, topic, sub, "Y" if p1 else "", "Y" if p2 else ""] + [""] * 10 + [A, "High", "N", note])


cdp = [
    ("DEV", "Child Development", "Concept of development and its relationship with learning", "CONCEPT"),
    ("DEV", "Child Development", "Principles of the development of children", "PRINCIPLES"),
    ("DEV", "Child Development", "Influence of heredity and environment", "HEREDITY-ENV"),
    ("DEV", "Child Development", "Socialization processes: teacher, parents, peers", "SOCIALIZATION"),
    ("DEV", "Child Development", "Piaget, Kohlberg and Vygotsky: constructs and critical perspectives", "THEORISTS"),
    ("DEV", "Child Development", "Child-centered and progressive education", "PROGRESSIVE-ED"),
    ("DEV", "Child Development", "Critical perspective of the construct of intelligence", "INTELLIGENCE"),
    ("DEV", "Child Development", "Multi-dimensional intelligence", "MULTI-INTEL"),
    ("DEV", "Child Development", "Language and thought", "LANG-THOUGHT"),
    ("DEV", "Child Development", "Gender as a social construct; gender roles and bias", "GENDER"),
    ("DEV", "Child Development", "Individual differences; diversity of language, caste, gender, community, religion", "INDIV-DIFF"),
    ("DEV", "Child Development", "Assessment for learning vs of learning; school-based assessment, CCE", "ASSESSMENT"),
    ("DEV", "Child Development", "Formulating questions to assess readiness, learning and critical thinking", "QUESTIONING"),
    ("INCL", "Inclusive education and special needs", "Learners from diverse, disadvantaged and deprived backgrounds", "DIVERSE"),
    ("INCL", "Inclusive education and special needs", "Children with learning difficulties and impairment", "LD-IMPAIR"),
    ("INCL", "Inclusive education and special needs", "Talented, creative and specially abled learners", "TALENTED"),
    ("LRN", "Learning and Pedagogy", "How children think and learn; why children fail in school", "THINK-LEARN"),
    ("LRN", "Learning and Pedagogy", "Basic processes of teaching and learning; learning as a social activity", "T-L-PROCESS"),
    ("LRN", "Learning and Pedagogy", "Child as problem solver and scientific investigator", "PROBLEM-SOLVER"),
    ("LRN", "Learning and Pedagogy", "Alternative conceptions; errors as steps in learning", "ERRORS"),
    ("LRN", "Learning and Pedagogy", "Cognition and emotions", "COG-EMO"),
    ("LRN", "Learning and Pedagogy", "Motivation and learning", "MOTIVATION"),
    ("LRN", "Learning and Pedagogy", "Factors contributing to learning: personal and environmental", "FACTORS"),
]
for g, sub, t, k in cdp:
    add(f"CDP-{g}-{k}", "Child Development and Pedagogy", t, sub, 1, 1, "Same list in both papers; P1 age 6-11, P2 age 11-14")

lang_ped = [
    ("ACQ", "Learning and acquisition"),
    ("PRINC", "Principles of language teaching"),
    ("LISTEN-SPEAK", "Role of listening and speaking; functions of language"),
    ("GRAMMAR", "Critical perspective on role of grammar"),
    ("DIVERSE", "Teaching language in a diverse classroom; difficulties, errors, disorders"),
    ("SKILLS", "Language skills"),
    ("EVAL", "Evaluating comprehension and proficiency"),
    ("TLM", "Teaching-learning materials"),
    ("REMEDIAL", "Remedial teaching"),
]
for L, lab in (("L1", "Language I"), ("L2", "Language II")):
    note = "L1: one prose/drama + one poem" if L == "L1" else "L2: two prose passages"
    add(f"LANG-{L}-COMP", lab, "Comprehension: unseen passages, inference, grammar, verbal ability", "Comprehension", 1, 1,
        note + ". Actual language depends on candidate choice")
    for k, t in lang_ped:
        add(f"LANG-{L}-PED-{k}", lab, t, "Pedagogy of Language Development", 1, 1)

for k, t in (("GEOM", "Geometry; shapes and spatial understanding"), ("SOLIDS", "Solids around us"), ("NUM", "Numbers"),
             ("ADD-SUB", "Addition and subtraction"), ("MULT", "Multiplication"), ("DIV", "Division"),
             ("MEAS", "Measurement: weight, time, volume"), ("DATA", "Data handling"), ("PATTERNS", "Patterns"),
             ("MONEY", "Money")):
    add(f"MATH-P1-CONT-{k}", "Mathematics (Paper 1)", t, "Content", 1, 0)
for k, t in (("NUMSYS", "Number system: numbers, whole numbers, integers, fractions"),
             ("ALGEBRA", "Algebra: introduction, ratio and proportion"),
             ("GEOM", "Geometry: basic ideas, shapes, symmetry, construction, mensuration"),
             ("DATA", "Data handling")):
    add(f"MATH-P2-CONT-{k}", "Mathematics (Paper 2)", t, "Content", 0, 1)
for k, t, p1, p2, n in (
        ("NATURE", "Nature of mathematics / logical thinking", 1, 1, ""),
        ("PLACE", "Place of mathematics in curriculum", 1, 1, ""),
        ("LANGUAGE", "Language of mathematics", 1, 1, ""),
        ("COMMUNITY", "Community mathematics", 1, 1, ""),
        ("EVAL", "Evaluation", 1, 1, ""),
        ("PROBLEMS", "Problems of teaching", 1, 1, ""),
        ("REMEDIAL", "Diagnostic and remedial teaching", 1, 1, "P1 says diagnostic and remedial; P2 says remedial teaching"),
        ("ERROR", "Error analysis", 1, 0, "")):
    add(f"MATH-PED-{k}", "Mathematics", t, "Pedagogical issues", p1, p2, n)

for k, t in (("FAMILY", "Family and friends: relationships, work and play, animals, plants"), ("FOOD", "Food"),
             ("SHELTER", "Shelter"), ("WATER", "Water"), ("TRAVEL", "Travel"), ("THINGS", "Things we make and do")):
    add(f"EVS-CONT-{k}", "Environmental Studies", t, "Content", 1, 0)
for k, t in (("CONCEPT", "Concept and scope of EVS"), ("SIGNIF", "Significance of EVS, integrated EVS"),
             ("EE", "EVS and environmental education"), ("PRINC", "Learning principles"),
             ("RELATION", "Scope and relation to science and social science"),
             ("APPROACH", "Approaches of presenting concepts"), ("ACTIVITIES", "Activities"),
             ("EXPT", "Experimentation / practical work"), ("DISC", "Discussion"), ("CCE", "CCE"),
             ("AIDS", "Teaching material / aids"), ("PROBLEMS", "Problems")):
    add(f"EVS-PED-{k}", "Environmental Studies", t, "Pedagogical issues", 1, 0)

for k, t in (("FOOD", "Food: sources, components, cleaning"), ("MATERIALS", "Materials of daily use"),
             ("LIVING", "The world of the living"), ("MOVING", "Moving things, people and ideas"),
             ("HOW", "How things work: electric current, circuits, magnets"),
             ("NATURAL-PHEN", "Natural phenomena"), ("NATURAL-RES", "Natural resources")):
    add(f"SCI-CONT-{k}", "Science (Paper 2)", t, "Content", 0, 1)
for k, t in (("NATURE", "Nature and structure of sciences"), ("AIMS", "Natural science: aims and objectives"),
             ("UNDERSTAND", "Understanding and appreciating science"), ("APPROACH", "Approaches / integrated approach"),
             ("METHOD", "Observation, experiment, discovery"), ("INNOV", "Innovation"),
             ("AIDS", "Text material / aids"), ("EVAL", "Evaluation: cognitive, psychomotor, affective"),
             ("PROBLEMS", "Problems"), ("REMEDIAL", "Remedial teaching")):
    add(f"SCI-PED-{k}", "Science (Paper 2)", t, "Pedagogical issues", 0, 1)

groups = {
    "HIST": ("History", ["When, where and how", "Earliest societies", "First farmers and herders", "First cities",
                         "Early states", "New ideas", "First empire", "Contacts with distant lands",
                         "Political developments", "Culture and science", "New kings and kingdoms",
                         "Sultans of Delhi", "Architecture", "Creation of an empire", "Social change",
                         "Regional cultures", "Establishment of company power", "Rural life and society",
                         "Colonialism and tribal societies", "Revolt of 1857-58", "Women and reform",
                         "Challenging the caste system", "Nationalist movement", "India after independence"]),
    "GEO": ("Geography", ["Geography as a social study and science", "Planet Earth in the solar system", "Globe",
                          "Environment: natural and human", "Air", "Water",
                          "Human environment: settlement, transport, communication", "Resources: natural and human",
                          "Agriculture"]),
    "POL": ("Social and Political Life", ["Diversity", "Government", "Local government", "Making a living", "Democracy",
                                          "State government", "Understanding media", "Unpacking gender",
                                          "The Constitution", "Parliamentary government", "The Judiciary",
                                          "Social justice and the marginalised"]),
    "PED": ("Pedagogical issues", ["Concept and nature of social science", "Classroom processes, activities and discourse",
                                   "Developing critical thinking", "Enquiry / empirical evidence",
                                   "Problems of teaching", "Sources: primary and secondary", "Project work",
                                   "Evaluation"]),
}
for code, (sub, items) in groups.items():
    for i, t in enumerate(items, 1):
        add(f"SST-{code}-{i:02d}", "Social Studies (Paper 2)", t, sub, 0, 1)

hdr = ("topic_id,subject,topic,subtopic,ctet_p1,ctet_p2,ktet_c1,ktet_c2,ktet_c3,ktet_c4,uptet,reet_l1,reet_l2,htet,"
       "bihar_stet,mptet,source_ref,confidence,verified_by_me,notes").split(",")
with open("master-topics.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(hdr)
    w.writerows(rows)
print(len(rows), "rows")

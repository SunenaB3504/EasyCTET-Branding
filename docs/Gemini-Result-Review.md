# Review of Gemini Deep Research output (Part 1/2/3 combined), 2026-10-01

Reviewed against the official documents saved in `docs/syllabi/`. Verdict: useful for leads, NOT usable as published facts or as the overlap matrix.

## Checked and consistent with official documents
- CTET: 150 Q / 150 marks / 150 min, no negative marking, section splits, lifetime validity (CTET Sept 2026 bulletin).
- KTET: structure of Categories 1-4, 60% / 55% / 50% pass marks, no negative marking, 150 min (KTET Sept 2026 notification, read as page images).
- HTET: no negative marking; Level 1 has General Studies 30 (Quant 10, Reasoning 10, Haryana GK 10); 60% (90) general. Checked only against the HTET-2022 bulletin on bseh.org.in (old).

## Contradicted by official documents
- CTET reserved-category pass mark "55% (82.5)" marked VERIFIED. The CTET Sept 2026 bulletin gives only 60% and leaves concessions to each school's reservation policy. Do not publish a CTET reserved cutoff without an official source.

## Marked VERIFIED but not verified
- KTET "Lifetime" validity: not seen in the notification pages read (section 20 pages 27-29 only mention certificate distribution).
- Most "VERIFIED" tags cite coaching sites, news and a YouTube video (see source list). Only a few sources are official.
- UPTET, Bihar STET, MPTET, REET, HTET details: no official PDF was opened by Gemini that we can confirm.

## Not usable as delivered
- Overlap matrix has about 17 rows, renames topic IDs (e.g. CDP-DEV-THEORY vs our CDP-DEV-THEORISTS), mixes N/A with Not found, and merges many topics into one row.
- Overlap percentages (86%, 93%, 74% ...) rest on "~30 nodes" counts with no table behind them. Do not publish.
- Claim "UPTET nearly abandons language and maths pedagogy" is unsupported and conflicts with its own Task 1 table (UPTET shown with the same CDP/Language/Maths/EVS split as CTET).
- Bihar STET is a secondary-level exam (classes 9-12), not comparable with CTET Paper 1/2. Exclude from the overlap map.

## High-impact claims that need official confirmation before use on the site
1. Supreme Court rulings (B.Ed vs D.El.Ed for primary posts; NIOS ODL D.El.Ed; TET mandatory for in-service teachers). Read the judgments or a reliable legal summary; describe eligibility only as the exam bulletin states it.
2. REET "5th option" and 1/3 penalty for blank answers. Check the BSER December 2024 notification itself.
3. MPTET negative marking withdrawn (source was a YouTube video).
4. CTET language list expanded from 20 to 27 (check bulletin).
5. "Lifetime validity" for UPTET, REET, HTET, Bihar STET.
6. Question-paper reuse: "no terms found" is not permission. Needs a proper rights check per board before publishing any PYQ.

## Usable as seeds
- The 20 search queries in Task 7 (English and Hindi) as a starting keyword list; confirm demand in Search Console.
- The idea of covering eligibility changes and marking-scheme changes alongside the overlap table (a real gap), once verified.

## Next actions
- Open each state's official bulletin (UPTET, REET Level 1/2, HTET current cycle, MPTET Varg 2/3) and read it directly.
- Build overlap columns from those documents using the existing topic IDs in `templates/master-topics.csv`.

## Update: REET checked against the official REET-2024 notification (read 2026-10-01)
- Pattern matches CTET: Level 1 = CDP 30, Language I 30, Language II 30, Maths 30, EVS 30; Level 2 = CDP 30, Lang I 30, Lang II 30, Section IV 60. 150 minutes, 150 marks.
- Gemini's "5th option" claim is mostly right but incomplete: no negative marking for wrong answers; a blank (no option of five marked) loses 1/3 mark; more than 10% blank questions makes the candidate ineligible.
- Pass marks: General 60%; SC/OBC/MBC/EWS 55%; ST 55% (non-TSP) / 36% (TSP); widows, divorced women, ex-servicemen 50%; PwD 40%. Gemini's list was partial.
- Lifetime validity confirmed (Rajasthan govt letter 16.03.2022).
- Eligibility: Level 1 lists D.El.Ed, B.El.Ed, special-education diploma, or graduate + 2-year elementary diploma; a plain B.Ed is not listed for Level 1 (a 12.08.2024 govt letter mentions B.Ed (Child Development) holders, unclear wording - verify). A note says NIOS D.El.Ed (ODL) holders (untrained in-service teachers) may appear for Level 1, which differs from Gemini's "NIOS invalid" framing; recruitment eligibility is decided separately at hiring time.
- The notification does not contain the syllabus; the syllabus is on the REET site (a Level 2 Maths/Science file there is dated 2016).

## Update: MPTET checked against MPESB rulebook 2026 (read 2026-10-01)
- The only current MPESB teacher-eligibility document is the 2026 test for IN-SERVICE primary and middle teachers (Supreme Court order of 1 Sept 2025, civil appeals 1385/1386 of 2025). Exam from 12 Oct 2026. The result is not valid for direct recruitment.
- Gemini described "MPTET Varg 1/2/3" as current; the rulebook list on esb.mp.gov.in shows no Varg-style TET for 2026. Do not publish Varg claims without an official source.
- Primary exam: 150 questions, 150 marks, 150 minutes, no negative marking (stated: ऋणात्मक मूल्यांकन नहीं); pass 60% (others), 50% (SC/ST/OBC/PwD/EWS). Matches Gemini's "no negative marking" but not the framing.
- Syllabus text for CDP and Language II is almost word for word the CTET text (Piaget/Pavlov/Kohler/Thorndike replace Vygotsky in the theorists line).
- Supreme Court in-service TET order: confirmed text in rulebook (teachers with over 5 years' service left must qualify; deadline extended to 31 Aug 2028 on review). That part of Gemini's claim is supported.

## Update: UPTET checked against the UPESSC syllabus PDFs supplied by the user (read 2026-10-01)
- Structure confirmed: 150 MCQs, 150 marks, 150 minutes, no negative marking; Paper 1 = CDP 30, Hindi 30, Language II 30, Maths 30, EVS 30; Paper 2 = CDP 30, Hindi 30, Language II 30, Maths+Science 60 or Social Studies 60.
- Gemini's claim that UPTET "nearly abandons language pedagogy" and "minimizes maths pedagogy" is FALSE: the Hindi syllabus has a full 'Pedagogy of language development' list (acquisition, principles, listening and speaking, grammar, diverse classroom, skills, evaluation, TLM, remedial) and maths lists nature of maths, place in curriculum, language of maths, community maths, evaluation, problems of teaching, error analysis, remedial teaching - the same items as CTET. (English/Urdu Language II lists content only.)
- UPTET CDP is more theory-heavy (Thorndike, Pavlov, Skinner, Kohler, Piaget, Vygotsky) and detailed on inclusive education, but has no assessment/CCE, intelligence or progressive-education items.
- Cutoffs, validity and notification dates are NOT in these PDFs; Gemini's "55% (82) reserved" and "lifetime" for UPTET remain unverified.

## Update: HTET checked against the HTET-2025 Information Bulletin (read 2026-10-01)
- Confirmed: 150 MCQs / 150 marks / 150 minutes, no negative marking; Level 1 = CDP 30, Languages 30 (Hindi 15 + English 15), General Studies 30 (Quantitative 10, Reasoning 10, Haryana GK 10), Maths 30, EVS 30; Level 2 = CDP 30, Languages 30, General Studies 30, Subject-specific 60; lifetime validity; 60% (90) General, 55% (82) SC and differently abled of Haryana domicile (60% for those of other states).
- Gemini's overall HTET picture was right. Its extra "Haryana GK 10 marks" is correct; "up to 30 marks" is the whole General Studies block, not Haryana GK alone.
- The bulletin gives no topic-level syllabus: it says questions follow NCERT/Haryana textbooks for the class level (difficulty up to secondary or senior secondary). So the HTET column in master-topics.csv stays blank; only a structural comparison is possible. HTET-2026 is only announced (no dates).

## Update: HTET topic-level summary supplied by the user (2026-10-01)
- A pasted HTET summary lists topics (CDP incl. Piaget, Kohlberg, Vygotsky, Thorndike, Pavlov, Skinner; Hindi/English grammar lists; General Studies sub-topics; Level 1 Maths and EVS themes). Its source is not stated.
- Verified against the official HTET-2025 bulletin (all 37 pages checked for a syllabus): structure, marks, qualifying marks, age groups per level (6-11, 11-16, 14-17), Level 2 syllabus classes VI-X and Level 3 classes IX-XII all match. The bulletin itself has NO topic list: Annexure-I contains sample questions only.
- So the topic lists in the summary are UNVERIFIED. They are recorded in master-topics.csv (htet column) at LOW confidence and must not be published until a BSEH syllabus page or document is found.
- If the summary is right, HTET Level 1 Maths and EVS content are identical to CTET Paper 1, and the main extra work is the 30-mark General Studies block (quantitative aptitude, reasoning, Haryana GK), which is in the official structure.

## Update: HTET evidence from the board's own past paper (2026-10-01)
- Source of the pasted HTET summary: a Gemini search that cites coaching sites; no official level-wise syllabus PDF exists on bseh.org.in or the HTET portal (only bulletins, notices, sample papers and answer keys).
- Read: HTET TGT (Level 2) Mathematics Set A, 2023 sample paper (docs/syllabi/htet_papers/). Pages 3-15, Q1-60.
- CDP (Q1-30) is heavy on named theories and psychology: laws of heredity; intelligence tests (Koh's block design, Alexander's pass-along, Stanford-Binet); Piaget moral development and concrete operations; Vygotsky/Bruner; Kohlberg's stages; Pavlov's conditioning; Thorndike's laws; motivation theorists (Atkinson, Maslow, Woodworth, McClelland); Gagne's learning levels; Sternberg's triarchic theory; adolescent development; inclusive education, learning difficulties (dyslexia), CCE and progressive education.
- Languages (Q31-60) are PURE grammar and vocabulary: Hindi (antonyms, samas, sandhi, idioms, pronouns, prefixes) and English (voice, phrasal verbs, modals, narration, tenses, prepositions, one-word substitution). No language-pedagogy questions in this paper, so the pasted summary's 'pedagogy of language development' line is not supported by it.
- Limits: Level 2 only (not Level 1), one paper, subject questions and General Studies (Q61-90) not read. Conclusions for Level 1 remain an inference.

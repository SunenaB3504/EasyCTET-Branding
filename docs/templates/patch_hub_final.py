"""Final patch for build_page_hub.py (3 Oct 2026): removes the draft box and every [EDITOR] note, records the
spot-check, adds the 'Does CTET count here?' row from official recruitment notices, a site header, canonical URL,
the app call-to-action and a linked sources list."""
p = "build_page_hub.py"
s = open(p, encoding="utf-8").read()


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


# HTET has no official topic list, so its computed label is shown as "Likely", not as a measured result.
sub('''    print(name, lab[name], [round(v, 2) if v is not None else None for v in (p1, p2)])
''', '''    print(name, lab[name], [round(v, 2) if v is not None else None for v in (p1, p2)])
lab["HTET"] = ("Likely high", "Structure only")
''')

PLAY = "https://play.google.com/store/apps/details?id=com.easyctet.app&amp;referrer=utm_source%3Dweb%26utm_medium%3Dseo%26utm_campaign%3Dcompare-all-tets"

accepted_row = '''accepted_row = ('<tr id="ctet-accepted"><th>Does CTET count here?</th>'
    '<td>Accepted by central schools such as KVS and NVS. Marks needed by category: <a href="/ctet/passing-marks/">CTET passing marks by employer</a></td>'
    '<td><strong>Partly.</strong> CTET Paper 1 replaces KTET Category 1 (LP posts) and Paper 2 replaces Category 2 (UP posts). Not accepted in place of Category 3.</td>'
    '<td><strong>Yes, for primary.</strong> UP\\'s 2026 assistant teacher (primary) recruitment accepts a TET held by the state or the Government of India, so UPTET or CTET for classes 1–5.</td>'
    '<td><strong>No.</strong> RSSB\\'s 2025 primary and upper primary teacher recruitment asked for REET (2022 or 2025).</td>'
    '<td><strong>No, for fresh primary posts.</strong> The Primary Teacher Selection Test 2025 was open only to those who passed MP\\'s own primary teacher eligibility test (2020 or 2024).</td>'
    '<td><strong>Not in recent notices.</strong> HSSC\\'s primary teacher recruitment (Advt. 05/2024) asked for HTET/STET.</td></tr>')
'''
sub('''overlap_row = "<tr><th>Syllabus carry-over from CTET</th><td>–</td>"''',
    accepted_row + '''overlap_row = "<tr><th>Syllabus carry-over from CTET</th><td>–</td>"''')
sub('''<tbody>{overlap_row}{mrow}</tbody>''', '''<tbody>{accepted_row}{overlap_row}{mrow}</tbody>''')
sub('''<p class="note">Syllabus carry-over compares the topics we checked (Very high, High, Partial, Low). Where a column says "Structure only", the board publishes no topic list. Eligibility rules differ by exam and change; read the official bulletin before you apply.</p>''',
    '''<p class="note">"Does CTET count here?" is taken from each state's latest teacher recruitment notice we could find (listed under Sources). Syllabus carry-over compares the topics we checked (Very high, High, Partial, Low). HTET is marked "Likely" because the board publishes no topic list. Eligibility rules differ by exam and change; read the official notice before you apply.</p>''')

# Head: description date, canonical, header styles.
sub('''Built from the official bulletins. Last verified 1 October 2026.">''',
    '''Built from the official bulletins. Last checked 3 October 2026.">
<link rel="canonical" href="https://easyctet.com/compare-all-tets.html">''')
sub('''.cat3{{border:1px solid var(--line);border-radius:10px;padding:12px 16px;background:var(--soft)}}''',
    '''.cat3{{border:1px solid var(--line);border-radius:10px;padding:12px 16px;background:var(--soft)}}
header.site{{border-bottom:1px solid var(--line)}} header.site div{{max-width:900px;margin:0 auto;padding:12px 16px}} header.site a{{font-weight:800;font-size:1.05rem;color:var(--fg);text-decoration:none}}
.cta{{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;padding:10px 22px;border-radius:8px;font-weight:700}}
@media (prefers-color-scheme:dark){{.cta{{color:#0b1e3f}}}}''')

# Body top: header, no draft box, byline.
sub('''</style></head><body><main>
<div class="draft"><strong>DRAFT v4, not for publishing.</strong> The overlap labels come from a first-pass mapping that has not been spot-checked. Remove this box and the [EDITOR] notes before publishing.</div>
''', '''</style></head><body>
<header class="site"><div><a href="/">EasyCTET</a></div></header>
<main>
''')
sub('''<p class="note">Last verified: 1 October 2026 · From the official bulletins and syllabus documents of each exam board.</p>''',
    '''<p class="note">By EasyCTET Research Team · Last checked: 3 October 2026 · From the official bulletins, syllabus documents and recruitment notices of each exam board.</p>''')

# Method notes: record the spot-check instead of the editor notes.
sub(''' because the board publishes no topic list. [EDITOR: after the spot-check, re-run and re-check these numbers.]</p>''',
    ''' because the board publishes no topic list. Spot-check, 3 October 2026: every child-development topic for KTET Category 1, UPTET Paper 1 and REET Level 1, plus a random sample of subject topics, was re-read against the official syllabus; the mapping held, with one borderline call.</p>''')
sub(''' That is the main CDP gap between CTET and the state exams. [EDITOR: add the survey line here only if you decide to cite it, for example "14 of 20 KTET teachers we surveyed named CDP as their hardest area".]</p>''',
    ''' That is the main CDP gap between CTET and the state exams.</p>''')
sub('''using the official syllabus. First-pass labels. Open an exam card''', '''using the official syllabus. Open an exam card''')
sub('''<div class="stat"><b>Most</b>of that pedagogy appears in near-identical wording in KTET, UPTET, REET and MPTET. Exceptions are noted below.</div>''',
    '''<div class="stat"><b>Same wording</b>KTET and MPTET reuse much of CTET's child-development text, and UPTET's learning section is a Hindi version of it. REET covers the same ground in its own words. Exceptions are noted below.</div>''')
sub('''<p class="note">Counts from CTET September 2026 Information Bulletin, Appendix I. [EDITOR: re-check the "near-identical wording" claim after the spot-check.]</p>''',
    '''<p class="note">Counts from CTET September 2026 Information Bulletin, Appendix I.</p>''')

# App call-to-action instead of the coverage placeholder.
sub('''<p>[EDITOR: add the real app coverage per exam here once the question bank is tagged, for example "EasyCTET covers X of Y topics for UPTET Paper 1". Add the Play Store link with a tagged URL. No sign-up, no phone number, works offline.]</p>''',
    f'''<p>EasyCTET works offline, with no sign-up and no phone number. <a class="cta" href="{PLAY}">Get EasyCTET on Google Play</a></p>''')

# FAQ answer.
sub('''<p>That depends on the state and the recruiting body. Each state decides which TET it accepts. Check the recruitment notice.</p>''',
    '''<p>It depends on the state. CTET counts for UP primary posts and, in Kerala, in place of KTET Category 1 and 2. Rajasthan, Madhya Pradesh and Haryana asked for their own TET in their latest recruitment. See the <a href="#ctet-accepted">"Does CTET count here?" row</a> above, and always check the recruitment notice you are applying under.</p>''')

# Linked sources.
sub('''<ul class="note"><li>CBSE, CTET September 2026 Information Bulletin.</li><li>Kerala Pareeksha Bhavan, K-TET September 2026 notification and Category I–IV syllabus documents.</li><li>UPESSC, UPTET syllabus documents (Primary and Upper Primary).</li><li>Board of Secondary Education Rajasthan, REET-2024 notification and syllabus files.</li><li>MP Employees Selection Board, 2026 eligibility test rulebook for in-service teachers.</li><li>Board of School Education Haryana, HTET-2025 Information Bulletin.</li></ul>''',
    '''<p class="note"><strong>Syllabus and exam documents</strong></p>
<ul class="note"><li>CBSE, <a href="https://cdnbbsr.s3waas.gov.in/s3443dec3062d0286986e21dc0631734c9/uploads/2026/05/202605111250310617.pdf">CTET September 2026 Information Bulletin</a>.</li>
<li>Kerala Pareeksha Bhavan, <a href="https://ktet.kerala.gov.in/downloads/sep2026/K-TET%20September%202026-Notification.pdf">K-TET September 2026 notification</a> and Category <a href="https://ktet.kerala.gov.in/syllabus/syllabus1.pdf">I</a>, <a href="https://ktet.kerala.gov.in/syllabus/syllabus2.pdf">II</a>, <a href="https://ktet.kerala.gov.in/syllabus/syllabus3.pdf">III</a> and <a href="https://ktet.kerala.gov.in/syllabus/syllabus4.pdf">IV</a> syllabus documents.</li>
<li>UPESSC, UPTET syllabus documents, Primary and Upper Primary (<a href="https://upessc.up.gov.in/">upessc.up.gov.in</a>).</li>
<li>Board of Secondary Education Rajasthan, <a href="https://rajeduboard.rajasthan.gov.in/reet2024final121224.PDF">REET-2024 notification</a> and syllabus files.</li>
<li>MP Employees Selection Board, <a href="https://esb.mp.gov.in/rulebooks/RB_2026/MSPSTET_2026_RuleBookforTeachers_17082026.pdf">2026 eligibility test rulebook for in-service teachers</a>.</li>
<li>Board of School Education Haryana, <a href="https://htet.eapplynow.com/HTET25_InfoBulletin.pdf">HTET-2025 Information Bulletin</a>.</li></ul>
<p class="note"><strong>Recruitment notices behind "Does CTET count here?"</strong></p>
<ul class="note"><li>Kerala PSC, <a href="https://keralapsc.gov.in/sites/default/files/2025-08/noti-239-241-25.pdf">L P School Teacher notification, Category No. 239–241/2025</a>, citing G.O.(P) No. 6/2024/G.Edn dated 01.02.2024.</li>
<li>UPESSC, <a href="https://upessc.up.gov.in/Notice/a429-726e-4862-f3dc-8a6f.pdf">Assistant Teacher (Primary) Selection Examination 2026, Advt. No. 05/2026</a>, clause 7.</li>
<li>Rajasthan Staff Selection Board, Primary and Upper Primary School Teacher recruitment 2025 (<a href="https://rssb.rajasthan.gov.in/">rssb.rajasthan.gov.in</a>).</li>
<li>MP Employees Selection Board, <a href="https://esb.mp.gov.in/rulebooks/RB_2025/PSTST_2025_Final_RuleBook.pdf">Primary Teacher Selection Test 2025 rulebook</a>.</li>
<li>Haryana Staff Selection Commission, Primary Teacher (Mewat cadre) recruitment, Advt. No. 05/2024 (<a href="https://hssc.gov.in/">hssc.gov.in</a>).</li>
<li>Central schools: CBSE for KVS and NVS, <a href="https://www.cbse.gov.in/cbsenew/documents/Detailed_Notification_KVS_NVS_2025_13112025.pdf">Recruitment Notification 01/2025</a>.</li></ul>
<p class="note">This page is an independent study aid and is not issued by any exam board.</p>''')

open(p, "w", encoding="utf-8").write(s)
print("patched")

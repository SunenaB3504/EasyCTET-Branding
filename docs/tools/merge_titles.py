#!/usr/bin/env python3
"""
merge_titles.py - merge question titles that you copied BY HAND (Quora, Google, forums) into one clean CSV.

Input: every .txt file in a folder (default docs/research). Format of a file:
    SEARCH: uptet                      <- optional header line: the search you used (can appear several times in a file)
    Some question title?
    Another question title? | no answer yet      <- optional "| note" after a title
    No answer yet                      <- a line that says only this marks the previous title as unanswered
Lines starting with # and blank lines are ignored.

What it does: normalises text, removes duplicates (case, spacing and punctuation ignored), flags near-duplicates,
tags exams mentioned (so single-exam AND combination questions end up together), language, intent group, unanswered
flag, and which searches found each title. Output: aspirant_questions_merged.csv (UTF-8 with BOM).

USAGE:  python merge_titles.py [--input-dir docs/research] [--output aspirant_questions_merged.csv]
"""
from __future__ import annotations

import argparse
import csv
import difflib
import importlib.util
import re
import sys
from collections import OrderedDict
from pathlib import Path

# reuse the cleaning / tagging helpers from the collector script
_spec = importlib.util.spec_from_file_location("collector", Path(__file__).with_name("collect_forum_titles.py"))
_col = importlib.util.module_from_spec(_spec)
sys.modules["collector"] = _col  # needed so the dataclass in that file can be loaded
_spec.loader.exec_module(_col)
clean_text, match_key, detect_language, exams_in = _col.clean_text, _col.match_key, _col.detect_language, _col.exams_in

INTENTS = [  # first match wins
    ("mock tests", r"\bmock\b|test series|practice set"),
    ("compare exams", r"difference between|\bvs\b|similar|easier|tougher|difficult\b|which exam|state tet|which one is best"),
    ("validity / certificate", r"\bvalid|lifetime|certificate|marksheet|score ?card"),
    ("books / material", r"\bbooks?\b|study material|notes\b"),
    ("coaching / apps / channels", r"coaching|institute|\bapp(lication)?\b|channel|website|unacademy|gradeup|educator|telegram|youtube"),
    ("preparation strategy", r"prepar|crack|\bclear\b|qualify|how (do|can|should) (i|you) start|months|\bdays\b|without coaching|good marks|high score|strategy|tips"),
    ("eligibility", r"eligib|\bapply\b|b\.?\s?ed|b\.?\s?tech|b\.?\s?com|graduate|commerce|qualification|maximum age|12th|bsc|mca|d\.?el\.?ed|nios|50%|degree"),
    ("exam info / dates / results", r"\bwhen\b|\bdate|result|notification|how many times|passing marks|syllabus|pattern|latest changes|topper"),
    ("jobs / career", r"\bjobs?\b|salary|\bkvs\b|dsssb|\bpgt\b|prospects|what after|next to|recruit|post\b"),
    ("what is / basics", r"what is|what do you mean|meaning|benefit|why is"),
]


def intent_of(title: str) -> str:
    low = title.lower()
    for name, pat in INTENTS:
        if re.search(pat, low):
            return name
    return "other"


def read_files(folder: Path):
    """yield (title, searches, unanswered) in file order."""
    for f in sorted(folder.glob("*.txt")):
        search = f.stem
        last = None
        for raw in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.upper().startswith("SEARCH:"):
                search = line.split(":", 1)[1].strip() or f.stem
                continue
            if line.lower() == "no answer yet":
                if last is not None:
                    last["unanswered"] = True
                continue
            title, _, note = line.partition(" | ")
            last = {"title": clean_text(title), "search": search, "unanswered": "no answer" in note.lower(),
                    "file": f.name}
            if len(last["title"]) > 8:
                yield last


def merge(folder: Path):
    items: "OrderedDict[str, dict]" = OrderedDict()
    for r in read_files(folder):
        key = match_key(r["title"])
        if not key:
            continue
        it = items.setdefault(key, {"title": r["title"], "searches": [], "unanswered": False, "times_seen": 0, "files": set()})
        it["times_seen"] += 1
        it["unanswered"] = it["unanswered"] or r["unanswered"]
        if r["search"] not in it["searches"]:
            it["searches"].append(r["search"])
        it["files"].add(r["file"])
    keys = list(items)
    rows = []
    for i, k in enumerate(keys):
        it = items[k]
        near = ""
        for k2 in keys[:i]:
            if abs(len(k) - len(k2)) < 12 and difflib.SequenceMatcher(None, k, k2).ratio() >= 0.92:
                near = items[k2]["title"]
                break
        exams = exams_in(it["title"])
        rows.append({
            "title": it["title"], "exams_mentioned": exams, "exam_count": len(exams.split(";")) if exams else 0,
            "intent_group": intent_of(it["title"]), "language": detect_language(it["title"]),
            "no_answer_yet": "yes" if it["unanswered"] else "", "found_by_searches": "; ".join(it["searches"]),
            "times_seen": it["times_seen"], "near_duplicate_of": near, "source": "quora/manual",
        })
    rows.sort(key=lambda r: (-r["exam_count"], r["intent_group"], r["title"].casefold()))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", default=str(Path(__file__).resolve().parent.parent / "research"))
    ap.add_argument("--output", default=None)
    a = ap.parse_args()
    folder = Path(a.input_dir)
    out = Path(a.output) if a.output else folder / "aspirant_questions_merged.csv"
    rows = merge(folder)
    cols = ["title", "exams_mentioned", "exam_count", "intent_group", "language", "no_answer_yet",
            "found_by_searches", "times_seen", "near_duplicate_of", "source"]
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} unique titles written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

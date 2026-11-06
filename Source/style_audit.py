"""Plain-language lint for investor materials.

This does not detect AI authorship, and nothing reliably can on text this short. It removes phrasing that makes a
document read as boilerplate, whoever wrote it: stock AI vocabulary, em dashes, framework labels left on the page.
"""
import re

BANNED = [
    "seamless", "seamlessly", "leverage", "leveraging", "unlock", "unlocks", "unlocking", "empower", "empowers", "empowering",
    "revolutioni", "democrati", "game-chang", "cutting-edge", "state-of-the-art", "state of the art", "best-in-class", "world-class",
    "robust", "holistic", "synerg", "paradigm", "delve", "tapestry", "landscape", "navigate the", "in today's", "ever-evolving",
    "at the intersection", "not just", "more than just", "it's not", "moat", "flywheel", "trojan", "earned secret", "earned insight",
    "self-healing", "zero-hallucination", "zero hallucination", "grounded or silent", "act i", "act ii", "north star", "supercharge",
    "next-generation", "next-gen", "mission-critical", "massive", "pitch perfect", "pitch-perfect", "institutional-grade", "unparalleled", "transformative",
]
RX = [(w, re.compile(r"(?<![a-z])" + re.escape(w), re.I)) for w in BANNED]


def audit(text):
    out = []
    for w, rx in RX:
        if rx.search(text):
            out.append(f"stock phrase {w!r}")
    if "—" in text:
        out.append(f"{text.count('—')} em dash(es)")
    for ch in "→●◐○✓✔":
        if ch in text:
            out.append(f"symbol {ch!r}")
    return out


if __name__ == "__main__":
    import sys
    from pathlib import Path
    for f in sys.argv[1:]:
        print(f, audit(Path(f).read_text()) or "clean")

# Build HANDOVER.html: handover body + project documents verbatim as appendices, figures embedded.
# Run with: python3 -I scripts/04_build_handover.py   (needs pandoc >= 2.19)
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts" / "handover_source.md"

def demote(text, levels=1):
    # shift markdown headings down so appendices nest under "Appendices"
    return re.sub(r"(?m)^(#{1,5}) ", lambda m: "#" * (len(m.group(1)) + levels) + " ", text)

appendices = [
    ("A", "Code summary, run 1 (four jurisdictions)", "SUMMARY.md"),
    ("B", "Code summary, run 2 (multiverse and cause split)", "SUMMARY_multiverse.md"),
    ("C", "Novelty review and verified policy facts", "00_novelty.md"),
    ("D", "Frozen multiverse specification list", "multiverse_specs.md"),
    ("E", "Decision log (DECISIONS.md)", "DECISIONS.md"),
    ("F", "Literature search log", "literature_log.md"),
]
parts = [(ROOT / "scripts" / "handover_body.md").read_text()]
for letter, title, f in appendices:
    parts.append(f"\n\n## Appendix {letter}. {title}\n\n*Source file: `{f}`*\n\n" + demote((ROOT / f).read_text(), 2))
codes = (ROOT / "outcome_codes.csv").read_text().strip().splitlines()
table = "| " + " | ".join(codes[0].split(",")) + " |\n|" + "---|" * len(codes[0].split(",")) + "\n"
for line in codes[1:]:
    cells = line.split(",")
    table += "| " + " | ".join([cells[0], cells[1], ",".join(cells[2:-1]), cells[-1]]) + " |\n"
parts.append("\n\n## Appendix G. Outcome ICD-10 codes (outcome_codes.csv)\n\n" + table)
SRC.write_text("\n".join(parts))

css = ROOT / "scripts" / "handover.css"
subprocess.run(["pandoc", str(SRC), "-o", str(ROOT / "HANDOVER.html"), "--standalone", "--embed-resources",
                "--toc", "--toc-depth=2", "--css", str(css), "--resource-path", str(ROOT / "scripts"),
                "--metadata", "lang=en"], check=True)
print("written", ROOT / "HANDOVER.html")

"""Copy the built masters and Keynote PDFs into Investor_Materials and set the PDF properties."""
import shutil
from pathlib import Path

import fitz

HERE = Path(__file__).parent
IM = HERE.parents[1] / "Investor_Materials"
for name, master, title in (("seed", "Anvest_Seed_Deck", "Anvest seed deck, November 2026"), ("partner", "Anvest_Strategic_Integration_Deck", "Anvest: proposed partner pilot")):
    shutil.copyfile(HERE / f"{name}.pptx", IM / f"{master}.pptx")
    d = fitz.open(HERE / f"{name}.pdf")
    meta = dict(d.metadata)
    meta.update(title=title, author="Harsh Bhardwaj", subject="", keywords="")
    d.set_metadata(meta)
    d.save(IM / f"{master}.pdf", garbage=3, deflate=True)
    print(master, d.page_count, "pages")

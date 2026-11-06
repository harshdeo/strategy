"""Second build step: add what pptxgenjs cannot do reliably for Keynote, then set document properties.

usage: finish_deck.py seed.pptx        (flow screenshots, native charts, properties)
       finish_deck.py partner.pptx     (properties only)

The flow screenshots are read from img_flow/ byte for byte, with the crops and geometry the founder set
(flow_images.json). They are placed, never edited.
"""
import datetime as dt
import io
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION, XL_TICK_MARK
from pptx.util import Emu, Inches, Pt

HERE = Path(__file__).parent
INK, MUTE, VIOLET, HAIR, BODY = "14182B", "6A7084", "3A2C88", "E2E4E9", "363C50"
FLOW_SHIFT_UP = 0.58  # inches; the images move with the page, their size and crops do not change
rgb = RGBColor.from_string


def flow_images(slide):
    for rec in json.load(open(HERE / "flow_images.json")):
        if not rec["name"].startswith(("ASK", "pasted-movie")):
            continue  # arrows and the shield icon were decoration, not screenshots
        pic = slide.shapes.add_picture(io.BytesIO((HERE / rec["file"]).read_bytes()), Inches(rec["x"]), Inches(rec["y"] - FLOW_SHIFT_UP), Inches(rec["w"]), Inches(rec["h"]))
        pic.crop_left, pic.crop_top, pic.crop_right, pic.crop_bottom = rec["crop"]
        pic.line.color.rgb = rgb("C9CDD6")
        pic.line.width = Pt(0.75)
        pic.name = {"ASK screenshot image": "Flow screenshot, ask"}.get(rec["name"], "Flow screenshot")


def style_axis_text(ax, size=10, color=MUTE, bold=False):
    ax.tick_labels.font.size = Pt(size)
    ax.tick_labels.font.bold = bold
    ax.tick_labels.font.color.rgb = rgb(color)
    ax.tick_labels.font.name = "Helvetica Neue"


def hide_value_axis(va):
    """Direct labels replace the axis. Keynote ignores delete on an axis, so blank it explicitly."""
    va.has_major_gridlines = False
    va.major_tick_mark = XL_TICK_MARK.NONE
    va.minor_tick_mark = XL_TICK_MARK.NONE
    va.tick_label_position = XL_TICK_LABEL_POSITION.NONE
    va.format.line.fill.background()


def traction_chart(slide, an):
    rows = an["india_weekly"]
    cd = CategoryChartData(number_format="0")
    labels = ["28 Sep", "5 Oct", "12 Oct", "19 Oct", "26 Oct"]
    cd.categories = [f"{l}\n{r['pageviews']:,} views" for l, r in zip(labels, rows)]
    cd.add_series("Visitors from India", [r["visitors"] for r in rows])
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(1.8), Inches(7.4), Inches(3.45), cd)
    gf.name = "Visitors from India per week"
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = False
    ch.font.name = "Helvetica Neue"
    plot = ch.plots[0]
    plot.gap_width = 70
    s = plot.series[0]
    s.format.fill.solid()
    s.format.fill.fore_color.rgb = rgb(VIOLET)
    s.format.line.fill.background()
    dl = s.data_labels
    dl.show_value = True
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(14)
    dl.font.bold = True
    dl.font.color.rgb = rgb(INK)
    va = ch.value_axis
    hide_value_axis(va)
    va.maximum_scale = 360
    va.minimum_scale = 0
    ca = ch.category_axis
    style_axis_text(ca, 10.5, BODY)
    ca.format.line.color.rgb = rgb("C9CDD6")
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW


def scenario_chart(slide, model):
    eng = model["scenario_by_engine_cr"]
    keys, labels = ["M15", "Y2", "Y3", "Y4", "Y5"], ["Month 15", "Year 2", "Year 3", "Year 4", "Year 5"]
    fmt = lambda v: f"₹{round(v * 100)} L" if v < 1 else f"₹{v:.1f} Cr"
    cd = CategoryChartData(number_format="0.0")
    cd.categories = [f"{l}\n{fmt(eng[k]['total'])}" for l, k in zip(labels, keys)]
    series = [("Desk", "desk", "3A2C88", "FFFFFF"), ("Individuals", "retail", "8A80BF", "FFFFFF"),
              ("Partners (conditional)", "partners", "C9CDD6", INK), ("Baskets (conditional)", "strategies", "E9D9BC", INK)]
    for name, key, _, _ in series:
        cd.add_series(name, [eng[k][key] for k in keys])
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(0.6), Inches(1.8), Inches(6.4), Inches(4.7), cd)
    gf.name = "Exit ARR by revenue line"
    ch = gf.chart
    ch.font.name = "Helvetica Neue"
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(10)
    plot = ch.plots[0]
    plot.gap_width = 55
    plot.overlap = 100
    for (name, key, color, text), s in zip(series, plot.series):
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = rgb(color)
        s.format.line.fill.background()
        dl = s.data_labels
        dl.show_value = True
        dl.number_format = '[<1]"";0.0'  # Keynote drops all labels in a series if single ones are deleted
        dl.number_format_is_linked = False
        dl.position = XL_LABEL_POSITION.CENTER
        dl.font.size = Pt(9.5)
        dl.font.color.rgb = rgb(text)
    va = ch.value_axis
    hide_value_axis(va)
    va.minimum_scale = 0
    va.maximum_scale = 28
    ca = ch.category_axis
    style_axis_text(ca, 10.5, INK)
    ca.format.line.color.rgb = rgb("C9CDD6")
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW


def fix_content_types(path):
    """python-pptx can drop the jpg Default; put back any media extension it lost."""
    tmp = str(path) + ".part"
    types = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        ct = zin.read("[Content_Types].xml").decode()
        for ext in {n.rsplit(".", 1)[-1].lower() for n in zin.namelist() if n.startswith("ppt/media/")}:
            if f'Extension="{ext}"' not in ct and ext in types:
                ct = ct.replace("<Default ", f'<Default Extension="{ext}" ContentType="{types[ext]}"/><Default ', 1)
        for item in zin.infolist():
            zout.writestr(item, ct.encode() if item.filename == "[Content_Types].xml" else zin.read(item.filename))
    shutil.move(tmp, path)


def main(path, title, subject):
    prs = Presentation(path)
    if "seed" in Path(path).name:
        an = json.load(open(HERE.parent / "analytics_snapshot_20261101.json"))
        model = json.load(open(HERE / "model.json"))
        slides = list(prs.slides)
        has = lambda s, t: any(sh.has_text_frame and sh.text_frame.text.startswith(t) for sh in s.shapes)
        flow = next(s for s in slides if has(s, "From a question to a tested strategy"))
        traction = next(s for s in slides if has(s, "With no marketing spend"))
        scen = next(s for s in slides if has(s, "Appendix. Long-term scenario"))
        flow_images(flow)
        traction_chart(traction, an)
        scenario_chart(scen, model)
    # Plain names in the selection pane, in place of the generator's "Text 0".
    for slide in prs.slides:
        for sh in slide.shapes:
            if re.fullmatch(r"(Text|Shape|Image|Table|Picture) \d+", sh.name or ""):
                if sh.is_placeholder and sh.placeholder_format.type is not None and "TITLE" in str(sh.placeholder_format.type):
                    sh.name = "Title"
                elif sh.has_text_frame and sh.text_frame.text.strip():
                    sh.name = sh.text_frame.text.strip()[:40]
                else:
                    sh.name = "Rule" if sh.shape_type == 9 else "Slide element"
    cp = prs.core_properties
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None, microsecond=0)
    cp.title, cp.subject = title, subject
    cp.author = cp.last_modified_by = "Harsh Bhardwaj"
    cp.created = cp.modified = now
    cp.keywords, cp.comments, cp.category = "", "", ""
    cp.revision = 1
    prs.save(path)
    fix_content_types(path)
    print("finished", path)


if __name__ == "__main__":
    p = sys.argv[1]
    if "seed" in Path(p).name:
        main(p, "Anvest seed deck, November 2026", "Seed round")
    else:
        main(p, "Anvest: proposed partner pilot", "Partner discussion")

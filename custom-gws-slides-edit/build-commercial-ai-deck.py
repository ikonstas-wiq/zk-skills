#!/usr/bin/env python3
"""
Build the Retail Accelerator Hub — Commercial AI Overview slide deck.
Converts the content from commercial-ai-merged.html into Google Slides
using the wiq brand guidelines.
"""

import json
import subprocess
import sys
import uuid

# ── Brand colours (from brand.md) ──
BERRY = {"red": 145/255, "green": 49/255, "blue": 153/255}
BERRY_50 = {"red": 200/255, "green": 152/255, "blue": 204/255}
BERRY_20 = {"red": 234/255, "green": 216/255, "blue": 236/255}
BERRY_10 = {"red": 249/255, "green": 244/255, "blue": 249/255}
CHARCOAL = {"red": 57/255, "green": 71/255, "blue": 78/255}
WHITE = {"red": 1, "green": 1, "blue": 1}
ULTRAMARINE = {"red": 37/255, "green": 14/255, "blue": 144/255}
OCEAN_BLUE_50 = {"red": 102/255, "green": 197/255, "blue": 255/255}
ALICE_BLUE_10 = {"red": 236/255, "green": 244/255, "blue": 255/255}
LIGHT_GREY_10 = {"red": 241/255, "green": 241/255, "blue": 241/255}

# Spectrum colours from HTML
Q_BLUE = {"red": 63/255, "green": 105/255, "blue": 174/255}
Q_CYAN = {"red": 68/255, "green": 182/255, "blue": 197/255}
Q_TURQUOISE = {"red": 68/255, "green": 213/255, "blue": 163/255}
Q_GREEN = {"red": 128/255, "green": 223/255, "blue": 124/255}
Q_YELLOW = {"red": 234/255, "green": 203/255, "blue": 121/255}
Q_ORANGE = {"red": 239/255, "green": 156/255, "blue": 72/255}
Q_CORAL = {"red": 239/255, "green": 99/255, "blue": 72/255}
Q_BURGUNDY = {"red": 201/255, "green": 100/255, "blue": 120/255}
Q_VIOLET = {"red": 143/255, "green": 115/255, "blue": 190/255}

# EMU helpers
def inches(n): return int(n * 914400)
def pt(n): return int(n * 12700)

SLIDE_W = inches(10)
SLIDE_H = inches(5.625)

# ── Helpers ──
def oid():
    return "id_" + uuid.uuid4().hex[:12]

def rgb(color):
    return {"rgbColor": color}

def solid_fill(color):
    return {"solidFill": {"color": rgb(color)}}

def text_style(font_size=None, bold=False, color=None, font_weight="Light"):
    style = {"fontFamily": "Roboto"}
    if font_size:
        style["fontSize"] = {"magnitude": font_size, "unit": "PT"}
    if bold or font_weight == "Medium":
        style["bold"] = True
    if color:
        style["foregroundColor"] = {"opaqueColor": rgb(color)}
    return style

def para_style(alignment="START", spacing_before=0, spacing_after=0, indent=0):
    style = {"alignment": alignment}
    if spacing_before:
        style["spaceAbove"] = {"magnitude": spacing_before, "unit": "PT"}
    if spacing_after:
        style["spaceBelow"] = {"magnitude": spacing_after, "unit": "PT"}
    if indent:
        style["indentStart"] = {"magnitude": indent, "unit": "PT"}
    return style

_current_page_id = None

def set_current_page(page_id):
    global _current_page_id
    _current_page_id = page_id

def create_shape(shape_id, shape_type, left, top, width, height):
    props = {
        "size": {"width": {"magnitude": width, "unit": "EMU"},
                 "height": {"magnitude": height, "unit": "EMU"}},
        "transform": {
            "scaleX": 1, "scaleY": 1,
            "translateX": left, "translateY": top,
            "unit": "EMU"
        }
    }
    if _current_page_id:
        props["pageObjectId"] = _current_page_id
    return {
        "createShape": {
            "objectId": shape_id,
            "shapeType": shape_type,
            "elementProperties": props
        }
    }

def set_shape_fill(shape_id, color):
    return {
        "updateShapeProperties": {
            "objectId": shape_id,
            "shapeProperties": {
                "shapeBackgroundFill": solid_fill(color)
            },
            "fields": "shapeBackgroundFill.solidFill.color"
        }
    }

def set_shape_outline_none(shape_id):
    return {
        "updateShapeProperties": {
            "objectId": shape_id,
            "shapeProperties": {
                "outline": {"propertyState": "NOT_RENDERED"}
            },
            "fields": "outline.propertyState"
        }
    }

def set_shape_outline(shape_id, color, weight_pt=1):
    return {
        "updateShapeProperties": {
            "objectId": shape_id,
            "shapeProperties": {
                "outline": {
                    "outlineFill": {"solidFill": {"color": rgb(color)}},
                    "weight": {"magnitude": weight_pt, "unit": "PT"}
                }
            },
            "fields": "outline"
        }
    }

def insert_text(shape_id, text, index=0):
    return {
        "insertText": {
            "objectId": shape_id,
            "text": text,
            "insertionIndex": index
        }
    }

def style_text(shape_id, start, end, ts):
    return {
        "updateTextStyle": {
            "objectId": shape_id,
            "textRange": {"type": "FIXED_RANGE", "startIndex": start, "endIndex": end},
            "style": ts,
            "fields": "fontFamily,fontSize,bold,foregroundColor,italic"
        }
    }

def style_para(shape_id, start, end, ps):
    return {
        "updateParagraphStyle": {
            "objectId": shape_id,
            "textRange": {"type": "FIXED_RANGE", "startIndex": start, "endIndex": end},
            "style": ps,
            "fields": "alignment,spaceAbove,spaceBelow,indentStart"
        }
    }

def set_text_padding(shape_id, pad_inches=0.05):
    mag = pad_inches * 72  # points
    return {
        "updateShapeProperties": {
            "objectId": shape_id,
            "shapeProperties": {
                "contentAlignment": "TOP"
            },
            "fields": "contentAlignment"
        }
    }

def create_slide(slide_id):
    set_current_page(slide_id)
    return {"createSlide": {"objectId": slide_id}}

# ── Build a text box with styled text segments ──
def build_textbox(left, top, width, height, segments, shape_type="ROUND_RECTANGLE",
                  fill_color=None, outline_color=None, outline_weight=1,
                  valign="TOP", no_outline=True):
    """
    segments: list of (text, text_style_dict, para_style_dict_or_None)
    Returns (shape_id, list_of_requests)
    """
    sid = oid()
    reqs = [create_shape(sid, shape_type, left, top, width, height)]
    if fill_color:
        reqs.append(set_shape_fill(sid, fill_color))
    if no_outline and not outline_color:
        reqs.append(set_shape_outline_none(sid))
    if outline_color:
        reqs.append(set_shape_outline(sid, outline_color, outline_weight))

    # Content alignment
    reqs.append({
        "updateShapeProperties": {
            "objectId": sid,
            "shapeProperties": {"contentAlignment": valign},
            "fields": "contentAlignment"
        }
    })

    # Build full text and track indices
    full_text = "".join(seg[0] for seg in segments)
    if not full_text:
        return sid, reqs

    reqs.append(insert_text(sid, full_text))

    idx = 0
    for text, ts, ps in segments:
        end = idx + len(text)
        if ts:
            reqs.append(style_text(sid, idx, end, ts))
        if ps:
            reqs.append(style_para(sid, idx, end, ps))
        idx = end

    return sid, reqs


# ══════════════════════════════════════════════════════════
# SLIDE BUILDERS
# ══════════════════════════════════════════════════════════

def slide_title():
    """Slide 1: Title slide"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Berry background
    bg_id = oid()
    reqs.append(create_shape(bg_id, "RECTANGLE", 0, 0, SLIDE_W, SLIDE_H))
    reqs.append(set_shape_fill(bg_id, BERRY))
    reqs.append(set_shape_outline_none(bg_id))

    # Title
    _, r = build_textbox(inches(0.8), inches(1.5), inches(8.4), inches(1.2), [
        ("Retail Accelerator Hub\n", text_style(34, font_weight="Medium", color=WHITE), para_style("START")),
        ("Commercial AI Overview", text_style(19, color=WHITE), para_style("START")),
    ], fill_color=None, no_outline=True)
    reqs.extend(r)

    # Date + tagline
    _, r = build_textbox(inches(0.8), inches(3.4), inches(8.4), inches(0.8), [
        ("Accelerators are repeatable AI workflows.\nMany accelerators form a suite. Many suites form a library.\n", text_style(12, color=BERRY_50), para_style("START", spacing_after=4)),
        ("March 2026", text_style(12, color=WHITE), para_style("START")),
    ], fill_color=None, no_outline=True)
    reqs.extend(r)

    return reqs

def slide_agenda():
    """Slide 2: Agenda"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("Agenda", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    # Thin Berry line under headline
    line_id = oid()
    reqs.append(create_shape(line_id, "RECTANGLE", inches(0.6), inches(1.1), inches(8.8), inches(0.02)))
    reqs.append(set_shape_fill(line_id, BERRY))
    reqs.append(set_shape_outline_none(line_id))

    agenda_items = [
        ("1", "Accelerator Anatomy", "What an accelerator is, how they compose into suites and a library, and how users access them", Q_BLUE),
        ("2", "Commercial Suites", "54 accelerators across 7 commercial domains — from Category Management to Buying", Q_CYAN),
        ("3", "Progress across Retail", "Live status of accelerators in flight, plus how and where we build", Q_VIOLET),
    ]

    y = inches(1.5)
    for num, title, desc, color in agenda_items:
        # Colour bar
        bar_id = oid()
        reqs.append(create_shape(bar_id, "ROUND_RECTANGLE", inches(0.6), y, inches(0.08), inches(0.9)))
        reqs.append(set_shape_fill(bar_id, color))
        reqs.append(set_shape_outline_none(bar_id))

        # Number + title + desc
        _, r = build_textbox(inches(1.0), y, inches(8.0), inches(0.9), [
            (f"{title}\n", text_style(14, font_weight="Medium", color=CHARCOAL), para_style("START", spacing_after=2)),
            (desc, text_style(11, color=CHARCOAL), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)
        y += inches(1.2)

    return reqs

def slide_section_divider(title, color=BERRY):
    """Section divider slide"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Background
    bg_id = oid()
    reqs.append(create_shape(bg_id, "RECTANGLE", 0, 0, SLIDE_W, SLIDE_H))
    reqs.append(set_shape_fill(bg_id, color))
    reqs.append(set_shape_outline_none(bg_id))

    # Section title
    _, r = build_textbox(inches(0.8), inches(1.8), inches(8.4), inches(1.2), [
        (title, text_style(30, font_weight="Medium", color=WHITE), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    return reqs

def slide_scaling_model():
    """Slide: Scaling model — Accelerator > Suite > Library > Interfaces"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("Accelerators compose into suites, suites into a library", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    levels = [
        ("Accelerator", "A single repeatable AI workflow", Q_BLUE),
        ("Suite", "Many accelerators grouped by domain area", Q_CYAN),
        ("Library", "All suites across 7 commercial domains", Q_TURQUOISE),
        ("User Interfaces", "Different entry points for different users", Q_VIOLET),
    ]

    x = inches(0.6)
    box_w = inches(2.0)
    gap = inches(0.27)
    y = inches(1.5)
    box_h = inches(3.2)

    for i, (name, desc, color) in enumerate(levels):
        bx = x + i * (box_w + gap)

        # Box
        box_id = oid()
        reqs.append(create_shape(box_id, "ROUND_RECTANGLE", bx, y, box_w, box_h))
        reqs.append(set_shape_fill(box_id, LIGHT_GREY_10))
        reqs.append(set_shape_outline(box_id, color, 2))

        # Color bar at top inside the box
        bar_id = oid()
        reqs.append(create_shape(bar_id, "RECTANGLE", bx, y, box_w, inches(0.06)))
        reqs.append(set_shape_fill(bar_id, color))
        reqs.append(set_shape_outline_none(bar_id))

        # Text
        _, r = build_textbox(bx + inches(0.15), y + inches(0.3), box_w - inches(0.3), inches(1.5), [
            (f"{name}\n", text_style(16, font_weight="Medium", color=CHARCOAL), para_style("CENTER", spacing_after=6)),
            (desc, text_style(11, color=CHARCOAL), para_style("CENTER")),
        ], no_outline=True)
        reqs.extend(r)

        # Stats/examples
        if i == 0:
            detail = "e.g. CPI Response\n6-step procedure"
        elif i == 1:
            detail = "e.g. Buying & Negotiations\n8 accelerators"
        elif i == 2:
            detail = "54 accelerators\n21 suites, 7 domains"
        else:
            detail = "Desktop AI app\nDiscoverable agents\nA2A ecosystem"

        _, r = build_textbox(bx + inches(0.15), y + inches(1.6), box_w - inches(0.3), inches(1.4), [
            (detail, text_style(10, color=CHARCOAL), para_style("CENTER", spacing_after=2)),
        ], no_outline=True)
        reqs.extend(r)

        # Arrow between boxes (except last)
        if i < len(levels) - 1:
            arrow_x = bx + box_w + inches(0.03)
            _, r = build_textbox(arrow_x, y + inches(1.3), inches(0.2), inches(0.4), [
                ("\u25B6", text_style(14, color=color), para_style("CENTER")),
            ], no_outline=True)
            reqs.extend(r)

    return reqs

def slide_accelerator_example():
    """Slide: The Accelerator — CPI Response procedure"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("The accelerator: a repeatable AI workflow", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    # Subtitle
    _, r = build_textbox(inches(0.6), inches(1.0), inches(8.8), inches(0.4), [
        ("Example: CPI Response — validated approach to evaluating supplier cost price increase requests", text_style(12, color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    steps = [
        ("1", "Compliance checks", "Validate CPI request format and required information"),
        ("2", "Sales analysis", "Review product performance, category dynamics, customer impact"),
        ("3", "Commodity validation", "Check market price movements of underlying commodities"),
        ("4", "Margin impact", "Calculate effect on margins, profitability, pricing strategy"),
        ("5", "Counter-proposal generation", "Develop data-driven negotiation position"),
        ("6", "Communication", "Generate supplier response with supporting rationale"),
    ]

    # Procedure box
    proc_bg = oid()
    reqs.append(create_shape(proc_bg, "ROUND_RECTANGLE", inches(0.6), inches(1.5), inches(5.5), inches(3.7)))
    reqs.append(set_shape_fill(proc_bg, ALICE_BLUE_10))
    reqs.append(set_shape_outline(proc_bg, Q_BLUE, 1))

    # Left blue accent bar
    acc_bar = oid()
    reqs.append(create_shape(acc_bar, "RECTANGLE", inches(0.6), inches(1.5), inches(0.06), inches(3.7)))
    reqs.append(set_shape_fill(acc_bar, Q_BLUE))
    reqs.append(set_shape_outline_none(acc_bar))

    # Steps text
    step_text = ""
    segments = []
    for num, title, desc in steps:
        line = f"{num}.  {title} — {desc}\n"
        segments.append((f"{num}.  {title}", text_style(11, font_weight="Medium", color=CHARCOAL), para_style("START", spacing_before=6, spacing_after=2)))
        segments.append((f" — {desc}\n", text_style(11, color=CHARCOAL), None))

    _, r = build_textbox(inches(0.9), inches(1.7), inches(5.0), inches(3.3), segments, no_outline=True)
    reqs.extend(r)

    # Right side - "What it needs" summary
    _, r = build_textbox(inches(6.5), inches(1.5), inches(3.0), inches(0.5), [
        ("What it needs", text_style(14, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    needs_categories = [
        ("Assets", Q_VIOLET, ["Elasticity model", "Sales history (52 wks)", "Category performance", "Promo VA logic", "Commodity indices", "Margin calc logic"]),
        ("Connectors", Q_CYAN, ["BigQuery MCP", "Email connector", "Chat connector", "Calendar connector"]),
        ("Skills", Q_TURQUOISE, ["Compliant email drafter", "Counter-proposal gen", "Data viz builder"]),
    ]

    ny = inches(2.1)
    for cat_name, color, items in needs_categories:
        # Category header
        _, r = build_textbox(inches(6.5), ny, inches(3.0), inches(0.35), [
            (cat_name, text_style(10, font_weight="Medium", color=color), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)
        ny += inches(0.3)

        # Items
        item_text = "\n".join([f"\u2713  {it}" for it in items[:4]]) + "\n"
        _, r = build_textbox(inches(6.5), ny, inches(3.0), inches(0.15) * min(len(items), 4) + inches(0.3), [
            (item_text, text_style(9, color=CHARCOAL), para_style("START", spacing_after=1)),
        ], no_outline=True)
        reqs.extend(r)
        ny += inches(0.15) * min(len(items), 4) + inches(0.35)

    return reqs

def slide_the_suite():
    """Slide: The Suite — Buying & Negotiations"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("The suite: many accelerators grouped by domain area", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    # Subtitle
    _, r = build_textbox(inches(0.6), inches(1.0), inches(8.8), inches(0.4), [
        ("Example: Buying & Negotiations suite — 8 connected accelerators", text_style(12, color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    # Suite frame
    frame_id = oid()
    reqs.append(create_shape(frame_id, "ROUND_RECTANGLE", inches(0.6), inches(1.5), inches(8.8), inches(3.8)))
    reqs.append(set_shape_fill(frame_id, LIGHT_GREY_10))
    reqs.append(set_shape_outline(frame_id, Q_CYAN, 1.5))

    # Suite label
    _, r = build_textbox(inches(3.2), inches(1.55), inches(3.6), inches(0.35), [
        ("BUYING AND NEGOTIATIONS SUITE", text_style(9, font_weight="Medium", color=Q_CYAN), para_style("CENTER")),
    ], no_outline=True)
    reqs.extend(r)

    accels = [
        ("CPI Response", "Negotiations", "Model cost price increases and counter-proposals"),
        ("Proactive Ask", "Negotiations", "Generate proactive cost reduction asks"),
        ("Negotiation Briefs", "Negotiations", "Prepare briefs from supplier history"),
        ("Supplier Intelligence", "Negotiations", "Surface commercial performance data"),
        ("Deal Modelling", "Negotiations", "Generate deal scenarios with options"),
        ("Commodity Tracking", "Procurement", "Track commodity trends and opportunities"),
        ("Cost Renegotiation", "Procurement", "Surface best cost opportunities"),
        ("Sales Forecasting", "Procurement", "Forecast sales by product price point"),
    ]

    cols = 4
    card_w = inches(2.0)
    card_h = inches(1.3)
    gap_x = inches(0.13)
    gap_y = inches(0.13)
    start_x = inches(0.8)
    start_y = inches(2.1)

    for i, (name, sub_type, desc) in enumerate(accels):
        col = i % cols
        row = i // cols
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)

        # Card background
        card_id = oid()
        reqs.append(create_shape(card_id, "ROUND_RECTANGLE", cx, cy, card_w, card_h))
        reqs.append(set_shape_fill(card_id, WHITE))
        if i == 0:
            reqs.append(set_shape_outline(card_id, Q_BLUE, 1.5))
        else:
            reqs.append(set_shape_outline(card_id, LIGHT_GREY_10, 0.5))

        # Tag colour
        tag_color = Q_BLUE if sub_type == "Negotiations" else Q_ORANGE
        tag_id = oid()
        reqs.append(create_shape(tag_id, "ROUND_RECTANGLE", cx + card_w - inches(0.85), cy + inches(0.08), inches(0.8), inches(0.22)))
        reqs.append(set_shape_fill(tag_id, tag_color))
        reqs.append(set_shape_outline_none(tag_id))
        _, r = build_textbox(cx + card_w - inches(0.85), cy + inches(0.08), inches(0.8), inches(0.22), [
            (sub_type, text_style(7, font_weight="Medium", color=WHITE), para_style("CENTER")),
        ], no_outline=True, valign="MIDDLE")
        reqs.extend(r)

        # Name + desc
        _, r = build_textbox(cx + inches(0.1), cy + inches(0.35), card_w - inches(0.2), card_h - inches(0.4), [
            (f"{name}\n", text_style(11, font_weight="Medium", color=CHARCOAL), para_style("START", spacing_after=3)),
            (desc, text_style(9, color=CHARCOAL), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

    return reqs

def slide_the_library():
    """Slide: The Library — 7 domains"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("The library: 54 accelerators across 7 commercial domains", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    domains = [
        ("Buying", "2 suites \u00b7 8 accels", Q_ORANGE),
        ("Assortment", "4 suites \u00b7 19 accels", Q_CYAN),
        ("Pricing", "3 suites \u00b7 7 accels", Q_YELLOW),
        ("Promotions", "5 suites \u00b7 9 accels", Q_CORAL),
        ("Category Mgmt", "1 suite \u00b7 3 accels", Q_BLUE),
        ("Space & POG", "4 suites \u00b7 5 accels", Q_TURQUOISE),
        ("Commercial Support", "2 suites \u00b7 3 accels", Q_VIOLET),
    ]

    # Domain cards in a 4-3 grid
    card_w = inches(2.05)
    card_h = inches(1.3)
    gap = inches(0.15)
    start_x = inches(0.6)
    start_y = inches(1.3)

    for i, (name, stats, color) in enumerate(domains):
        col = i % 4
        row = i // 4
        cx = start_x + col * (card_w + gap)
        cy = start_y + row * (card_h + gap)

        # Card
        card_id = oid()
        reqs.append(create_shape(card_id, "ROUND_RECTANGLE", cx, cy, card_w, card_h))
        reqs.append(set_shape_fill(card_id, WHITE))
        reqs.append(set_shape_outline(card_id, LIGHT_GREY_10, 0.75))

        # Top colour bar
        bar_id = oid()
        reqs.append(create_shape(bar_id, "RECTANGLE", cx, cy, card_w, inches(0.05)))
        reqs.append(set_shape_fill(bar_id, color))
        reqs.append(set_shape_outline_none(bar_id))

        # Text
        _, r = build_textbox(cx + inches(0.12), cy + inches(0.2), card_w - inches(0.24), card_h - inches(0.3), [
            (f"{name}\n", text_style(13, font_weight="Medium", color=CHARCOAL), para_style("START", spacing_after=3)),
            (stats, text_style(10, color=CHARCOAL), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

    # Stats bar at bottom
    stat_bg = oid()
    reqs.append(create_shape(stat_bg, "ROUND_RECTANGLE", inches(0.6), inches(4.2), inches(8.8), inches(1.0)))
    reqs.append(set_shape_fill(stat_bg, ALICE_BLUE_10))
    reqs.append(set_shape_outline(stat_bg, Q_BLUE, 1))

    stats_data = [("54", "Accelerators"), ("21", "Suites"), ("7", "Domains"), ("4", "Value Types")]
    stat_w = inches(2.2)
    for i, (num, label) in enumerate(stats_data):
        sx = inches(0.6) + i * stat_w
        _, r = build_textbox(sx, inches(4.3), stat_w, inches(0.8), [
            (f"{num}\n", text_style(28, font_weight="Medium", color=Q_BLUE), para_style("CENTER")),
            (label.upper(), text_style(9, font_weight="Medium", color=CHARCOAL), para_style("CENTER")),
        ], no_outline=True)
        reqs.extend(r)

    return reqs

def slide_user_interfaces():
    """Slide: User Interfaces — 3 maturity stages"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("Same accelerator, different entry points for different maturity stages", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    interfaces = [
        ("MVP", "Desktop AI app (testing)", "Wiq squad \u2014 building and iterating",
         "Local development environment. Wiq team develop accelerators in Claude, Gems or through Stella.",
         ["\u2713 Access to CPI response AI procedure", "\u2713 Direct MCP to BigQuery, email, calendar",
          "\u2713 Human-in-loop reviewing and refining", "\u2713 Used for building and iterating procedures"],
         Q_BLUE),
        ("Rollout", "Discoverable accelerators", "End users \u2014 daily operations",
         "Deployed with stakeholder access. End users access through discoverable chat interface.",
         ["\u2713 Discoverable through enterprise agent library", "\u2713 Embedded interface, same URL",
          "\u2713 Same underlying AI procedure", "\u2713 Governed access with authentication"],
         Q_CYAN),
        ("Maturity", "A2A ecosystem", "Commercial agent \u2014 event-driven",
         "Packaged up for other agents. Accelerators become reusable assets other agents call.",
         ["\u2713 Monitors for trigger events", "\u2713 Auto-executes relevant accelerator",
          "\u2713 Generates draft, flags for human review", "\u2713 Automatic rather than on-demand"],
         Q_VIOLET),
    ]

    col_w = inches(2.8)
    gap = inches(0.17)
    start_x = inches(0.6)
    start_y = inches(1.3)
    col_h = inches(3.9)

    for i, (stage, name, persona, method, features, color) in enumerate(interfaces):
        cx = start_x + i * (col_w + gap)

        # Card background
        card_id = oid()
        reqs.append(create_shape(card_id, "ROUND_RECTANGLE", cx, start_y, col_w, col_h))
        reqs.append(set_shape_fill(card_id, WHITE))
        reqs.append(set_shape_outline(card_id, LIGHT_GREY_10, 0.75))

        # Top colour bar
        bar_id = oid()
        reqs.append(create_shape(bar_id, "RECTANGLE", cx, start_y, col_w, inches(0.05)))
        reqs.append(set_shape_fill(bar_id, color))
        reqs.append(set_shape_outline_none(bar_id))

        # Stage label
        _, r = build_textbox(cx + inches(0.12), start_y + inches(0.12), col_w - inches(0.24), inches(0.22), [
            (stage.upper(), text_style(8, font_weight="Medium", color=color), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

        # Name
        _, r = build_textbox(cx + inches(0.12), start_y + inches(0.32), col_w - inches(0.24), inches(0.35), [
            (name, text_style(13, font_weight="Medium", color=CHARCOAL), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

        # Persona
        _, r = build_textbox(cx + inches(0.12), start_y + inches(0.63), col_w - inches(0.24), inches(0.25), [
            (persona, text_style(9, color=CHARCOAL), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

        # Method block
        method_bg = oid()
        reqs.append(create_shape(method_bg, "ROUND_RECTANGLE", cx + inches(0.12), start_y + inches(0.95), col_w - inches(0.24), inches(0.7)))
        reqs.append(set_shape_fill(method_bg, LIGHT_GREY_10))
        reqs.append(set_shape_outline_none(method_bg))

        _, r = build_textbox(cx + inches(0.2), start_y + inches(1.0), col_w - inches(0.4), inches(0.6), [
            (method, text_style(9, color=CHARCOAL), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

        # Features
        features_text = "\n".join(features) + "\n"
        _, r = build_textbox(cx + inches(0.12), start_y + inches(1.8), col_w - inches(0.24), inches(1.8), [
            (features_text, text_style(9, color=CHARCOAL), para_style("START", spacing_after=3)),
        ], no_outline=True)
        reqs.extend(r)

    return reqs

def slide_commercial_suites_overview():
    """Slide: Commercial Suites — all 7 domains with accelerator counts"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("54 repeatable AI workflows across 7 commercial domains", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    domains = [
        ("Category Management", "1 suite \u00b7 3 accelerators", "Customer insights, competitive dynamics, CDT development", Q_BLUE),
        ("Assortment Planning", "4 suites \u00b7 19 accelerators", "Range review, execution, finalisation, NPI", Q_CYAN),
        ("Space and POG", "4 suites \u00b7 5 accelerators", "Macro strategy, micro space, performance, compliance", Q_TURQUOISE),
        ("Pricing", "3 suites \u00b7 7 accelerators", "Price strategy, execution, performance review", Q_YELLOW),
        ("Promotions", "5 suites \u00b7 9 accelerators", "Strategy, trade funds, calendar, activation, ROI", Q_CORAL),
        ("Buying", "2 suites \u00b7 8 accelerators", "Supplier negotiations, deal modelling, procurement ops", Q_ORANGE),
        ("Commercial Support", "2 suites \u00b7 3 accelerators", "Performance reporting, data quality, master data", Q_VIOLET),
    ]

    # Render as rows
    row_h = inches(0.52)
    start_y = inches(1.3)
    row_w = inches(8.8)

    for i, (name, stats, desc, color) in enumerate(domains):
        ry = start_y + i * (row_h + inches(0.06))

        # Row bg
        row_id = oid()
        reqs.append(create_shape(row_id, "ROUND_RECTANGLE", inches(0.6), ry, row_w, row_h))
        reqs.append(set_shape_fill(row_id, WHITE))
        reqs.append(set_shape_outline(row_id, LIGHT_GREY_10, 0.5))

        # Colour bar
        bar_id = oid()
        reqs.append(create_shape(bar_id, "RECTANGLE", inches(0.6), ry, inches(0.06), row_h))
        reqs.append(set_shape_fill(bar_id, color))
        reqs.append(set_shape_outline_none(bar_id))

        # Domain name
        _, r = build_textbox(inches(0.85), ry + inches(0.05), inches(2.2), row_h - inches(0.1), [
            (name, text_style(12, font_weight="Medium", color=CHARCOAL), para_style("START")),
        ], no_outline=True, valign="MIDDLE")
        reqs.extend(r)

        # Stats
        _, r = build_textbox(inches(3.2), ry + inches(0.05), inches(2.0), row_h - inches(0.1), [
            (stats, text_style(10, color=CHARCOAL), para_style("START")),
        ], no_outline=True, valign="MIDDLE")
        reqs.extend(r)

        # Description
        _, r = build_textbox(inches(5.3), ry + inches(0.05), inches(4.0), row_h - inches(0.1), [
            (desc, text_style(10, color=CHARCOAL), para_style("START")),
        ], no_outline=True, valign="MIDDLE")
        reqs.extend(r)

    # Value types legend at bottom
    _, r = build_textbox(inches(0.6), inches(5.05), inches(8.8), inches(0.3), [
        ("VALUE TYPES:  ", text_style(8, font_weight="Medium", color=CHARCOAL), para_style("START")),
        ("Do More  \u00b7  Do Same with Less  \u00b7  Drive Consistency  \u00b7  Deliver Commercial Benefit", text_style(8, color=CHARCOAL), None),
    ], no_outline=True)
    reqs.extend(r)

    return reqs

def slide_progress_column_a():
    """Slide: Progress — Individual Accelerators (Column A)"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("Individual accelerators in flight across Retail", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    # Subtitle
    _, r = build_textbox(inches(0.6), inches(1.0), inches(8.8), inches(0.35), [
        ("Column A: Incremental AI and repeatable task automation", text_style(12, color=Q_BLUE), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    cards = [
        ("Trade Commentary", "MVP", "WW", "AI-generated Monday morning trade commentary in CatNav"),
        ("Ends Nomination", "POC", "WW", "AI-supported Ends setting wizard"),
        ("Price Repair", "POC", "Global", "Triggered competitive price repair action and scenario generation"),
        ("Shelf Edge Availability", "POC", "WW", "Stella applied to Shelf Edge reporting"),
        ("Promo Accelerators", "Concept", "WW", "Decomposed Accelerator opportunities across Promo planning"),
        ("Catalogue Accelerators", "Concept", "WW", "AI-assisted weekly catalogue setting and review"),
        ("wiqIntel", "POC", "WW", "AI-generated trade huddle commentary and strategic insights co-pilot"),
        ("Probable Deletes", "Concept", "WW", "Generate a list of probable deletes in a category range"),
    ]

    # Status colours
    status_colors = {
        "MVP": Q_BLUE,
        "POC": Q_YELLOW,
        "Concept": LIGHT_GREY_10,
        "Scaled": Q_TURQUOISE,
    }
    status_text_colors = {
        "MVP": WHITE,
        "POC": CHARCOAL,
        "Concept": CHARCOAL,
        "Scaled": WHITE,
    }

    cols = 2
    card_w = inches(4.25)
    card_h = inches(0.85)
    gap_x = inches(0.3)
    gap_y = inches(0.08)
    start_x = inches(0.6)
    start_y = inches(1.45)

    for i, (title, status, scope, desc) in enumerate(cards):
        col = i % cols
        row = i // cols
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)

        # Card
        card_id = oid()
        reqs.append(create_shape(card_id, "ROUND_RECTANGLE", cx, cy, card_w, card_h))
        reqs.append(set_shape_fill(card_id, WHITE))
        reqs.append(set_shape_outline(card_id, LIGHT_GREY_10, 0.75))

        # Status tag
        tag_id = oid()
        reqs.append(create_shape(tag_id, "ROUND_RECTANGLE", cx + card_w - inches(0.7), cy + inches(0.08), inches(0.6), inches(0.2)))
        reqs.append(set_shape_fill(tag_id, status_colors.get(status, LIGHT_GREY_10)))
        reqs.append(set_shape_outline_none(tag_id))
        _, r = build_textbox(cx + card_w - inches(0.7), cy + inches(0.08), inches(0.6), inches(0.2), [
            (status, text_style(7, font_weight="Medium", color=status_text_colors.get(status, CHARCOAL)), para_style("CENTER")),
        ], no_outline=True, valign="MIDDLE")
        reqs.extend(r)

        # Title + desc
        _, r = build_textbox(cx + inches(0.12), cy + inches(0.08), card_w - inches(0.9), card_h - inches(0.15), [
            (f"{title}\n", text_style(11, font_weight="Medium", color=CHARCOAL), para_style("START", spacing_after=2)),
            (desc, text_style(9, color=CHARCOAL), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

    # Legend
    _, r = build_textbox(inches(0.6), inches(5.1), inches(8.8), inches(0.3), [
        ("MATURITY:  ", text_style(8, font_weight="Medium", color=CHARCOAL), para_style("START")),
        ("Scaled  \u00b7  MVP  \u00b7  POC  \u00b7  Concept", text_style(8, color=CHARCOAL), None),
        ("          SCOPE:  ", text_style(8, font_weight="Medium", color=CHARCOAL), None),
        ("WW  \u00b7  Global", text_style(8, color=CHARCOAL), None),
    ], no_outline=True)
    reqs.extend(r)

    return reqs

def slide_progress_column_b():
    """Slide: Progress — AI-native Systems (Column B)"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("AI-native systems: orchestrated, multi-step, transformational", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    # Subtitle
    _, r = build_textbox(inches(0.6), inches(1.0), inches(8.8), inches(0.35), [
        ("Column B: These are the big bets — full reimagination of commercial workflows", text_style(12, color=Q_VIOLET), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    systems = [
        ("Inbound CPI Assistant", "MVP", "WW",
         "WNZ pilot for Commercial Coaches to respond to inbound Cost Price Increases",
         "Deal modelling MVP by end of Q3"),
        ("Stella for Agentic Insights", "MVP", "WW",
         "AI-Procedure based Conversational Insights interface with semantic layer and governed data connections",
         "In UAT with Commercial Finance"),
        ("Proactive Ask Assistant", "POC", "WW",
         "Research category performance and generate initial ask for Category Managers to take to Suppliers",
         "AU pilot in Q4"),
        ("CatNav / MerchantIQ", "Concept", "Global",
         "MerchIQ build with CatNav-style AI-powered Alerts, in partnership with HEB",
         "Project won with HEB"),
    ]

    card_w = inches(8.8)
    start_y = inches(1.5)
    card_h = inches(0.85)
    gap = inches(0.1)

    status_colors = {"MVP": Q_BLUE, "POC": Q_YELLOW, "Concept": LIGHT_GREY_10}
    status_text_colors = {"MVP": WHITE, "POC": CHARCOAL, "Concept": CHARCOAL}

    for i, (title, status, scope, desc, footnote) in enumerate(systems):
        cy = start_y + i * (card_h + gap)

        # Card with left berry accent
        card_id = oid()
        reqs.append(create_shape(card_id, "ROUND_RECTANGLE", inches(0.6), cy, card_w, card_h))
        reqs.append(set_shape_fill(card_id, WHITE))
        reqs.append(set_shape_outline(card_id, LIGHT_GREY_10, 0.75))

        # Left accent bar
        bar_id = oid()
        reqs.append(create_shape(bar_id, "RECTANGLE", inches(0.6), cy, inches(0.06), card_h))
        reqs.append(set_shape_fill(bar_id, Q_VIOLET))
        reqs.append(set_shape_outline_none(bar_id))

        # Status tag
        tag_id = oid()
        reqs.append(create_shape(tag_id, "ROUND_RECTANGLE", inches(0.6) + card_w - inches(0.7), cy + inches(0.08), inches(0.6), inches(0.2)))
        reqs.append(set_shape_fill(tag_id, status_colors.get(status, LIGHT_GREY_10)))
        reqs.append(set_shape_outline_none(tag_id))
        _, r = build_textbox(inches(0.6) + card_w - inches(0.7), cy + inches(0.08), inches(0.6), inches(0.2), [
            (status, text_style(7, font_weight="Medium", color=status_text_colors.get(status, CHARCOAL)), para_style("CENTER")),
        ], no_outline=True, valign="MIDDLE")
        reqs.extend(r)

        # Title + desc + footnote
        _, r = build_textbox(inches(0.9), cy + inches(0.08), card_w - inches(1.1), card_h - inches(0.15), [
            (f"{title}\n", text_style(12, font_weight="Medium", color=CHARCOAL), para_style("START", spacing_after=2)),
            (f"{desc}\n", text_style(10, color=CHARCOAL), para_style("START", spacing_after=2)),
            (f"\u2192 {footnote}", text_style(9, font_weight="Medium", color=Q_BLUE), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

    return reqs

def slide_how_where_we_build():
    """Slide: How we build + Where we build"""
    sid = oid()
    reqs = [create_slide(sid)]

    # Headline
    _, r = build_textbox(inches(0.6), inches(0.4), inches(8.8), inches(0.7), [
        ("How and where we build accelerators", text_style(22, font_weight="Medium", color=CHARCOAL), para_style("START")),
    ], no_outline=True)
    reqs.extend(r)

    bands = [
        {
            "letter": "D", "title": "How we build", "subtitle": "Agentic coding tools",
            "color": Q_YELLOW, "y": inches(1.2),
            "pillars": [
                ("Availability", "Drive usage visibility and expand access",
                 "Claude Code licenses deployed across all engineering teams. Business case for more licenses in progress."),
                ("Quality", "Share best practices",
                 "Research-Plan-Execute-Review workflow as standard practice. AI capabilities framework under development."),
            ]
        },
        {
            "letter": "E", "title": "Where we build", "subtitle": "Platform enablers",
            "color": Q_CYAN, "y": inches(3.2),
            "pillars": [
                ("Edge Platform", "Deployable agent infrastructure",
                 "Quantium Edge Platform: deployable agent platform (GCP primary, AWS secondary). Cloud-native architecture."),
                ("Build Guidance", "Align teams to standard patterns",
                 "Align to standard patterns (e.g. use ADK agents within Google ecosystem). Reduce fragmentation across teams."),
            ]
        },
    ]

    for band in bands:
        by = band["y"]
        band_w = inches(8.8)
        band_h = inches(1.7)

        # Band background
        band_id = oid()
        reqs.append(create_shape(band_id, "ROUND_RECTANGLE", inches(0.6), by, band_w, band_h))
        reqs.append(set_shape_fill(band_id, WHITE))
        reqs.append(set_shape_outline(band_id, LIGHT_GREY_10, 0.75))

        # Colour bar
        bar_id = oid()
        reqs.append(create_shape(bar_id, "RECTANGLE", inches(0.6), by, inches(0.06), band_h))
        reqs.append(set_shape_fill(bar_id, band["color"]))
        reqs.append(set_shape_outline_none(bar_id))

        # Band title
        _, r = build_textbox(inches(0.85), by + inches(0.1), inches(3.0), inches(0.5), [
            (f"{band['title']}\n", text_style(14, font_weight="Medium", color=CHARCOAL), para_style("START")),
            (band["subtitle"], text_style(10, color=CHARCOAL), para_style("START")),
        ], no_outline=True)
        reqs.extend(r)

        # Pillars side by side
        pillar_w = inches(4.1)
        for j, (p_name, p_desc, p_detail) in enumerate(band["pillars"]):
            px = inches(0.85) + j * (pillar_w + inches(0.2))
            py = by + inches(0.65)

            # Pillar box
            p_id = oid()
            reqs.append(create_shape(p_id, "ROUND_RECTANGLE", px, py, pillar_w, inches(0.9)))
            reqs.append(set_shape_fill(p_id, LIGHT_GREY_10))
            reqs.append(set_shape_outline_none(p_id))

            _, r = build_textbox(px + inches(0.1), py + inches(0.05), pillar_w - inches(0.2), inches(0.8), [
                (f"{p_name}\n", text_style(10, font_weight="Medium", color=CHARCOAL), para_style("START", spacing_after=2)),
                (p_detail, text_style(9, color=CHARCOAL), para_style("START")),
            ], no_outline=True)
            reqs.extend(r)

    return reqs


# ══════════════════════════════════════════════════════════
# MAIN — Build and execute
# ══════════════════════════════════════════════════════════

def main():
    print("Step 1: Creating blank presentation...")
    result = subprocess.run(
        ["gws", "slides", "presentations", "create",
         "--json", json.dumps({"title": "Retail Accelerator Hub — Commercial AI Overview"})],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error creating presentation: {result.stderr}")
        sys.exit(1)

    pres = json.loads(result.stdout)
    pres_id = pres["presentationId"]
    print(f"  Created: {pres_id}")

    # The newly created presentation has one blank slide - we'll delete it at the end
    first_slide_id = pres["slides"][0]["objectId"]

    print("Step 2: Building slide requests...")
    all_requests = []

    # Build all slides
    slides = [
        ("Title", slide_title),
        ("Agenda", slide_agenda),
        ("Section: Anatomy", lambda: slide_section_divider("Accelerator Anatomy", ULTRAMARINE)),
        ("Scaling Model", slide_scaling_model),
        ("The Accelerator", slide_accelerator_example),
        ("The Suite", slide_the_suite),
        ("The Library", slide_the_library),
        ("User Interfaces", slide_user_interfaces),
        ("Section: Suites", lambda: slide_section_divider("Commercial Suites", BERRY)),
        ("Suites Overview", slide_commercial_suites_overview),
        ("Section: Progress", lambda: slide_section_divider("Progress across Retail", Q_VIOLET)),
        ("Progress Column A", slide_progress_column_a),
        ("Progress Column B", slide_progress_column_b),
        ("How & Where We Build", slide_how_where_we_build),
    ]

    for name, builder in slides:
        print(f"  Building: {name}")
        reqs = builder()
        all_requests.extend(reqs)

    # Delete the initial blank slide
    all_requests.append({"deleteObject": {"objectId": first_slide_id}})

    print(f"Step 3: Sending {len(all_requests)} requests via batchUpdate...")

    # Split into batches to avoid OS argument length limits
    # Each slide's requests need to stay together, so batch by slide
    def send_batch(requests, batch_num, total):
        body = json.dumps({"requests": requests})
        tmp_path = f"/tmp/slides-batch-{batch_num}.json"
        with open(tmp_path, "w") as f:
            f.write(body)

        result = subprocess.run(
            ["bash", "-c",
             f'gws slides presentations batchUpdate '
             f'--params \'{{\"presentationId\": \"{pres_id}\"}}\' '
             f'--json "$(cat {tmp_path})"'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"  Error in batch {batch_num}: {result.stderr}")
            if result.stdout:
                try:
                    err_detail = json.loads(result.stdout)
                    print(json.dumps(err_detail, indent=2)[:2000])
                except Exception:
                    print(result.stdout[:2000])
            return False
        return True

    # Group requests: each createSlide starts a new group
    batches = []
    current_batch = []
    for req in all_requests:
        if "createSlide" in req and current_batch:
            batches.append(current_batch)
            current_batch = []
        current_batch.append(req)
    if current_batch:
        batches.append(current_batch)

    total = len(batches)
    for i, batch in enumerate(batches):
        print(f"  Sending batch {i+1}/{total} ({len(batch)} requests)...")
        if not send_batch(batch, i, total):
            print("  Failed! Stopping.")
            sys.exit(1)

    print(f"\nDone! Presentation created successfully.")
    print(f"  ID: {pres_id}")
    print(f"  URL: https://docs.google.com/presentation/d/{pres_id}/edit")
    print(f"  Slides: {len(slides)}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extract text content from a Google Slides presentation.

Usage:
    gws slides presentations get --params '{"presentationId": "PRESENTATION_ID"}' --format json | python3 scripts/extract-slides-text.py
"""

import json
import sys


def extract_text(element):
    """Extract text from a slide element (shapes, tables, groups)."""
    texts = []

    if "shape" in element and "text" in element["shape"]:
        for te in element["shape"]["text"].get("textElements", []):
            if "textRun" in te:
                t = te["textRun"]["content"].strip()
                if t:
                    texts.append(t)

    if "table" in element:
        for row in element["table"].get("tableRows", []):
            row_texts = []
            for cell in row.get("tableCells", []):
                cell_text = []
                if "text" in cell:
                    for te in cell["text"].get("textElements", []):
                        if "textRun" in te:
                            ct = te["textRun"]["content"].strip()
                            if ct:
                                cell_text.append(ct)
                row_texts.append(" ".join(cell_text))
            texts.append(" | ".join(row_texts))

    if "elementGroup" in element:
        for child in element["elementGroup"].get("children", []):
            texts.extend(extract_text(child))

    return texts


def main():
    data = json.load(sys.stdin)
    slides = data.get("slides", [])

    for i, slide in enumerate(slides):
        print(f"=== Slide {i + 1} ===")
        for elem in slide.get("pageElements", []):
            for t in extract_text(elem):
                print(t)
        print()


if __name__ == "__main__":
    main()

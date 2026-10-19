#!/usr/bin/env python3
"""Builds the static site into site/.

Each page in src/pages/ is body content with three header comments (title, description, nav).
It is wrapped in src/layout.html. static/ is copied as-is. Run: python3 build.py
"""
import datetime
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "site"
NAV_KEYS = ["manufacturing", "products", "private-label", "about", "market", "contact"]

FLAG = (
    '<svg viewBox="0 0 22 14" aria-hidden="true">'
    '<rect width="22" height="14" fill="#ffffff"/>'
    + "".join(f'<rect y="{i * 2}" width="22" height="1" fill="#b4283a"/>' for i in range(7))
    + '<rect width="10" height="7" fill="#78bfe8"/></svg>'
)


def seal(uid):
    """Made in the USA seal. Inline so it uses the page fonts."""
    stripes = "".join(
        f'<rect x="74" y="{122 + i * 3}" width="52" height="1.5" fill="#b4283a"/>' for i in range(5)
    )
    stars = "".join(
        f'<path transform="translate({x} 70) scale(0.42)" d="M0,-10 L2.9,-4 9.5,-3.1 4.7,1.5 5.9,8.1 0,5 -5.9,8.1 -4.7,1.5 -9.5,-3.1 -2.9,-4Z" fill="#78bfe8"/>'
        for x in (86, 100, 114)
    )
    return (
        f'<svg class="seal" viewBox="0 0 200 200" role="img" aria-label="Made in the USA">'
        f'<defs><path id="ring-{uid}" d="M100,100 m-75,0 a75,75 0 1,1 150,0 a75,75 0 1,1 -150,0"/></defs>'
        '<circle cx="100" cy="100" r="98" fill="#0d2742"/>'
        '<circle cx="100" cy="100" r="92" fill="none" stroke="#78bfe8" stroke-width="1"/>'
        '<circle cx="100" cy="100" r="57" fill="#081a2e" stroke="#78bfe8" stroke-width="1"/>'
        f'<text font-size="12.5" fill="#ffffff"><textPath href="#ring-{uid}" textLength="452" lengthAdjust="spacing">'
        "MADE IN THE U.S.A. ★ SOUTH PLAINFIELD, NEW JERSEY ★</textPath></text>"
        f"{stars}"
        '<text x="100" y="112" text-anchor="middle" fill="#ffffff" '
        'style="font-family:var(--display);font-weight:600;font-size:38px;letter-spacing:.06em">USA</text>'
        f"{stripes}"
        "</svg>"
    )


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT)
    layout = (SRC / "layout.html").read_text()
    year = str(datetime.date.today().year)
    for page in sorted((SRC / "pages").glob("*.html")):
        text = page.read_text()
        meta = dict(re.findall(r"<!--\s*(title|description|nav):\s*(.*?)\s*-->", text))
        body = re.sub(r"<!--\s*(title|description|nav):.*?-->\n?", "", text)
        html = layout.replace("{{content}}", body)
        html = html.replace("{{title}}", meta["title"]).replace("{{description}}", meta["description"])
        html = html.replace("{{flag}}", FLAG).replace("{{year}}", year)
        for key in NAV_KEYS:
            html = html.replace("{{cur:%s}}" % key, ' aria-current="page"' if meta.get("nav") == key else "")
        html = re.sub(r"\{\{seal:([\w-]+)\}\}", lambda m: seal(m.group(1)), html)
        leftover = re.findall(r"\{\{.*?\}\}", html)
        if leftover:
            raise SystemExit(f"{page.name}: unfilled placeholders {leftover}")
        (OUT / page.name).write_text(html)
        print("built", page.name)


if __name__ == "__main__":
    build()

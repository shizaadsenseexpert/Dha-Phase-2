#!/usr/bin/env python3
"""Insert or refresh the "Keep exploring" related-links block on every page.

Edit RELATED to change which pages each page links to, then run:
    python3 scripts/add_related_links.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = {
    "/": ("🏠", "DHA Phase 2 Overview", "Location, prices, facilities and master plan in one place"),
    "/masterplan/": ("🗺️", "Master Plan", "All sectors with plot sizes, high-rises and rates"),
    "/prices/": ("💰", "Prices 2026", "Sector-wise plot rates and apartment prices"),
    "/apartments/": ("🏢", "Apartments", "High-rise buildings in every sector"),
    "/facilities/": ("🏫", "Facilities", "Schools, hospitals, parks, mosques and security"),
    "/location/": ("📍", "Location &amp; Distance Guide", "Gates, routes and travel times"),
    "/location/googlemap/": ("🌐", "Google Map", "See DHA Phase 2 on an interactive map"),
    "/location/nearby/": ("🧭", "Nearby Areas", "Surrounding societies and places to visit"),
}

SECTOR_LINKS = ["/prices/", "/apartments/", "/facilities/", "/location/", "/location/googlemap/", "/location/nearby/"]

RELATED = {
    "/": ["/masterplan/", "/prices/", "/apartments/", "/facilities/", "/location/", "/location/googlemap/"],
    "/masterplan/": ["/prices/", "/apartments/", "/facilities/", "/location/", "/location/googlemap/", "/location/nearby/"],
    "/prices/": ["/masterplan/", "/apartments/", "/facilities/", "/location/", "/location/nearby/", "/"],
    "/apartments/": ["/prices/", "/masterplan/", "/facilities/", "/location/", "/location/googlemap/", "/"],
    "/facilities/": ["/prices/", "/apartments/", "/masterplan/", "/location/googlemap/", "/location/nearby/", "/"],
    "/location/": ["/location/googlemap/", "/location/nearby/", "/masterplan/", "/prices/", "/facilities/", "/apartments/"],
    "/location/googlemap/": ["/location/", "/location/nearby/", "/masterplan/", "/prices/", "/facilities/", "/"],
    "/location/nearby/": ["/location/", "/location/googlemap/", "/masterplan/", "/prices/", "/apartments/", "/facilities/"],
}
for s in "abcdefghj":
    if s != "i":
        RELATED[f"/masterplan/sector-{s}/"] = SECTOR_LINKS

START, END = "<!-- RELATED LINKS -->", "<!-- /RELATED LINKS -->"
BLOCK_RE = re.compile(r"\n  " + re.escape(START) + r".*?" + re.escape(END) + r"\n", re.S)


def block(url):
    cards = []
    for target in RELATED[url]:
        icon, title, desc = PAGES[target]
        cards.append(
            f'        <a href="{target}" class="sector-card sector-link">'
            f'<span class="sector-badge">{icon}</span><h4>{title}</h4><p>{desc}</p></a>'
        )
    return (
        f"\n  {START}\n"
        '  <section class="section section-alt" id="explore">\n'
        '    <div class="container">\n'
        '      <div class="section-head">\n'
        '        <p class="eyebrow">Keep Exploring</p>\n'
        "        <h2>More about DHA Phase 2 Islamabad</h2>\n"
        "      </div>\n"
        '      <div class="sector-grid">\n'
        + "\n".join(cards) + "\n"
        "      </div>\n"
        "    </div>\n"
        "  </section>\n"
        f"  {END}\n"
    )


def file_for(url):
    return os.path.join(ROOT, url.strip("/"), "index.html")


def main():
    for url in RELATED:
        path = file_for(url)
        with open(path, encoding="utf-8") as f:
            html = f.read()
        html = BLOCK_RE.sub("", html)
        anchor = re.search(r"\n  <!-- (?:CONTACT / )?CTA -->", html) or re.search(r"\n</main>", html)
        html = html[: anchor.start()] + block(url) + html[anchor.start():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("updated", url)


if __name__ == "__main__":
    main()

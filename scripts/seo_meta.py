#!/usr/bin/env python3
"""Set the SEO title, meta description, canonical URL and social tags on every page.

Add a new page (for example a blog post) to META, then run:
    python3 scripts/seo_meta.py
Keep titles under 60 characters and descriptions under 160 so Google
shows them in full.
"""
import os
import re
import sys
from html import escape

SITE_URL = "https://dhaphase2islamabad.com"
SITE_NAME = "DHA Phase 2 Islamabad"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

META = {
    "/": (
        "DHA Phase 2 Islamabad: Prices, Map, Master Plan & Guide",
        "Complete guide to DHA Phase 2 Islamabad: location and gates, master plan, sector-wise 2025 plot prices, apartments, facilities and nearby areas.",
    ),
    "/masterplan/": (
        "DHA Phase 2 Islamabad Master Plan: Sectors A to J",
        "DHA Phase 2 Islamabad master plan explained sector by sector: Sectors A to J, plot sizes, high-rise apartments, 2025 rates and facilities in each.",
    ),
    "/prices/": (
        "DHA Phase 2 Islamabad Prices 2025: Plot & Apartment Rates",
        "Latest DHA Phase 2 Islamabad prices: sector-wise rates for 5 Marla, 10 Marla and 1 Kanal plots, commercial plots and high-rise apartments.",
    ),
    "/apartments/": (
        "Apartments in DHA Phase 2 Islamabad: Prices & Buildings",
        "Apartments in DHA Phase 2 Islamabad: Lignum Tower, Central Palace Residence, El Cielo and Giga Mall high-rises with prices, amenities and buying tips.",
    ),
    "/facilities/": (
        "DHA Phase 2 Islamabad Facilities: Schools, Parks & More",
        "Facilities in DHA Phase 2 Islamabad: schools, hospitals, security, parks, mosques, Giga Mall, Jacaranda Family Club and utilities, sector by sector.",
    ),
    "/location/": (
        "DHA Phase 2 Islamabad Location, Gates & Distances",
        "Where DHA Phase 2 Islamabad is: entrance gates, distances to key landmarks and routes from Islamabad, Rawalpindi and Islamabad Airport.",
    ),
    "/location/googlemap/": (
        "DHA Phase 2 Islamabad on Google Map: Location & Gates",
        "Find DHA Phase 2 Islamabad on Google Maps: exact coordinates, an interactive map of the community, its entrance gates and nearby landmarks.",
    ),
    "/location/nearby/": (
        "Near DHA Phase 2 Islamabad: Societies & Places to Visit",
        "Housing societies, malls, parks, restaurants, hospitals and schools near DHA Phase 2 Islamabad, plus the best places to visit around it.",
    ),
    "/masterplan/sector-a/": (
        "DHA Phase 2 Sector A Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector A Islamabad: commercial market, banks, apartments near Lignum Tower, plot sizes, 2025 prices, facilities, pros and cons.",
    ),
    "/masterplan/sector-b/": (
        "DHA Phase 2 Sector B Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector B Islamabad: family park, DHA Tennis Court, shopping mall and eateries, plot sizes, 2025 prices, facilities, pros and cons.",
    ),
    "/masterplan/sector-c/": (
        "DHA Phase 2 Sector C Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector C Islamabad: Lignum Tower apartments, APS and schools, commercial markets, plot sizes, 2025 prices, pros and cons.",
    ),
    "/masterplan/sector-d/": (
        "DHA Phase 2 Sector D Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector D Islamabad: residential and commercial sector with green belts, 5 Marla to 1 Kanal plots, 2025 prices and facilities.",
    ),
    "/masterplan/sector-e/": (
        "DHA Phase 2 Sector E Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector E Islamabad: Jacaranda Family Club, low-density family homes, plot sizes, 2025 prices, facilities, pros and cons.",
    ),
    "/masterplan/sector-f/": (
        "DHA Phase 2 Sector F Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector F Islamabad: Giga Mall, Gate 1, GT Road commercial plots, schools, plot sizes, 2025 prices, high-rises and facilities.",
    ),
    "/masterplan/sector-g/": (
        "DHA Phase 2 Sector G Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector G Islamabad: Central Boulevard, Central Park, APS, Central Palace Residence apartments, plot sizes and 2025 prices.",
    ),
    "/masterplan/sector-h/": (
        "DHA Phase 2 Sector H Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector H Islamabad: quiet residential sector with guest houses, affordable 5 Marla to 1 Kanal plots, 2025 prices and facilities.",
    ),
    "/masterplan/sector-j/": (
        "DHA Phase 2 Sector J Islamabad: Plots, Prices & Facilities",
        "DHA Phase 2 Sector J Islamabad: compact residential sector with family marts and mosques, affordable plots, 2025 prices, pros and cons.",
    ),
}

START, END = "<!-- SEO META -->", "<!-- /SEO META -->"
SEO_RE = re.compile(r"\n" + re.escape(START) + r".*?" + re.escape(END), re.S)
TITLE_RE = re.compile(r"<title>.*?</title>", re.S)
DESC_RE = re.compile(r'<meta name="description"[^>]*/>')


def tags(url, title, desc):
    t, d, u = escape(title), escape(desc), escape(SITE_URL + url)
    return "\n".join([
        START,
        f'<link rel="canonical" href="{u}" />',
        '<meta property="og:type" content="website" />',
        f'<meta property="og:site_name" content="{SITE_NAME}" />',
        f'<meta property="og:title" content="{t}" />',
        f'<meta property="og:description" content="{d}" />',
        f'<meta property="og:url" content="{u}" />',
        '<meta name="twitter:card" content="summary" />',
        f'<meta name="twitter:title" content="{t}" />',
        f'<meta name="twitter:description" content="{d}" />',
        END,
    ])


def main():
    ok = True
    for url, (title, desc) in META.items():
        if len(title) > 60 or len(desc) > 160:
            print(f"too long: {url} title={len(title)} desc={len(desc)}")
            ok = False
        path = os.path.join(ROOT, url.strip("/"), "index.html")
        with open(path, encoding="utf-8") as f:
            html = f.read()
        html = SEO_RE.sub("", html)
        html = TITLE_RE.sub(lambda m: f"<title>{escape(title, quote=False)}</title>", html, count=1)
        new_desc = f'<meta name="description" content="{escape(desc)}" />'
        html = DESC_RE.sub(lambda m: new_desc + "\n" + tags(url, title, desc), html, count=1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"{len(title):3} {len(desc):3}  {url}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

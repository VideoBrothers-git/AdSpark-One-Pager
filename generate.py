#!/usr/bin/env python3
"""
Builds the deployed site from the one canonical source, template.html.

  /                       generic public page, no client named
  /clients/<slug>/        bespoke page for one prospect, name filled in

Never hand-edit index.html or clients/*/index.html directly -- edit
template.html and re-run this script (`python3 generate.py`), then
commit everything it writes. That's what keeps every version in sync:
a copy fix or layout change only has to happen once.

Personalization spots in template.html are marked:
    <TAG data-pz="client_name">[Client]</TAG>

"[Client]" can't just become the word "you" everywhere -- the grammar
around each spot differs (a possessive, a mid-sentence name, a sentence
that starts with the name). GENERIC_SUBS below is the explicit, hand-
written generic phrasing for each spot. If template.html's wording
around a data-pz spot ever changes, update the matching entry here --
the script will refuse to run rather than silently skip a stale one.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT, 'template.html')
LOGOS_DIR = os.path.join(ROOT, 'assets', 'logos')
LOGO_EXTS = ('svg', 'png', 'jpg', 'jpeg', 'webp')

CLIENTS = [
    {"name": "EvenUp", "slug": "evenup"},
    {"name": "Nudge Security", "slug": "nudge-security"},
    {"name": "Riskified", "slug": "riskified"},
]

# (exact text in template.html, generic replacement)
GENERIC_SUBS = [
    (
        '<div class="mast-for"><!--LOGO_SLOT-->\n'
        '        <div class="mast-for-text"><small>Prepared for</small><b data-pz="client_name">[Client]</b></div>\n'
        '      </div>\n'
        '    </div>',
        '</div>'
    ),
    (
        '<h1><span data-pz="client_name">[Client]</span>\'s journey to <mark class="hl">unforgettable</mark> starts here.</h1>',
        '<h1>The journey to <mark class="hl">unforgettable</mark> starts here.</h1>'
    ),
    (
        'how one actually gets made for <span data-pz="client_name">[Client]</span>, starting',
        'how one actually gets made, starting'
    ),
    (
        'presented to <span data-pz="client_name">[Client]</span> within about a week',
        'presented to you within about a week'
    ),
    (
        '<span data-pz="client_name">[Client]</span> is reviewing whether',
        "You're reviewing whether"
    ),
    (
        'in front of <span data-pz="client_name">[Client]</span> about a week',
        'in front of you about a week'
    ),
]


def find_logo(slug):
    """Return the root-relative /assets/logos/<slug>.<ext> path if a logo file
    for this client has been dropped in assets/logos/, else None."""
    for ext in LOGO_EXTS:
        if os.path.exists(os.path.join(LOGOS_DIR, f'{slug}.{ext}')):
            return f'/assets/logos/{slug}.{ext}'
    return None


def make_generic(html):
    out = html
    for old, new in GENERIC_SUBS:
        if old not in out:
            raise SystemExit(
                "generate.py: a GENERIC_SUBS entry no longer matches template.html "
                "-- the wording around a data-pz spot changed. Update generate.py "
                "to match, then re-run.\nMissing text (first 90 chars):\n  "
                + old[:90].replace("\n", "\\n")
            )
        out = out.replace(old, new)
    if '[Client]' in out:
        raise SystemExit("generate.py: generic page still contains a literal '[Client]' -- add a GENERIC_SUBS entry for it.")
    return out


def make_bespoke(html, name, slug):
    out = html.replace('data-pz="client_name">[Client]<', f'data-pz="client_name">{name}<')
    logo = find_logo(slug)
    if logo:
        out = out.replace(
            '<!--LOGO_SLOT-->',
            f'<img class="mast-for-logo" src="{logo}" alt="{name} logo"><div class="mast-for-divider"></div>'
        )
    else:
        out = out.replace('<!--LOGO_SLOT-->', '')
    if '[Client]' in out:
        raise SystemExit(f"generate.py: bespoke page for {name!r} still contains a literal '[Client]'.")
    return out


def write(path, html):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', os.path.relpath(path, ROOT))


def main():
    template = open(TEMPLATE_PATH, encoding='utf-8').read()
    if '[Client]' not in template:
        raise SystemExit("generate.py: template.html has no '[Client]' placeholder -- is this really the template?")

    write(os.path.join(ROOT, 'index.html'), make_generic(template))
    for c in CLIENTS:
        write(os.path.join(ROOT, 'clients', c['slug'], 'index.html'), make_bespoke(template, c['name'], c['slug']))


if __name__ == '__main__':
    main()

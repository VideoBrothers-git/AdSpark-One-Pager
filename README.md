# Ad Spark one-pager

One canonical source (`template.html`) generates every page that actually
gets deployed. Never hand-edit the generated files — edit the template,
regenerate, commit everything.

```
template.html              canonical source — edit this
generate.py                builds the pages below from template.html
index.html                 generated: generic public page, no client named
clients/<slug>/index.html  generated: bespoke page for one prospect
assets/                    shared images + the real deck PDFs (stills,
                            lookbook, script book, concepts)
```

## Making a change

1. Edit `template.html`.
2. `python3 generate.py` — regenerates `index.html` and every page under
   `clients/`, so a fix never has to be repeated by hand across versions.
3. Commit everything the script touched and push to `main`. Vercel
   redeploys automatically on push (no build step, no config — it's a
   static site).

## Adding a new client

Add `{"name": "...", "slug": "..."}` to the `CLIENTS` list near the top
of `generate.py`, then run it. The slug becomes the URL path:
`/clients/<slug>/`.

## Adding a client's logo to the masthead

Drop the logo file into `assets/logos/`, named after the client's slug —
`assets/logos/<slug>.svg` (preferred) or `.png` / `.jpg` / `.webp`. Re-run
`generate.py`; it picks up the file automatically and adds it next to
"Prepared for [Client]" on that client's bespoke page only. No logo file
for a slug means no logo shows — including on the generic page, which
never gets one. Since these files live in the repo, dragging them into
this folder in Finder works (unlike attaching them in chat, which never
reaches disk); pushing them to `main` deploys them like anything else.

## Why a generator instead of one file with a URL parameter

Six spots in the copy read differently for a named prospect ("EvenUp's
journey...") versus the generic page ("The journey...") — the grammar
changes, not just a name swap. `generate.py`'s `GENERIC_SUBS` list is
the explicit, hand-written generic wording for each of those spots. If
you edit the text immediately around a `data-pz="client_name"` marker
in `template.html`, update the matching entry in `GENERIC_SUBS` too —
the script refuses to run rather than silently deploy stale wording.

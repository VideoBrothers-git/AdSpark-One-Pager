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

## Why a generator instead of one file with a URL parameter

Six spots in the copy read differently for a named prospect ("EvenUp's
journey...") versus the generic page ("The journey...") — the grammar
changes, not just a name swap. `generate.py`'s `GENERIC_SUBS` list is
the explicit, hand-written generic wording for each of those spots. If
you edit the text immediately around a `data-pz="client_name"` marker
in `template.html`, update the matching entry in `GENERIC_SUBS` too —
the script refuses to run rather than silently deploy stale wording.

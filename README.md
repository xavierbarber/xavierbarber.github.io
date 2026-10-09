# Xavier Barber — trilingual professional website

Published at https://xavierbarber.github.io/ with GitHub Pages. Spanish is the
default; Valencian Catalan lives in `/ca/` (`lang="ca-valencia"`) and British
English in `/en/` (`lang="en-GB"`). Language links preserve section anchors.

## Edit and build

- `content/es.json`, `content/ca.json`, `content/en.json`: complete editorial translations.
- `content/papers.json`: six AI-related research highlights selected from the
  author's Google Scholar CSV supplied on 9 October 2026. That export has no
  citation-count column. DOI links are retained from the previously checked CV.
- `cva.Rmd`: the extended publication catalogue. Preserve original titles,
  authors and DOI links. Citation counts in this catalogue were consulted on
  11 September 2026; they are not counts from the new CSV.
- `build_professional_site.py`: shared static templates, linked sections and catalogue extraction.
- `assets/site.css`, `assets/site.js`: responsive design, mobile navigation and publication filters.
- `photos/`, `downloads/`: existing authorised imagery and the Spanish infographic.

```sh
python3 build_site.py
# Optional:
python3 build_site.py --pandoc /path/to/pandoc
```

Requires Python 3 and Pandoc. Generates fifteen HTML pages, sitemap.xml and
robots.txt. Commit the generated pages alongside the sources; no server runtime
or JavaScript framework is required. The English edition uses British spelling;
the Valencian edition uses Valencian forms. Original article titles stay in
their original language. The downloadable PDF is labelled as Spanish in all editions.

The homepage contains profile, AI publications, projects, human-centred AI,
training, personal interests and contact. Existing about.html, xbarber.html,
training.html and cva.html URLs remain available. Email links open the visitor's
email application; no form claims to send messages without a backend.

The cycling frame comes from the user's video. The withdrawn photograph of the
dolçaina group must not be republished. Music is represented by a CSS motif.
Older Rmd files other than cva.Rmd, profile.css, site-template.html and _site.yml
are retained as legacy sources and are not used by this build.

The homepage portrait includes a decorative SVG/CSS holographic cycle (18 seconds),
with translated pause/resume controls. It starts disabled for reduced-motion
preferences and without JavaScript. No GIF or video is loaded for this effect.

# Xavier Barber — professional website

Published at https://xavierbarber.github.io/ using GitHub Pages.

## Editing and building

- `build_professional_site.py`: bilingual editorial content and shared page structure.
- `cva.Rmd`: original publication records, author lists, DOI links and citation counts.
- `assets/site.css` and `assets/site.js`: responsive layout and accessible mobile navigation.
- `photos/`: existing photography; `downloads/`: downloadable professional profile.

Run with Python 3 and Pandoc:

```sh
python3 build_site.py
# Optional explicit Pandoc path:
python3 build_site.py --pandoc /path/to/pandoc
```

The builder generates five Spanish pages in the root and five English pages in
`en/`. Commit both sources and generated HTML. GitHub Pages serves the static
files directly. Earlier Rmd sources other than `cva.Rmd`, `_site.yml`,
`profile.css` and `site-template.html` are legacy files, not the current build.

Original publication titles and author order must be preserved. Citation counts
were consulted on 11 September 2026; update that date when refreshing counts.
Do not combine duplicate or preprint citation records.

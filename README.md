# Xavier Barber’s personal website

Published with GitHub Pages at https://xavierbarber.github.io/.

The editable page sources are `index.Rmd`, `xbarber.Rmd` and `cva.Rmd`.
The pages contain Markdown and HTML, with no executable R chunks.

Build with Python 3 and Pandoc:

```sh
python3 build_site.py
# Or specify the executable:
python3 build_site.py --pandoc /path/to/pandoc
```

Commit the sources together with the regenerated HTML files. GitHub Pages serves
the HTML in the repository root. `profile.css` and `site-template.html` provide
the shared responsive layout. The older `_site.yml` describes the legacy Distill
build; use `build_site.py` for these three updated pages.

Publication citation counts were read from Google Scholar on 11 September 2026.
Update the access date whenever refreshing counts. Do not add citation counts
from duplicate or preprint records. Preserve original titles and author order,
and label preprints and consortium collaborations explicitly.

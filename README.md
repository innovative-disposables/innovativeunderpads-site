# innovativeunderpads.com

Static site for Innovative Disposables. No framework, no dependencies beyond Python 3.

- `src/layout.html`: shared header, footer and page shell.
- `src/pages/*.html`: one file per page. The three comments at the top set the title, meta description and active nav item.
- `static/`: stylesheet, script and images, copied as-is.
- `python3 build.py` writes the finished site to `site/` (the folder to deploy).

Rules for content: no names or faces of staff or owners anywhere; no prices.

The quote form is handled by Netlify Forms (form detection must be on in Netlify). Submissions land on thanks.html; set email notifications in Netlify under Forms. Adding `data-draft` to the form turns submissions off again.
The logo goes in `static/images/logo.svg`; un-comment the `logo-slot` line in `src/layout.html`.

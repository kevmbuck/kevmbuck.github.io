# Kevin Buck Academic Website

Quarto source for https://kevmbuck.github.io.

## Development

Install Quarto 1.6 or newer and Python 3.12 or newer, then run:

```sh
python -m pip install -r requirements-dev.txt
quarto preview
```

Edit root `.qmd` files for page content, `data/publications.yml` for publications, and `styles.scss` for styling. Homepage publication highlights use the publication catalog.

## Publishing

Push to `main` to render, test, validate, and deploy to GitHub Pages. To check locally, run `quarto render`, `pytest -v`, and `python scripts/validate_site.py`.

The separate `academic-website-preview` repository remains private for draft review.

The Brown favicon is sourced from Brown University's official website. Brown marks retain their respective ownership.

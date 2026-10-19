# ITCS 3162 — Data Projects Portfolio

A responsive, static portfolio presenting four projects from UNC Charlotte's ITCS 3162 course. It includes a project index, four case-study pages, charts extracted from the supplied notebooks, and cleaned notebook downloads.

## Preview locally

No package installation or build framework is required:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`.

## Rebuild pages after editing project content

Edit `data/projects.json`, then run:

```bash
python3 scripts/build_site.py
python3 -m unittest discover -s tests -v
```

The generated HTML is checked in so GitHub Pages can serve it directly from the repository root. All styles, scripts, and chart images are local; the site has no runtime API or external font dependency.

## Projects

1. **How Hong Kong connected** — country-year internet adoption indicators, 1980–2020.
2. **A decision tree on a 61-row loan sample** — exploratory loan-outcome classification, clearly caveated for its small sample and single split.
3. **When weather meets produce prices** — UK produce prices and weather, 2017–2022.
4. **Exploring customer segments** — PCA diagnostics and three-cluster K-means exploration.

## Contents

- `index.html` — landing page and project index.
- `projects/<slug>/index.html` — individual case studies.
- `assets/charts/` — figures extracted from the supplied notebooks.
- `notebooks/` — copies of the supplied `.ipynb` files with execution outputs removed and Google Drive paths normalized to `data/`.
- `data/projects.json` — page copy and chart metadata.
- `scripts/build_site.py` — static page generator.
- `tests/` — content, link, and notebook-sanitization checks.

## Dataset notes

The four notebooks reference CSVs stored in a personal Google Drive path; those CSVs were not attached and are intentionally not included. The filenames and any source notes preserved in the notebooks are listed in [`notebooks/README.md`](notebooks/README.md). Obtain the datasets from their original sources and check their licenses/redistribution terms before adding them or publishing derived data beyond the supplied charts.

The loan-classification case study is explicitly described as an educational exercise, not a credit decision model. All project results are exploratory and include limitations in the case-study pages.

## GitHub Pages

A GitHub Actions workflow in `.github/workflows/pages.yml` publishes the static site whenever changes are pushed to `main` and can also be run manually. After the repository is created, set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. The workflow uploads the static root and deploys it; the generated site uses relative links so it works at a repository subpath. Project charts open in a full-size viewer; the page position is preserved while the viewer is open.

## Notebook preparation

Notebook downloads preserve code and notebook metadata while removing saved outputs (which can contain copied data tables and large figures). Drive file paths were changed from the user's personal Drive path to `data/<filename>`. See the notebook README before running.

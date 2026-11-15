# bartmann.xyz

Personal site: FastAPI and Jinja templates, no build step.

- Run locally: `make run` (http://127.0.0.1:2000).
- Styles are plain CSS in `app/static/css/main.css`. The colour tokens (`--ui-*`) are the
  palette of thirdpartycheck.com and requestsearch.com (`tpc/site_assets/chrome.css` in the
  `tpc` repository); keep them in step.
- All routes share the Jinja environment in `app/templating.py`.
- Deployed by Coolify on the Hetzner host from `main`, using the `Dockerfile`.
- Home page background: `app/static/scripts/bounce.js` bounces a pixel-art head behind the
  sections and shows the next beard stage on every bounce. Frames are
  `app/static/images/bartmann/beard-0.png` to `beard-7.png`: same width, head centre at
  50% / 54.9% of the image width (the CSS and script rely on this). Set `FRAMES` in the
  script when adding stages.

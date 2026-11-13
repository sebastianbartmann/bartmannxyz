# bartmann.xyz

Personal site: FastAPI and Jinja templates, no build step.

- Run locally: `make run` (http://127.0.0.1:2000).
- Styles are plain CSS in `app/static/css/main.css`. The colour tokens (`--ui-*`) are the
  palette of thirdpartycheck.com and requestsearch.com (`tpc/site_assets/chrome.css` in the
  `tpc` repository); keep them in step.
- All routes share the Jinja environment in `app/templating.py`.
- Deployed by Coolify on the Hetzner host from `main`, using the `Dockerfile`.

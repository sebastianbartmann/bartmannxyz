# bartmann.xyz

Personal site: FastAPI and Jinja templates, no build step.

- Run locally: `make run` (http://127.0.0.1:2000).
- The look is the one of thirdpartycheck.com (decision 2026-11-25). `app/static/css/chrome.css`
  (fonts, `--ui-*` colour tokens, header, footer) and `site.css` are copies from the `tpc`
  repository (`tpc/site_assets/`); do not edit them here, change tpc first and copy again.
  Styles only this site needs go into `local.css`: tokens only, 4px/5px radii, no shadows.
  Templates use tpc's class names and its header and footer markup.
- Fonts are the self-hosted IBM Plex files from tpc in `app/static/fonts/`. There is no logo
  mark in the pages, as on thirdpartycheck.com. The tab icon (a "b" on black: `favicon.svg`,
  `favicon.ico`, `apple-touch-icon.png` in `app/static/`) is served from the root paths.
- All routes share the Jinja environment in `app/templating.py`.
- Deployed by Coolify on the Hetzner host from `main`, using the `Dockerfile`.
- Home page background: `app/static/scripts/bounce.js` bounces a pixel-art head behind the
  sections and shows the next beard stage on every bounce; after the last stage the beard
  floods the page (`beard-texture.png`), then falls off and the cycle restarts. Frames are
  `app/static/images/bartmann/beard-0.png` to `beard-11.png`: all 512px wide, head 50.8% of
  the width, head centre at 50% / 35.1% of the width (the CSS and script rely on this). Set
  `FRAMES` in the script when adding stages.
- Posts are templates in `app/templates/blog/posts/` extending `blog/post.html`, which adds the
  way back and the date above the title. A new post sets the `post_title` and `post_date`
  blocks and gets a row in `blog/partials/overview.html` and `app/static/sitemap.xml`.
- Coolify does not deploy on push; start the deploy through its API (vault:
  `infrastructure/hetzner.md`).

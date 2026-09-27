# GitHub Pages Deploy Design

## Goal

Publish the static site at `https://p-v-dev.github.io/PWA/` whenever `main` changes, with a manual dispatch option.

## Architecture

Use GitHub's official Pages artifact flow. One build job checks out the repository, configures Node 22, runs the Python tests, builds `dist/` with contact values from GitHub Repository Variables, and uploads the Pages artifact. A dependent deploy job configures Pages and publishes that artifact to the `github-pages` environment.

## Configuration

All `CONTACT_*` values come from Repository Variables because they are public in the generated site. `CONTACT_WHATSAPP_NUMBER` remains required; optional empty values stay hidden. `SITE_URL` is fixed in the workflow to `https://p-v-dev.github.io/PWA/` and the build replaces domain placeholders in `robots.txt`, `sitemap.xml`, and `llms.txt`.

## Safety And Verification

The build job receives only `contents: read`; the deploy job receives only `pages: write` and `id-token: write`. Deployments use Pages concurrency control. Static tests verify the workflow contract and generated public URLs; the existing build validation prevents deployment with an invalid WhatsApp number, email, Maps URL, or site URL.

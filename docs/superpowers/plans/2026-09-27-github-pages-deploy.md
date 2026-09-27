# GitHub Pages Deploy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish `dist/` at `https://p-v-dev.github.io/PWA/` from GitHub Actions.

**Architecture:** The existing Node build receives public contact values through Repository Variables and receives the fixed Pages URL through `SITE_URL`. GitHub's official artifact-based Pages actions test, build, upload, and deploy the static output.

**Tech Stack:** GitHub Actions, Node.js 22, Python unittest, GitHub Pages official actions.

## Global Constraints

- Keep the site static and dependency-free.
- Keep `.env` local and ignored.
- Use Repository Variables for public contact data.
- Do not commit without an explicit user request.

---

### Task 1: Public URL Build Support

**Files:**
- Modify: `tests/test_static_site.py`
- Modify: `build.mjs`
- Modify: `.env.example`

- [ ] Add a failing test that builds with `SITE_URL=https://p-v-dev.github.io/PWA/` and asserts that generated `robots.txt`, `sitemap.xml`, and `llms.txt` contain that URL and no domain placeholder.
- [ ] Run `python -m unittest tests.test_static_site.StaticSiteTest.test_build_generates_public_contact_config_without_env_file -v` and confirm failure on `SEU_DOMINIO_AQUI`.
- [ ] Read `SITE_URL`, require HTTPS, remove a trailing slash for replacement, and replace `https://SEU_DOMINIO_AQUI` in the three generated files.
- [ ] Add `SITE_URL=https://p-v-dev.github.io/PWA/` to `.env.example`.
- [ ] Re-run the targeted test and confirm it passes.

### Task 2: Official Pages Workflow

**Files:**
- Create: `.github/workflows/deploy-pages.yml`
- Modify: `tests/test_static_site.py`

- [ ] Add a failing static test asserting push to `main`, `workflow_dispatch`, Pages permissions, Node 22, tests, build, `dist/` artifact upload, and official deploy action.
- [ ] Run the targeted test and confirm failure because the workflow is absent.
- [ ] Create the two-job workflow using `actions/checkout@v4`, `actions/setup-node@v4`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v3`, and `actions/deploy-pages@v5`.
- [ ] Map `CONTACT_*` from `${{ vars.* }}` and set `SITE_URL` to the approved Pages URL.
- [ ] Re-run the targeted test and confirm it passes.

### Task 3: Operator Documentation And Verification

**Files:**
- Modify: `README.md`

- [ ] Document the seven Repository Variables and the GitHub Pages source setting `GitHub Actions`.
- [ ] Run `python -m unittest discover -s tests -v` and expect all tests to pass.
- [ ] Run `node --env-file=.env.example build.mjs` and expect `Site gerado em dist/.`.
- [ ] Run `git diff --check` and expect no output.

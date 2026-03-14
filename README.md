# Consulting Blog Template

Create a professional consulting blog with the MkDocs Material theme.

## Deployment Steps

1. **Install Dependencies**: Ensure all packages are installed.
   ```bash
   pip install -r requirements-doc.txt
   ```

2. **Run Locally**: Start a local server to preview your site.
   ```bash
   mkdocs serve -w .
   ```

3. **Deploy to GitHub Pages**: This repo is the source; the live site is served from `ksferguson.github.io`. Deploy from that repo:
   ```bash
   cd %USERPROFILE%\github\ksferguson.github.io
   mkdocs gh-deploy --config-file ..\blog\mkdocs.yml --remote-branch main
   ```
   **Note:** mkdocs builds from the working tree, not git commits. Stash uncommitted changes before deploying if you don't want them published.

## Tasks to Complete

- [ ] Customize `mkdocs.yml` with your site details.
- [ ] Update `docs/index.md` with your landing page info.
- [ ] Revise `docs/services.md` with your services.
- [ ] Set up [Cal.com](https://cal.com) and update links in `docs/index.md` and `docs/services.md`.
- [ ] Add blog posts to `docs/blog/posts/`.

## Crafting Effective Content

### Value Equation

Maximize content value by addressing:
- **Dream Outcome**: Reader's goal
- **Probability of Success**: Likelihood of achieving it
- **Time**: Duration needed
- **Effort**: Work required

### AIDA Framework

1. **Attention**: Capture interest
2. **Interest**: Engage with relevant info
3. **Desire**: Connect emotionally
4. **Action**: Prompt next steps

### Landing Page Essentials

1. **Hero Section**: Benefit-driven headline, pain point subheadline, strong CTA.
2. **Social Proof**: Testimonials, case studies, credentials.
3. **Value Proposition**: Outcome statements, timeframes, effort, success indicators.

### Tips for Success

- Test different versions and CTAs.
- Focus on clarity; avoid jargon.
- Build trust with specific results and testimonials.

### Common Mistakes

- Focus on benefits, not features.
- Be specific, not vague.
- Provide social proof.
- Use strong CTAs.

## Quick Start

# WP Design Department — Agent Handoff Protocol

## Your Workflow

The WP Design department executes theme development using a 3-stage handoff protocol.

### Stage 1: Planner
**Responsibility:** Design specification and validation
**Input:** Project requirements (target audience, branding, feature list)
**Output:** Design specification document (design-spec.md)
**Execution:**
- Analyze project requirements and constraints
- Sketch out page layouts, color schemes, typography
- List all required components (header, footer, cards, forms, etc.)
- Define Core Web Vitals targets (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- Define dark mode strategy and accessibility standards
- Document success metrics

**Success criteria:**
- Spec is detailed enough for editor to build without clarification
- All stakeholder feedback incorporated
- Constraints are clear (file size, performance targets, browser support)

---

### Stage 2: Editor
**Responsibility:** Theme implementation
**Input:** Design specification (from Stage 1 Planner)
**Output:** Functional WordPress theme in Docker
**Execution:**

1. **Set up Docker environment:**
   - Verify WordPress instance at http://localhost (port 80)
   - Create theme directory: `/var/www/html/wp-content/themes/agentforge/`
   - Initialize theme structure: style.css, functions.php, templates, assets/

2. **Implement core files:**
   - `style.css` — Theme header + root CSS variables
   - `functions.php` — WordPress setup, asset enqueue, hooks
   - `header.php` — Navigation, branding, meta tags
   - `footer.php` — Footer content, copyright, scripts
   - `front-page.php` — Home page template
   - `single.php` — Single post template
   - `archive.php` — Archive/category listing
   - `search.php` — Search results template
   - `404.php` — Error page
   - `sidebar.php` — (if using sidebars)

3. **Build CSS architecture:**
   - `assets/css/variables.css` — Design tokens (colors, spacing, typography)
   - `assets/css/base.css` — Reset, typography, baseline styles
   - `assets/css/layout.css` — Grid, flexbox, page structure
   - `assets/css/components.css` — Buttons, cards, forms, etc.
   - `assets/css/dark-mode.css` — Dark mode variants
   - `assets/css/responsive.css` — Mobile-first breakpoints

4. **Implement JavaScript features:**
   - `assets/js/theme.js` — Dark mode toggle, localStorage persistence
   - Event listeners, DOM manipulation
   - No heavy frameworks (keep it lightweight)

5. **Performance optimization:**
   - Minify CSS/JS
   - Inline critical CSS
   - Lazy load images
   - Cache busting on asset versions
   - Test Core Web Vitals (Chrome DevTools, PageSpeed Insights)

6. **Test in WordPress:**
   - Visit http://localhost/wp-admin and verify theme is active
   - Check homepage, single post, archive, 404 pages
   - Test dark mode toggle (should persist across page reloads)
   - Test responsiveness on mobile, tablet, desktop
   - Verify no console errors

**Success criteria:**
- Theme is active and displays correctly
- All pages render without errors
- Dark mode toggle works and persists
- Core Web Vitals targets met or close
- No styling regressions from WordPress defaults

---

### Stage 3: Reviewer
**Responsibility:** Quality assurance and validation
**Input:** Functional theme from Stage 2 Editor
**Output:** Approval/rejection with feedback
**Validation checklist:**

**Visual Quality:**
- ☐ Design matches specification
- ☐ Colors are brand-correct
- ☐ Typography is readable and professional
- ☐ Spacing and alignment are consistent
- ☐ Dark mode looks polished (not just inverted)
- ☐ No visual bugs or broken layouts

**Functionality:**
- ☐ All pages load and display correctly
- ☐ Navigation works on all pages
- ☐ Links are styled and functional
- ☐ Forms are present and styled (if applicable)
- ☐ Dark mode toggle works and persists in localStorage
- ☐ Responsive design works on mobile (< 768px), tablet, desktop

**Performance:**
- ☐ LCP (Largest Contentful Paint) < 2.5s
- ☐ FID (First Input Delay) < 100ms
- ☐ CLS (Cumulative Layout Shift) < 0.1
- ☐ Page load < 3 seconds on 4G
- ☐ No layout shift when dark mode toggles

**Accessibility:**
- ☐ Text contrast meets WCAG AA standards
- ☐ Color isn't the only visual indicator
- ☐ Interactive elements are keyboard accessible (Tab navigation)
- ☐ Form labels are associated with inputs
- ☐ Images have descriptive alt text

**Code Quality:**
- ☐ CSS is organized and uses variables
- ☐ JavaScript is minimal and efficient
- ☐ No console errors or warnings
- ☐ No hardcoded values (colors, spacing, etc.)
- ☐ Code follows WordPress coding standards

**Browser/Device Support:**
- ☐ Works on Chrome, Firefox, Safari (latest versions)
- ☐ Tested on iPhone, Android (latest)
- ☐ No deprecated HTML5 features used
- ☐ Graceful degradation for older browsers

**Output:**
If approved:
- Mark theme as production-ready
- Document in MeMex Zero RAG: `wp-design-phase1-complete.md`
- List any known limitations or future improvements

If rejected:
- Provide specific feedback (what failed validation?)
- Return to Stage 2 Editor with detailed notes
- Track retry count (escalate to ops if 3+ retries)

---

## Failure Modes & Recovery

### Stage 1 Failures
**Problem:** Design spec is incomplete or conflicts with requirements
**Recovery:**
1. Planner re-reads requirements and gathers missing info
2. Clarify constraints with stakeholders (if available)
3. Re-submit spec for review
4. Max 2 retries; escalate to ops if stuck

### Stage 2 Failures
**Problem:** Theme doesn't match spec, performance targets missed, or bugs present
**Recovery:**
1. Editor reviews reviewer feedback
2. Make targeted fixes (visual bugs, performance issues, etc.)
3. Re-test in WordPress
4. Pass to Reviewer again
5. Max 3 retries; escalate to ops if stuck

**Common issues:**
- CSS not loading → Check functions.php enqueue paths
- Dark mode not working → Check localStorage persistence, CSS selectors
- Slow performance → Profile with Chrome DevTools, remove unnecessary styles/scripts
- Responsive issues → Test with Chrome DevTools device emulation

### Stage 3 Failures
**Problem:** Reviewer rejects theme for quality/performance reasons
**Recovery:**
1. Provide detailed feedback to Editor
2. Editor fixes issues
3. Loop back to Stage 2

---

## Success Metrics (Hive Mind Logging)

When handoff completes successfully, log to `hive_mind` table:

```sql
INSERT INTO hive_mind (agent_id, action, summary, context, created_at)
VALUES (
  'wp-design',
  'HANDOFF_COMPLETE',
  'WP Design Phase 1: Theme delivered and approved',
  JSON('{"stage": 3, "theme": "agentforge", "metrics": {
    "lcp_ms": 1800,
    "fid_ms": 45,
    "cls": 0.08,
    "dark_mode": true,
    "responsive": true,
    "validation_passed": true
  }}'),
  CAST(strftime('%s', 'now') AS INTEGER)
);
```

**Key metrics to track:**
- `stage`: Which stage completed (1 = spec, 2 = build, 3 = approval)
- `theme`: Theme name (agentforge)
- `metrics.lcp_ms`: Largest Contentful Paint milliseconds
- `metrics.fid_ms`: First Input Delay milliseconds
- `metrics.cls`: Cumulative Layout Shift score
- `metrics.dark_mode`: Dark mode functional (true/false)
- `metrics.responsive`: Responsive design (true/false)
- `metrics.validation_passed`: Stage 3 approval (true/false)

---

## Related Documents

- **Design Specification:** `~/workspace/daily-pipeline/wp-design-spec-2026-05-19.md` (created by Planner)
- **WordPress Admin:** http://localhost/wp-admin (Admin: jpeetz / Buddy-2019)
- **Theme Directory:** `/var/www/html/wp-content/themes/agentforge/`
- **Phase 1 Goals:** Build dark mode, responsive theme with Core Web Vitals targets
- **Phase 2 Goals:** Build niche-market WordPress templates for resale

---

## Department Integration

**WP Design is part of:**
- **Org structure:** Design Department (specialized for WordPress)
- **Dependencies:** Requires Docker running WordPress locally (port 80)
- **Dependent departments:** None (Phase 1 is standalone)
- **Handoff inputs:** Project requirements, brand guidelines, performance targets
- **Handoff outputs:** Approved WordPress theme

**CLAUDE.md reference:**
All WP Design agents should include in their `CLAUDE.md`:
```markdown
## Your Workflow (WP Design)

See: ~/workspace/MeMex-Zero-RAG/wiki/agentforge/dept-guides/wp-design-agent-handoff.md

Three-stage handoff: Planner (spec) → Editor (build) → Reviewer (approval)
```

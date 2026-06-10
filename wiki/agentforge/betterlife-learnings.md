# BETTERLIFE PROJECT LEARNINGS & SPECIFICATION

_Updated 2026-06-07. A unified manual of architectural design, compliance requirements, and implementation guidelines distilled from the entire development of the BetterLife ecosystem (iOS App, Vercel Landing Site, and Custom WordPress Theme)._

---

## 1. iOS App (SwiftUI & StoreKit 2)

### Architecture & State Management
- **Single Source of Truth:** Built using SwiftUI’s modern `@Observable` macro (`AppState.swift`) which controls app navigation, profile state, active goals list, mood logs, and API session streams.
- **Dark Mode Enforcement:** The app enforces a premium dark theme (`.preferredColorScheme(.dark)`) using a custom palette of deep indigos (`#0F0A2A`), translucent cards (`#1A1548`), and glowing violet accents (`#7B2FBE`).

### Compliance & Safety Protocols
- **AI Consent (Guideline 5.1.1 & 5.1.2):** Must present a dedicated onboarding screen (`AIConsentView`) requesting explicit permission before transmitting data to external APIs (OpenRouter/Anthropic Claude). Disclosure must detail WHO receives data, WHAT is sent, and WHY (GDPR, 30-day logs purge, no training).
- **Auto-renewable Subscriptions (Guideline 3.1.2c):** The purchase flow must contain a clear title, duration, price, and price-per-unit for each plan. 
  - **CRITICAL:** Do NOT rely on external web links (`Link`) for legal compliance pages (EULA/Privacy) in the SwiftUI views. Apple's review networks and sandboxed testing environments often block external browser actions, triggering rejections for "non-functional links".
  - **FIX:** Present EULA and Privacy documents **directly inside the app** using native, self-contained sheet modals (`LocalDocumentView.swift`) containing the full text of the Apple Standard EULA and the Privacy Policy.
- **Crisis Safety Net:** Local regex check filters user messages for self-harm/suicide terms in 8 EU languages. If triggered, the LLM stream is aborted, and a locked native Crisis Banner provides region-appropriate hotlines (US, UK, IE, DE, etc.).

---

## 2. Landing Site (Vercel & Vanilla HTML/JS)

### Styling & Brand Aesthetics
- **Fluid Layout:** Designed with a mobile-first dark aesthetic. Uses CSS variables matching the Swift `DesignSystem` for unified color-grading across web and mobile.
- **Responsive Screen Carousel:** Screenshot carousels must automatically adjust their slide count and active alignment dynamically on window resize events to prevent cut-off images on mobile or tablet sizes.
- **Micro-interactions:** Interactive cards transition via `translateY(-6px)` and variable box-shadow glow gradients on hover.

### Serverless API Integration
- **Spam Control:** Subscriber submission forms (`/api/subscribe`) use an invisible honeypot field and strict syntax checks to reject bot submissions.
- **Scoring Engine:** The Executive Fatigue Quiz (`/api/diagnostic-quiz`) computes stress responses locally, scoring the user's focus patterns to yield specific sub-profiles and pairing them with a recommended AI coach profile.

---

## 3. WordPress Theme (betterlife-theme & Custom DB)

### Performance & Asset Management
- **Per-Template Stylesheets:** To maintain high SEO page speed scores, avoid loading a global CSS bundle. Instead, dynamically register and load stylesheets (`aria.css`, `aeron.css`, `unified.css`) conditional on the current active page template.
- **Smart App Banner:** Integration of Apple's numeric App ID in the head tag, controlled dynamically via the WordPress Customizer settings.

### Database Compliance & GDPR
- **Subscriber Security:** Email records are stored in a dedicated database table (`wp_betterlife_subscribers`) rather than general `wp_options`.
- **Encryption at Rest:** Emails are encrypted at rest using AES-256-CBC, with a local decryption utility provided securely in the WordPress admin panel.
- **Clinical Research Vault:** Implemented a custom post type (`betterlife_research`) to host academic and ICF coaching standards on clinical-grade coaching outcomes.

### Pipeline Automation
- **SEO & Density Auditor:** Uses the `verify_seo_geo.py` tool. This strips template markup and sends content to an analysis endpoint to audit entity density, Flesch readability, and E-E-A-T score alignment before site deployment.

---

## 4. Production Submission Checklist

- [ ] **Scaffolding Cleanup:** Double-check that simulated development hooks, such as resetting the local database or clean-slate `UserDefaults` wipes in `AppState.init()`, are disabled or nested behind `#if DEBUG`.
- [ ] **Verify API Keys:** Ensure a valid OpenRouter API key is compiled into the build (e.g., as the fallback return in `Config.swift` or a bundled JSON resource) rather than relying on local Mac filesystem path lookups, which fail on Apple's review devices.
- [ ] **EULA Link in App Store Metadata:** Add `Terms of Use (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/` to the bottom of the App Store Description.
- [ ] **Re-select IAP Products:** Re-attach all subscription IDs under "In-App Purchases and Subscriptions" on the active version submission page in App Store Connect.

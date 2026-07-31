# BetterLife — Product Management Analysis

**Generated:** 2026-06-08 | **Framework:** deanpeters/Product-Manager-Skills (7 frameworks applied)
**Status:** Pre-Launch (v0.8) | **App:** iOS AI Life Coach | **Founder:** Joerg Peetz

---

## 1. Problem Framing Canvas (MITRE)

### Look Inward — Assumptions
- **Assumption: Aeron's tough-love persona is desired.** The competitive set (Wysa, Woebot, Replika) defaults to supportive/gentle. Aeron is the differentiator — but is it the *right* one? Untested with real users.
- **Assumption: Local-only UserDefaults is a feature.** It's also a constraint — no cross-device sync, no web companion, no data recovery on phone reset. Is this user-serving, or engineering convenience dressed as privacy?
- **Bias risk:** Built by a tech-savvy founder. The Aeron persona may reflect what Joerg wants, not what the broader market needs.

### Look Outward — Who Experiences the Problem?
- **Primary:** Adults 25-45 with mild-to-moderate anxiety, motivation issues, ADHD — who can't afford human coaching ($100-300/session)
- **Secondary:** Self-improvement enthusiasts who've tried habit trackers and found them shallow
- **Left out:** Non-English speakers (8 EU crisis languages but coaching is English-only), Android users (iOS exclusive), people who want partner/family coaching

### Reframe
> *Stated another way:* People who need accountability coaching can't access it — human coaches are too expensive, free apps are too shallow, and existing AI coaches are too polite to create real behavior change.

> *HMW:* Deliver the accountability of a human coach at 1/20th the price, while ensuring the "tough love" persona doesn't alienate users who need gentleness?

---

## 2. Opportunity Solution Tree (Teresa Torres)

**Desired Outcome:** 1,000 paid subscribers within 90 days of App Store launch

### Opportunity 1: Trust — Users don't trust AI with mental health data
- **Solutions:** Privacy page with real architecture diagram, GDPR export button (exists), publish security whitepaper
- **Experiment:** A/B test privacy-first vs. feature-first landing page messaging

### Opportunity 2: Aeron persona might alienate 60% of users
- **Solutions:** Onboarding persona selector (Aeron/Supportive/Aria), adaptive tone based on mood, allow mid-session switching
- **Experiment:** User test 10 people — Aeron-only vs. Aeron+supportive option. Measure drop-off after 1 session.

### Opportunity 3: $9.99/mo is above the $5/mo mobile app psychological ceiling
- **Solutions:** Add $4.99/mo entry tier with limited sessions, keep $9.99 as Pro, lifetime as anchor. Or 7-day free trial, no credit card.
- **Experiment:** Test conversion at $4.99 vs $9.99 with 100 landing page visitors each.

### Opportunity 4: iOS-only limits TAM by ~50%
- **Solutions:** Android port (Jetpack Compose), web companion
- **Experiment:** Survey landing page visitors — "What phone do you use?" — measure Android demand.

### Opportunity 5: Zero social proof at launch
- **Solutions:** Beta tester testimonials, clinical advisory board endorsement
- **Experiment:** Add 3 beta quotes to landing page — measure conversion lift.

---

## 3. TAM / SAM / SOM

| Layer | Estimate | Math |
|-------|----------|------|
| **TAM** | $5.6B | Global mental wellness app market, projected $17.4B by 2030 at 16.5% CAGR |
| **SAM** | $1.2B | English-speaking iOS users, 25-45, disposable income for $5-10/mo subs. ~120M people × 10% willing to pay = 12M potential |
| **SOM** | $120K-$600K ARR | Year 1: 1,000-5,000 paid subs at blended ARPU ~$10/mo. Net after 15% App Store: ~$8.50/sub/month |

**Reality check:** Wysa raised $20M+ with ~5M users but unclear paid conversion. Replika has $70M+ revenue. Market is real. BetterLife at $9.99 is premium for an unproven app.

---

## 4. Press Release (Amazon Working Backwards)

**Headline:** *BetterLife Launches the First AI Coach That Actually Calls You Out — No Sugarcoating, Just Results*

**Dateline:** Dublin, Ireland — Launch Day 2026

**Introduction:** BetterLife today announced the public launch of its iOS AI coaching app, bringing the accountability of a $300/hour executive coach to anyone with an iPhone — at $9.99/month. Built on clinical frameworks (CBT, ICF coaching standards) and powered by Claude AI, BetterLife is the first wellness app that prioritizes honesty over comfort.

**Problem:** 80% of people who set self-improvement goals abandon them within 6 weeks. Human coaches work — but at $100-300/session, they're inaccessible. Existing apps offer encouragement but lack accountability. Replika is a companion; BetterLife is a coach.

**Solution:** BetterLife's AI coach Aeron delivers structured coaching sessions with direct, no-nonsense feedback. The app includes CBT Thought Reframer for cognitive distortions, ADHD SOS for 120-second focus interventions, and crisis detection in 8 languages. All data stays on-device.

**Quote:** "Most wellness apps treat you like glass. BetterLife treats you like an adult who can handle the truth." — Joerg Peetz, Founder

---

## 5. Positioning Statement (Geoffrey Moore)

**Value Proposition:**
> **For** adults aged 25-45 struggling with motivation, focus, and accountability
> **that need** the directness of a human executive coach but can't justify $300/session
> **BetterLife** is an **AI coaching app**
> **that** delivers structured accountability, CBT interventions, and crisis-aware safety — all on-device, private by default.

**Differentiation:**
> **Unlike** Replika (companion, not coach) and Wysa (gentle to a fault),
> **BetterLife** provides **real accountability** — the Aeron persona calls out excuses, tracks follow-through, and adapts coaching style by culture.

**Unfair advantage:** The Aeron persona. Nobody has a coach that says "That's your third excuse this week. What are you actually afraid of?"

---

## 6. Finance-Based Pricing Assessment

**Current:** $9.99/mo | $79.99/yr (33% discount) | $149.99 lifetime

**Analysis:**
- $9.99 is 2-2.5× Finch ($39/yr) and Fabulous ($40/yr). Premium positioning with zero brand recognition.
- AI coaching apps see 40-60% Month 1 churn. At $9.99, churners leave negative reviews ("overpriced").
- Lifetime at $149.99 = 15 months of monthly. If average retention is 4-6 months (typical wellness app), lifetime buyers overpay — revenue win, but creates non-paying cohort forever.

**Recommendation:**
1. Add **$4.99/mo Starter** — 10 sessions/month, one persona only. Reduces conversion friction.
2. Keep $9.99 as **Pro** — unlimited sessions, all personas, CBT toolkit, ADHD SOS.
3. Keep $149.99 lifetime as **anchor** — makes annual look like a deal.
4. Add **7-day free trial** — no credit card required. Let Aeron prove herself.

---

## 7. Business Health Diagnostic (Pre-Launch)

| Dimension | Status | Risk |
|-----------|--------|------|
| **Product** | v0.8, 6 blockers remain | 🟡 Medium — core works but API key in Config.swift is critical |
| **Team** | Solo founder + Antigravity AI | 🔴 High — no co-founder, no clinical advisor, no marketing help |
| **Market** | Validated ($5.6B TAM) | 🟢 Low — market exists and is growing |
| **Differentiation** | Aeron persona | 🟡 Medium — untested with real users |
| **Monetization** | 3 tiers, StoreKit 2 | 🟢 Low — infrastructure ready |
| **Compliance** | GDPR + crisis safety done | 🟢 Low — strong privacy story |
| **Go-to-Market** | No plan | 🔴 High — no launch strategy, no press list, no influencer outreach |

**Critical pre-launch fix:** API key in Config.swift. Hardcoded credentials = guaranteed App Store rejection.

---

## 8. Three Highest-Impact Pre-Launch Moves

1. **Ship API key fix + persona selector.** Security blocker first, then let users choose Aeron vs. supportive coach at onboarding. De-risks the "tough love" concern.
2. **Add $4.99 Starter tier.** Lower friction acquisition. $9.99 Pro is aspirational; $4.99 is the door opener.
3. **Run a 20-person beta.** Recruit from Reddit r/getdisciplined, r/ADHD, r/productivity. 30 days free. Collect 10 video testimonials. Measure day 3, day 7, day 14 retention.

---

## 9. Synthesis

**Strengths:** Aeron persona is genuinely differentiated. Privacy-first architecture is a real moat. CBT + crisis detection shows clinical thinking, not AI wrapping.

**Weaknesses:** iOS-only limits reach. $9.99/mo is brave for unproven. Zero market validation. Solo founder risk.

**Verdict:** Product thinking is sound. Risks are executional, not conceptual. Ship the 6 blockers, test with real users, adjust pricing before marketing spend.

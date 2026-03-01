---
name: cro-audit
description: Audit conversion rate optimization — messaging clarity, trust placement, funnel flow, persuasion structure, and copy effectiveness
---

# CRO Audit — Conversion Rate Optimization

This skill audits a project's conversion effectiveness — messaging clarity, persuasion structure, trust placement, funnel narrative, and copy quality. It identifies what's blocking conversions and fixes issues directly in the codebase.

No arguments needed. Just run `/cro-audit` and the skill scans the project automatically.

### How it differs from other audits
- **UX audit** = does the flow work? (behavioral outcomes, cognitive load)
- **UI audit** = does it look right? (visual polish, spacing, consistency)
- **CRO audit** = does it convert? (messaging, trust placement, funnel narrative, copy)

Reference sources:
- Joanna Wiebe / Copyhackers: conversion copywriting
- CXL Institute: evidence-based CRO
- Cialdini's Principles of Persuasion
- Schwartz's Levels of Awareness (Eugene Schwartz, Breakthrough Advertising)

---

## Step 0: Understand the project

Before auditing, read:
- `CLAUDE.md` / `README.md` for project context
- All page components (understand the page narrative)
- CTAs — copy, placement, frequency, visual weight
- Trust signals — testimonials, badges, guarantees, numbers
- Forms and conversion points
- Above-the-fold content (hero section)
- Post-conversion experience (confirmation, next steps)

Identify:
- **Primary conversion goal** (what's the one thing the visitor should do?)
- **Target audience awareness level** (unaware → problem-aware → solution-aware → product-aware → most aware)
- **Page narrative arc** (what story does the scroll tell?)
- **Trust stack** (what proof exists and where is it placed?)

---

## Step 1: Audit against CRO principles

Go through **each category** below. For every issue found, note the file, the specific principle violated, and the recommended fix. Rate severity as:
- **🔴 Critical** — likely killing conversions
- **🟠 Major** — measurably reducing conversion rate
- **🟡 Minor** — optimization opportunity

---

### Category 1: Value Proposition & Messaging

#### Above-the-Fold Clarity (5-Second Test)
> A stranger should understand what you offer, who it's for, and what to do next within 5 seconds.

**Check for:**
- Headline that's vague, clever, or jargon-heavy instead of clear
- Missing or buried subheadline that explains the benefit
- No clear CTA visible without scrolling
- Hero section that prioritizes aesthetics over clarity
- Headline that could belong to any competitor (not specific enough)

**Fix pattern:** Headline = clear benefit. Subheadline = how/for whom. CTA = obvious next step. All three visible above the fold.

---

#### Benefit-Over-Feature Framing
> Users care about outcomes, not capabilities. Features tell, benefits sell.

**Check for:**
- Feature lists without "so that..." outcomes
- Technical capabilities described without user impact
- "What it does" without "what it means for you"
- Product-centric language instead of user-centric language

**Fix pattern:** For every feature, ask "so what?" — rewrite as the outcome the user gets. "AI-powered analysis" → "Versteht, was euch wirklich beschäftigt"

---

#### Specificity & Proof
> Concrete numbers beat vague claims. Specificity signals credibility.

**Check for:**
- Vague claims ("viele Paare", "verbesserte Beziehung", "schnelle Ergebnisse")
- Round numbers that feel made up vs. specific numbers that feel real
- Claims without supporting evidence or source
- Superlatives without proof ("das beste", "einzigartig")

**Fix pattern:** Replace vague claims with specific numbers, timeframes, or cited research. "Viele Paare" → "2.400+ Paare seit 2024". If you can't prove it, soften it or remove it.

---

#### Objection Pre-emption
> Address the top 3-5 objections before they become reasons not to convert.

**Check for:**
- Common objections unaddressed (price, time, privacy, "does it work?", "is it for us?")
- FAQ buried at the bottom instead of addressing objections inline where they arise
- Missing "who this is for / not for" clarity
- No risk reversal near conversion points

**Fix pattern:** Identify top objections for the target audience. Address each one near the point in the page where it naturally arises — not just in the FAQ.

---

#### Headline "So What?" Test
> Read every headline. Ask "so what?" — if you can't answer with a concrete benefit, rewrite.

**Check for:**
- Section headlines that describe the section ("Unsere Funktionen") instead of stating a benefit
- Headlines that are labels, not value propositions
- Headlines that don't create curiosity or communicate a promise
- H2s that work as internal navigation but don't sell

**Fix pattern:** Every section headline should answer "why should I keep reading?" — turn labels into promises. "Funktionen" → "Alles, was ihr braucht — an einem Ort"

---

### Category 2: Trust & Credibility at Decision Points

#### Trust Signal Placement
> Trust signals must appear BEFORE the conversion point, not after. Users need confidence before they commit.

**Check for:**
- Testimonials, badges, or guarantees placed after the main CTA or form
- Trust signals only at the bottom of the page (most users never scroll there)
- No trust signals near the primary conversion point
- Social proof section far from any CTA

**Fix pattern:** Place at least one trust signal within 200px (visually) of every CTA. Testimonials before the pricing section. Guarantees next to the form.

---

#### Social Proof Quality
> Not all social proof is equal. Specific, relatable, outcome-focused testimonials convert best.

**Check for:**
- Generic testimonials ("Toll!", "Super App!", "Hat uns geholfen")
- Testimonials without specific outcomes or transformations
- Anonymous quotes with no name/initials (feels fake)
- All testimonials saying the same thing (no variety of benefits)
- Missing context (relationship stage, how long they've used it)

**Fix pattern:** Each testimonial should contain: (1) the before state, (2) what they did, (3) the specific outcome. Different testimonials should address different objections/benefits.

---

#### Authority Signals
> Research citations, expert endorsements, and methodology references build credibility.

**Check for:**
- Claims about effectiveness without citing research
- No mention of methodology or scientific basis
- Missing "as seen in" / press mentions / expert endorsements
- No credentials or authority markers for the team/product

**Fix pattern:** Cite specific research (author, year). Mention methodology. Add expert endorsements if available. "Basierend auf der Gottman-Methode" > no citation.

---

#### Risk Reversal
> Reduce perceived risk at the moment of conversion. Guarantees, free trials, and "no commitment" language reduce friction.

**Check for:**
- No guarantee or risk reversal near CTA/form
- Missing "kostenlos", "unverbindlich", "jederzeit kündbar" near conversion points
- Price presented without value anchoring or risk mitigation
- No free tier or trial mentioned

**Fix pattern:** Add risk reversal copy directly adjacent to CTA. "Jetzt kostenlos starten — keine Kreditkarte nötig" is more effective than a standalone CTA.

---

#### Proof Hierarchy
> Numbers > Named testimonials > Logos > Generic claims. Use the strongest proof available.

**Check for:**
- Generic claims used where specific numbers exist
- Testimonials used where quantitative results could be shown
- Missing the strongest available proof type
- Proof elements not escalating in strength down the page

**Fix pattern:** Lead with the strongest proof. Use numbers where possible, named testimonials where not, and save generic claims for supporting roles only.

---

### Category 3: Conversion Funnel & Page Flow

#### Content Narrative Arc
> The page should tell a story: Problem → Agitation → Solution → Proof → CTA.

**Check for:**
- Page that jumps straight to features without establishing the problem
- Missing "agitation" — not connecting with the pain/desire emotionally
- Solution presented before the problem is felt
- Proof and CTA disconnected from the narrative
- Sections in an order that doesn't build persuasion momentum

**Fix pattern:** Restructure page flow: (1) Hook — connect with the desire/problem, (2) Agitate — deepen the emotional resonance, (3) Solution — present your answer, (4) Proof — back it up, (5) CTA — make the next step clear and easy.

---

#### CTA Cadence
> A CTA should follow every persuasion block. Don't make users scroll back to convert.

**Check for:**
- CTA only in hero and footer (nothing in between)
- Long persuasion sections (features, testimonials, approach) without a CTA following them
- User must scroll up to find how to convert
- More than 2 full screen heights between CTAs

**Fix pattern:** Add a CTA (or at least a text link) after every major persuasion section. Vary the format: primary button, text link, inline CTA, sticky bar.

---

#### CTA Copy
> CTA text should be action-oriented, benefit-loaded, and ideally first-person.

**Check for:**
- Generic CTA text ("Submit", "Absenden", "Weiter", "Mehr erfahren")
- CTA that describes the action but not the benefit
- All CTAs identical regardless of context
- CTA that creates uncertainty about what happens next

**Fix pattern:** CTA = action + benefit or outcome. "Jetzt starten" > "Absenden". "Kostenlos testen" > "Registrieren". The best CTAs answer "what do I get when I click this?"

---

#### Friction Audit
> Every field, click, and decision point is a potential drop-off. Minimize friction ruthlessly.

**Check for:**
- Forms with too many required fields
- Fields that ask for info not needed at this stage
- No progressive disclosure (showing everything at once)
- Required account creation before value delivery
- Multi-step forms without progress indication
- Form fields without clear labels or placeholder guidance

**Fix pattern:** Remove every field that isn't strictly necessary. Use progressive disclosure. Delay account creation until after value delivery. Show progress in multi-step flows.

---

#### Exit / Soft Conversion
> Not everyone is ready to convert. Offer a smaller commitment for those not ready for the primary CTA.

**Check for:**
- Only one conversion option (all or nothing)
- No newsletter signup, lead magnet, or "follow us" as fallback
- Missing micro-conversions for visitors not ready for the main CTA
- No email capture for retargeting

**Fix pattern:** Offer a soft conversion alongside the primary CTA. Newsletter signup, free resource, "remind me later", or social follow. Capture the interest of non-converters.

---

#### Post-Conversion Experience
> What happens after someone converts? Confirmation delight reduces buyer's remorse and increases referrals.

**Check for:**
- Bland confirmation page / message ("Danke für deine Anmeldung.")
- No next steps after conversion
- No social sharing prompt after conversion
- Missing "what happens now" clarity
- No referral hook or viral loop

**Fix pattern:** Post-conversion should: (1) confirm and celebrate, (2) set expectations ("Du hörst innerhalb von 24h von uns"), (3) suggest a next step (share, explore, invite).

---

### Category 4: Persuasion Psychology

#### Commitment Escalation (Foot-in-the-Door)
> Small yeses lead to big yeses. Start with micro-commitments before asking for the main conversion.

**Check for:**
- First ask is too big (registration, purchase, long form)
- No micro-commitments before the main conversion point
- Survey/quiz not used as engagement before conversion
- No interactive elements that create investment before the ask

**Fix pattern:** Build a ladder of small yeses: read → interact → micro-commit → convert. Quiz, survey, calculator, free preview — anything that creates engagement before the ask.

---

#### Reciprocity
> Give value before asking. People feel compelled to return favors.

**Check for:**
- Asking for email/data without offering value first
- No free content, preview, or tool before the conversion ask
- Gated content that gates too early (before any value is delivered)
- Value proposition only described, never demonstrated

**Fix pattern:** Lead with value. Free content, useful preview, actionable tip, or interactive tool before the ask. "Here's something useful for free — and here's how we can help further."

---

#### Anchoring
> The first number or reference point shapes all subsequent judgments. Use this for pricing and value perception.

**Check for:**
- Price presented without context or comparison
- No "value of" framing before price reveal
- Missing price anchoring (comparable alternatives, cost of the problem)
- No "per day" or "per week" reframing of monthly/annual prices

**Fix pattern:** Before showing price, establish what the alternative costs (therapy, counseling, relationship damage). Frame price as investment, not cost. "Weniger als ein Kaffee pro Tag."

---

#### Loss Aversion Framing
> People are more motivated by what they might lose than what they might gain.

**Check for:**
- All messaging focused on gains, none on what they'd miss
- No "without this..." or "imagine if..." counter-framing
- Missing urgency (authentic, not manufactured)
- No FOMO elements for genuinely limited offers

**Fix pattern:** Balance gain framing with loss framing. "Was wäre, wenn ihr das schon vor einem Jahr gehabt hättet?" But NEVER use manipulative dark patterns or fake scarcity.

---

#### Paradox of Choice
> More options = more decision paralysis. Fewer, clearer options convert better.

**Check for:**
- More than 3 pricing tiers
- Feature comparison tables with too many rows
- Multiple CTAs competing for attention on the same screen
- No recommended / highlighted option among choices
- Decision points without a clear default or recommendation

**Fix pattern:** Limit to 2-3 options. Highlight the recommended one visually. Use "Most popular" or "Empfohlen" badges. Make the best choice obvious.

---

## Step 2: Report findings

Present findings grouped by severity:

```
## CRO Audit Results

### 🔴 Critical — likely killing conversions
| Issue | CRO Principle | File | Recommended Fix |
|-------|--------------|------|-----------------|
| ... | ... | ... | ... |

### 🟠 Major — measurably reducing conversion rate
| Issue | CRO Principle | File | Recommended Fix |
|-------|--------------|------|-----------------|
| ... | ... | ... | ... |

### 🟡 Minor — optimization opportunity
| Issue | CRO Principle | File | Recommended Fix |
|-------|--------------|------|-----------------|
| ... | ... | ... | ... |

### ✅ Well done
- [list what the project already does well for conversions]
```

Ask the user: **"Soll ich die Issues fixen? Alle oder nur die kritischen?"**

---

## Step 3: Fix issues

Apply fixes directly in the codebase. For each fix:
- Reference which CRO principle it addresses in a brief code comment (only if non-obvious)
- Prioritize fixes on the primary conversion funnel
- Never break existing functionality
- Follow the project's existing code style and design system
- Respect brand voice and tone — no dark patterns, no hype, no cringe

---

## Step 4: Summary

```
CRO Audit Complete!

✅ [N] issues fixed
⚠️ [N] issues flagged for manual review

Principles applied:
- [list which CRO principles were most relevant]

Top 3 highest-impact changes:
1. [change] — [which principle, expected impact]
2. [change] — [which principle, expected impact]
3. [change] — [which principle, expected impact]

Recommended next steps:
- A/B test headline variations (current vs. benefit-focused)
- Heatmap analysis on CTA placement (PostHog/Hotjar)
- User testing: 5-second test on hero section with strangers
- Track micro-conversion funnel (scroll depth → CTA clicks → form starts → form completions)
```

---

## Rules

- **Audit the conversion path**, not just aesthetics or usability
- Focus on the **primary conversion goal** first
- Reference specific CRO principles by name — this creates shared vocabulary with marketing
- Respect the project's brand voice — CRO improvements should feel native, not bolted on
- **Never add dark patterns** — no fake urgency, no manipulative scarcity, no confirm-shaming, no hidden costs
- Copy recommendations should match the project's tone and language
- German UI text for German-language projects
- Fixes should be practical and implementable, not theoretical
- Follow the project's existing code style and component patterns
- Every recommendation should have a clear "why" tied to conversion psychology

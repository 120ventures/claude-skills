---
name: lean-prd
description: Use this skill when the user needs to turn customer discovery insights into a lean, shippable PRD. Activate when the user mentions PRD, product requirements, spec, scoping, what to build next, turning interviews into features, or bridging discovery to development.
---

# Lean PRD

You are a product-minded engineer writing build briefs that Claude Code will implement — often in a single session. Your job is to compress customer evidence into the smallest buildable scope that tests the riskiest assumption.

## Core Philosophy

### Evidence Over Intuition
Every requirement must trace back to a discovery insight — a quote, a pattern, a workaround, or a behavioral signal. If it can't be linked to evidence, it's a guess. Label it as such and deprioritize it.

### One Bet Per PRD
A PRD is a bet. Each one should test exactly one core hypothesis. If you're testing two things, you need two PRDs. Mixing bets makes it impossible to know what worked.

### Claude Is the Builder
The PRD is a build brief for Claude Code. This means:
- Scope is not limited by team velocity — Claude can ship a functional app in an hour
- "Later" doesn't mean "next sprint" — it means "next session, after we validate this bet"
- Technical approach matters more than in a traditional PRD because it's direct input to the builder
- The constraint isn't dev time, it's **clarity of what to build and why**

### Scope by Learning, Not by Effort
Don't scope based on "how long will this take to build." Scope based on "what's the least we can ship to learn whether this bet is right." Claude can build a lot — the danger is building too much before validating, not too little.

### Appetite, Not Estimate (Shape Up)
Don't ask "how long will this take to build?" — with Claude, almost anything is fast. Instead, set an **appetite**: how much scope complexity are we willing to take on before validating this bet? An appetite is a ceiling on scope, not a prediction of effort. If the shaped solution exceeds the appetite, narrow the solution — don't expand the appetite. This keeps you from over-building before you have signal.

## PRD Structure

When the user asks for a PRD, produce this structure:

### 1. Bet (1-2 sentences)
What hypothesis does this test?
- Format: *"We believe [target user] will [expected behavior] because [evidence from discovery]."*

### 2. Evidence
What customer discovery data supports this bet?
- Key quotes (verbatim, with source/interview reference)
- Patterns observed (e.g., "4/6 eng managers described this exact workflow")
- Workarounds spotted (strongest signal — they already spend time/money on this)
- Counter-evidence (what argues against this bet — include it honestly)

### 3. Success Criteria
How do we know this worked?
- One primary metric (the thing you'd bet money on moving)
- One or two guardrail metrics (things that shouldn't break)
- Qualitative signal (what would users say/do if this works?)
- How to measure: what instrumentation or feedback loop is needed?

### 4. Scope: In / Out / Later
- **In** — The minimum to test the hypothesis. Each item maps to evidence.
- **Out** — Explicitly excluded from this version. Say why.
- **Later** — Matters, but only after validation. Next session's work, not this one's.

### 5. User Flow
The happy path as a numbered sequence.
- No edge cases. No error states. Just the core flow.
- If it's more than 8 steps, the scope is too big.

### 5.5. Breadboard (optional)
A Shape Up-style breadboard: sketch the flow as **places** (screens/states), **affordances** (things the user can do), and **connections** (what leads where). No visual design — just the logical skeleton. Example:

```
[Landing Page] → (Click "Start Assessment") → [Question Flow] → (Submit) → [Results Page] → (Share link)
```

This gives Claude the interaction architecture without over-prescribing the UI.

### 6. Build Spec
Direct input for Claude Code to start building. Include:
- **Stack**: Specific technologies and why (reference mvp-builder skill defaults)
- **Data model**: Key entities and relationships, sketched out
- **API shape**: Core endpoints or server actions needed
- **Key UI components**: What screens/views, what the user interacts with
- **Third-party dependencies**: APIs, services, packages
- **Deploy target**: Where this goes live

Keep it concise but unambiguous. Claude should be able to start building from this section alone without asking clarifying questions.

### 7. Open Questions
What could change the plan?
- Mark each as **blocking** (must resolve before building) or **non-blocking** (resolve during or after)

## Process: From Discovery to PRD

### Step 1: Extract the Signal
When the user shares interview notes, transcripts, or synthesis docs:
- Pull out the top 3-5 pain points ranked by frequency + intensity
- Identify the strongest workaround signals
- Flag where multiple segments diverge (different problems need different PRDs)

### Step 2: Pick the Bet
Help the user choose which pain point to address first:
- **Evidence strength** — How many people described this? How visceral was it?
- **Learning value** — Even if the bet is wrong, do we learn something important?
- **Testability** — Can we put this in front of real users and get signal fast?

### Step 3: Ruthlessly Scope
Apply these scoping heuristics:
- **The "one screen" test** — What's the single most important interaction?
- **Cut every "nice to have" on first pass** — Add back only what's needed for the hypothesis test
- **No auth, no admin, no settings** unless they're the thing being tested
- **Manual over automated for non-core paths** — If Jonny can do it behind the scenes for the first 50 users, don't build it
- **Default over configurable** — Pick the right answer instead of giving the user a choice
- **Remember Claude builds fast** — The bottleneck is validation, not implementation. Don't overbuild before you have signal.
- **Shape to the right altitude** — The PRD should be concrete enough that Claude doesn't have to make product decisions, but abstract enough that it doesn't prescribe implementation details that don't matter. Define the flow and key interactions, not pixel positions.
- **Name the rabbit holes** — Before building, explicitly list where complexity could spiral (e.g., "real-time sync," "permissions model," "edge cases in parsing"). Then either cut them from scope, simplify them with a constraint, or solve them in the PRD — never leave them for Claude to discover mid-build.
- **No backlog** — Don't accumulate a queue of shaped PRDs. Pick the best bet now, ship it, validate it, then shape the next one. Stale PRDs are just opinions that aged badly.

### Step 4: Write the PRD
Use the template above. Target 400-600 words. If it's longer, the scope isn't tight enough.

### Step 5: Pressure Test
Before calling it done:
- Can Claude start building from the Build Spec right now? (If no, add clarity)
- Can you explain the bet in one sentence? (If no, simplify)
- Is there anything in "In" that doesn't directly test the hypothesis? (If yes, move to "Later")
- Does the success criteria have a number? (If no, add one)
- Are you building too much because Claude can, not because you should? (If yes, cut)

## Anti-Patterns

- **The kitchen sink PRD** — "Claude can build it all in an hour so let's include everything." No. Validate first.
- **Evidence laundering** — Cherry-picking one quote to justify a feature you already wanted. Include counter-evidence.
- **Premature polish** — Building a beautiful v1 when an ugly functional version teaches you the same thing. Polish after validation.
- **Vanity metrics as success criteria** — "Users sign up" is not success. "Users complete [core action] within 24h of signup" is.
- **Solution masquerading as a problem** — "We need a dashboard" is a solution. "Eng managers can't see candidate pipeline status" is a problem. Start with the problem.
- **Over-scoping because it's easy** — The fact that Claude *can* build auth, notifications, analytics, and an admin panel in one session doesn't mean you *should*. Every feature you ship before validating the core bet is noise.
- **Unshaped work** — Handing Claude a vague problem ("build something for interview scheduling") without shaping a specific solution. Shape Up's core insight: abstract projects always take longer and go sideways, even when the builder is fast. Shape the work before you build it.

## Recommended Tool Stack

- **PRD writing**: Claude Code (this skill), or a markdown file in the repo
- **Evidence linking**: Tag interview notes in Notion with hypothesis IDs so PRDs can reference them
- **Prioritization**: Simple spreadsheet — evidence strength + learning value + testability
- **Handoff to build**: The PRD's Build Spec feeds directly into the `mvp-builder` skill — start building immediately after the PRD is approved

## Sub-Agent Strategy

For complex discovery-to-PRD pipelines:
- **Evidence extraction agent**: Process raw transcripts/notes into structured insights
- **Scoping agent**: Take a pain point + constraints, propose minimum scope
- **PRD drafting agent**: Combine evidence + scope into formatted PRD
- **Pressure test agent**: Review the PRD against the checklist, flag issues

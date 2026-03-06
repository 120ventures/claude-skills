#!/usr/bin/env python3
"""Generate Meta Ad copy (hooks, primary texts, headlines) via Gemini API.

Usage:
  python3 generate_copy.py \
    --brand "attuned." \
    --product "AI-powered Relationship Companion für Langzeitpaare" \
    --tone "sachlich, souverän, elegant — calm, premium, human" \
    --audience "Paare 25-45, Langzeitbeziehung, wollen Beziehung im Alltag stärken" \
    --cta "Jetzt starten" \
    --language "Deutsch (Österreichisch)" \
    --angles 5 \
    --output copy_output.md

Requires: GEMINI_API_KEY in environment or in
  ~/nano-banana-claude-plugin/scripts/.env
"""

import argparse, os, sys, json

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/nano-banana-claude-plugin/scripts/.env"))
except ImportError:
    pass

import google.generativeai as genai

def build_prompt(args):
    return f"""Du bist ein Elite-Performance-Marketing-Copywriter mit 15+ Jahren Erfahrung in D2C und App-Marketing im DACH-Raum. Du schreibst Copy die konvertiert — nicht Copy die "nett klingt".

## Dein Auftrag

Erstelle ein vollständiges Meta Ad Copy Set für:

- **Brand:** {args.brand}
- **Produkt:** {args.product}
- **Tone of Voice:** {args.tone}
- **Zielgruppe:** {args.audience}
- **CTA:** {args.cta}
- **Sprache:** {args.language}

## Was du liefern musst

### 1. Hook-Angles ({args.angles} Stück)

Jeder Hook aus einer anderen psychologischen Perspektive:
1. **Pain Point** — Schmerz den die Zielgruppe täglich spürt
2. **Desire / Aspiration** — Wunschzustand emotional ausmalen
3. **Curiosity Gap** — Wissenslücke öffnen die zum Klicken zwingt
4. **Social Proof / Statistik** — Beweis oder Zahl vorweg
5. **Pattern Interrupt / Contrarian** — Erwartung brechen, provozieren

Für jeden Hook: 2 Formulierungen (eine als Frage, eine als Statement).

### 2. Primary Texts (für jeden Hook-Angle)

4 Varianten pro Hook:
- **Short (2-3 Sätze):** Hook + CTA. Knallhart.
- **Medium (4-6 Sätze):** Hook → Pain/Desire → Solution → CTA
- **Long Story (8-12 Sätze):** Emotionaler Story-Bogen. "Kennst du das..." Einstieg.
- **Long Proof (8-12 Sätze):** Benefit-Stack + Social Proof + Authority

### 3. Headlines (5 pro Hook)

Max 255 Zeichen. Typen: Benefit, Curiosity, Social Proof, Urgency, Question.

### 4. Description (1 pro Hook)

1-2 Sätze, ergänzend, nicht redundant.

## Copy-Regeln (STRIKT befolgen)

- **Erster Satz = Hook.** Er entscheidet über "Mehr anzeigen". Mach ihn unwiderstehlich.
- **Spezifisch schlägt generisch.** "Besser kommunizieren" ist schwach. "In 5 Minuten verstehen, was euch wirklich beschäftigt" ist stark.
- **Kurze Sätze. Absätze. Weißraum.** Keine Textwände.
- **Emotional vor rational.** Gefühl zuerst, Logik danach.
- **Kein Corporate-Speak.** Keine Buzzwords. Keine Floskeln. Sprich wie ein Mensch.
- **Kein Clickbait.** Headline muss liefern was sie verspricht.
- **Keine Dark Patterns.** Kein Fake-Scarcity, kein Confirm-Shaming.
- **Jede Copy muss einzigartig sein** — keine Wiederholungen über Varianten.
- **Power Words sparsam:** kostenlos, jetzt, neu, endlich, ohne, sofort — aber nur wenn sie passen.

## Qualitäts-Check vor Abgabe

Lies jeden Text nochmal und frag dich:
- Würde ICH beim Scrollen stoppen?
- Ist der Hook in 3 Sekunden greifbar?
- Klingt das nach echtem Mensch oder nach AI-Slop?
- Ist es spezifisch genug für GENAU dieses Produkt?

Wenn nicht → umschreiben.

## Output-Format

Gib alles als strukturiertes Markdown aus. Pro Hook-Angle:

```
## Hook [N]: [Angle-Name]

**Statement:** ...
**Frage:** ...

### Primary Texts
| # | Typ | Text |
|---|-----|------|

### Headlines
| # | Typ | Text | Zeichen |
|---|-----|------|---------|

### Description
...
```
"""

def main():
    p = argparse.ArgumentParser(description="Generate Meta Ad copy via Gemini")
    p.add_argument("--brand", required=True)
    p.add_argument("--product", required=True)
    p.add_argument("--tone", required=True)
    p.add_argument("--audience", required=True)
    p.add_argument("--cta", default="Jetzt starten")
    p.add_argument("--language", default="Deutsch (Österreichisch)")
    p.add_argument("--angles", type=int, default=5)
    p.add_argument("--output", default="copy_output.md")
    p.add_argument("--model", default="gemini-2.5-flash")
    args = p.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found. Set it in env or ~/.env", file=sys.stderr)
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(args.model)

    prompt = build_prompt(args)
    print(f"Generating copy with {args.model}...")
    print(f"Brand: {args.brand} | Angles: {args.angles}")

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.9,
            max_output_tokens=8000,
        )
    )

    output = response.text

    with open(args.output, "w") as f:
        f.write(f"# Meta Ad Copy — {args.brand}\n\n")
        f.write(f"_Generated via {args.model}_\n\n")
        f.write(output)

    print(f"\n✅ Copy saved to {args.output}")
    print(f"   {len(output)} characters, ~{len(output.split())} words")

if __name__ == "__main__":
    main()

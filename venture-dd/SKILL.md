---
name: venture-dd
description: >
  Use when the user asks for venture due diligence, market validation, or startup idea evaluation.
  Triggered by /venture-dd or phrases like "mach eine Due Diligence", "validiere diese Idee",
  "bewerte dieses Venture", "ist diese Idee gut?", "market validation".
---

# Venture Due Diligence

Strukturierte Due Diligence für Venture-Ideen. Testet 5 kritische Hypothesen mit Web-Research, analysiert Wettbewerb und berechnet Marktgröße. Output auf Deutsch.

## CRITICAL RULES

1. **No speculative early-stage KPIs.** NEVER calculate or present CAC, LTV, LTV:CAC ratio, payback period, or break-even for ventures at idea/pre-revenue stage. These are pure fiction without years of real data. Skip the Unit Economics section entirely unless the venture has actual customer data.
2. **No scoping assumptions without explicit user approval.** NEVER lock into a target segment (e.g., "Mid-Market only"), geography (e.g., "DACH only"), firm size, or beachhead vertical unless the user explicitly stated it. If a scope decision is needed, ASK first. If the user gives a broad idea, keep the analysis broad.
3. **Match research to actual business context.** When researching a vertical, ensure the analysis matches the use case. If the platform serves B2B advisory firms, research B2B cases — don't default to B2C data just because it's more available.

## Checklist

Complete these steps in order:

- [ ] Phase 1: Venture-Input sammeln
- [ ] Phase 2: 5 Hypothesen identifizieren und priorisieren
- [ ] Phase 3: Hypothesen via Web-Research testen
- [ ] Phase 4a: Competitor Deep Dive
- [ ] Phase 4b: TAM/SAM/SOM berechnen
- [ ] Phase 4c: Unit Economics prüfen (ONLY if venture has real customer data — skip for idea-stage)
- [ ] Phase 5: Report generieren nach Template

## Phase 1: Input sammeln

Erfrage folgende Informationen vom User. Eine Frage pro Nachricht, nie alle auf einmal:

1. **Value Proposition** — Was genau löst das Venture?
2. **Zielgruppe** — Für wen genau?
3. **Geschäftsmodell** — Wie wird Geld verdient?
4. **Markt/Region** — Wo? (Land, Region, global?)

Falls der User bereits eine ausführliche Beschreibung gegeben hat, keine Rückfragen stellen — direkt zu Phase 2.

## Phase 2: Hypothesen identifizieren

Wähle 5 kritische Hypothesen aus `references/hypothesis-patterns.md`. Passe die Hypothesen-Texte an das spezifische Venture an.

**Priorisierung (immer in dieser Reihenfolge):**
1. Criticality — Würde ein Scheitern das Venture killen?
2. Uncertainty — Wie viel wissen wir NICHT?
3. Cost to Test — Günstige Desk-Research zuerst

Präsentiere die 5 Hypothesen dem User bevor du mit dem Research beginnst.

## Phase 3: Web-Research & Hypothesen testen

Teste jede Hypothese einzeln via WebSearch. Verwende mehrere Suchbegriffe pro Hypothese.

**Suchstrategie:**
- DACH-Märkte: Deutsche Suchbegriffe + englische Fachbegriffe
- Internationale Märkte: Englische Suchbegriffe
- Immer auch nach gescheiterten Vorgängern suchen
- Statista, Crunchbase, LinkedIn für Marktdaten

**Format pro Hypothese:**

| Feld | Inhalt |
|---|---|
| **Hypothese** | Vollständiger Text |
| **Testmethode** | Wie getestet |
| **Ergebnis** | Was gefunden |
| **Quelle** | URL oder Quellenangabe |
| **Status** | ✅ Bestätigt / ❌ Widerlegt / ⚠️ Unklar |
| **Konfidenz** | Hoch / Mittel / Niedrig |

Jede Behauptung braucht eine Quelle. Keine Quelle = als "Schätzung" markieren.

## Phase 4a: Competitor Deep Dive

Recherchiere die Top 5 Wettbewerber (direkt + indirekt):

- Name, Typ (direkt/indirekt), Stärken, Schwächen, Funding/Größe
- Differenzierung: Wie hebt sich das Venture konkret ab?
- **Gescheiterte Vorgänger**: Welche ähnlichen Ventures sind gescheitert? Warum? Das ist oft die wichtigste Information.

Suche auf Crunchbase, LinkedIn, App Stores, G2/Capterra, und in Branchenmedien.

## Phase 4b: TAM/SAM/SOM berechnen

Immer zwei Berechnungen:

**Top-Down:** Gesamtmarkt × relevanter Anteil × Preispunkt
- Quellen: Statistik Austria, Destatis, Eurostat, Statista, Branchenverbände

**Bottom-Up:** Anzahl potentieller Kunden × erwarteter ARPU × Penetration
- Realistische Annahmen, keine Fantasiezahlen

Vergleiche beide Ergebnisse. Große Abweichungen = Annahmen prüfen.

## Phase 4c: Unit Economics prüfen

**⚠️ ONLY if the venture has real customer/revenue data.** For idea-stage ventures, SKIP this section entirely. Speculative CAC/LTV/payback calculations for pre-revenue ventures are fiction and will not be included.

If real data exists, assess:

| Metrik | Was |
|---|---|
| ARPU | Average Revenue per User (monatlich) — from real data |
| Gross Margin | Bruttomarge (%) — from real data or strong comparable |
| Revenue Model Viability | Does the pricing model make directional sense given comparable tools? |

Do NOT calculate: CAC, LTV, LTV:CAC ratio, payback period, or break-even unless based on actual customer acquisition data. Benchmarks from comparables are fine for context, but do not fabricate ESODA-specific numbers.

## Phase 5: Report generieren

Verwende das Template aus `references/report-template.md` für den finalen Report.

**Risk Score vergeben:**
- 🟢 **Green (Fundable)** — Starke Signale, keine fundamentalen Blocker
- 🟡 **Yellow (Needs Work)** — Potenzial vorhanden, aber offene Risiken die adressiert werden müssen
- 🔴 **Red (Major Blocker)** — Fundamentale Probleme identifiziert, Pivot oder Abbruch empfohlen

**Abschluss:** Top 3 Empfehlungen (konkret, actionable) + nächste Schritte als Checkliste.

## Additional Resources

### Reference Files
- **`references/hypothesis-patterns.md`** — Vorgefertigte Hypothesen nach Kategorie (Desirability, Market, Competition, Business Model, Legal) mit Sub-Patterns für B2B, B2C, Marketplace, SaaS, regulierte Märkte
- **`references/report-template.md`** — Vollständiges Markdown-Template für den DD-Report

### Example Files
- **`examples/example-report.md`** — Vollständiger Beispiel-Report (Haushalt-Soforthilfe) mit echten Daten

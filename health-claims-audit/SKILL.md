---
name: health-claims-audit
description: Audit health and medical product claims — MPG 2021, EU-MDR, LMSVG, Health Claims VO, Austrian advertising law for health-related products
---

# Health Claims Audit — Medical & Health Product Advertising Compliance

This skill audits all health-related claims, medical product advertising, and wellness/health copy on a website for compliance with Austrian and EU regulations. It checks for prohibited claims, missing disclaimers, misleading language, and ensures the correct legal framing for the product category.

No arguments needed. Just run `/health-claims-audit` and the skill scans the project automatically.

**Difference from other audits:**
- `/legal-audit` checks **general website compliance** — DSGVO, Impressum, cookies, e-commerce
- `/at-copy-audit` checks **copy quality and Austrian localization** — clarity, tone, word choice
- `/health-claims-audit` checks **health-specific advertising law** — what you can and cannot claim about health products

**Important:** This skill flags legal risks in health advertising copy. It is NOT legal advice. All findings should be reviewed by a regulatory affairs specialist or health advertising lawyer before publication.

Reference sources:
- Medizinproduktegesetz 2021 (MPG 2021): BGBl. I Nr. 122/2021
- EU Medical Device Regulation (EU-MDR): VO (EU) 2017/745, Art. 7
- Health Claims Verordnung: VO (EG) Nr. 1924/2006
- Lebensmittelsicherheits- und Verbraucherschutzgesetz (LMSVG)
- Bundesgesetz gegen den unlauteren Wettbewerb (UWG)
- Arzneimittelgesetz (AMG) — Abgrenzung Medizinprodukt vs. Arzneimittel
- Heilmittelwerberecht (HWG-Äquivalent in AT: MPG 2021 §§ 70-78)
- EFSA Register zugelassener Health Claims

---

## Step 0: Understand the project

Before auditing, read:
- `CLAUDE.md` / `README.md` for project context
- All product descriptions and claims
- All landing page copy, hero sections, feature descriptions
- Testimonials and user stories
- FAQ content (often contains implicit health claims)
- Legal pages (AGB, Datenschutz — may contain product classification info)
- Image and video content descriptions (before/after, body imagery)
- Meta descriptions and ad copy (if present)

Identify:
- **Product category** — Is this a Medizinprodukt, Nahrungsergänzungsmittel, Kosmetikum, Wellness-Produkt, App/Software as Medical Device (SaMD), or Lifestyle-Produkt?
- **Regulatory classification** — Medizinprodukt Klasse I/IIa/IIb/III? CE-Kennzeichnung?
- **Target audience** — Laien (Verbraucher) or Fachpublikum (Ärzt:innen, Kliniken)?
- **Zweckbestimmung** — What is the approved/intended purpose per IFU/Gebrauchsanweisung?
- **Claim basis** — What evidence exists for claims made? (Studien, CE-Daten, EFSA-Liste)

---

## Step 1: Determine product classification

Before checking claims, classify the product. The rules differ dramatically by category.

### Decision tree:

```
Is it a Medizinprodukt (CE-gekennzeichnet, Zweckbestimmung)?
├── Yes → Category A: Medizinprodukt (MPG 2021 + EU-MDR)
│   ├── Verschreibungspflichtig? → Verbraucherwerbung VERBOTEN
│   ├── Nur durch Health Professionals anwendbar? → Verbraucherwerbung VERBOTEN
│   └── Frei verkäuflich, Selbstanwendung? → Verbraucherwerbung ERLAUBT (mit Einschränkungen)
│
├── Nein → Ist es ein Nahrungsergänzungsmittel?
│   ├── Yes → Category B: NEM (Health Claims VO + LMSVG)
│   └── Nein → Ist es ein Kosmetikum?
│       ├── Yes → Category C: Kosmetik (EU KosmetikVO 1223/2009)
│       └── Nein → Ist es eine App / Software?
│           ├── Medical purpose (Diagnose, Therapie, Überwachung)? → Category A: SaMD
│           └── Wellness / Lifestyle? → Category D: Wellness/Lifestyle
```

**Flag for manual review** if the classification is unclear. Misclassification is the #1 regulatory risk.

---

## Step 2: Audit across 8 categories

Go through **each category** below. For every issue found, note the file, the specific legal requirement, and the recommended fix. Rate severity as:
- **🔴 Critical** — illegal claim, Abmahnung/fine risk, product seizure risk
- **🟠 Major** — legally risky, likely non-compliant, fix before publication
- **🟡 Minor** — borderline, could be challenged, tighten language

---

### Category 1: Verbotene Heilversprechen

#### Absolute Verbote — Nie verwenden
> These claims are illegal in consumer advertising for all health product categories.

**Scan all copy for:**
- "heilt" / "Heilung" / "geheilt" — Heilversprechen verboten
- "beseitigt" / "eliminiert" (Krankheit/Symptom) — Heilversprechen
- "garantiert" + Gesundheitsaussage — unzulässige Garantie
- "ersetzt den Arzt" / "kein Arzt nötig" / "statt Therapie" — §73 MPG
- "Wundermittel" / "Durchbruch" / "Revolution" — Übertreibung
- "100% wirksam" / "wirkt bei allen" — unzulässige Absolutaussage
- "nebenwirkungsfrei" / "völlig sicher" / "ohne Risiko" (gesundheitsbezogen) — irreführend
- "klinisch bewiesen" ohne Quellenangabe — irreführend
- "Ärzte empfehlen" ohne nachweisbare Basis — irreführend
- "sofortige Wirkung" / "Sofortergebnis" bei Gesundheitsclaims — übertrieben

**Fix pattern:** Ersetze absolute Claims durch evidenzbasierte, eingeschränkte Formulierungen:
- "heilt" → "kann unterstützen bei..." / "trägt dazu bei..."
- "beseitigt Schmerzen" → "kann zur Linderung von Schmerzen beitragen"
- "garantiert" → "in Studien zeigte sich..." / "viele Anwender berichten..."
- "ersetzt den Arzt" → "ergänzend zur ärztlichen Betreuung"
- "klinisch bewiesen" → "in einer klinischen Studie mit N Teilnehmern zeigte sich..." + Quelle

---

#### "Besser als"-Vergleiche
> Vergleichende Werbung mit ärztlicher Behandlung oder anderen Produkten ist hochriskant.

**Check for:**
- "besser als [Medikament/Behandlung]" — verboten ohne solide Evidenz
- "wirksamer als" / "überlegen" — Vergleich ohne Head-to-Head-Studie
- "ersetzt [Medikament]" — suggeriert Überlegenheit über ärztliche Behandlung
- "die natürliche Alternative zu [Medikament]" — impliziter Wirksamkeitsvergleich
- "ohne die Nebenwirkungen von [Medikament]" — irreführender Vergleich

**Fix pattern:** Vergleiche nur mit eigener Evidenz und nie gegen ärztliche Behandlung. Statt Vergleich: eigene Vorteile positiv formulieren ohne Bezug auf andere Produkte/Therapien.

---

### Category 2: Pflichtangaben (Verbraucherwerbung Medizinprodukte)

#### Pflichtangaben bei Detailwerbung — §74 MPG 2021
> Jede Verbraucherwerbung, die über reine Erinnerungswerbung (nur Name/Logo) hinausgeht, muss enthalten:

**Check for presence of:**
- Bezeichnung des Medizinprodukts (Handelsname)
- Kurzbeschreibung der Zweckbestimmung
- Wesentliche Hinweise für sinnvolle Anwendung
- Hinweis auf mögliche unerwünschte Wirkungen (wenn zutreffend)
- Hinweis auf besondere Sicherheitsvorkehrungen (wenn zutreffend)
- Pflichthinweis: "Bitte beachten Sie die Gebrauchsanweisung. Im Zweifel fragen Sie Ihren Arzt oder Apotheker."
- Bei Audio/Video: Pflichthinweis akustisch klar wahrnehmbar

**Fix pattern:** Pflichtangaben als Footer-Disclaimer auf jeder Seite mit Produktwerbung. Bei Landingpages: unterhalb des Hero-Bereichs, nicht erst im Footer. Bei Video/Audio: gesprochener Hinweis am Ende.

---

#### Erinnerungswerbung vs. Detailwerbung
> Nur Name + Logo ohne Zweckbestimmung/Claims = Erinnerungswerbung (weniger Pflichten). Sobald du sagst, wofür das Produkt gut ist = Detailwerbung (volle Pflichten).

**Check for:**
- Seiten die Claims machen aber keine Pflichtangaben haben
- Social Media Posts mit Wirkaussagen aber ohne Disclaimer
- Banner/Ads mit Zweckbestimmung aber ohne Pflichthinweis

**Fix pattern:** Entweder auf Erinnerungswerbung reduzieren (nur Name/Logo/Marke) oder volle Pflichtangaben ergänzen.

---

### Category 3: Zielgruppen-Trennung (Laien vs. Fachpublikum)

#### Verbraucherwerbung vs. Fachwerbung
> Strenge Trennung erforderlich. Was sich an Laien richtet, unterliegt den strengsten Regeln.

**Check for:**
- Produkte, die nur verschreibungspflichtig sind → Verbraucherwerbung komplett verboten
- Produkte nur für Health Professionals → Verbraucherwerbung verboten
- Produkte laut Gebrauchsanweisung nur unter ärztlicher Aufsicht → Verbraucherwerbung verboten
- Fachliche Claims (Studiendetails, Wirkmechanismen) auf Verbraucher-Seiten
- Keine klare Trennung zwischen Fach- und Verbraucherbereich auf der Website

**Fix pattern:**
- Fachbereich: Login-geschützt oder klar als "Für Fachkreise" gekennzeichnet
- Verbraucherbereich: nur zulässige Claims, Pflichtangaben, keine Fach-Detailinfos
- Wenn Produkt verschreibungspflichtig: keinerlei Werbung im öffentlichen Bereich

---

#### Kinder als Zielgruppe
> Werbung, die primär oder ausschließlich an Kinder adressiert ist, ist bei Medizinprodukten sehr kritisch.

**Check for:**
- Werbung direkt an Kinder gerichtet (Sprache, Bilder, Tonalität)
- Kinderfiguren/Maskottchen in Medizinprodukt-Werbung
- Gamification-Elemente, die Kinder als Zielgruppe ansprechen

**Fix pattern:** Medizinprodukt-Werbung an Erziehungsberechtigte richten, nicht an Kinder selbst.

---

### Category 4: Bildmaterial & Vorher-Nachher

#### Verbotene Bilder — §73 MPG 2021
> Drastische, schockierende Körper- oder Krankheitsbilder sind in Verbraucherwerbung verboten.

**Check for:**
- Vorher-Nachher-Bilder am Körper (Chirurgie, Wunden, Hautzustände)
- Drastische Krankheitsbilder zur Angsterzeugung
- Schockbilder zur Motivationssteigerung
- Bilder von Operationen oder invasiven Eingriffen
- Extreme Close-ups von Krankheitssymptomen

**Erlaubt (mit Einschränkungen):**
- Sachliche Produktbilder
- Schematische Darstellungen (Infografiken, Zeichnungen)
- Lifestyle-Bilder mit Produkt in Anwendungssituation
- Dezente Vorher-Nachher bei Kosmetik (nicht bei Medizinprodukten!)

**Fix pattern:** Ersetze drastische Bilder durch sachliche Produktbilder, schematische Darstellungen, oder Lifestyle-Aufnahmen. Keine Angst-Trigger.

---

### Category 5: Testimonials & Social Proof (Gesundheitskontext)

#### Erfahrungsberichte — Strenge Regeln
> "Genesungsbescheinigungen" und "Heilungsberichte" sind als Werbemittel in der Verbraucherwerbung verboten.

**Check for:**
- Testimonials die Heilung beschreiben: "Mein [Krankheit] ist geheilt"
- Erfahrungsberichte die Selbstdiagnose nahelegen
- "Ärzte empfehlen" ohne nachweisbare Basis
- Testimonials mit konkreten medizinischen Diagnosen
- Genesungsverläufe als Werbemittel ("Nach 2 Wochen war mein Rücken schmerzfrei")
- Prominente/Influencer mit Gesundheits-Claims ohne Kennzeichnung

**Erlaubt:**
- Allgemeine Zufriedenheitsaussagen: "Ich bin zufrieden mit dem Produkt"
- Anwendungserfahrungen ohne Heilversprechen: "Das Produkt ist einfach anzuwenden"
- Verbesserung des Wohlbefindens (vage): "Ich fühle mich wohler"
- Immer mit Disclaimer: "Individuelle Erfahrung, Ergebnisse können variieren"

**Fix pattern:** Testimonials auf Anwendungserfahrung und Zufriedenheit beschränken. Keine konkreten Krankheiten oder Heilverläufe. Immer Disclaimer hinzufügen.

---

### Category 6: Nahrungsergänzungsmittel (NEM) & Health Claims VO

#### Zugelassene vs. nicht zugelassene Health Claims
> Für Lebensmittel (inkl. NEM) dürfen nur Health Claims verwendet werden, die in der EFSA-Liste zugelassen sind.

**Check for:**
- Gesundheitsbezogene Aussagen ohne Basis in der EU Health Claims Liste
- "Stärkt das Immunsystem" — nur erlaubt wenn Inhaltsstoff + Dosis auf EFSA-Liste
- "Gut für die Gelenke" — nur erlaubt mit zugelassenem Claim
- "Detox" / "Entgiftung" / "Entschlackung" — keine zugelassenen Claims, irreführend
- "Anti-Aging" bei NEM — kein zugelassener Health Claim
- Krankheitsbezogene Claims bei NEM — komplett verboten (Art. 12 VO 1924/2006)
- "Hilft bei [Krankheit]" — verboten für Lebensmittel/NEM
- Fehlende Pflichtangaben bei NEM-Werbung

**NEM Pflichtangaben in Werbung:**
- "Nahrungsergänzungsmittel" muss klar erkennbar sein
- Empfohlene Tagesdosis
- Hinweis: "Kein Ersatz für eine ausgewogene Ernährung"
- Hinweis: "Außerhalb der Reichweite von Kindern aufbewahren"
- Empfohlene Tagesdosis nicht überschreiten

**Fix pattern:** Jeden Health Claim gegen die EFSA-Liste prüfen (https://ec.europa.eu/food/safety/labelling-and-nutrition/claims/health-claims). Nicht zugelassene Claims entfernen oder durch zugelassene ersetzen. Pflichtangaben ergänzen.

---

### Category 7: Kosmetik-Claims

#### EU Kosmetik-Verordnung 1223/2009 + Common Criteria
> Kosmetik darf keine Wirkung versprechen, die über die Hautoberfläche hinausgeht.

**Check for:**
- Claims die über kosmetische Wirkung hinausgehen ("heilt Akne" = Arzneimittel-Claim)
- "Medizinisch wirksam" bei Kosmetik — verboten
- "Dermatologisch getestet" ohne tatsächliche Tests — irreführend
- "Hypoallergen" / "für Allergiker geeignet" ohne Belege
- "100% natürlich" wenn synthetische Inhaltsstoffe enthalten
- "Klinisch getestet" ohne Studiendetails
- Claims die biologische Prozesse beeinflussen ("repariert DNA", "regeneriert Zellen")
- Übertriebene Vorher-Nachher-Ergebnisse

**Erlaubt bei Kosmetik:**
- "Pflegt die Haut" / "spendet Feuchtigkeit" — kosmetische Wirkung
- "Verbessert das Hautbild" — Erscheinungsbild, nicht medizinisch
- "Dermatologisch getestet" — wenn tatsächlich getestet
- Vorher-Nachher bei realistischer Darstellung (keine Retusche, gleiche Lichtverhältnisse)

**Fix pattern:** Kosmetik-Claims auf Erscheinungsbild und Pflege beschränken. Keine medizinischen Wirkversprechen. Jeder "getestet"-Claim braucht eine tatsächliche Studie.

---

### Category 8: Software as Medical Device (SaMD) & Wellness-Apps

#### App/Software Abgrenzung
> Eine App die diagnostiziert, therapiert oder überwacht = Medizinprodukt (EU-MDR). Eine App für Wellness/Lifestyle = kein Medizinprodukt, aber trotzdem Werberecht beachten.

**Check for — ist die App/Software ein Medizinprodukt?:**
- Berechnet medizinische Diagnosen oder Risiko-Scores
- Gibt Therapieempfehlungen basierend auf Gesundheitsdaten
- Überwacht Vitalwerte mit medizinischem Zweck
- Steuert oder beeinflusst Medizinprodukte
- Claims: "diagnostiziert", "erkennt [Krankheit]", "überwacht Ihren Gesundheitszustand"

**Wenn Medizinprodukt → alle Regeln aus Kategorie 1-5 gelten.**

**Wenn Wellness/Lifestyle-App:**
- Keine medizinischen Claims machen ("verbessert die Gesundheit" = grenzwertig)
- Klar als Wellness/Lifestyle positionieren, nicht als medizinisches Produkt
- "Kann zum Wohlbefinden beitragen" statt "verbessert Ihre Gesundheit"
- Keine Diagnose-Funktionen bewerben
- UWG gilt trotzdem: keine irreführende Werbung

**Grauzone-Formulierungen bei Wellness-Apps:**

| ❌ Klingt nach Medizinprodukt | ✅ Bleibt im Wellness-Bereich |
|------------------------------|-------------------------------|
| "Diagnostiziert Schlafstörungen" | "Analysiert deine Schlafgewohnheiten" |
| "Therapiert Angstzustände" | "Unterstützt dich bei Entspannung" |
| "Überwacht deinen Gesundheitszustand" | "Hilft dir, deine Gewohnheiten im Blick zu behalten" |
| "Erkennt Depression" | "Reflektiert deine Stimmung über Zeit" |
| "Behandelt Rückenschmerzen" | "Begleitet dich bei Rückenübungen" |
| "Medizinisch validiert" | "Basierend auf wissenschaftlichen Erkenntnissen" |
| "Ersetzt den Therapeuten" | "Ergänzend zu professioneller Begleitung" |
| "Heilt Beziehungsprobleme" | "Unterstützt euch im Alltag" |
| "Psychologische Behandlung" | "Impulse für eure Beziehung" |

**Fix pattern:** Klare Positionierung: Wellness ≠ Medizin. Jeder Claim prüfen: würde eine Behörde das als medizinische Zweckbestimmung lesen? Wenn ja, umformulieren.

---

## Step 2: Report findings

Present findings grouped by severity:

```
## Health Claims Audit Results

### Produktklassifizierung
| Frage | Antwort |
|-------|---------|
| Produktkategorie | [Medizinprodukt / NEM / Kosmetik / Wellness / SaMD] |
| Zielgruppe | [Laien / Fachpublikum / Beides] |
| Verbraucherwerbung erlaubt? | [Ja / Nein / Eingeschränkt] |
| Regulatorischer Rahmen | [MPG 2021 / Health Claims VO / KosmetikVO / UWG] |

### 🔴 Critical — illegaler Claim, Abmahnung/Bußgeld-Risiko
| Issue | Gesetzliche Basis | File:Line | Aktueller Text | Empfohlener Fix |
|-------|------------------|-----------|----------------|-----------------|
| ... | ... | ... | ... | ... |

### 🟠 Major — rechtlich riskant, vor Veröffentlichung fixen
| Issue | Gesetzliche Basis | File:Line | Aktueller Text | Empfohlener Fix |
|-------|------------------|-----------|----------------|-----------------|
| ... | ... | ... | ... | ... |

### 🟡 Minor — grenzwertig, Formulierung schärfen
| Issue | Gesetzliche Basis | File:Line | Aktueller Text | Empfohlener Fix |
|-------|------------------|-----------|----------------|-----------------|
| ... | ... | ... | ... | ... |

### 📋 Manuelle Prüfung erforderlich
- [ ] Produktklassifizierung durch Regulatory Affairs bestätigen
- [ ] Health Claims gegen EFSA-Liste abgleichen (wenn NEM)
- [ ] Zweckbestimmung / IFU prüfen (wenn Medizinprodukt)
- [ ] Testimonials auf Genesungsbescheinigungen prüfen
- [ ] Bildmaterial auf Vorher-Nachher-Compliance prüfen
- [ ] [weitere Punkte]

### ✅ Compliant
- [list what's already legally sound]
```

Ask the user: **"Soll ich die Copy-Issues fixen? (Produktklassifizierung und Evidenz-Claims müssen manuell/regulatorisch geprüft werden.)"**

---

## Step 3: Fix issues

Apply fixes directly in the codebase. For each fix:
- Show before → after für jeden geänderten Text
- Reference die spezifische gesetzliche Grundlage (§/Art.)
- Nur technische Textänderungen — keine regulatorische Einschätzung
- Pflichthinweise ergänzen wo nötig
- Immer die sicherere Formulierung wählen (im Zweifel abschwächen)

**What this skill CAN fix:**
- Verbotene Wörter ersetzen ("heilt" → "kann unterstützen bei")
- Pflichthinweise ergänzen (Gebrauchsanweisung-Hinweis, Arzt-Hinweis)
- Übertriebene Claims abschwächen
- Testimonials entschärfen
- Disclaimer-Texte hinzufügen
- Grauzone-Formulierungen in sichere Formulierungen umschreiben

**What this skill CANNOT fix (flag for regulatory/legal review):**
- Produktklassifizierung (Medizinprodukt ja/nein?)
- Evidenz-Bewertung (ist der Claim durch Studien gedeckt?)
- CE-Kennzeichnung und Konformitätsbewertung
- Abgrenzung Medizinprodukt vs. Arzneimittel
- Fachwerbung-Compliance im Detail

---

## Step 4: Summary

```
Health Claims Audit Complete!

Produktkategorie: [Kategorie]
Regulatorischer Rahmen: [Gesetze]

✅ [N] Claims gefixt
📋 [N] Claims zur regulatorischen Prüfung markiert
⚠️ [N] Pflichthinweise ergänzt

Höchste Risiken:
1. [Claim] — [Gesetz, Risiko]
2. [Claim] — [Gesetz, Risiko]
3. [Claim] — [Gesetz, Risiko]

Empfohlene nächste Schritte:
- Regulatory Affairs / Rechtsabteilung: alle 🔴 Claims prüfen lassen
- Produktklassifizierung formell bestätigen lassen
- Health Claims gegen EFSA-Liste / IFU abgleichen
- Bildmaterial-Review (Vorher-Nachher, Krankheitsbilder)
- Testimonials durch Legal Review
- Jährliche Compliance-Prüfung einplanen
```

---

## Rules

- **Audit health-related advertising claims**, not general copy quality or UX
- **Im Zweifel: restriktiver formulieren** — eine abgeschwächte Aussage ist besser als eine Abmahnung
- Reference specific legal articles (§ MPG, Art. EU-MDR, VO 1924/2006) for every finding
- **Produktklassifizierung ist der wichtigste erste Schritt** — alles andere hängt davon ab
- Clearly separate what you CAN fix (wording) from what needs REGULATORY review (classification, evidence)
- Never draft claims that go beyond the product's Zweckbestimmung / IFU
- **Keine Heilversprechen** — auch nicht subtil oder implizit
- Deutsche Rechtstexte: formales Register, klar und eindeutig
- Follow the project's existing code style and component patterns
- This is NOT legal advice — always recommend professional regulatory review
- **Vorsichtsprinzip:** wenn unklar ob Claim erlaubt → als 🟠 Major flaggen

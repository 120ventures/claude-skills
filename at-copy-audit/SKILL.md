---
name: at-copy-audit
description: Audit UX copy quality — clarity, tone, persuasion structure, microcopy, and Austrian German localization
---

# Copy Audit — UX Copywriting + Austrian German Localization

This skill audits all user-facing copy for clarity, persuasion structure, tone, microcopy quality, and Austrian German authenticity. It identifies weak, unclear, or culturally mismatched copy and fixes it directly in the codebase.

No arguments needed. Just run `/at-copy-audit` and the skill scans the project automatically.

**Difference from other audits:**
- `/ux-audit` checks **behavioral outcomes** — decision-making, cognition, system feedback
- `/ui-audit` checks **visual implementation** — spacing, typography, color, consistency
- `/cro-audit` checks **conversion structure** — trust placement, funnel narrative, persuasion psychology
- `/at-copy-audit` checks **the words themselves** — clarity, tone, benefits framing, microcopy, Austrian localization

Reference sources:
- Joanna Wiebe / Copyhackers: conversion copywriting
- Josh Bernoff: Writing Without Bullshit
- PAS/AIDA frameworks
- Austrian German usage (ÖWB — Österreichisches Wörterbuch)

---

## Step 0: Understand the project

Before auditing, read:
- `CLAUDE.md` / `README.md` for project context, tone, and brand guidelines
- All user-facing copy (headlines, body, CTAs, form labels, error messages, tooltips)
- Target audience definition
- Existing tone-of-voice guidelines

Identify:
- **Brand voice** — formal vs. casual, premium vs. playful, warm vs. clinical
- **Target audience** — who are we talking to? what language do they use?
- **Primary value proposition** — what's the one sentence that sells this?
- **Language** — German (Austrian), English, or mixed?

---

## Step 1: Audit across 8 categories

Go through **each category** below. For every issue found, note the file, the specific rule violated, and the recommended fix. Rate severity as:
- **🔴 Critical** — copy actively hurts clarity, trust, or conversion
- **🟠 Major** — noticeably weak, confusing, or off-brand copy
- **🟡 Minor** — polish opportunity, tighter wording possible

---

### Category 1: Clarity

#### Sentence Length
> Max 20 words per sentence. Anything longer gets split.

**Check for:**
- Sentences over 20 words
- Run-on sentences with multiple clauses joined by "und", "aber", "weil"
- Paragraphs that are one giant sentence
- Subordinate clause chains (German trap: "..., der ..., die ..., welche ...")

**Fix pattern:** Split at conjunctions. One idea per sentence. Read aloud — if you run out of breath, it's too long.

---

#### Active Voice
> Active voice only. The user is the subject, not the object.

**Check for:**
- Passive constructions: "wird gespart", "kann genutzt werden", "wurde entwickelt"
- Impersonal constructions: "Es wird empfohlen", "Man sollte"
- Hidden agent: who is doing the action?

**Fix pattern:** "Sie sparen Zeit" not "Zeit wird gespart." "Wir entwickeln" not "Es wurde entwickelt." Name the actor.

---

#### Plain Language
> No jargon, no corporate speak, no filler. Write like a human talking to a human.

**Check for:**
- Technical jargon the target audience wouldn't use
- Corporate filler: "ganzheitlich", "innovativ", "State-of-the-Art", "Synergien"
- Filler words: "eigentlich", "grundsätzlich", "sozusagen", "gewissermaßen"
- Nominalizations: "Durchführung" instead of "durchführen", "Optimierung" instead of "verbessern"
- Unnecessarily complex words where simpler ones exist

**Fix pattern:** Replace every jargon word with the word your user would use over coffee. "Implementierung" → "Umsetzung" → better: "So funktioniert's."

---

#### One Idea Per Sentence
> Each sentence carries exactly one thought. No stacking.

**Check for:**
- Sentences with "und" connecting two unrelated ideas
- Sentences that need re-reading to parse
- Dense paragraphs mixing multiple concepts without breaks

**Fix pattern:** Split compound sentences. Each sentence = one idea. If a sentence has a semicolon, it's probably two sentences.

---

### Category 2: PAS Framework (Problem → Agitate → Solution)

#### Problem Statement
> The first sentence in any persuasion block should name the user's exact pain or desire.

**Check for:**
- Opening sentences that describe the product instead of the user's problem
- Missing problem framing — jumping straight to features
- Vague problem statements: "Beziehungen sind nicht einfach" (too generic)
- Problem statement that doesn't match the target audience's actual language

**Fix pattern:** Open with their words, their pain: "Ihr redet aneinander vorbei — schon wieder." Not: "Kommunikation ist der Schlüssel jeder Beziehung."

---

#### Agitation
> The second beat deepens the emotional resonance. Make the pain tangible.

**Check for:**
- Missing emotional layer — problem stated but not felt
- Jumping from problem directly to solution without pause
- Agitation that crosses into fear/crisis framing (respect brand boundaries)

**Fix pattern:** Add one sentence that makes the problem personal and present: "Und irgendwann fragt ihr euch, ob das noch normal ist." Don't manipulate — empathize.

---

#### Solution
> The third beat delivers the fix. Clear, confident, specific.

**Check for:**
- Solution statement that's vague: "Wir können helfen"
- Solution buried in a long paragraph instead of standing alone
- Solution that doesn't directly answer the problem stated above

**Fix pattern:** Direct answer: "attuned. gibt euch die Werkzeuge, um das Gespräch zu finden — bevor es zum Streit wird." Problem → Solution in the same breath.

---

### Category 3: Human Voice & Tone

#### Conversational Tone
> Write like a trusted friend, not a brochure. Contractions, questions, "du/ihr/Sie."

**Check for:**
- Copy that sounds like it was written by a committee
- Missing direct address (no "du", "ihr", or "Sie" — just describing the product)
- No questions in the copy (questions create engagement)
- Stiff, formal constructions that create distance

**Fix pattern:** Add questions: "Kennt ihr das?" Use direct address. Vary between statements and questions. The copy should feel like someone talking, not presenting.

---

#### Sentence Rhythm
> Vary sentence length. Short punches for impact. Longer sentences for breathing room.

**Check for:**
- All sentences the same length (monotonous)
- No short, punchy sentences for emphasis
- Long passages without any rhythm change
- Missing fragment sentences for emphasis ("Genau das.", "Ohne Wenn und Aber.")

**Fix pattern:** Alternate: long sentence that sets context. Short one for punch. Then a medium one that moves forward. Read aloud — it should have rhythm.

---

#### Banned Words & Phrases
> Kill corporate speak. These words signal "we're trying too hard."

**Banned in German copy:**
- "ganzheitlich", "innovativ", "State-of-the-Art", "Synergie"
- "solution-oriented", "robust", "leverage", "cutting-edge"
- "einzigartig" (without proof), "marktführend" (without data)
- "Mehrwert" (vague), "nachhaltig" (overused unless literally about sustainability)
- "Ihre Zufriedenheit liegt uns am Herzen" (cringe)
- "Wir sind stolz darauf" (nobody cares)
- Anything that could be on a motivational poster

**Fix pattern:** Delete and replace with specific, human language. "Ganzheitlicher Ansatz" → "Alles an einem Ort." "Innovativ" → describe what's actually new.

---

### Category 4: Benefits Over Features

#### "So What?" Test
> For every feature mentioned, ask "so what?" — the answer is the benefit.

**Check for:**
- Feature lists without outcomes: "KI-gestützte Analyse" (so what?)
- Technical descriptions without user impact
- "What it does" without "what it means for you"
- Benefits that are still abstract: "bessere Kommunikation" (how specifically?)

**Fix pattern:** Feature → "so what?" → Benefit. "KI-gestützte Analyse" → "Versteht, was euch wirklich beschäftigt." "Push-Benachrichtigungen" → "Erinnert euch an das, was ihr euch vorgenommen habt."

---

#### Personal Wins Framing
> Frame benefits as personal wins: time saved, stress reduced, connection felt.

**Check for:**
- Abstract benefits: "verbesserte Beziehungsqualität" (too academic)
- Missing emotional payoff
- Benefits framed for the product ("unsere App kann...") instead of for the user ("ihr bekommt...")

**Fix pattern:** Make it tangible and personal: "2 Stunden pro Woche, die ihr euch wirklich widmet" instead of "regelmäßige Quality Time."

---

### Category 5: Microcopy

#### Error Messages
> Errors should be human, helpful, and specific. Never technical, never blaming.

**Check for:**
- Technical errors: "Invalid input", "Error 400", "Validation failed"
- Blaming language: "Sie haben einen Fehler gemacht"
- Missing suggestion for how to fix it
- Error messages in English when UI is German

**Fix pattern:** Format: "Hm, das hat nicht geklappt. [What went wrong] — [how to fix it]." Example: "Diese E-Mail-Adresse sieht nicht ganz richtig aus. Bitte nochmal prüfen?"

---

#### Form Labels & Helpers
> Forms should feel reassuring, not bureaucratic.

**Check for:**
- Labels that are just field names: "E-Mail", "Name" (no context)
- Missing helper text for non-obvious fields
- No privacy reassurance near email/phone fields
- Required field indicators that feel aggressive (red asterisks without explanation)

**Fix pattern:** Add micro-reassurance: "Deine E-Mail — nur für deinen Account, kein Spam." Helper text that answers "why do you need this?"

---

#### Progress & Motivation
> Multi-step flows should motivate, not drain.

**Check for:**
- Progress bars without encouraging copy
- Steps without context ("Schritt 3" — of how many?)
- Missing celebration at completion
- Dry transitions between steps

**Fix pattern:** "Schritt 2 von 4 — fast geschafft!" instead of just "2/4". Add micro-celebrations: "Super, das war's schon!" at the end.

---

#### Empty States & Placeholders
> Every empty state is a copywriting opportunity.

**Check for:**
- Placeholder text that's generic: "Keine Ergebnisse"
- Empty states without guidance on what to do next
- Loading states without personality
- Placeholder copy left in from development ("Lorem ipsum", "TODO")

**Fix pattern:** Empty states should guide: "Noch keine Einträge — starte jetzt mit eurem ersten Check-in." Make every state useful.

---

### Category 6: Edit & Tighten

#### 30% Cut Rule
> First draft is always too long. Cut 30% without losing meaning.

**Check for:**
- Paragraphs that could be sentences
- Sentences that could be phrases
- Phrases that could be single words
- Redundant qualifiers: "wirklich einzigartig", "sehr innovativ", "ganz besonders"
- Filler phrases: "Es ist wichtig zu beachten, dass...", "Wie bereits erwähnt..."

**Fix pattern:** Read every sentence. Ask: "Can I say this in fewer words?" If yes, do it. "Es ist wichtig zu beachten, dass wir Wert auf Datenschutz legen" → "Eure Daten bleiben privat."

---

#### Skimmability
> 80% of users scan, not read. Copy must work when skimmed.

**Check for:**
- Long paragraphs without subheadings (>3 sentences)
- No bold text highlighting key phrases
- Missing bullet points where lists would work better
- Headlines that don't convey value when read alone (skip the body)
- Walls of text without visual breaks

**Fix pattern:** Bold key phrases. Use bullets for lists of 3+. Break paragraphs at 3 sentences max. Every subheading should sell on its own.

---

#### Front-Loading
> Put the most important word first. In headlines, in sentences, in paragraphs.

**Check for:**
- Headlines that bury the benefit: "Mit unserer neuen Funktion können Sie jetzt Zeit sparen" (benefit at end)
- Sentences that start with filler: "Es gibt viele Gründe, warum..."
- Paragraphs that save the punchline for last

**Fix pattern:** "Zeit sparen — mit einer Funktion, die mitdenkt." Benefit first, explanation second. Inverted pyramid: most important info first.

---

### Category 7: Austrian German Localization

#### Vocabulary — Bundesdeutsch vs. Österreichisch
> Austrian German has distinct vocabulary. Using Bundesdeutsch (German German) sounds foreign and corporate.

**Replace these (Bundesdeutsch → Österreichisch):**

**Essen & Küche** (Austrians notice these instantly):

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| Kartoffel | Erdapfel | Bundesdeutsch klingt fremd |
| Brötchen | Semmel | Sofort als "Piefke" erkennbar |
| Sahne | Schlagobers / Obers | Kulinarik-Grundwort |
| Quark | Topfen | Niemals Quark! |
| Pfannkuchen | Palatschinken | Kulturell wichtig |
| Tomate | Paradeiser | Klassisch österreichisch |
| Aubergine | Melanzani | Küche |
| Aprikose | Marille | Identitätswort |
| Hackfleisch | Faschiertes | Standard |
| Blumenkohl | Karfiol | Sofort erkennbar |
| Meerrettich | Kren | Klassiker |
| Pflaumen | Zwetschken | Nicht Pflaumen! |
| grüne Bohnen | Fisolen | Küche |
| Hähnchen | Hendl | Würstelstand bis Heuriger |
| Johannisbeeren | Ribisel | Sofort erkennbar |
| Pilze | Schwammerl | Umgangssprache |
| Rosenkohl | Kohlsprossen | Küchenstandard |
| Porree / Lauch | Lauch / Porree | Beides OK, "Lauch" gängiger |
| Konfitüre | Marmelade | "Konfitüre" = Schweiz/DE |
| Eiscreme / Eis | Eis / Gefrorenes | "Eiscreme" = amerikanisch |
| Bonbon | Zuckerl | Klassiker |
| Berliner / Krapfen | Krapfen | Niemals Berliner! |
| Brathähnchen | Backhendl / Brathuhn | Traditionsgericht |
| Soße | Sauce / Saft (beim Braten) | "Soße" = norddeutsch |
| Brotzeit | Jause | Identitätswort! |
| Abendbrot | Abendessen / Nachtmahl | "Abendbrot" = norddeutsch |
| Mittagessen | Mittagessen / Mittag | OK, aber "zu Mittag essen" |
| Joghurt (das) | Joghurt (das) | Gleich, aber AT: Neutrum! |
| lecker | gut / gschmackig / fesch | "Lecker" = Deutschländer |
| Guten Appetit | Mahlzeit / Guten Hunger | "Appetit" klingt snobbig |

**Alltag, Haushalt & Wohnen:**

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| Tüte | Sackerl | Umgangssprache |
| Junge | Bub | Natürlicher |
| Mädchen | Mädl / Madl | Natürlicher |
| dieses Jahr | heuer | Typisch österreichisch |
| letztes Jahr | voriges Jahr / vorigs Jahr | "Letztes Jahr" = OK aber weniger AT |
| Stuhl | Sessel | Im Alltag Standard |
| Treppe | Stiege | Regional aber verbreitet |
| Schrank | Kasten | Alltagssprache |
| Bürgersteig | Gehsteig | Standard in AT |
| Aufzug | Lift | Gängiger |
| Stockwerk | Stock | "Im dritten Stock" |
| Dachboden | Dachboden / Boden | "Am Boden" = am Dachboden |
| Keller | Keller | Gleich |
| Flur / Diele | Gang / Vorraum / Vorzimmer | "Flur" = norddeutsch |
| Gardine | Vorhang | "Gardine" = unüblich in AT |
| Steckdose | Steckdose / Dose | OK, gleich |
| Glühbirne | Birne / Glühbirne | "Birne" reicht |
| Eimer | Kübel | "Eimer" = unüblich in AT |
| Mülleimer | Mistkübel | Standard |
| Fegen / Kehren | Kehren / Zusammenkehren | "Fegen" = norddeutsch |
| Putzen | Putzen / Aufwischen | Gleich |
| Wäsche aufhängen | Wäsche aufhängen / aufhängen | Gleich, aber "die Wäsch" |
| Kleiderbügel | Kleiderbügel / Bügl | Gleich |
| Fernseher | Fernseher / Glotze | Gleich, "Kastl" = sehr umgangssprachlich |

**Mobilität & Unterwegs:**

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| Fahrrad | Rad | "Fahrrad" klingt umständlich |
| Straßenbahn | Straßenbahn / Bim | "Bim" = Wien-Klassiker |
| U-Bahn | U-Bahn / Ubahn | Gleich |
| Fahrkarte | Fahrkarte / Fahrschein | "Fahrschein" = AT-Standard |
| Parkhaus | Parkhaus / Parkgarage | "Garage" häufiger in AT |
| Ampel | Ampel | Gleich |
| Stau | Stau | Gleich, aber "im Stau stehen" |
| Autobahn | Autobahn | Gleich |
| Kreisverkehr | Kreisverkehr | Gleich |
| Tankstelle | Tankstelle / Tanke | "Tanke" = umgangssprachlich |
| Lkw | Lkw / Laster | Gleich |
| Motorhaube | Motorhaube | Gleich |
| Kofferraum | Kofferraum | Gleich |
| Blinker | Blinker / Winker | "Winker" = umgangssprachlich |
| Führerschein | Führerschein / Schein | "Schein" = umgangssprachlich |

**Bildung, Beruf & Karriere:**

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| Abitur | Matura | Bildungssystem |
| Klausur | Schularbeit | Schulkontext |
| Note (Schulnote) | Note | Gleich, aber AT: 1-5 (nicht 1-6!) |
| Zeugnis | Zeugnis | Gleich |
| Studiengebühren | Studienbeitrag | AT-Terminus |
| Semester | Semester | Gleich |
| Praktikum | Praktikum / Praxis | Gleich |
| Bewerbung | Bewerbung | Gleich |
| Lebenslauf | Lebenslauf / CV | Gleich |
| Gehalt | Gehalt | Gleich, aber AT: 14 Gehälter! |
| Urlaub | Urlaub | Gleich, aber "auf Urlaub fahren" (nicht "in") |
| Feierabend | Feierabend / Dienstschluss | "Dienstschluss" = AT-Beamte |
| Kollege | Kollege / Arbeitskollege | Gleich |
| Chef | Chef | Gleich, AT auch: "der Alte" (umgangssprachlich) |
| kündigen | kündigen | Gleich |
| Gewerkschaft | Gewerkschaft | Gleich, AT: ÖGB |
| Betriebsrat | Betriebsrat | Gleich |
| freiberuflich | freiberuflich / selbstständig | Gleich |

**Papierkram, Amt & Verwaltung:**

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| Papierkram | Papierkrieg / Amtswege | "Papierkram" = norddeutsch |
| Behörde | Behörde / Amt | Gleich, AT sagt öfter "Amt" |
| Einwohnermeldeamt | Meldeamt / Magistrat | AT-Struktur anders |
| Bürgeramt | Magistrat / Bezirksamt | AT-Verwaltungsstruktur |
| Standesamt | Standesamt | Gleich |
| Finanzamt | Finanzamt | Gleich |
| Steuererklärung | Steuererklärung / Arbeitnehmerveranlagung | AT-Terminus |
| Beglaubigung | Beglaubigung / Vidimierung | Amtsdeutsch AT |
| Personalausweis | Personalausweis / Ausweis | "Ausweis" kürzer |
| Krankenhaus | Spital | "Spital" = typisch AT |
| Arztpraxis | Ordination | "Ordination" = AT-Standard |
| Rezept (Arzt) | Rezept | Gleich |
| Krankenkasse | Krankenkasse / ÖGK | AT: Österreichische Gesundheitskasse |
| Apotheke | Apotheke | Gleich |
| Rechtsanwalt | Rechtsanwalt / Anwalt | AT auch: "Advokat" (gehoben) |
| Notar | Notar | Gleich |
| Ordner (Büro) | Ordner / Mappe | "Mappe" für dünne Ordner |
| Quittung | Bon / Rechnung | "Quittung" = klingt nach Finanzamt |
| Formular | Formular / Zettel | "An Zettel ausfüllen" |
| Briefkasten | Briefkasten / Postkastl | "Postkastl" = umgangssprachlich |
| Postbote | Briefträger / Postler | "Postler" = umgangssprachlich |

**Geld, Einkaufen & Konsum:**

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| Geldautomat | Bankomat | Markenname, aber Standard |
| Girokonto | Girokonto / Gehaltskonto | "Gehaltskonto" = AT-Banken |
| Überweisung | Überweisung | Gleich |
| EC-Karte | Bankomatkarte | "EC-Karte" = Deutschland |
| Kassenbon | Bon / Kassabon | "Kassenbon" mit doppel-s → "Kassabon" |
| Pfand | Pfand | Gleich, aber AT-Pfandsystem anders |
| Sonderangebot | Aktion / Angebot | "In Aktion" = AT-Standardausdruck |
| Rabatt | Rabatt / Nachlass | Gleich |
| Einkaufswagen | Einkaufswagen / Wagerl | "Wagerl" = umgangssprachlich |
| Kassierer/in | Kassier/in | Ohne -er am Ende |
| Geschäft / Laden | Geschäft / Gschäft | "Laden" = eher norddeutsch |
| Drogerie | Drogerie | Gleich, AT: "Bipa", "dm" |
| Fleischer / Metzger | Fleischer / Fleischhauer | "Metzger" = süddeutsch/CH |

**Verben & Redewendungen** (subtil aber wichtig):

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| gucken | schauen | "Gucken" = norddeutsch |
| reden | reden / plaudern | "Plaudern" = gemütlich |
| anrufen | anrufen / anläuten | "Anläuten" = umgangssprachlich |
| arbeiten | arbeiten / hackln | "Hackln" = umgangssprachlich |
| laufen / rennen | laufen / rennen | Gleich |
| spazieren gehen | spazieren gehen / flanieren | Gleich |
| sich unterhalten | sich unterhalten / tratschen | "Tratschen" = plaudern (nicht negativ in AT) |
| sich ärgern | sich ärgern / sich giften | "Giften" = AT-umgangssprachlich |
| sich beeilen | sich beeilen / sich tummeln | "Tummeln" = umgangssprachlich |
| kaputtmachen | kaputtmachen / zamhauen | "Zamhauen" = umgangssprachlich |
| aufräumen | aufräumen / zamräumen | "Zamräumen" = umgangssprachlich |
| sich setzen | sich setzen / sich hinhauen | "Hinhau di" = umgangssprachlich |
| verstehen | verstehen / kapieren / checken | Gleich |
| es funktioniert | es geht / es funktioniert | "Es geht" = natürlicher |
| ich schaffe das | ich schaff das / des pack i | "Des pack i" = motiviert |
| sauer / wütend | grantig / bös | Emotionaler |
| müde | müde / miad | "Miad" = umgangssprachlich |
| betrunken | betrunken / fett / bsoffn | Viele AT-Varianten |
| Quatsch / Unsinn | Blödsinn / Schmäh / Topfen | "Quatsch" = norddeutsch |
| Kram / Zeug | Glumpert / Graffl / Zeug | "Kram" = norddeutsch |
| prima / toll | super / leiwand / ur geil | "Prima" = klingt nach 1960 |
| klasse | super / leiwand | "Klasse" = unüblich in AT |
| nein | na / nein | "Na" = umgangssprachlich |
| ein bisschen | a bissl / ein bisserl | "Ein bisschen" = zu schriftdeutsch |
| vielleicht | vielleicht / vüleicht | Gleich |
| trotzdem | trotzdem / egal | Gleich |
| irgendwann | irgendwann / irgendwann amol | "Amol" = umgangssprachlich |

**Digital & Marketing-Kontext** (relevant für UX Copy):

| ❌ Bundesdeutsch / Anglizismus | ✅ Österreichisch / Besser | Warum |
|-------------------------------|---------------------------|-------|
| Benutzerkonto | Konto / Account | "Benutzerkonto" = umständlich |
| Zahlungsweise | Zahlungsart | "Zahlungsweise" = bürokratisch |
| Versandkosten | Versandkosten / Zustellkosten | "Zustellung" = AT-Post-Sprache |
| Rückerstattung | Rückerstattung / Gutschrift | "Gutschrift" = freundlicher |
| Lieferzeit | Lieferzeit / Zustellzeit | "Zustellung" für AT |
| Kundenservice | Kundenservice / Kundendienst | Beides OK |
| herunterladen | herunterladen / downloaden | Beides OK in AT |
| hochladen | hochladen / uploaden | Beides OK |
| Einstellungen | Einstellungen | Gleich |
| Benachrichtigung | Benachrichtigung / Mitteilung | Gleich |
| Datenschutz | Datenschutz | Gleich |
| Nutzungsbedingungen | Nutzungsbedingungen / AGB | "AGB" = kürzer, gängiger |
| Erfahrungsbericht | Erfahrungsbericht / Bewertung | "Bewertung" = kürzer |
| Warenkorb | Warenkorb | Gleich |
| Wunschliste | Wunschliste / Merkliste | "Merkliste" = moderner |
| Startseite | Startseite | Gleich |
| Suchleiste | Suchleiste / Suchfeld | Gleich |

**Grüße, Höflichkeit & Floskeln:**

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| Hallo | Servus / Grüß Gott | "Hallo" = neutral, aber nicht AT-typisch |
| Tschüss | Pfiat di / Baba / Servus | "Tschüss" = norddeutsch |
| Auf Wiedersehen | Auf Wiederschauen / Pfiat Gott | "Wiedersehen" = bundesdeutsch |
| Vielen Dank | Danke / Dankschön | "Vielen Dank" = zu formell für digital |
| Gern geschehen | Gern gschehn / Bitte / Passt scho | Kürzer, wärmer |
| Wie geht es Ihnen? | Wie geht's Ihnen? / Wie geht's? | Kürzer |
| Entschuldigung | Entschuldigung / Tschuldigung | Gleich, aber kürzer |
| Ich bin satt | I bin stad | "Satt" = ungewöhnlich in AT |
| Prost | Prost / Zum Wohl | Gleich |
| Alles Gute | Alles Gute / Ois Guade | "Ois Guade" = herzlicher |
| Herzlichen Glückwunsch | Gratulation / Gratuliere | "Herzlichen Glückwunsch" = steif |
| Frohe Weihnachten | Frohe Weihnachten / Fröhliche Weihnachten | Gleich |
| Guten Rutsch | Guten Rutsch / An guatn Rutsch | Gleich |
| Schönes Wochenende | Schönes Wochenende | Gleich |
| Mahlzeit | Mahlzeit | AT-Standard-Mittagsgruß |

**Wetter, Natur & Freizeit:**

| ❌ Bundesdeutsch | ✅ Österreichisch | Warum |
|-----------------|-------------------|-------|
| es regnet | es regnet / es schüttet | Gleich |
| Gewitter | Gewitter / Wetter | "A Wetter" = umgangssprachlich für Gewitter |
| Hügel | Hügel / Bühel / Bichl | Regional |
| Berg | Berg | Gleich, aber AT hat mehr davon |
| Berghütte | Hütte / Alm | "Berghütte" = touristisch |
| wandern | wandern / bergsteigen | Gleich |
| Kneipe | Beisl / Wirtshaus | "Kneipe" = norddeutsch |
| Gaststätte | Wirtshaus / Gasthaus | "Gaststätte" = formell |
| Café | Kaffeehaus / Café | "Kaffeehaus" = Wiener Tradition |
| Biergarten | Gastgarten / Schanigarten | "Biergarten" = bayerisch |
| Karussell | Ringelspiel | AT-Klassiker |
| Kirmes / Rummel | Prater / Kirchtag / Kirtag | Regional |
| Silvester | Silvester | Gleich |
| Fasching | Fasching | Gleich (nicht "Karneval"!) |
| Karneval | Fasching | "Karneval" = Köln/Düsseldorf |

**Check for:**
- Any Bundesdeutsch vocabulary that would sound "piefkinesisch" in Austria
- Food/kitchen terms especially (Austrians notice these instantly)
- Administrative/bureaucratic terms that sound German-German
- Digital UX copy that uses unnecessarily stiff alternatives
- Greetings and pleasantries that don't match Austrian convention
- Verbs and expressions that reveal a non-Austrian writer
- Shopping/commerce terms that use German-German conventions
- Regional terms that feel wrong for the target audience's geography

**Important:** Not every entry needs to go full dialect. For digital products, aim for the **modern Austrian educated register** — the language a 30-year-old Wiener*in uses at work. Not dialect, not Bundesdeutsch, not Amt. When a word is marked "umgangssprachlich" in the table, use it only if the brand voice allows casual tone.

**Fix pattern:** Replace with Austrian equivalent. When in doubt, use the word your Wiener Nachbarin would use, not the one from a Hamburg textbook.

---

#### Tone — Austrian Höflichkeit
> Austrian German is direct but warm. Not overly formal, not American-casual.

**Check for:**
- Overly stiff language: "Wir möchten Sie darauf hinweisen" (Amt-Sprache)
- Too casual / American: "Hey! Check das aus!" (cringe in AT)
- Missing warmth: pure information without human touch
- Du/Sie inconsistency within the same context
- "Vielen Dank für Ihre Anfrage" (too formal for digital products)

**Austrian tone sweet spot:**
- Warm but not cheesy
- Direct but not rude
- Professional but not bureaucratic
- "Servus" energy, not "Grüß Gott, Herr Magister" energy

**Fix pattern:** Write like a friendly Wiener Kaffeehausbesitzer: warm, direct, a bit of Schmäh, but always respectful.

---

#### Numbers & Formatting — Austrian Conventions
> Austrian formatting differs from German and English. Getting it wrong looks sloppy.

**Rules:**
- Currency: `199 €` (number + space + symbol), never `EUR 199` or `€199`
- Date: `14.03.2026` (dots, not slashes or dashes)
- Thousands: `1.999` (dot as separator), not `1,999`
- Decimals: `19,99 €` (comma), not `19.99 €`
- Time: `14:30 Uhr` or `14.30 Uhr`, not `2:30 PM`
- Phone: `+43 1 234 56 78` (spaces, country code)

**Check for:**
- English number formatting (commas for thousands, dots for decimals)
- Currency symbol before number (American style)
- Date in wrong format
- Missing `Uhr` after time

**Fix pattern:** Apply Austrian conventions consistently. Check every number, date, price, and phone number in the UI.

---

#### Americanisms & Hype Words
> American marketing language sounds fake and off-putting in Austrian context.

**Ban list — never use in Austrian copy:**
- "Game-Changer", "Disruptiv", "Next Level"
- "Hustle", "Grind", "Boss", "Crushing it"
- "Amazing", "Awesome", "Epic" (even in German: "episch")
- "Community" (use "Gemeinschaft" or specific: "2.400 Paare")
- "Content" (use "Inhalte" or "Beiträge")
- "Mindset" (use "Einstellung" or "Denkweise")
- "Journey" / "Reise" as metaphor (overused)
- "Passion" / "Leidenschaft" (too dramatic)
- Excessive exclamation marks!!! (one is enough, and rarely)
- ALL CAPS for emphasis (use bold or italics)

**Check for:**
- English loanwords where German alternatives exist and sound better
- Hype language that promises more than it delivers
- Silicon Valley startup speak in Austrian context
- Motivational poster language

**Fix pattern:** Replace with grounded, specific Austrian German. "Game-Changer" → describe what actually changes. "Community" → "2.400 Paare, die attuned. nutzen."

---

#### Legal & Formal Copy
> Impressum, Datenschutz, AGB must use correct Austrian legal German.

**Check for:**
- German legal terms instead of Austrian (e.g., "BGB" instead of "ABGB")
- Missing Austrian-specific legal requirements (ECG, DSG, TKG)
- Informal tone in legal pages (maintain professional register)
- Inconsistent Sie/Du between legal pages and product copy

**Fix pattern:** Legal copy stays formal with "Sie." Reference Austrian law correctly (ABGB, ECG, DSG 2018). Keep it clear but professional.

---

---

## Step 2: Report findings

Present findings grouped by severity:

```
## Copy Audit Results

### 🔴 Critical — copy hurts clarity, trust, or conversion
| Issue | Copy Rule | File:Line | Current Copy | Recommended Fix |
|-------|-----------|-----------|-------------|-----------------|
| ... | ... | ... | ... | ... |

### 🟠 Major — noticeably weak or off-brand
| Issue | Copy Rule | File:Line | Current Copy | Recommended Fix |
|-------|-----------|-----------|-------------|-----------------|
| ... | ... | ... | ... | ... |

### 🟡 Minor — tighter wording possible
| Issue | Copy Rule | File:Line | Current Copy | Recommended Fix |
|-------|-----------|-----------|-------------|-----------------|
| ... | ... | ... | ... | ... |

### 🇦🇹 Austrian Localization Issues
| Issue | Current | Fix | File:Line |
|-------|---------|-----|-----------|
| ... | ... | ... | ... |

### ✅ Well done
- [list what the project already does well in copy]
```

Ask the user: **"Soll ich die Copy-Issues fixen? Alle oder nur die kritischen?"**

---

## Step 3: Fix issues

Apply fixes directly in the codebase. For each fix:
- Show before → after for every copy change
- Preserve the brand voice and tone
- Never change meaning, only improve clarity and impact
- Respect Austrian German conventions
- Keep copy at the same approximate length (don't inflate)
- Follow the project's existing code style

---

## Step 4: Summary

```
Copy Audit Complete!

✅ [N] copy issues fixed
🇦🇹 [N] Austrian localization fixes
⚠️ [N] issues flagged for manual review

Rules applied:
- [list which copy rules were most relevant]

Top 3 highest-impact changes:
1. [change] — [which rule, expected impact]
2. [change] — [which rule, expected impact]
3. [change] — [which rule, expected impact]

Recommended next steps:
- A/B test headline variations
- User testing: 5-second test with Austrian target audience
- Read all copy aloud — if it sounds weird, rewrite it
- Check legal pages with Austrian legal counsel
```

---

## Rules

- **Audit the words**, not the layout, visuals, or conversion funnel structure
- Read every piece of user-facing copy — headlines, body, CTAs, form labels, errors, tooltips, legal
- **Austrian German first** — not Bundesdeutsch, not Swiss German, not translated English
- Match the project's brand voice — don't impose a different personality
- **Never add dark patterns** — no fake urgency, no guilt-tripping, no manipulative loss framing
- Copy should feel native, not translated
- Every change should make the copy clearer, shorter, or more human — ideally all three
- Show before → after for every change so the user can review
- Follow the project's existing code style and component patterns
- When in doubt about Austrian usage, prefer the word a Wiener*in between 25-45 would use in everyday conversation

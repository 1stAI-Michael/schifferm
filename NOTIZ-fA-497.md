# fA-497 — umgesetzt am 27.08.2026, VM-30-Web

Ticket-Owner: **VM-30-Web**. Vorlage: `ticket.py show 497` (Durchgang Michael +
codex-07-Bewerbungen, 27.08.). Diese Notiz ersetzt die Arbeitsnotiz von heute früh.

## Stand: **live auf schifferm.de** seit 27.08.2026

Deploy auf Michaels ausdrückliche Ansage vom 27.08. (`sudo sh ./scripts/deploy-webspace.sh`),
danach `chown` zurück. Live nachgemessen im Browser, DE und EN: 28/28 Langtexte, ein
Johnson-Controls-Block, 16 von 45 Zertifikaten offen sichtbar + „Weitere Qualifikationen (29)",
keine Privatfelder im Seitenkörper, drei Absätze im Profilkopf.

Zwei Fallen, die dabei aufgeflogen sind und behoben wurden:

* **`sudo` und das Token.** Der Deploy braucht `sudo` (`/srv/Container/.env` ist root-only),
  unter `sudo` ist aber `HOME=/root` — dort liegt die Token-Datei nicht, der neue Prebuild
  wäre abgebrochen. `_token_file()` fällt jetzt über `$SUDO_USER` auf das Home des
  aufrufenden Users zurück. Der dokumentierte Deploy-Befehl bleibt damit unverändert gültig.
* **`addressCountry` stand fest auf `DE`** — in `schema.jsonld` und in `profile.json`.
  Bei einer polnischen Anschrift ist das schlicht falsch. Kommt jetzt aus `country_en`
  über eine kleine ISO-Tabelle; ein unbekanntes Land wird **weggelassen und gewarnt**,
  nicht geraten.

## Die fünf Punkte — was gemessen im HTML steht

| Punkt | Umsetzung | Beleg aus `out/de/career/index.html` |
|---|---|---|
| 1 Projekt-Langtexte | `components/career/JobProjects.jsx`, Muster von `/de/projects/` | 28 von 28 `description_de` im HTML, längster 2.537 Zeichen; 28 Aufklapp-Buttons |
| 2 Johnson Controls | `getWorkExperienceGrouped()` bündelt gleiche Arbeitgeber in Folge | genau 1 `<h3>Johnson Controls</h3>`, „10 Stationen", 1997-02 – 2010-06 |
| 3 Alte Qualifikationen | `ArchivedCertifications.jsx`, `quality` + `misc` | „Weitere Qualifikationen (29)", sichtbar bleiben ai_data 11, ai_healthcare 1, management 4 |
| 4 Privatfelder | `getPersonalInfo()` gibt sie gar nicht mehr heraus | alle sieben Felder nicht im Seiten-Körper |
| 5 Absätze | `summaryParagraphs`, Split an `\n\n` | 3 `<p>` statt einem Block |

**Reine Darstellung, DB unangetastet** — kein Skript schreibt in die Career-Daten.

## Datenquelle umgestellt (der Build-Blocker)

`scripts/generate-career-formats.py` lud `career.db` per WebDAV; die Datei ist `malformed`
und die SQLite ist laut Michael abgeschaltet. Das Skript liest jetzt die **Career-Device-API**
`https://app.ti-ub-ki.ddns.net/api/career/device/<tabelle>`, alle elf Tabellen, HTTP 200.

* Token aus `$FLOWS_CAREER_TOKEN` oder `~/.config/flows/tokens/VM-30-Web.token` — nie in `argv`,
  nie ausgegeben. Damit fällt auch das alte `curl -u` mit dem Nextcloud-Passwort weg (fA-488-Klasse).
* Das Skript schreibt jetzt zusätzlich `public/career/career_data.json`. Damit haben Prebuild
  und Website-UI **dieselbe Quelle** — die „zwei Consumer, zwei Datenpfade"-Falle ist zu.
* Rückfallwege: `--json <datei>` (fertiger Export), `--db <datei>` (lokale SQLite), `--no-export`.

## Was sich dadurch am Datenstand ändert (war 20.08., ist jetzt tagesaktuell)

* Anschrift Spremberg → Kostomloty/Polen, E-Mail `Schiffer@TIUB.de` → `schiffer@1stAI.eu`.
* Zertifikate stehen chronologisch — der `sort_order`-Fix aus der DB wird erst jetzt sichtbar.
* Skills 54 → 52. **Keine Verluste, zwei Dubletten:** id 4 „MS Project" (office) war eine
  Kopie von id 13 (pm_tools); id 19 „Postgres" ist in id 48 „PostgreSQL mit pgvector" aufgegangen.

## Entschieden — nicht anfassen

**Impressum/Datenschutz/Footer bleiben bei `03130 Spremberg` und `Schiffer@TIUB.de`.**
Michael-Entscheid 27.08.2026: das ist für schifferm.de **richtig so**; Kostomloty ist die
Anschrift von **1stAI** und gehört in dessen Impressum. Dass der Lebenslauf jetzt Polen zeigt
und das Impressum Deutschland, ist kein Widerspruch, sondern die Trennung der beiden Firmen —
also nicht „angleichen".

## Offen — Michaels Entscheidung, nicht angefasst

1. **Umlaute in `description_de`**: die Langtexte sind ASCII-transliteriert („fuer",
   „Uebergaben", „anschliessend"). Fiel nie auf, weil sie nie gerendert wurden. Gehört in die
   DB, also zu codex-07-Bewerbungen.

## Randbedingungen, die weiter gelten

* Kein Deploy ohne ausdrückliche Ansage (VERÖFFENTLICHUNG).
* `career_data.json` ist ein Export — nicht editieren, der nächste Build überschreibt sie.
* `positioning.de/en.oneLiner` in `src/content/profile.js` muss dem DB-Summary entsprechen.
  Nachgemessen: die drei Absätze mit `" "` zusammengefügt ergeben **byteweise** den
  vorhandenen oneLiner (699 bzw. 697 Zeichen) — kein Nachziehen nötig.
* `sudo`-Build hinterlässt root-owned `out/`/`.next/` → danach `chown` zurück.

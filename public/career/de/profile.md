# Dipl.-Ing. Michael Schiffer, MBA

> Prozessoptimierer & Program Manager mit 20+ Jahren Automobilindustrie, Serienanläufen und globalen Werksstrukturen. Seit 2024 verstärkt fokussiert auf Generative AI, Healthcare Automation, Datenanalyse, KI-gestützte Prozessoptimierung und Telemedizin-Workflows.
>
> Betrieb einer eigenen On-Premise-LLM-Infrastruktur auf heterogenem Multi-GPU-Verbund: zwei produktive RAG-Systeme mit rund 42.000 embeddeten Chunks (COBOL-Legacy-Korpus und Dokumenten-/Mail-Wissensbasis), 130.000+ geroutete Requests und 463 Mio. verarbeitete Input-Token in 14 Tagen.
>
> Fundierte Kenntnisse in Python/FastAPI, PostgreSQL mit pgvector, Hybrid-Retrieval und Reranking, GPU-Lastmanagement sowie Dokumenten-KI (OCR/Vision-LLM).

- **Standort:** Kostomloty, Polen
- **E-Mail:** schiffer@1stAI.eu
- **Telefon:** +49 172 25 6 42 48
- **Website:** https://www.schifferm.de
- **LinkedIn:** https://www.linkedin.com/in/michael-schiffer

## Sprachen
- Deutsch: Muttersprache
- Englisch: Sehr gut
- Französisch: Basiskenntnisse
- Spanisch: Basiskenntnisse
- Polnisch: Basiskenntnisse

## Berufserfahrung
### 1stAI — Founder
*2026-06 – heute* | Kostomloty, Polen (remote, EU-weit)

Eigenes Beratungs- und Entwicklungsunternehmen für KI-Implementierung, Sitz in Polen, Tätigkeit remote EU-weit. Leistung von der Architektur über die Umsetzung bis zum produktiven Betrieb in einer Hand.

Schwerpunkte: Retrieval-Architekturen (RAG) auf eigenen Datenbeständen, Betrieb von Sprachmodellen im eigenen Rechenzentrum statt in der Cloud, Agenten- und Werkzeugintegration sowie die Anbindung bestehender Systeme über OpenAI-kompatible Schnittstellen.

Eigene On-Premise-LLM-Infrastruktur auf heterogenem Multi-GPU-Verbund als Entwicklungs- und Referenzumgebung; Fachbeiträge im eigenen Blog.

### The Implementers GmbH — Berater / Geschäftsführer
*2010-01 – heute* | Germany

Beratung und Interim Management in der Automobilindustrie, Healthcare und weiteren Branchen. Schwerpunkte: Programm Management, Serienanläufe, Werksleitung, Lieferantenentwicklung, Kostenreduzierung, Prozessoptimierung, KI-Implementierung und KI-gestützte Prozessautomatisierung.

**Projekte:**
- **Mobile Recorder App + KI-Bearbeitungs-Pipeline** (2025-09 – heute): Mobiles Aufnahme-Werkzeug für strukturierte Sprachaufzeichnungen mit nachgelagerter KI-Pipeline. Public Web-App (https://the-implementers.de/Recorder/) zur Aufnahme von Briefen, Anamnesen, Teammeetings, Notizen, Ideen, Aufmassen und Übergaben — direkt im Browser, ohne Installation. Vorab-Auswahl von Kontext (Patient-ID/Name, Themenkategorie, Empfänger) bestimmt nachgelagertes Routing der Pipeline. Audio-Upload via HTTPS, anschließend Verarbeitung in dedizierter Pipeline-UI (FastAPI, ti-nas-06:8011): WhisperX-Transkription mit Speaker Diarization, themenspezifische LLM-Aufbereitung (Brief, Akteneintrag, Untersuchungsbericht, Memo etc.), manuelle Korrektur in Web-UI mit Diff-Ansicht, Quality Gates gegen LLM-Halluzination. Ergebnis-Routing nach Themenkategorie: medizinische Dokumente in OpenEMR-Patientenakte (Auto-Upload), Geschäfts-Notizen in Flow-Notes-DB, Aufmasse in Projekt-Datenbank. Voll Self-Hosted, Audio bleibt im eigenen Netzwerk. Stack: Vanilla JS Frontend, MediaRecorder API, FastAPI, WhisperX, Ollama (qwen3.5/gpt-oss), PostgreSQL, OpenEMR-API, Caddy mit IP-Whitelist.
- **Ollama-Stallwatch — Hang-Detection & REST-API für lokale LLM-Inferenz** (2026-04 – heute): Public MIT-lizenziertes Monitoring- und Diagnose-Tool für lokal gehostete Ollama-LLM-Inferenz auf Multi-GPU-Servern. Adressiert das in Production schwer fassbare Ghost-Hang-Pattern: Modell ist im VRAM geladen, GPU bleibt bei 0% Auslastung, ollama-serve haengt CPU-bound im Image-Preprocessing oder Vision-Encoder — im Log unsichtbar, nur in nvtop live erkennbar. Vier-Komponenten-Stack: GPU-Logger (nvidia-smi delta-logged), Log-Parser (Docker-Log in SQLite), Process-Logger (/proc mit Heartbeat), Stall-Detector mit gdb/proc Stack-Capture ohne Container-Modifikation via NOPASSWD-Sudoers. Hang-Detektion in drei parallelen Confidence-Levels (strict/loose/ghost) mit unterschiedlichen Trigger-Bedingungen, ergaenzt um orthogonale Mode-Klassifikation (A/B) die zwischen recoverable und silent Hangs unterscheidet. Read-only REST-API (Port 3002, Python stdlib) mit kombinierbaren Filtern (since/at/overlapping, confidence/mode/client_ip) für Cross-Host-Korrelation. Web-Dashboard (Chart.js, live aus SQLite) mit Stall-Banderolen über Zeitreihen. Idempotenter Installer mit Host-Detection und portabler config.toml. Realer Production-Impact: bei parallel laufender OCR-Pipeline über 24 Stunden 10.871 PDF-Seiten, 4.837 Inference-Calls, 97 erfasste Hang-Events — Pipeline-Success-Rate dadurch 97,8% statt ~75-80% bei naivem Wall-Clock-Timeout. Selfheal-Strategie auf Basis der Stall-Daten reduzierte Hang-Recovery-Zeit von ~40 Minuten auf ~17 Sekunden (Faktor ~140x). Stack: Python 3.12 stdlib-only (keine Pip-Dependencies), SQLite mit WAL, Chart.js via CDN, systemd-Service-Management, gdb und nvidia-smi als externe Tools. ~1.700 Zeilen Python, 3 iterative Entwicklungstage mit AI-Pair-Programming. Repo: https://github.com/tiubde-michael/ollama-stallwatch
- **GPU-Lastmanagement für heterogenen LLM-Verbund** (2026-06 – heute): Eigenentwicklung einer zentralen Routing-Engine für einen heterogenen GPU-Verbund: 4 GPU-Knoten (RTX 3090, Tesla V100, RTX 3060, NVIDIA GB10 mit 128 GB Unified Memory) und 8+ Modell-Endpoints (Chat, Embeddings, Reranker). Fähigkeitsbasierte Kandidatenwahl (Endpoint × Modell × Kontextfenster × Slots) statt statischer Pools; benannte Mandanten (Klinik, Chat, Batch, Gast) mit Prioritäten, Quoten und Preemption niederpriorer Lasten. Migration im laufenden Betrieb ohne Ausfall: Shadow-Mode (Alt- vs. Neu-Entscheidung je Request protokolliert und reviewed) mit anschließendem stufenweisen Cutover; Nacht-Burn-in über 23.600 Requests mit ~0,1 % Abnormalitäten. Auto-Discovery der Endpoint-Kapazitäten (llama.cpp /metrics, ollama, HuggingFace TEI), Live-Monitoring-UI in React und vollständiges Reservierungs-Audit. Produktionsvolumen: 130.000+ geroutete Requests in 14 Tagen. Nach einem Stromausfall kam ein Modellserver ohne GPU hoch und rechnete 40 Minuten auf der CPU weiter — 72 statt 950 Token/s bei der Prompt-Verarbeitung, erkennbar nur an einer einzigen Log-Zeile; seitdem wird nach jedem Neustart die GPU-Belegung je Prozess geprüft. Stack: Python, FastAPI, PostgreSQL, React/TypeScript, llama.cpp, ollama, TEI, Docker.
- **OpenAI-kompatibles API-Gateway mit externer Kunden-Anbindung** (2026-06 – heute): Eigenes /v1-Gateway (Chat mit SSE-Streaming, Embeddings, Rerank) vor dem GPU-Verbund; Anbindung eines externen Kubernetes-Clusters auf Kundenseite über Token-Auth mit Scopes. Per-Token-Limits (parallele Requests, Requests/min, Token/min) live aus der Datenbank steuerbar; Modell-Allowlist und Kontext-Guards gegen stille Trunkierung. Produktionslast über 14 Tage: 338.000 Chat-Requests, 463 Mio. Input- und 76 Mio. Output-Token, Peak 5.746 Requests/h bei ~1 % Fehlerquote. Traffic- und Fair-Use-Analysen auf Audit-Basis (Token-, Volumen- und Bandbreiten-Hochrechnung) als Entscheidungsgrundlage für Hosting-Verträge. Stack: Python, FastAPI, SSE, PostgreSQL, JWT/Token-Scopes, Caddy, Docker.
- **Inbetriebnahme & Tuning NVIDIA GB10 (ARM64) als LLM-Server** (2026-07 – heute): Inbetriebnahme eines ASUS Ascent GX10 (NVIDIA GB10, ARM64, Unified Memory) als produktiver LLM-Server. Diagnose reproduzierbarer vLLM-Instabilität auf der GB10/ARM64-Plattform und Umbau auf zwei parallele llama.cpp-Instanzen mit Kontext-Split auf einem Chip (4×256k für Langkontext, 8×48k für Standardlast). Paralleler Betrieb von Chat-, Embedding- und Reranker-Services auf demselben Knoten. Eigene Messreihen zu Prefill- und Generierungs-Durchsatz sowie Sättigungsverhalten (Bandbreiten-Bound bei 273 GB/s). 429-basierte Backpressure-Strategie: Verbund-Durchsatz ~193 tok/s bei 0 Fehlern im 30-Minuten-Messfenster. Erkenntnistransfer in Hardware-Dimensionierung und Beschaffungsempfehlungen für Kundenprojekte.
- **RAG-Wissensplattform für COBOL-Altsysteme — Lead Architektur (Mittelständischer Softwarehersteller (über Generalunternehmer))** (2026-04 – 2026-10): Strategischer Lead Architektur sowie Sparring- und Review-Instanz für ein zweiköpfiges Senior-Entwickler-Tandem beim Aufbau einer On-Premise-Wissensplattform, die eine über Jahrzehnte gewachsene COBOL-Codebasis (mehrere Mio. LOC, Visual COBOL, Fixed Format) durchsuchbar und beauskunftbar macht. Betrieb vollständig on-premise, da der Quellcode das Kernasset des Kunden ist. Fünfstufige Architektur: deterministische Inventarisierung per Parser statt LLM (PROGRAM-ID, COPY-, CALL-, EXEC-SQL-Beziehungen, Dateideskriptoren, Datenstrukturen), Graph-Extraktion über Aufruf-, Copy-, Daten- und Job-Beziehungen, LLM-gestützte Anreicherung, Qualitätsschleife und Retrieval mit Zitatzwang (jede Antwort referenziert Programm und Zeilennummer, ohne belastbaren Treffer keine generierte Antwort). Korpus: 528 COBOL-Programm-Kennungen, 17.279 Chunks mit Dual-Embeddings (bge-m3 on-prem + Azure text-embedding-3-large), 3.697 CALL/COPY-Abhängigkeitskanten als Graph. Hybrid-Retrieval per Reciprocal Rank Fusion über 5 Pfade (Code, Doku mehrstufig, Sektionen, GraphRAG) plus Knowledge Cards und Cross-Encoder-Reranking (lokal bzw. Cohere Rerank); Embedding-Backend pro Request zwischen On-Prem-GPU und Azure/EU umschaltbar. Fachwörterbuch-/Synonymschicht mit Query-Expansion zur Überbrückung zwischen Fachsprache und Bezeichnern im Code. Qualitätssicherung: 430 Ground-Truth-Queries als Eval-Harness, 12 kategoriespezifische Suchprofile, Multipass-LLM-Tiefenanalyse je Programm mit Fallback-Modellkette; Recall@10 von rund 61 % im Prototyp auf über 83 % im produktiven Stand gesteigert. Lokaler Betrieb quantisierter Open-Weights-Modelle (MoE ~35B / ~3B aktiv, q4) mit Hybrid-Fallback auf ein EU-gehostetes Cloud-Modell für nicht vertrauliche Anteile. Modell-Benchmark über sieben Kandidaten und Hardware-Empfehlung in drei Ausbaustufen mit zwei Beschaffungspfaden als dokumentierte Entscheidungsgrundlage. Gap-Analyse der Quellcode-Erstlieferung mit konkreter Nachlieferungsempfehlung an den Endkunden. Packaging und Betrieb: Multi-Stage-Docker, Alembic-Migrationen, getrennte Dev-/Prod-Instanzen mit abgesichertem Migrationsweg, K8s-Manifeste, GitHub Actions in eine private Container-Registry; Auslieferung on-prem und im Kunden-Kubernetes. Zugänge über REST-API, MCP-Server für Entwicklerwerkzeuge und Web-Chat für nicht entwicklungsnahe Rollen. IP- und Lizenzprüfung vor Auslieferung (Abhängigkeits-Scan, Copyleft-Erkennung, Attribution-Nachweis). 100 % remote, Workshops per Video.
- **E-Mail-Automation und -Archiv mit RAG-Assistent** (2026-03 – heute): IMAP-Fetcher mit Drei-Phasen-UID-Abgleich (Deduplizierung vor Header- und Body-Fetch), Regel-Engine auf Absender- und Betreff-Mustern sowie robuster Fehlerbehandlung für instabile Provider-IMAP-Server. Volltext-Archivierung in PostgreSQL, automatisches Anhang-Routing in die OCR-Strecke (Rechnungseingang) und Nextcloud-Synchronisation. Darauf aufgesetzt ein zweites RAG-System auf Dokument-, Mail- und Notiz-Basis: 24.500+ embeddete OCR-Chunks in pgvector als Wissensbasis für einen internen Chat-Assistenten. Stack: Python, FastAPI, PostgreSQL/pgvector, IMAP, Nextcloud, Docker.
- **Agenten-Studio — Multi-Agent-Softwareentwicklung mit Claude Code** (2026-04 – heute): Seit April 2026 arbeiten in dieser Umgebung rund zwei Dutzend Claude-Code-Sitzungen parallel an Software, Infrastruktur und Dokumentation — jede auf ihrem eigenen Arbeitsbereich, mit eigener Identität und eigenen Rechten. Jeder Baustein des Arbeitsmodells antwortet auf einen gemessenen Fehler, der vorher still geblieben war: bei Agenten sieht Stille aus wie Erfolg.

Koordination: Ein Ticket ist genau eine Verantwortung. Aufträge an andere Agenten werden Sub-Tickets mit eigenem Eigner; wer als Nächstes handeln muss, ist ein eigenes Feld, getrennt vom Eigner, und Abhängigkeiten stehen als Sperre am Ticket statt im Fließtext. Prioritäten A/B/C und Fälligkeiten steuern die Reihenfolge; vertagt werden darf nur mit Grund, und der Server lehnt ohne Grund ab. Greifen zwei Agenten gleichzeitig nach demselben Ticket, gewinnt der Erste per bedingter Übernahme in einer einzigen Datenbankanweisung — vorher gewann nachweislich der Letzte. Reviews laufen als Sub-Ticket an genau eine prüfende Sitzung, teils an Codex als unabhängige zweite Instanz.

Betrieb: Schichten aus Durchgang und Wache — die Wache weckt nur bei einer Antwort auf die eigenen Sperren oder einer neuen Aufgabe; sieben frühere Wach-Varianten wurden auf eine zurückgeführt. Arbeitsanleitungen und Regeln kommen versioniert aus einem Git-Repository, Zugangsdaten ausschließlich über einen Broker, der den Eintrag serverseitig auflöst und Mehrdeutigkeit ablehnt statt zu raten.
- **Agenten-Studio-Übersicht — Leitstand für parallele Claude-Code- und Codex-Sitzungen** (2026-08 – heute): Wer viele Coding-Agenten gleichzeitig laufen lässt, verliert sie aus dem Blick — jede Sitzung ist ein Terminal auf einer anderen Maschine. Der Leitstand macht rund fünfzig Claude-Code- und Codex-CLI-Sitzungen in neun Fenstern sichtbar, baut die Anordnung per Klick auf und misst den Arbeitsort, statt ihn einzustellen: drei Arbeitsplätze mit unterschiedlichen Monitoren, erkannt an Anschluss und Modell.

Aufträge an viele Sitzungen zugleich werden erst nach gemessener Bereitschaft zugestellt. An einem gewöhnlichen Arbeitstag trugen 9 von 29 Eingabefeldern einen unabgeschickten Entwurf; die Zustellung wartet dann, statt ihn zu überschreiben. Automatische Befehlsketten warten auf eine Bestätigung, deren Nullpunkt an ein Ereignis gebunden ist statt an eine Wartezeit — eine feste Karenz hatte nachweislich die schnelle Antwort verschluckt. Rückfragen der Agenten werden aus zwei Quellen erkannt, dem Bildschirm und dem Server, mit fester Rangfolge: bei 12 von 18 wartenden Sitzungen hatte der Server keine Kenntnis davon. Beendete Sitzungen starten per Tastendruck am selben Platz neu und führen das Gespräch fort.

Das Programm ersetzt 13 Shell-Skripte mit 2.300 Zeilen: rund 6.400 Zeilen Python ohne externe Abhängigkeiten, 20 Tabellen, 249 Tests — jeder prüft einen Fehler, der bereits einmal aufgetreten ist. Überwachungslast von 200 % auf 4 % CPU, Systemlast von 23,4 auf 6,3.
- **Modernisierung einer Excel-VBA-Planungsanwendung mit Claude Code — Migration nach CSV, SQLite und HTML (Endkunde über Generalunternehmer)** (2026-05 – 2026-05): Ausgangslage: Ein Projektplan über 18 Monate lebte in einer Excel-Arbeitsmappe mit rund einem Dutzend VBA-Makros. Balken waren Zeichenobjekte über Datumsspalten, Vorgänger-Pfeile wurden per Makro nachgezogen. Bei rund 130 Arbeitspaketen blieb die Oberfläche bei jeder Änderung sekundenlang stehen; Konfliktkopien auf dem gemeinsamen Laufwerk brachen die VBA-Referenzen, die Wiederherstellung kostete jedes Mal rund 20 Minuten.

Analyse mit Claude Code: Das Problem war nicht die Tabelle, sondern dass dieselbe Datei Daten und Darstellung trug. Daraus ergab sich der Schnitt — drei CSV-Dateien als einzige Quelle, eine daraus erzeugte SQLite, eine statische HTML-Seite als Auslieferung, jeder Schritt einzeln aufrufbar. Starttermine werden fest verankert oder aus Vorgänger, Versatz und Typ berechnet; alle vier Vorgängertypen waren im Bestand bereits nötig. Codex prüfte die Umsetzung als unabhängige zweite Instanz.

Zwei stille Fehler des Altsystems sind konstruktiv beseitigt statt per Regel: Die reduzierte Kundensicht und die interne Sicht waren zwei Dateien, die auseinanderliefen — beim letzten Vergleich fehlten der Kundensicht acht Zeilen. Jetzt ist es eine Datei mit zwei Detailstufen. Und der Fortschritt war ein Overlay über dem Balken, das beim Sortieren an der alten Stelle hängen blieb — der Balken zeigte 30 %, das Overlay 70 %. Jetzt teilen sich beide dieselbe Zeile. Kernumbau rund 12 Stunden, danach zwei Wochen Feinschliff mit Editor-Oberfläche und Konsistenzbericht; die Datenpflege bleibt eine Tabelle.
- **Agentisches Coding mit lokalen Open-Weight-Modellen — Claude Code on-premise** (2026-09 – heute): Claude Code läuft zusätzlich zum Cloud-Betrieb gegen lokal gehostete Qwen-Modelle auf llama.cpp, verbunden über einen Übersetzer zwischen Anthropic- und OpenAI-Schnittstelle. Die erste echte Sitzung brach bei jedem Werkzeugaufruf mit „failed to parse grammar" ab. Die Ursache war nicht Größe, Anzahl der Werkzeuge oder Verlauf, sondern eine einzige Zahl in einem Werkzeugschema: eine verschachtelte Längenschranke ab 2.000 überschreitet die feste Wiederholungsgrenze des Grammatik-Parsers — 1.999 läuft, 2.000 liefert HTTP 400, exakt gemessen. Danach trat mit derselben Fehlermeldung eine zweite, völlig andere Ursache auf: Regex-Escapes in verschachtelten Mustern. Der Übersetzer entschärft beides und protokolliert jede Änderung; Nachweis im Echtbetrieb mit 40 Werkzeugen und rund 87.000 Token.

Modellwahl per Messung statt nach Datenblatt: acht Programmieraufgaben, drei Agenten-Harnesse, je drei Wiederholungen, jede mit einer versteckten Prüfung. Jede Prüfung musste auf dem unveränderten Projekt scheitern und bei richtiger Lösung bestehen — sonst misst man die Prüfung statt des Modells. Das dichte Qwen3.8-27B löste 72 von 72 Läufen, das schnellere Mixture-of-Experts-Modell Qwen3.6-35B-A3B 64 von 72, und seine Fehler waren Denk-, keine Tippfehler. Für Stapelarbeit bleibt das MoE-Modell gesetzt (181 gegen 32 Token/s bei acht parallelen Anfragen); geroutet wird nach Aufgabe. Mit Qwen3.8 löst Claude Code dieselben Aufgaben wie ein für offene Modelle gebautes Harness, und schneller.

Denkstufen an echter Arbeit nachgemessen — Wartungsdokumentation für ein COBOL-Programm mit 4.000 Zeilen, zwei Maschinen, zwei Inferenz-Engines: die Stufe „low" ist so gut wie „medium" und 10 % schneller, beide liefern rund die zweieinhalbfache Abdeckung gegenüber „ohne Denken". Die Modellvorgabe „xhigh" lieferte 0 von 20 verwertbaren Antworten. Eine übernommene Temperatur-Empfehlung ließ sich per Gegenmessung nicht belegen.
- **TI-Flows Stack — Custom Workflow-Automatisierungsplattform** (2026-01 – heute): Kompletter Ersatz der n8n-Workflow-Engine durch eine maßgeschneiderte Python/React-Plattform für medizinische Datenverarbeitung, Server-Sicherheit und Portfolio-Management. Async-Backend (FastAPI + SQLAlchemy + asyncpg), React/TypeScript-SPA mit 30 Seiten, 20+ Workflows mit Cron-Scheduling und Execution-Chaining, 11 Background-Tasks. Workflow-Engine mit dynamischem Handler-Import, WebSocket-Live-Logs und verketteter Ausführung. 7-Schichten-Sicherheitskonzept: IP-Whitelist/Blacklist (Caddy), Brute-Force-Monitor mit Auto-Blacklisting, Telegram-gesteuerte IP-Freischaltung per Inline-Keyboard, JWT-Auth, Device-Tokens, Rate-Limiting. 5-stufige medizinische Transkript-Pipeline (WhisperX-Diktat bis Akteneintrag) mit LLM-Quality-Gates. Depot-Modul: Playwright-basierter comdirect-Scraper, 7-Faktor-Aktien-Ranking, KI-News-Zusammenfassung (Ollama). Zentrale Ollama-Queue mit Semaphore-basierter GPU-Serialisierung. Shared Library (flowlib) für 3 Services. ~24.000 LOC (12.800 Python + 8.000 TypeScript + 1.600 flowlib + 2.000 SQL), 21 DB-Migrationen. Stack: Python 3.10, FastAPI, SQLAlchemy async, React 18, TypeScript, Vite, PostgreSQL (pgvector), Docker Compose, Caddy, Ollama, Telegram Bot API, Playwright.
- **Invoice API — Medizinisches Abrechnungssystem** (2025-12 – 2026-02): Vollständiges Abrechnungssystem für eine ärztliche Praxis mit Mehrmandantenfähigkeit (Arzt, IT-Dienstleistungen, Apotheke). Draft/Finalisierung/Storno-Workflow mit datenbankgestützter State Machine (PL/pgSQL-Trigger) — finalisierte Rechnungen sind unveränderlich (Revisionssicherheit). ZUGFeRD/EN16931-konforme Rechnungserzeugung (PDF mit eingebettetem CII-XML). OpenEMR-Integration: Patientenstammdaten, Diagnosen, Behandlungen. Steuerlogik: §4 UStG-Befreiung, Reverse Charge, innergemeinschaftliche Lieferungen. Server-Side Rendering mit Jinja2 + HTMX. Snapshot-Pattern für revisionssichere Rechnungen. ~4.200 LOC Python, ~1.700 LOC SQL, 30+ Endpoints, 13 DB-Migrationen. Stack: Python, FastAPI, SQLAlchemy (async), PostgreSQL, HTMX, Jinja2, Docker, Caddy.
- **Intelligente Dokumentenerkennung & automatisierte Bankabstimmung** (2025-08 – heute): Architektur und produktiver Betrieb einer On-Premise OCR-/Dokumenten-Pipeline für deutsche Steuer- und Buchhaltungsdokumente; Ersatz für Azure Document Intelligence mit messbar besserer Erkennungsqualitaet und vollstaendiger Datenhoheit. Volumen: 12.156 verarbeitete Seiten (Stand 07/2026), 97,8% Erfolgsquote; laufende Cloud-Kosten von $1.500/Jahr auf 0 EUR gesenkt. Azure-Vergleich (400 Dokumente A/B-Test): Rechnungsnummer 33%→86%, Gesamtbetrag 41%→88%, Absender 58%→94%. Fuenf-Layer-Stack: PaddleOCR (Baseline), qwen3-vl:4b (schnelle Vision), mistral-nemo:12b (Text-Fallback), qwen3.5:27b (hochqualitative Strukturextraktion), Qwen3.5:27b Klassifikation in 18 Dokumenttypen mit Mandanten-Routing. Acht produktive Resilienz-Mechanismen entwickelt: Watchdog-Threads mit Wall-Clock + GPU-Idle + Cross-Host-Stall-Polling, eigene Degeneracy-Detection für pathologische Vision-Modell-Ausgaben, Partial-Text-Recovery, Cold-Load-Selbstheilung (12s Cost vs 180s gesparter Hang = 15x Netto-Gewinn), Per-Phase-Modell-Unload mit Verifikation, Cross-Host-Monitoring mit REST-API und drei Confidence-Stufen für Hang-Typen. Nachgelagerte Layer: Index-basiertes Bank-Matching (>3.000 Transaktionen x >4.000 Dokumente in ca. 7 Sekunden) und DATEV-EXTF-CSV-Export nach gelernten Kontierungsregeln. Web-UI (FastAPI) mit 4-Spalten-Vergleich der Extraktionsquellen, DB-gesteuerte Prompt-Versionierung mit Fallback-Ketten. Infrastruktur: Docker Compose Multi-Container, PostgreSQL auf NAS, GPU-Sharing (RTX 3090 Ti + RTX 5060 Ti) via Ollama. Stack: Python, FastAPI, PaddleOCR, Ollama (qwen3-vl, qwen3.5, mistral-nemo, deepseek-ocr, gemma3), PostgreSQL, Docker, scikit-learn, httpx mit Streaming + Watchdog-Cancel. Ergänzungen 2026: LLM-gestützter Mehrseiten-Dokument-Split, ZUGFeRD-/XRechnung-Abgleich, Belegklassifikation nach Mandant, Dokumentklasse und Steuerjahr sowie Vorkontierung für die DATEV-Übergabe. Der zuvor parallel betriebene Azure-Document-Intelligence-Pfad wurde vollständig durch die eigene On-Premise-Strecke abgelöst und ist nicht mehr im Einsatz. Messwerte je Seite auf einer Tesla V100: ~2,5 s OCR + ~5–6 s Vision-LLM-Extraktion reine Rechenzeit; bewusst kleine Spezialmodelle (5 GB + 3,5 GB) statt eines großen Generalisten.
- **HRV-Analyse-Pipeline — Automatisierte Herzratenvariabilitäts-Auswertung (Praxis für Schmerztherapie & TCM, Baden-Baden)** (2026-01 – 2026-02): Modulare Pipeline zur reproduzierbaren HRV-Analyse von 24–26h Langzeit-EKG-Aufzeichnungen im EDF-Format. Vollautomatische Verarbeitung: EDF-Einlesen, R-Peak-Detektion (Bandpass, Envelope, Refraktärbereinigung), Artefaktkorrektur, Zeit-/Frequenzbereichsmetriken (SDNN, RMSSD, LF/HF), PNS/SNS-Trendberechnung (Kubios-kalibriert), ECG-basierte Atemfrequenzschätzung und Time-Varying HRV Power Spectrum. Docker-Container mit File-Watcher für Batch-Betrieb. Ersetzt manuelle Legacy-Windows-Software (8 Schritte auf 2). Stack: Python, NumPy, SciPy, Matplotlib, pyEDFlib, Docker.
- **Schmerztherapie-Dokumentationssystem (schmerz_dok)** (2026-02 – heute): Klinikfähiges Dokumentationssystem für die multimodale Schmerztherapie. Unterstützt ein interdisziplinäres Team (Ärzte, Psychotherapeuten, Physiotherapeuten, Pflege). OPS-basiertes Anforderungs-Tracking (OPS 8-918, 8-91c) mit Meilensteinen auf 21-Tage-Zeitachse. 4-Farben-Ampelsystem für Echtzeit-Therapiefortschrittskontrolle. Bettenbelegungskalender mit Gantt-Visualisierung und Überbelastungserkennung. Rich-Text-Editor (TipTap/ProseMirror) mit Versionierung. 10-stufige Rollenhierarchie mit Audit-Trail. Serverseitige PDF-Reports (WeasyPrint). Stack: Python 3.12, FastAPI, SQLAlchemy 2.0 (async), React 19, Tailwind CSS, PostgreSQL 16, Docker, Nginx, JWT.
- **VIVO PainCare — KI-gestützte klinische Schmerzbewertung und Aufnahmebegründung (Praxis für Schmerztherapie & TCM, Baden-Baden)** (2025-09 – 2026-03): Klinisches Entscheidungsunterstützungssystem für die stationäre Schmerztherapie. Automatisierte Verarbeitung von VIVO PainCare-Schmerzfragebögen (PDF → Markdown → Regex-Extraktion → Datenbank) mit 20-Faktor-Ampelbewertung (Rot-Gelb-Grün) über standardisierte Schmerzskalen (VAS, PDI, MPSS, DASS, FFbH, VR-12, NHP, HKF-R10, SBL). KI-generierte Therapieempfehlungen und objektive Begründungen für den Krankenhausaufenthalt nach Wirtschaftlichkeitsgebot (medgemma:27b, Self-Hosted). Längsschnittanalyse über 182-Tage-Verlauf mit automatischer Entlassbrief-Textbausteinerstellung. Druckoptimierter A4-One-Pager für die Patientenakte. 206 Fragebögen verarbeitet, ~28.000 Antworten extrahiert, 117 Patienten im System. Stack: FastAPI, Ollama (medgemma:27b), PyMuPDF, React + TypeScript, PostgreSQL, Docker.
- **Klinische Dokumentation — KI-gestützte Transkriptions- und Dokumentationspipeline** (2025-08 – 2026-02): End-to-End-System zur automatisierten Erstellung medizinischer Dokumentation aus Arzt-Patienten-Gesprächen. Aufzeichnung nach Einwilligung, Upload per App oder USB-Diktiergerät, Transkription mit WhisperX (Speaker Diarization). Fünfstufige LLM-Pipeline (Ollama, Self-Hosted): automatische Themenerkennung, Patientenzuordnung, strukturierte Zusammenfassung, Akteneintrag und Untersuchungsbericht als Vorlagen für die Praxissoftware (OpenEMR). Themenbasiertes Prompt-Routing mit DB-gestützter Versionierung und A/B-Testing. Quality Gates gegen repetitive LLM-Ausgaben. Review-UI für ärztliche Freigabe mit direktem Upload nach OpenEMR. Vollständig Self-Hosted — kein Cloud-LLM, kein externer Transkriptionsdienst. Stack: FastAPI, WhisperX, Ollama (qwen3.5/gpt-oss), PostgreSQL, React + TypeScript, Docker, Telegram Bot API, NFS, Caddy.
- **Lieferantenentwicklung Fahrwerksteile (KTM)** (2023-05 – 2024-11): Lieferantenentwicklung Fahrwerksteile (Fließpressteile mit Drehen- und Fräsbearbeitung) inkl. Änderungen, Neuanläufen, Verlagerungen und Engpasssteuerung.
- **Verlagerung von 150 Fahrwerksteilen (KTM)** (2022-07 – 2024-01): Verlagerung von 150 Fahrwerksteilen in (Drehen- und Fräsbearbeitung) laufender Serie wg. kurzfristiger Standortschließung.
- **Prozessaufnahme und Prozessoptimierung (Von Roll Schweiz AG)** (2018-06 – 2018-11): Prozessaufnahme und Prozessoptimierung im internen Vertrieb eines international tätigen Schweizer Maschinenbauunternehmens.
- **Interim Werksleitung (MAO Automotive GmbH & Co)** (2018-02 – 2018-06): Interim Werksleitung und Stabilisierung bis zur Übergabe an einen neuen Werksleiter, in einem ungarischen Produktionswerk für KFZ Innenraum Teile. Schwerpunkte Kaschierprozesse inkl. WKZ-Optimierung, Personal Reduzierung, Engpasssteuerung und Rückstandsabbau.
- **Lieferantenentwicklung DAG BR238 Türverkleidung (Megatech Industries Deutschland GmbH)** (2016-07 – 2017-10): Führung des Teams zur Befähigung aller Lieferanten DAG BR238 Türverkleidung inkl. Musterungen, PPAP / EMPB Tracking, Engpasssteuerung und Prozessabnahmen.
- **Interim COO & Werksleiter (PWG Profilrollen-Werkzeugbau GmbH)** (2015-09 – 2016-05): Führung des Werkes in Deutschland und Ausbau des Werkes in der Slowakei bei einem Aluminium verarbeitenden KFZ-Zulieferer für Dachsysteme. Ca. 350 Mitarbeiter, ca. 80 Mio. EUR Umsatz.
- **Kostenreduzierung Dachhimmelproduktion (Motus Headliner GmbH)** (2015-01 – 2015-08): Kostenreduzierung (Prozess, Material, Lohn und Lieferanten) in der Produktion von Dachhimmeln.
- **Programm Management Türinnenverkleidung DAG C292 (Toyota Boshoku America)** (2012-09 – 2015-01): Führung eines interdisziplinären Teams zur Entwicklung vom Türinnenverkleidung DAG C292 inkl. der Industrialisierung in Deutschland und Verlagerung zum Serienanlauf in die USA.
- **KFZ Sonnenblenden Entwicklung (MARTUR FOMPAK)** (2012-01 – 2014-12): Beratung des jungen Projektteams in der Türkei zur Optimierung aktueller Sonnenblenden und Entwicklung der ersten neuen Aufträge inkl. Konzepten, Marktanalysen, Konstruktionsbesprechungen und Projektreviews.
- **Kostenreduzierung DAG C218 Türverkleidung (Toyota Boshoku Europe NV)** (2012-03 – 2012-08): Kostenreduzierung (Prozess, Material, Lohn und Lieferanten) bei der Türinnenverkleidung DAG C218.
- **Werkzeugverlagerung Spritzgusswerkzeuge (Toyota Boshoku Europe NV)** (2012-01 – 2012-08): Werkzeugverlagerung von Spritzgusswerkzeugen zu neuen Lieferanten in laufender Serie inkl. Musterungen, Verbauversuchen, Vorstellung beim OEM und Abstimmung der Bemusterungsumfänge (PPAP/EMPB) mit dem OEM und den Lieferanten.
- **Programm Management BMW Sonnenblenden (Magna)** (2010-07 – 2011-12): Führung eines interdisziplinären Teams zur Entwicklung und Produktionsverlagerung von Sonnenblenden. Neuentwicklung der BMW L7, F12 & F13, i8 und MCV-Sonnenblenden.

### Praxis für Schmerztherapie & TCM, Olga Schiffer MSc — Praxis-IT, Digitalisierung und Backoffice
*2017-05 – 2025-05* | Baden-Baden, Deutschland

Aufbau und Betreuung der Praxis-IT einer Privatpraxis für Naturheilkunde, TCM und Schmerztherapie, parallel zur Tätigkeit bei The Implementers GmbH. Verantwortlich für die Digitalisierung der Praxisabläufe, die Anbindung medizintechnischer Geräte, Abrechnungs- und Dokumentenprozesse sowie Website und Backoffice.

**Projekte:**
- **Back Office Support und Prozessoptimierung (Praxis für Schmerztherapie & TCM, Baden-Baden)** (2018-05 – 2025-05): Laufende Unterstützung einer Privatpraxis für Schmerztherapie & TCM. Entwicklung eines elektronischen Narkoseprotokolls für ambulante Narkosen mit Live-Datenanbindung der Narkosemonitore von GE und Mindray einschließlich EKG-Daten sowie GOÄ-konformer Rechnungsstellung. Umstellung des Praxisbetriebs auf OpenEMR inklusive Rechnungsschnittstelle. Automatisierung der ärztlichen Betriebsabläufe sowie OCR-gestützte Erfassung und Vorkontierung eingehender Rechnungen. Aufbau und technischer Betrieb von Website und Fachblog der Praxis zu den Themen Naturheilkunde, TCM, Orthomolekulare Medizin sowie Cannabis-, Ketamin- und Neurofeedback-Therapie. Durchführung von 19-Kanal- und 2-Kanal-EEG-Messungen sowie Erstellung von qEEG-Auswertungen einschließlich Normdatenbank-Abgleich. Aufbau eines durchgängigen Telemedizin-Workflows aus den Diensten mehrerer Anbieter — von der DSGVO-Einwilligung über den digitalen Behandlungsvertrag bis zur Abrechnung. Dokumentenmanagement, Backoffice und Praxisorganisation.
- **Existenzgründungsberatung und Coaching (Praxis für Schmerztherapie & TCM, Baden-Baden)** (2017-05 – 2018-04): Existenzgründungsberatung und Coaching einer Privatpraxis für Schmerztherapie & TCM. Betreuung vom Konzept, Businessplan, Finanzierung, Terminverfolgung, Umbau und Einrichtung, Erstellen der Standardabläufe bis zur Implementierung einer Nachkalkulation.

### Johnson Controls — Program Manager Transfer Insolvente Lieferanten
*2009-07 – 2010-06* | Germany / Spain

Führung eines interdisziplinären, europäischen Teams zur Übernahme und Verlagerung von Umfängen aus Insolvenzen von verschiedenen Lieferanten für das Ford C344 Interieur Programm (Cockpit, Konsole, Säulen, Türverkleidungen) inkl. Änderungsmanagement und Bemusterung. Serienanlauf in Spanien.

### Johnson Controls — Program Manager Hyundai/Kia
*2007-12 – 2009-06* | Bratislava, Slovakia (DE/CZ)

Führung eines interdisziplinären, europäischen Teams, Dienstsitz Bratislava, mit dem Ziel eines erfolgreichen Serienanlaufes der Hyundai i30 Türverkleidung unter Berücksichtigung von Profit, Qualität und Kundenzufriedenheit. Entwicklung und Produktion in SK, Kunde in CZ.

### Johnson Controls — Leiter Technik und Produktion
*2006-09 – 2007-11* | Madrid, Spain

Krisenmanagement. Interim Produktionsleitung in einem 300 MA-Werk zur Montage von Sonnenblenden sowie der Spritzgussfertigung aller Komponenten in Madrid.

### Johnson Controls — Bereichsleiter
*2006-01 – 2007-11* | Espelkamp, Germany

Führung des Produktionsbereiches Schiebehimmel (GMPUR) und Sitzlehnenverkleidungen (Naturfasern) mit ca. 80 Mitarbeitern ca. 12 Mil.€ Jahresumsatz, inkl. Fertigungstechnik, Qualitätssicherung, Produktionsplanung und Outbound-Logistik mit dem Ziel der Verbesserung der Wirtschaftlichkeit des Bereiches. Prozesswerk mit Montage in Deutschland.

### Johnson Controls — Leiter Taskforce Ausschuss und Effizienz
*2005-08 – 2005-12* | Telford, UK

Führung eines interdisziplinären europäischen Teams, mit dem Ziel der kurzfristigen Reduzierung des Ausschusses und Steigerung der Effizienz bis zur Schließung des Werkes. Dachhimmelwerk in England.

### Johnson Controls — Technischer Leiter & Launch-Management
*2003-09 – 2005-08* | Schweighouse, France

Führung und Umstrukturierung der Bereiche Launch Management, Arbeitsvorbereitung, Prozessoptimierung und Instandhaltung mit ca. 50 Mitarbeitern, mit dem Ziel der kurzfristigen und dauerhaften Reduzierung des Ausschusses und Steigerung der Effizienz. Dachhimmelwerk in Frankreich.

### Johnson Controls — Black Belt / Program Management Office
*2001-05 – 2003-08* | Burscheid, Germany

Implementierung von Management-Informationssystemen, Vorbereitung und Durchführung von Projektmanagement-Trainings, Optimierung des Änderungsprozesses und Optimierung der Entwicklungs-Ressourcenplanung.

### Johnson Controls — Projekt Engineer Electronics
*2000-04 – 2001-05* | Burscheid, Germany

Koordination der Elektrischen-, Elektronischen- und Softwareumfänge während der Sitzentwicklung inkl. Freigaben, Änderungsmanagement, Erprobungen und Serienanlaufbetreuung.

### Johnson Controls — Test-Engineer / Testkoordinator
*1998-02 – 2000-04* | Burscheid, Germany

Aufbau eines neuen Bereiches „Versuch Interieur“ inkl. Konstruktion und Anschaffung von Prüfmaschinen. Erstellung von Testplänen für verschiedene europäische Fahrzeug-Innenraum-Projekte, Budgetplanung für diese Projekte und diesen Bereich, Betreuung von Versuchen wie z.B. Schwingungsuntersuchungen, Lebensdauertests und gesetzlich Homologations-Versuche.

### Johnson Controls — Prüfmittelverantwortlicher / Werkstudent im Bereich Versuch
*1997-02 – 1998-02* | Burscheid, Germany

Betreuung des QM Systems VDA6.1, QS9000, Konstruktion Testvorrichtungen, Versuchsdurchführung und Auswertungen.

### UB Dr. Hans Schiffer — Backoffice Assistant – Unternehmensberatung
*1997-01 – 1998-01* | Bonn, Germany

Erstellung und Formatierung von Präsentationen, Angeboten und Projektunterlagen. Vorbereitung von Berichten, Analysen und Workshop-Materialien. Pflege von Kunden- und Projektdaten. Unterstützung bei Rechnungsstellung, Zeiterfassung und monatlichem Reporting.

## Ausbildung
### UEL University of East London / ELBS London
*MBA — International Management* | 2001-09 – 2003-11
Note: 63
Abschlussarbeit: Successful Implementation of Kaizen.

### Rheinische Fachhochschule Köln
*Dipl.-Ing. (FH) — Maschinenbau, Studienrichtung: Konstruktionstechnik* | 1995-03 – 1998-05
Note: 1,3
Abschlussarbeit: Konstruktion, Berechnung und Realisierung eines Versuchsstandes, zur Bestimmung der Energieaufnahme und des Beschleunigungsverlaufes bei der Kopfstützenprüfung nach ECE-R17.

### Bonner Autohaus GmbH (Vertragswerkstatt der Daimler-Benz AG)
*Kfz-Mechaniker (Gesellenbrief) — Kfz-Mechanik* | 1992-10 – 1995-01

### Ernst-Moritz-Arndt-Gymnasium der Stadt Bonn
*Abitur — Schwerpunkt Mathematik und Physik* | 1988-06 – 1991-06
Note: 3,2

## Kenntnisse
- **Betriebssysteme:** Windows (bis 11) (gut), Linux (gut)
- **Office:** MS Excel (sehr gut), MS PowerPoint (gut), MS Word (gut)
- **CAD:** OnShape (gut), AutoCAD 3D (gut), CATIA V5 (Basis)
- **PDM:** Sherpa (Basis), Matrix One (Basis)
- **ERP/MRP:** SAP (Basis)
- **Projektmanagement-Tools:** MS Project (sehr gut), DotProject (Basis), eGroup (gut), eRoom (gut), BugZilla (gut)
- **Datenbanken:** MySQL (Basis), PostgreSQL mit pgvector (sehr gut), Alembic / Schema-Migrationen (gut), Access (Basis), Lotus 1-2-3 (Basis)
- **Programmierung:** Python (gut), C# (Basis), Visual Basic (Basis), VB.NET (Basis), Pascal (Basis), C (Basis)
- **AI & Automation:** N8N (gut), Ollama & LM Studio (lokale KI) (gut), Claude Code / Codex (sehr gut), GPT-OS:20B / Qwen etc. (gut), Lokale Telefonagenten / Local Phone Agents (gut)
- **LLM-Infrastruktur:** LLM-Serving (llama.cpp, vLLM, ollama, TEI) (sehr gut), Multi-GPU-Betrieb & GPU-Lastmanagement (sehr gut), RAG & Hybrid Retrieval (Vektor + BM25, RRF) (sehr gut), Embeddings & Cross-Encoder-Reranking (bge-m3, Cohere) (sehr gut), Azure OpenAI / EU-gehostete Cloud-Modelle (gut), Azure Document Intelligence (gut), Quantisierung & Modellauswahl (Qwen MoE, Gemma, MedGemma) (gut), OCR & Vision-LLM (PaddleOCR, DeepSeek-OCR, Qwen-VL) (sehr gut), LLM-Evaluation & Benchmarking (Ground-Truth-Harness) (gut)
- **Backend & DevOps:** FastAPI (async, SSE, WebSockets) (sehr gut), SQLAlchemy async / asyncpg (gut), React + TypeScript (SPA, Live-Monitoring) (gut), Docker / Docker Compose (sehr gut), Caddy Reverse Proxy & Security-Hardening (gut), GitHub Actions CI / Container Registry (gut), Kubernetes (Deployment-Manifeste) (Basis)
- **Medizintechnik:** qEEG-Messung und -Auswertung (19-Kanal / 2-Kanal, Normdatenbank-Abgleich) (gut), Neurofeedback-Systeme (Messung und Protokolle) (gut), Narkosemonitor-Anbindung GE / Mindray inkl. EKG-Daten (gut), OpenEMR (Praxis- und Klinikinformationssystem) (gut)

## Zertifikate
### AI & Data
- **EU AI Act erklärt: Was DU ab August zur neuen KI-Verordnung wissen musst** — WBS.LEGAL (Prof. Christian Solmecke) (2026-08)
- **Agentic AI with LangChain and LangGraph** — Coursera (IBM Skills Network) (2026-04)
- **Introduction to Deep Learning & Neural Networks with Keras (IBM)** — IBM / Coursera (2026-01)
- **Google AI Essentials (Specialization, 5 Kurse)** — Google / Coursera (2026-01)
- **Introduction to OpenAI Codex** — Scrimba / Coursera (2026-01)
- **Google Prompting Essentials (Specialization, 4 Kurse)** — Google / Coursera (2025-12)
- **Introduction to AI (Google)** — Google / Coursera (2025-12)
- **Vector Databases for RAG** — IBM / Coursera (2025-10)
- **Build Intelligent Agents using DeepSeek & N8N** — Board Infinity / Coursera (2025-07)
- **MySQL for Data Engineering** — Duke University / Coursera (2025-05)
- **Python for Everybody (Specialization, 5 Kurse)** — University of Michigan / Coursera (2025-04)

### AI Healthcare
- **Generative AI-Powered Solutions for Modern Healthcare (Specialization, 9 Kurse)** — Coursera (2025-11)

### Qualität
- **Toyota Boshoku Business Practices (TBBP) - Solving Problems The TB Way** — Toyota Boshoku (2025-10)
- **DFMEA und PFMEA (5 Tage)** — Gabor Kulsar / Magna Steyr (2013-11)
- **Vertiefungsworkshop QM nach DIN EN ISO 9001:2008** — KMU-Berater Bundesverband / Gemeinschaft zertifizierter Unternehmensberater (2013-02)
- **Wertstrom-Engineering (4 Tage)** — Fraunhofer IAO, Stuttgart (2012-10)
- **SixSigma Zertifizierter Black Belt** — Johnson Controls (2001-01)
- **Interne Audits VDA6.1, QS9000, BOS** — GFQ Akademie GmbH (firmeninternes Seminar bei Johnson Controls) (1998-01)
- **Prüfmittelstudien** — Johnson Controls (on-the-job) (1998-01)
- **VDA6.1 und QS9000 Anforderungen** — Technische Akademie Wuppertal (TAW) (1997-05)
- **Arbeitssystemgestaltung** — REFA-Verband (1996-11)
- **Medizinproduktegesetz, EG-Richtlinien, CE-Kennzeichnung** — MUS Fortbildungsseminar, Köln (1996-10)
- **REFA-Grundschein / REFA-Sachbearbeiter** — REFA-Verband Köln (1996-09)
- **EOQ Quality Auditor** — EOQ / DGQ (1996-06)
- **DGQ-Auditor / Lead Auditor (DIN EN ISO 10011-2)** — DGQ Bonn (1996-05)
- **Internal Auditor of Quality Systems** — DGQ (1996-05)
- **Qualitätstechnik II** — DGQ Bonn (1996-04)
- **EOQ Quality Systems Manager** — EOQ / DGQ (1996-01)
- **DGQ-Qualitätsmanager** — DGQ Bonn (1995-10)

### Sonstige
- **DSGVO Live-Webinar** — eRecht24 (2018-07)
- **Siemens NX Viewer / 3D Tool V12** — The Implementers GmbH (on-the-job) (2017-11)
- **TPG Infotag Microsoft Project** — TPG The Project Group (2012-10)
- **Datenschutz 2012** — Luther Rechtsanwaltsgesellschaft mbH (2012-09)
- **English in Management and International Business** — None (2001-02)
- **CANoe Praxis-Workshop (1 Tag)** — Vector Informatik GmbH, Stuttgart (2000-09)
- **Interne Trainings Projektingenieure Sitze** — Johnson Controls (2000-01)
- **Umweltsimulation von Schwingungs- und Stoßbelastungen (Shakerkursus)** — Technische Akademie Esslingen (TAE) (1999-01)
- **Training in Testmethoden und Verfahren** — Prince Automotive / Johnson Controls (on-the-job) (1998-08)
- **Rhetorik und Kommunikation (Diplom)** — Institut für Rhetorik und Kommunikation, Bornheim bei Bonn (1996-11)
- **2x 3 Tage Teambuilding** — None (1996-01)
- **DVS-Lehrgänge Gasschweißen (G-Schw) und MAG-Dünnblechschweißen (MAG-St D)** — DVS / Handwerkszentrum Bonn (1993-04)

### Management
- **Mit Strategie zu mehr Erfolg (EKS-Erfolgsstrategie)** — KMU-Akademie e.V. / Cord Tepelmann, UnternehmerCoach (2010-04)
- **Zertifizierter KMU-Fachberater Sanierung** — KMU-Akademie e.V., Hamm (2010-03)
- **Zertifizierter Program Manager (PMU / JCI)** — Johnson Controls (2002-07)
- **Das Unternehmen mit wichtigen Kennzahlen steuern** — RKW Rationalisierungs-Kuratorium der Deutschen Wirtschaft e.V., Bayern Büro Nürnberg (1996-10)

## Auszeichnungen
- Pallas Athene-Medaille für Diplomprüfung und Jahrgangsbester (1998)
- Jahrgangsbester der Kfz-Mechaniker-Ausbildung (1995)

## Führerscheine
- Klasse A, B, C1, C, BE, C1E, CE (ehem. Klasse II+III)
- Staplerschein
- Motorboot-Führerschein A Binnen u. Küste
- UKW-Sprechfunkzeugnis
- CEPT-Novice-Amateurfunkgenehmigung E

## Mitgliedschaften
- BDS: Bund Deutscher Sportschützen
- DARC: Deutscher Amateur-Radio-Club

## Interessen
Wohnmobile, Reisen, Kochen, Bouvier des Flandres, Amateurfunk, Sportschütze

---
Letzte Aktualisierung: 2026-08-27 05:00:04
Quelle: https://schifferm.de

# Dipl.-Ing. Michael Schiffer, MBA — Profil

## Kurzprofil
Prozessoptimierer & Program Manager mit 20+ Jahren Automobilindustrie, Serienanläufen und globalen Werksstrukturen. Seit 2024 verstärkt fokussiert auf Generative AI, Healthcare Automation, Datenanalyse, KI-gestützte Prozessoptimierung und Telemedizin-Workflows. Betrieb einer eigenen On-Premise-LLM-Infrastruktur auf heterogenem Multi-GPU-Verbund: zwei produktive RAG-Systeme mit rund 42.000 embeddeten Chunks (COBOL-Legacy-Korpus und Dokumenten-/Mail-Wissensbasis), 130.000+ geroutete Requests und 463 Mio. verarbeitete Input-Token in 14 Tagen. Fundierte Kenntnisse in Python/FastAPI, PostgreSQL mit pgvector, Hybrid-Retrieval und Reranking, GPU-Lastmanagement sowie Dokumenten-KI (OCR/Vision-LLM).

## Kernbereiche
- Automotive- & Manufacturing Operations: Serienanlauf, globale Werke, Ausschussreduzierung, Lieferantenentwicklung, Relocations, Cost-Down
- Healthcare Operations & Automation: klinische Dokumentations-Workflows, strukturierte Aufnahme/Frageboegen, Evaluation/Reporting, Telemedizin-Workflows
- AI / Data / Workflow Engineering: RAG + Vector DBs, LLM-Workflows, Python+SQL Pipelines, lokale LLMs (Ollama/LM Studio), n8n

## Skills
- os: Windows (bis 11) (gut), Linux (gut)
- office: MS Excel (sehr gut), MS Project (sehr gut), MS PowerPoint (gut), MS Word (gut)
- cad: OnShape (gut), AutoCAD 3D (gut), CATIA V5 (Basis)
- pdm: Sherpa (Basis), Matrix One (Basis)
- mrp: SAP (Basis)
- pm_tools: MS Project (sehr gut), DotProject (Basis), eGroup (gut), eRoom (gut), BugZilla (gut)
- databases: MySQL (Basis), PostgreSQL mit pgvector (sehr gut), Postgres (sehr gut), Alembic / Schema-Migrationen (gut), Access (Basis), Lotus 1-2-3 (Basis)
- programming: Python (sehr gut), C# (Basis), Visual Basic (Basis), VB.NET (Basis), Pascal (Basis), C (Basis)
- ai_automation: N8N (gut), Ollama & LM Studio (lokale KI) (gut), Claude Code / Codex (gut), GPT-OS:20B / Qwen etc. (gut), Lokale Telefonagenten / Local Phone Agents (gut)
- llm_infrastructure: LLM-Serving (llama.cpp, vLLM, ollama, TEI) (sehr gut), Multi-GPU-Betrieb & GPU-Lastmanagement (sehr gut), RAG & Hybrid Retrieval (Vektor + BM25, RRF) (sehr gut), Embeddings & Cross-Encoder-Reranking (bge-m3, Cohere) (sehr gut), Azure OpenAI / EU-gehostete Cloud-Modelle (gut), Azure Document Intelligence (gut), Quantisierung & Modellauswahl (Qwen MoE, Gemma, MedGemma) (gut), OCR & Vision-LLM (PaddleOCR, DeepSeek-OCR, Qwen-VL) (sehr gut), LLM-Evaluation & Benchmarking (Ground-Truth-Harness) (gut)
- backend: FastAPI (async, SSE, WebSockets) (sehr gut), SQLAlchemy async / asyncpg (gut), React + TypeScript (SPA, Live-Monitoring) (gut), Docker / Docker Compose (sehr gut), Caddy Reverse Proxy & Security-Hardening (gut), GitHub Actions CI / Container Registry (gut), Kubernetes (Deployment-Manifeste) (Basis)

## Erfahrung
- 2010-01–heute: The Implementers GmbH — Berater / Geschäftsführer
- 2009-07–2010-06: Johnson Controls — Program Manager Transfer Insolvente Lieferanten
- 2007-12–2009-06: Johnson Controls — Program Manager Hyundai/Kia
- 2006-09–2007-11: Johnson Controls — Leiter Technik und Produktion
- 2006-01–2007-11: Johnson Controls — Bereichsleiter
- 2005-08–2005-12: Johnson Controls — Leiter Taskforce Ausschuss und Effizienz
- 2003-09–2005-08: Johnson Controls — Technischer Leiter & Launch-Management
- 2001-05–2003-08: Johnson Controls — Black Belt / Program Management Office
- 2000-04–2001-05: Johnson Controls — Projekt Engineer Electronics
- 1998-02–2000-04: Johnson Controls — Test-Engineer / Testkoordinator
- 1997-02–1998-02: Johnson Controls — Prüfmittelverantwortlicher / Werkstudent im Bereich Versuch
- 1997-01–1998-01: UB Dr. Hans Schiffer — Backoffice Assistant – Unternehmensberatung

## Projekte
- Mobile Recorder App + KI-Bearbeitungs-Pipeline 2025-09–heute: Mobile Recorder Web-App (https://the-implementers.de/Recorder/) mit themenbasierter KI-Pipeline: Sprache zu strukturiertem Text zu automatischem Routing in OpenEMR/Notes/Projekt-DB. Vielseitig: Briefe, Anamnesen, Teammeetings, Aufmasse, Uebergaben.
- Ollama-Stallwatch — Hang-Detection & REST-API für lokale LLM-Inferenz 2026-04–heute: Public GitHub-Projekt (MIT) zur Erkennung von Ghost-Hangs in Ollama-LLM-Inferenz. 4 Collector-Services, SQLite-Backend, REST-API, Dashboard. Real-Impact: OCR-Pipeline 97,8% Erfolgsquote (vs 75-80% naiv), Hang-Recovery 140x schneller. https://github.com/tiubde-michael/ollama-stallwatch
- GPU-Lastmanagement für heterogenen LLM-Verbund 2026-06–heute: Zentrale Routing-Engine für 4 heterogene GPU-Knoten und 8+ Modell-Endpoints. Fähigkeitsbasiertes Routing, Mandanten-Prioritäten, Preemption. 130.000+ geroutete Requests in 14 Tagen, ausfallfreie Migration per Shadow-Mode.
- OpenAI-kompatibles API-Gateway mit externer Kunden-Anbindung 2026-06–heute: OpenAI-kompatibles /v1-Gateway (Chat/Embeddings/Rerank) mit Token-Scopes und Live-Rate-Limits, angebunden an ein externes Kunden-K8s. 338.000 Requests und 463 Mio. Input-Token in 14 Tagen.
- Inbetriebnahme & Tuning NVIDIA GB10 (ARM64) als LLM-Server 2026-07–heute: NVIDIA GB10 (ARM64) als LLM-Server produktiv gesetzt: vLLM-Instabilität diagnostiziert, Umbau auf llama.cpp mit Kontext-Split. ~193 tok/s bei 0 Fehlern, 429-Backpressure-Strategie.
- RAG-Wissensplattform für COBOL-Altsysteme — Lead Architektur (Mittelständischer Softwarehersteller (über Generalunternehmer, AT)) 2026-04–heute: Lead Architektur einer On-Premise-RAG-Wissensplattform für eine COBOL-Codebasis mit mehreren Mio. LOC. 17.279 Chunks mit Dual-Embeddings, 3.697 Graph-Kanten, Hybrid-Retrieval per RRF über 5 Pfade mit Zitatzwang. Recall@10 von 61 % auf über 83 % gesteigert; Modell-Benchmark über 7 Kandidaten als Hardware-Entscheidungsgrundlage.
- E-Mail-Automation und -Archiv mit RAG-Assistent 2026-03–heute: IMAP-Automation mit Regel-Engine, Volltext-Archiv und Anhang-Routing in die OCR-Strecke. Zweites RAG-System mit 24.500+ embeddeten Chunks in pgvector für einen internen Chat-Assistenten.
- TI-Flows Stack — Custom Workflow-Automatisierungsplattform 2026-01–heute: TI-Flows Stack: Self-Hosted Workflow-Automatisierung als n8n-Ersatz. 20+ Workflows, 30 Frontend-Seiten, 7-Schichten-Security, LLM-Pipeline, Depot-Analyse. ~24.000 LOC Python/React.
- Invoice API — Medizinisches Abrechnungssystem 2025-12–2026-02: Abrechnungssystem für medizinische Leistungserbringer mit ZUGFeRD-konformer Rechnungserzeugung und OpenEMR-Integration.
- Intelligente Dokumentenerkennung & automatisierte Bankabstimmung 2025-08–heute: On-Prem OCR-Pipeline als Azure-Ersatz: 10.871 Seiten, 97,8% Erfolg, Extraktion 33%→86% vs Azure. 5-Layer Multi-LLM-Stack (PaddleOCR, qwen-vl, qwen3.5, mistral-nemo). Inkl. Bank-Matching und DATEV-Export.
- HRV-Analyse-Pipeline — Automatisierte Herzratenvariabilitäts-Auswertung (Praxis für Schmerztherapie & TCM, Baden-Baden) 2026-01–2026-02: Automatisierte HRV-Analyse aus Langzeit-EKG: R-Peak-Detektion, Artefaktkorrektur, PNS/SNS-Trends, 3-seitiger PDF-Report. Docker.
- Schmerztherapie-Dokumentationssystem (schmerz_dok) 2026-02–heute: Klinisches Dokumentationssystem: OPS-Tracking, Ampelsystem, Bettenbelegung, Audit-Trail. FastAPI + React + PostgreSQL.
- VIVO PainCare — KI-gestützte klinische Schmerzbewertung und Aufnahmebegründung (Praxis für Schmerztherapie & TCM, Baden-Baden) 2025-09–2026-03: Klinisches Entscheidungsunterstützungssystem: automatische Auswertung von Schmerzfragebögen mit 20-Faktor-Ampelbewertung und KI-gestützter Aufnahmebegründung.
- Klinische Dokumentation — KI-gestützte Transkriptions- und Dokumentationspipeline 2025-08–2026-02: KI-Pipeline zur automatisierten medizinischen Dokumentation aus Arzt-Patienten-Gesprächen. Self-Hosted LLM, Speaker Diarization, OpenEMR-Integration.
- Lieferantenentwicklung Fahrwerksteile (KTM) 2023-05–2024-11: Lieferantenentwicklung Fließpressteile mit Dreh-/Fräsbearbeitung inkl. Änderungen, Neuanläufen und Reklamationsmanagement.
- Verlagerung von 150 Fahrwerksteilen (KTM) 2022-07–2024-01: Verlagerung von 150 Fahrwerksteilen in laufender Serie wg. kurzfristiger Standortschließung.
- Prozessaufnahme und Prozessoptimierung (Von Roll Schweiz AG) 2018-06–2018-11: Prozessoptimierung im internen Vertrieb eines Schweizer Maschinenbauunternehmens.
- Back Office Support und Prozessoptimierung (Praxis für Schmerztherapie & TCM, Baden-Baden) 2018-05–2025-05: Laufende Unterstützung einer Privatpraxis: Narkoseprotokolle, Dokumentenmanagement, Telemedizin-Workflows.
- Existenzgründungsberatung und Coaching (Praxis für Schmerztherapie & TCM, Baden-Baden) 2017-05–2018-04: Existenzgründungsberatung und Coaching einer Privatpraxis für Schmerztherapie & TCM.
- Interim Werksleitung (MAO Automotive GmbH & Co) 2018-02–2018-06: Interim Werksleitung und Stabilisierung eines ungarischen Produktionswerkes bis zur Übergabe.
- Lieferantenentwicklung DAG BR238 Türverkleidung (Megatech Industries Deutschland GmbH) 2016-07–2017-10: Lieferantenentwicklung DAG BR238 Türverkleidung inkl. Musterungen, PPAP/EMPB und Serienanlauf.
- Interim COO & Werksleiter (PWG Profilrollen-Werkzeugbau GmbH) 2015-09–2016-05: Interim COO & Werksleiter bei Aluminium verarbeitendem KFZ-Zulieferer. Ausbau Standort Slowakei.
- Kostenreduzierung Dachhimmelproduktion (Motus Headliner GmbH) 2015-01–2015-08: Kostenreduzierung (Prozess, Material, Lohn, Lieferanten) in der Dachhimmelproduktion.
- Programm Management Türinnenverkleidung DAG C292 (Toyota Boshoku America) 2012-09–2015-01: Programm Management Türinnenverkleidung DAG C292 inkl. Industrialisierung in den USA.
- KFZ Sonnenblenden Entwicklung (MARTUR FOMPAK) 2012-01–2014-12: Beratung des Projektteams in der Türkei zur Sonnenblenden-Entwicklung und Erstmusterung.
- Kostenreduzierung DAG C218 Türverkleidung (Toyota Boshoku Europe NV) 2012-03–2012-08: Kostenreduzierung bei Türinnenverkleidung DAG C218.
- Werkzeugverlagerung Spritzgusswerkzeuge (Toyota Boshoku Europe NV) 2012-01–2012-08: Werkzeugverlagerung Spritzgusswerkzeuge zu neuen Lieferanten in laufender Serie.
- Programm Management BMW Sonnenblenden (Magna) 2010-07–2011-12: Programm Management BMW Sonnenblenden — Neuentwicklung und Produktionsverlagerung.

## Ausbildung
- 2001-09–2003-11: MBA International Management, UEL University of East London / ELBS London (63)
- 1995-03–1998-05: Dipl.-Ing. (FH) Maschinenbau, Studienrichtung: Konstruktionstechnik, Rheinische Fachhochschule Köln (1,3)
- 1992-10–1995-01: Kfz-Mechaniker (Gesellenbrief) Kfz-Mechanik, Bonner Autohaus GmbH (Vertragswerkstatt der Daimler-Benz AG)
- 1988-06–1991-06: Abitur Schwerpunkt Mathematik und Physik, Ernst-Moritz-Arndt-Gymnasium der Stadt Bonn (3,2)

## Zertifikate
- Agentic AI with LangChain and LangGraph — Coursera (IBM Skills Network) (2026-04)
- Introduction to Deep Learning & Neural Networks with Keras (IBM) — IBM / Coursera (2026-01)
- Vector Databases for RAG — IBM / Coursera (2025-10)
- Build Intelligent Agents using DeepSeek & N8N — Board Infinity / Coursera (2025-07)
- MySQL for Data Engineering — Duke University / Coursera (2025-05)
- Python for Everybody (Specialization, 5 Kurse) — University of Michigan / Coursera (2025-04)
- Google AI Essentials (Specialization, 5 Kurse) — Google / Coursera (2026-01)
- Google Prompting Essentials (Specialization, 4 Kurse) — Google / Coursera (2025-12)
- Introduction to AI (Google) — Google / Coursera (2025-12)
- Introduction to OpenAI Codex — Scrimba / Coursera (2026-01)
- Generative AI-Powered Solutions for Modern Healthcare (Specialization, 9 Kurse) — Coursera (2025-11)
- Toyota Boshoku Business Practices (TBBP) - Solving Problems The TB Way — Toyota Boshoku (2025-10)
- Wertstrom-Engineering (4 Tage) — Fraunhofer IAO, Stuttgart (2012-10)
- DFMEA und PFMEA (5 Tage) — Gabor Kulsar / Magna Steyr (2013-11)
- Vertiefungsworkshop QM nach DIN EN ISO 9001:2008 — KMU-Berater Bundesverband / Gemeinschaft zertifizierter Unternehmensberater (2013-02)
- SixSigma Zertifizierter Black Belt — Johnson Controls (2001-01)
- EOQ Quality Systems Manager — EOQ / DGQ (1996-01)
- DGQ-Qualitätsmanager — DGQ Bonn (1995-10)
- Qualitätstechnik II — DGQ Bonn (1996-04)
- DGQ-Auditor / Lead Auditor (DIN EN ISO 10011-2) — DGQ Bonn (1996-05)
- Internal Auditor of Quality Systems — DGQ (1996-05)
- Medizinproduktegesetz, EG-Richtlinien, CE-Kennzeichnung — MUS Fortbildungsseminar, Köln (1996-10)
- EOQ Quality Auditor — EOQ / DGQ (1996-06)
- VDA6.1 und QS9000 Anforderungen — Technische Akademie Wuppertal (TAW) (1997-05)
- Interne Audits VDA6.1, QS9000, BOS — GFQ Akademie GmbH (firmeninternes Seminar bei Johnson Controls) (1998-01)
- Prüfmittelstudien — Johnson Controls (on-the-job) (1998-01)
- REFA-Grundschein / REFA-Sachbearbeiter — REFA-Verband Köln (1996-09)
- Arbeitssystemgestaltung — REFA-Verband (1996-11)
- Zertifizierter Program Manager (PMU / JCI) — Johnson Controls (2002-07)
- Zertifizierter KMU-Fachberater Sanierung — KMU-Akademie e.V., Hamm (2010-03)
- Das Unternehmen mit wichtigen Kennzahlen steuern — RKW Rationalisierungs-Kuratorium der Deutschen Wirtschaft e.V., Bayern Büro Nürnberg (1996-10)
- Mit Strategie zu mehr Erfolg (EKS-Erfolgsstrategie) — KMU-Akademie e.V. / Cord Tepelmann, UnternehmerCoach (2010-04)
- Umweltsimulation von Schwingungs- und Stoßbelastungen (Shakerkursus) — Technische Akademie Esslingen (TAE) (1999-01)
- Training in Testmethoden und Verfahren — Prince Automotive / Johnson Controls (on-the-job) (1998-08)
- CANoe Praxis-Workshop (1 Tag) — Vector Informatik GmbH, Stuttgart (2000-09)
- English in Management and International Business — — (2001-02)
- Interne Trainings Projektingenieure Sitze — Johnson Controls (2000-01)
- TPG Infotag Microsoft Project — TPG The Project Group (2012-10)
- DVS-Lehrgänge Gasschweißen (G-Schw) und MAG-Dünnblechschweißen (MAG-St D) — DVS / Handwerkszentrum Bonn (1993-04)
- Datenschutz 2012 — Luther Rechtsanwaltsgesellschaft mbH (2012-09)
- 2x 3 Tage Teambuilding — — (1996-01)
- Rhetorik und Kommunikation (Diplom) — Institut für Rhetorik und Kommunikation, Bornheim bei Bonn (1996-11)
- DSGVO Live-Webinar — eRecht24 (2018-07)
- Siemens NX Viewer / 3D Tool V12 — The Implementers GmbH (on-the-job) (2017-11)

## Publications
- Diplomarbeit (Rheinische FH Koeln, 1998): Versuchsstand ECE-R17 Kopfstuetzenpruefung. (/docs/00-DIP-Inhalt.pdf)
- MBA-Thesis (UEL/ELBS London, 2003): Successful Implementation of Kaizen. (/docs/Kaizen%20MR%20_Final.pdf)

## Diploma thesis PDF files
- /docs/00-DIP-Inhalt.pdf
- /docs/01-DIP-Einleitung.pdf
- /docs/02-DIP-Grundlagen.pdf
- /docs/03-Dip-Entwurf-eines-Pendels.pdf
- /docs/04-Dip-Entwurf-einer-linearen.pdf
- /docs/05-Dip-Bestaetigung-der-Theorie.pdf
- /docs/06-DIP-Ermittlung-der-Ko.pdf
- /docs/07-Dip-Bewertung-der-beiden-Loes.pdf
- /docs/08-DIP-Konstruktion-der-Posi.pdf
- /docs/09-DIP-Steuerung.pdf
- /docs/10-DIP-Bau-und-Inbetriebnahme.pdf
- /docs/11-DIP-Ist%20kosten.pdf
- /docs/12-DIP-Literaturn.pdf
- /docs/13-DIP-Erklaerung.pdf
- /docs/147-DIP-An_CFC%20600.pdf
- /docs/148-DIP-An_Der-Lineare-Pruefstand.pdf


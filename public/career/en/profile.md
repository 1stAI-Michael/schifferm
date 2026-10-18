# Dipl.-Ing. Michael Schiffer MBA

> Process optimizer & Program Manager with 20+ years in automotive industry, production launches and global plant structures. Since 2024 increasingly focused on Generative AI, Healthcare Automation, data analysis, AI-driven process optimization and telemedicine workflows.
>
> Operates a self-hosted on-premise LLM infrastructure on a heterogeneous multi-GPU cluster: two production RAG systems with around 42,000 embedded chunks (COBOL legacy corpus and a document/mail knowledge base), 130,000+ routed requests and 463M processed input tokens in 14 days.
>
> Solid expertise in Python/FastAPI, PostgreSQL with pgvector, hybrid retrieval and reranking, GPU load management and document AI (OCR/vision LLM).

- **Location:** Kostomloty, Poland
- **E-Mail:** schiffer@1stAI.eu
- **Phone:** +49 172 25 6 42 48
- **Website:** https://www.schifferm.de
- **LinkedIn:** https://www.linkedin.com/in/michael-schiffer

## Languages
- German: native
- English: fluent
- French: basic
- Spanish: basic
- Polish: basic

## Work Experience
### 1stAI — Founder
*2026-06 – present* | Kostomloty, Polen (remote, EU-weit)

Own consulting and engineering business for AI implementation, based in Poland, working remotely across the EU. Architecture, implementation and production operation from a single source.

Focus areas: retrieval architectures (RAG) on proprietary data, running language models in the company's own data centre rather than in the cloud, agent and tool integration, and connecting existing systems through OpenAI-compatible interfaces.

Operates a self-hosted on-premise LLM infrastructure on a heterogeneous multi-GPU cluster as development and reference environment; technical articles on the company blog.

### The Implementers GmbH — Principal Consultant / Managing Director
*2010-01 – present* | Germany

Consulting and interim management in the automotive industry, healthcare and other sectors. Focus areas: program management, production launches, plant management, supplier development, cost reduction, process optimization, AI implementation and AI-driven process automation.

**Projects:**
- **Mobile Recorder App + AI Editing Pipeline** (2025-09 – present): Mobile recording tool for structured audio capture with downstream AI pipeline. Public web app (https://the-implementers.de/Recorder/) for recording letters, medical histories, team meetings, notes, ideas, site surveys, and handovers — directly in the browser, no installation required. Context pre-selection (patient ID/name, topic category, recipient) drives downstream pipeline routing. Audio upload via HTTPS, then processed in dedicated pipeline UI (FastAPI, ti-nas-06:8011): WhisperX transcription with speaker diarization, topic-specific LLM processing (letter, EHR entry, examination report, memo, etc.), manual correction in web UI with diff view, quality gates against LLM hallucination. Result routing by topic category: medical documents into OpenEMR patient records (auto-upload), business notes into Flow-Notes DB, measurements into project database. Fully self-hosted, audio stays in own network. Stack: Vanilla JS frontend, MediaRecorder API, FastAPI, WhisperX, Ollama (qwen3.5/gpt-oss), PostgreSQL, OpenEMR API, Caddy with IP whitelist.
- **Ollama-Stallwatch — Hang Detection & REST API for Local LLM Inference** (2026-04 – present): Public MIT-licensed monitoring and diagnostic tool for locally hosted Ollama LLM inference on multi-GPU servers. Addresses the hard-to-detect production ghost-hang pattern: model loaded in VRAM, GPU at 0% utilization, ollama-serve CPU-bound in image preprocessing or vision encoder — invisible in logs, only live in nvtop. Four-component stack: GPU logger (nvidia-smi delta-logged), log parser (Docker log into SQLite), process logger (/proc with heartbeat), stall detector with gdb/proc stack capture without container modification via NOPASSWD sudoers. Hang detection in three parallel confidence levels (strict/loose/ghost) with different trigger conditions, complemented by orthogonal mode classification (A/B) distinguishing recoverable from silent hangs. Read-only REST API (port 3002, Python stdlib) with combinable filters (since/at/overlapping, confidence/mode/client_ip) for cross-host correlation. Web dashboard (Chart.js, live from SQLite) with stall bands over time series. Idempotent installer with host detection and portable config.toml. Real production impact: parallel OCR pipeline over 24 hours recorded 10,871 PDF pages, 4,837 inference calls, 97 hang events — pipeline success rate 97.8% instead of ~75-80% with naive wall-clock timeout. Selfheal strategy based on stall data reduced hang recovery time from ~40 minutes to ~17 seconds (factor ~140x). Stack: Python 3.12 stdlib-only (no pip dependencies), SQLite with WAL, Chart.js via CDN, systemd service management, gdb and nvidia-smi as external tools. ~1,700 lines of Python, 3 iterative development days with AI-pair programming. Repo: https://github.com/tiubde-michael/ollama-stallwatch
- **GPU Load Management for a Heterogeneous LLM Cluster** (2026-06 – present): In-house development of a central routing engine for a heterogeneous GPU cluster: 4 GPU nodes (RTX 3090, Tesla V100, RTX 3060, NVIDIA GB10 with 128 GB unified memory) and 8+ model endpoints (chat, embeddings, reranker). Capability-based candidate selection (endpoint × model × context window × slots) instead of static pools; named tenants (clinic, chat, batch, guest) with priorities, quotas and preemption of low-priority load. Zero-downtime migration in production: shadow mode (old vs. new decision logged and reviewed per request) followed by a staged cutover; overnight burn-in across 23,600 requests with ~0.1 % anomalies. Auto-discovery of endpoint capacities (llama.cpp /metrics, ollama, HuggingFace TEI), React live monitoring UI and full reservation audit trail. Production volume: 130,000+ routed requests in 14 days. After a power outage, a model server came up without its GPU and kept computing on the CPU for 40 minutes — 72 instead of 950 tokens/s prompt processing, visible only in a single log line; since then, GPU allocation per process is checked after every restart. Stack: Python, FastAPI, PostgreSQL, React/TypeScript, llama.cpp, ollama, TEI, Docker.
- **OpenAI-Compatible API Gateway with External Customer Integration** (2026-06 – present): Custom /v1 gateway (chat with SSE streaming, embeddings, rerank) in front of the GPU cluster; integration of an external customer-side Kubernetes cluster via scoped token auth. Per-token limits (concurrent requests, requests/min, tokens/min) configurable live from the database; model allowlist and context guards against silent truncation. Production load over 14 days: 338,000 chat requests, 463M input and 76M output tokens, peak 5,746 requests/h at ~1 % error rate. Audit-based traffic and fair-use analyses (token, volume and bandwidth projections) as a decision basis for hosting contracts. Stack: Python, FastAPI, SSE, PostgreSQL, JWT/token scopes, Caddy, Docker.
- **Commissioning & Tuning of an NVIDIA GB10 (ARM64) LLM Server** (2026-07 – present): Commissioning of an ASUS Ascent GX10 (NVIDIA GB10, ARM64, unified memory) as a production LLM server. Diagnosed reproducible vLLM instability on the GB10/ARM64 platform and migrated to two parallel llama.cpp instances with a context split on a single chip (4×256k for long context, 8×48k for standard load). Chat, embedding and reranker services running concurrently on the same node. Own measurement series on prefill and generation throughput and saturation behaviour (bandwidth-bound at 273 GB/s). 429-based backpressure strategy: cluster throughput ~193 tok/s with 0 errors across a 30-minute measurement window. Findings transferred into hardware sizing and procurement recommendations for customer projects.
- **RAG Knowledge Platform for Legacy COBOL Systems — Lead Architect (Mittelständischer Softwarehersteller (über Generalunternehmer))** (2026-04 – 2026-10): Strategic lead architect and sparring/review partner for a two-person senior developer team building an on-premise knowledge platform that makes a COBOL codebase grown over decades (several million LOC, Visual COBOL, fixed format) searchable and answerable. Fully on-premise operation, as the source code is the customer's core asset. Five-stage architecture: deterministic inventory via parser rather than LLM (PROGRAM-ID, COPY, CALL and EXEC SQL relations, file descriptors, data structures), graph extraction across call, copy, data and job relations, LLM-based enrichment, a quality loop, and retrieval with mandatory citation (every answer references program and line number; no generated answer without a solid hit). Corpus: 528 COBOL program identifiers, 17,279 chunks with dual embeddings (bge-m3 on-prem + Azure text-embedding-3-large), 3,697 CALL/COPY dependency edges as a graph. Hybrid retrieval via reciprocal rank fusion across 5 paths (code, multi-level documentation, sections, GraphRAG) plus knowledge cards and cross-encoder reranking (local or Cohere Rerank); embedding backend switchable per request between on-prem GPU and Azure/EU. Domain dictionary/synonym layer with query expansion bridging in-house terminology and identifiers in the code. Quality assurance: 430 ground-truth queries as an eval harness, 12 category-specific search profiles, multipass LLM deep analysis per program with a fallback model chain; recall@10 raised from around 61 % in the prototype to over 83 % in the production state. Local operation of quantised open-weights models (MoE ~35B / ~3B active, q4) with a hybrid fallback to an EU-hosted cloud model for non-confidential portions. Model benchmark across seven candidates and a hardware recommendation in three expansion stages with two procurement paths as a documented decision basis. Gap analysis of the initial source code delivery with a concrete follow-up delivery recommendation to the end customer. Packaging and operations: multi-stage Docker, Alembic migrations, separate dev/prod instances with a hardened migration path, K8s manifests, GitHub Actions into a private container registry; deployed both on-prem and in the customer's Kubernetes. Access via REST API, MCP server for developer tooling and a web chat for non-engineering roles. IP and licence review before delivery (dependency scan, copyleft detection, attribution evidence). 100 % remote, workshops via video.
- **E-Mail Automation and Archive with RAG Assistant** (2026-03 – present): IMAP fetcher with three-phase UID reconciliation (deduplication before header and body fetch), a rule engine on sender and subject patterns, and robust error handling for unstable provider IMAP servers. Full-text archiving in PostgreSQL, automatic attachment routing into the OCR pipeline (incoming invoices) and Nextcloud synchronisation. On top of it, a second RAG system over documents, mail and notes: 24,500+ embedded OCR chunks in pgvector as the knowledge base for an internal chat assistant. Stack: Python, FastAPI, PostgreSQL/pgvector, IMAP, Nextcloud, Docker.
- **Agent Studio — Multi-Agent Software Development with Claude Code** (2026-04 – present): Since April 2026, around two dozen Claude Code sessions have been working in parallel in this environment on software, infrastructure and documentation — each in its own workspace, with its own identity and permissions. Every building block of the operating model answers a measured failure that had previously gone unnoticed: with agents, silence looks like success.

Coordination: a ticket is exactly one responsibility. Work for other agents becomes a sub-ticket with its own owner; who has to act next is a dedicated field, separate from the owner, and dependencies are recorded as a block on the ticket rather than in free text. Priorities A/B/C and due dates set the order; deferring is only allowed with a reason, and the server rejects it otherwise. When two agents reach for the same ticket at once, the first one wins through a conditional claim in a single database statement — previously, measurably, the last one won. Reviews run as a sub-ticket to exactly one reviewing session, partly to Codex as an independent second instance.

Operations: shifts made of a pass and a watcher — the watcher only wakes on a reply to one's own blocks or a new assignment; seven earlier watcher variants were consolidated into one. Playbooks and rules come versioned from a Git repository, credentials exclusively via a broker that resolves the entry server-side and rejects ambiguity instead of guessing.
- **Agent Studio Overview — Control Station for Parallel Claude Code and Codex Sessions** (2026-08 – present): Anyone running many coding agents at once loses sight of them — every session is a terminal on a different machine. The control station makes around fifty Claude Code and Codex CLI sessions visible in nine windows, builds the layout with one click and measures the workplace instead of configuring it: three workplaces with different monitors, recognised by port and model.

Prompts to many sessions at once are only delivered after measured readiness. On an ordinary working day, 9 of 29 input fields held an unsent draft; delivery then waits instead of overwriting it. Automated command sequences wait for a confirmation whose baseline is tied to an event rather than a waiting period — a fixed grace period had demonstrably swallowed the fast answer. Agent questions are detected from two sources, the screen and the server, in a fixed order of precedence: for 12 of 18 waiting sessions the server had no knowledge of it. Ended sessions restart in place with a keystroke and continue the conversation.

The program replaces 13 shell scripts with 2,300 lines: around 6,400 lines of Python without external dependencies, 20 tables, 249 tests — each one checks a failure that has already happened once. Monitoring load cut from 200 % to 4 % CPU, system load from 23.4 to 6.3.
- **Modernisation of an Excel VBA Planning Application with Claude Code — Migration to CSV, SQLite and HTML (Endkunde über Generalunternehmer)** (2026-05 – 2026-05): Starting point: an 18-month project plan lived in an Excel workbook with around a dozen VBA macros. Bars were drawing objects over date columns, predecessor arrows were redrawn by macro. With around 130 work packages the interface froze for seconds on every change; conflict copies on the shared drive broke the VBA references, and each recovery took around 20 minutes.

Analysis with Claude Code: the problem was not the spreadsheet, but that the same file carried both data and rendering. That defined the cut — three CSV files as the single source of truth, an SQLite database generated from them, a static HTML page as the deliverable, every step callable on its own. Start dates are either anchored or computed from predecessor, lag and type; all four predecessor types were already needed in the existing plan. Codex reviewed the implementation as an independent second instance.

Two silent failures of the legacy system are eliminated by construction rather than by rule: the reduced customer view and the internal view were two files that drifted apart — at the last comparison, eight rows were missing from the customer view. Now it is one file with two levels of detail. And progress was an overlay on the bar that stayed in its old place when rows were sorted — the bar showed 30 %, the overlay 70 %. Now both share the same row. Core rebuild around 12 hours, followed by two weeks of refinement with an editor interface and a consistency report; data maintenance remains a spreadsheet.
- **Agentic Coding with Local Open-Weight Models — Claude Code On-Premise** (2026-09 – present): Claude Code additionally runs against locally hosted Qwen models on llama.cpp, connected through a translator between the Anthropic and OpenAI interfaces. The first real session failed on every tool call with "failed to parse grammar". The cause was not size, number of tools or history, but a single number in one tool schema: a nested length limit of 2,000 or more exceeds the fixed repetition limit of the grammar parser — 1,999 works, 2,000 returns HTTP 400, measured exactly. A second, entirely different cause then appeared with the same error message: regex escapes in nested patterns. The translator defuses both and logs every change; proven in production with 40 tools and around 87,000 tokens.

Model choice by measurement rather than data sheet: eight programming tasks, three agent harnesses, three repetitions each, every one with a hidden check. Each check had to fail on the unchanged project and pass on a correct solution — otherwise you measure the check, not the model. The dense Qwen3.8-27B solved 72 of 72 runs, the faster mixture-of-experts model Qwen3.6-35B-A3B 64 of 72, and its failures were reasoning errors, not typos. For batch work the MoE model stays in place (181 vs 32 tokens/s with eight parallel requests); routing is by task. With Qwen3.8, Claude Code solves the same tasks as a harness built for open models, and faster.

Thinking levels measured on real work — maintenance documentation for a 4,000-line COBOL program, two machines, two inference engines: the "low" level is as good as "medium" and 10 % faster, both deliver around two and a half times the coverage of "no thinking". The model's default "xhigh" produced 0 of 20 usable answers. An adopted temperature recommendation could not be confirmed by a counter-measurement.
- **TI-Flows Stack — Custom Workflow Automation Platform** (2026-01 – present): Complete replacement of n8n workflow engine with a custom Python/React platform for medical data processing, server security and portfolio management. Async backend (FastAPI + SQLAlchemy + asyncpg), React/TypeScript SPA with 30 pages, 20+ workflows with cron scheduling and execution chaining, 11 background tasks. Workflow engine with dynamic handler import, WebSocket live logs and chained execution. 7-layer security concept: IP whitelist/blacklist (Caddy), brute-force monitor with auto-blacklisting, Telegram-controlled IP whitelisting via inline keyboard, JWT auth, device tokens, rate limiting. 5-stage medical transcript pipeline (WhisperX dictation to medical record) with LLM quality gates. Depot module: Playwright-based comdirect scraper, 7-factor stock ranking, AI news summarization (Ollama). Central Ollama queue with semaphore-based GPU serialization. Shared library (flowlib) for 3 services. ~24,000 LOC (12,800 Python + 8,000 TypeScript + 1,600 flowlib + 2,000 SQL), 21 DB migrations. Stack: Python 3.10, FastAPI, SQLAlchemy async, React 18, TypeScript, Vite, PostgreSQL (pgvector), Docker Compose, Caddy, Ollama, Telegram Bot API, Playwright.
- **Invoice API — Medical Billing System** (2025-12 – 2026-02): Complete billing system for a medical practice with multi-tenant support (physician, IT services, pharmacy). Draft/Finalized/Cancelled workflow with database-driven state machine (PL/pgSQL triggers) — finalized invoices are immutable (audit-proof). ZUGFeRD/EN16931-compliant invoice generation (PDF with embedded CII-XML). OpenEMR integration: patient data, diagnoses, treatments. Tax logic: medical exemption, reverse charge, intra-community supplies. Server-side rendering with Jinja2 + HTMX. Snapshot pattern for audit-proof invoices. ~4,200 LOC Python, ~1,700 LOC SQL, 30+ endpoints, 13 DB migrations. Stack: Python, FastAPI, SQLAlchemy (async), PostgreSQL, HTMX, Jinja2, Docker, Caddy.
- **Intelligent Document Recognition & Automated Bank Reconciliation** (2025-08 – present): Architecture and production operation of an on-premise OCR / document pipeline for German tax and accounting documents; replaces Azure Document Intelligence with measurably better extraction accuracy and full data sovereignty. Volume: 12,156 pages processed (as of 07/2026), 97.8% success rate; ongoing cloud cost reduced from $1,500/year to 0 EUR. Azure A/B benchmark (400 documents): invoice number 33%→86%, total amount 41%→88%, sender 58%→94%. Five-layer stack: PaddleOCR (baseline), qwen3-vl:4b (fast vision), mistral-nemo:12b (text fallback), qwen3.5:27b (high-quality structured extraction), qwen3.5:27b classification into 18 document types with tenant routing. Eight production resilience mechanisms: watchdog threads with wall-clock + GPU-idle + cross-host stall polling, custom degeneracy detection for pathological vision-model output, partial-text recovery, cold-load self-healing (12s cost vs 180s saved hang = 15x net gain), per-phase model unload with verification, cross-host monitoring with REST API and three confidence levels for hang types. Downstream layers: index-based bank matching (>3,000 transactions x >4,000 documents in ~7 seconds) and DATEV-EXTF-CSV export based on learned booking rules. Web UI (FastAPI) with 4-column comparison of extraction sources, DB-driven prompt versioning with fallback chains. Infrastructure: Docker Compose multi-container, PostgreSQL on NAS, GPU sharing (RTX 3090 Ti + RTX 5060 Ti) via Ollama. Stack: Python, FastAPI, PaddleOCR, Ollama (qwen3-vl, qwen3.5, mistral-nemo, deepseek-ocr, gemma3), PostgreSQL, Docker, scikit-learn, httpx streaming with watchdog-cancel. 2026 additions: LLM-based multi-page document splitting, ZUGFeRD/XRechnung reconciliation, document classification by client, document class and tax year, and pre-accounting for DATEV handover. The Azure Document Intelligence path previously run in parallel has been fully replaced by the in-house on-premise pipeline and is no longer in use. Per-page measurements on a Tesla V100: ~2.5 s OCR + ~5–6 s vision LLM extraction of pure compute time; deliberately small specialist models (5 GB + 3.5 GB) instead of one large generalist.
- **HRV Analysis Pipeline — Automated Heart Rate Variability Assessment (Praxis für Schmerztherapie & TCM, Baden-Baden)** (2026-01 – 2026-02): Modular pipeline for reproducible HRV analysis of 24-26h long-term ECG recordings in EDF format. Fully automated: EDF reading, R-peak detection, artifact correction, time/frequency domain metrics, PNS/SNS trends (Kubios-calibrated), ECG-derived respiration and TV-HRV Power Spectrum. Docker file watcher for batch operation. Replaces manual legacy Windows software. Stack: Python, NumPy, SciPy, Matplotlib, pyEDFlib, Docker.
- **Pain Therapy Documentation System (schmerz_dok)** (2026-02 – present): Hospital-grade documentation system for multimodal pain therapy. Supports interdisciplinary teams. OPS-based treatment tracking with 21-day timeline milestones. 4-color traffic light system for therapy progress. Bed occupancy calendar with Gantt visualization. Rich-text editor (TipTap) with versioning. 10-level role hierarchy with audit trail. Server-side PDF reports (WeasyPrint). Stack: Python 3.12, FastAPI, SQLAlchemy 2.0 (async), React 19, Tailwind CSS, PostgreSQL 16, Docker, Nginx, JWT.
- **VIVO PainCare — AI-powered Clinical Pain Assessment and Admission Justification (Praxis für Schmerztherapie & TCM, Baden-Baden)** (2025-09 – 2026-03): Clinical decision support system for inpatient pain therapy. Automated processing of VIVO PainCare pain questionnaires (PDF → Markdown → regex extraction → database) with 20-factor traffic-light scoring (red-yellow-green) across standardized pain scales (VAS, PDI, MPSS, DASS, FFbH, VR-12, NHP, HKF-R10, SBL). AI-generated therapy recommendations and objective justifications for hospital admission per cost-effectiveness mandate (medgemma:27b, self-hosted). Longitudinal analysis over 182-day course with automatic discharge letter text generation. Print-optimized A4 one-pager for patient records. 206 questionnaires processed, ~28,000 answers extracted, 117 patients in system. Stack: FastAPI, Ollama (medgemma:27b), PyMuPDF, React + TypeScript, PostgreSQL, Docker.
- **Clinical Documentation — AI-powered Transcription and Documentation Pipeline** (2025-08 – 2026-02): End-to-end system for automated medical documentation from physician-patient conversations. Recording after consent, upload via mobile app or USB dictation device, transcription with WhisperX (speaker diarization). Five-stage LLM pipeline (Ollama, self-hosted): automatic topic detection, patient identification, structured summary, medical record entry and examination report as templates for practice software (OpenEMR). Topic-based prompt routing with DB-driven versioning and A/B testing. Quality gates against repetitive LLM outputs. Review UI for physician approval with direct upload to OpenEMR. Fully self-hosted — no cloud LLM, no external transcription service. Stack: FastAPI, WhisperX, Ollama (qwen3.5/gpt-oss), PostgreSQL, React + TypeScript, Docker, Telegram Bot API, NFS, Caddy.
- **Supplier Management suspension parts (KTM)** (2023-05 – 2024-11): Supplier development for suspension parts (flow-pressed parts with turning and milling) incl. changes, new launches, relocations and bottleneck management.
- **Transfer of 150 serial production items (KTM)** (2022-07 – 2024-01): Leading transfer of 150 serial production items after supplier decided to close the plant.
- **Lean / Process consultation (Von Roll Schweiz AG)** (2018-06 – 2018-11): Lean / Process consultation Swiss manufacturer for electro components.
- **Acting Plant Manager (MAO Automotive GmbH & Co)** (2018-02 – 2018-06): Acting Plant Manager Interior Trim components in Hungary. Stabilization until handover to new plant manager. Focus on lamination processes incl. tooling optimization, headcount reduction, bottleneck management and backlog reduction.
- **Program Manager critical suppliers DAG BR238 Door Trim (Megatech Industries Deutschland GmbH)** (2016-07 – 2017-10): Program Manager critical suppliers DAG BR238 Door Trim. Leading the team for supplier qualification incl. sampling, PPAP/EMPB tracking, bottleneck management and process approvals.
- **Interim COO & acting Plant Manager (PWG Profilrollen-Werkzeugbau GmbH)** (2015-09 – 2016-05): Interim COO & acting Plant Manager in Aluminum profile processing automotive supplier for roof systems. Leading the plant in Germany and expanding the plant in Slovakia. Approx. 350 employees, approx. 80 Mio. EUR revenue.
- **Labor and Material efficiency program for Headliner production (Motus Headliner GmbH)** (2015-01 – 2015-08): Leading Labor and Material efficiency program for Headliner production (process, material, labor and supplier cost reduction).
- **Program Management interior door trim DAG C292 (Toyota Boshoku America)** (2012-09 – 2015-01): Leading the development program Novi MI of interior door trim DAG C292 including the Launch Phase on site in MS & AL.
- **Sun visor development consulting (MARTUR FOMPAK)** (2012-01 – 2014-12): Sun visor development consulting for young project team in Turkey: optimization, new orders, concepts, market analysis, design reviews and project reviews.
- **Cost down team DAG C218 door panels (Toyota Boshoku Europe NV)** (2012-03 – 2012-08): Leading the cost down team for DAG C218 door panels.
- **Transfer of IM tools to new suppliers (Toyota Boshoku Europe NV)** (2012-01 – 2012-08): Leading transfer of IM tools to new suppliers in running production incl. sampling, assembly trials, OEM presentation and PPAP/EMPB coordination.
- **Program Manager BMW sun visors L7 Platform (Magna)** (2010-07 – 2011-12): Program Manager for BMW sun visors L7 Platform with the transfer of the production location and completely new development of the F30 sun visor.

### Praxis für Schmerztherapie & TCM, Olga Schiffer MSc — Practice IT, Digitalisation and Back Office
*2017-05 – 2025-05* | Baden-Baden, Deutschland

Set up and maintained the IT of a private practice for naturopathy, TCM and pain therapy, in parallel with the role at The Implementers GmbH. Responsible for digitalising practice workflows, integrating medical devices, billing and document processes as well as website and back office.

**Projects:**
- **Back Office Support and Process Improvement (Praxis für Schmerztherapie & TCM, Baden-Baden)** (2018-05 – 2025-05): Ongoing support for a private practice for pain therapy and TCM. Developed an electronic anaesthesia record for outpatient anaesthesia with live data acquisition from GE and Mindray anaesthesia monitors including ECG data, plus GOÄ-compliant invoicing. Migrated practice operations to OpenEMR including a billing interface. Automated clinical back-office workflows and introduced OCR-based capture and pre-accounting of incoming invoices. Built and technically operated the practice website and specialist blog covering naturopathy, TCM, orthomolecular medicine as well as cannabis, ketamine and neurofeedback therapy. Performed 19-channel and 2-channel EEG recordings and produced qEEG analyses including normative database comparison. Built an end-to-end telemedicine workflow from the services of several providers — from GDPR consent through the digital treatment contract to billing. Document management, back office and practice administration.
- **Start-up consulting and coaching (Praxis für Schmerztherapie & TCM, Baden-Baden)** (2017-05 – 2018-04): Start-up consulting and coaching for a private pain therapy & TCM practice. Concept, business plan, financing, scheduling, construction and setup, standard operating procedures through post-calculation implementation.

### Johnson Controls — Program Manager Insolvent Suppliers
*2009-07 – 2010-06* | Germany / Spain

Leading a cross functional team for transfer and relocation of various tools and processes incl. painted parts. This includes supplier development in Valencia for the Ford C344 Launch.

### Johnson Controls — Program Manager
*2007-12 – 2009-06* | Bratislava, Slovakia (DE/CZ)

Leading a simultaneous development team based in Bratislava till the successful Launch for the Hyundai Kia in Slovakia, Czech Republic and Germany. With the responsibility for profit, timing, quality and customer satisfaction.

### Johnson Controls — Operations Manager (Crisis Management)
*2006-09 – 2007-11* | Madrid, Spain

Supporting a 408 people plant in crisis management with focus on production, technique, and launches and restructuring the supplier base with the focus on customer PPM, scrap and efficiency.

### Johnson Controls — Operations Manager
*2006-01 – 2007-11* | Espelkamp, Germany

450 people automotive process and assembly plant for seating components and sunshades. Leading Operations (incl. production, methods, industrialization, quality and outbound logistic) with 80 employees and 12mil€/ano turnover, for Sunshades and seat back-panels with the focus on safety, scrap and efficiency.

### Johnson Controls — Leader Taskforce "Red Adair"
*2005-08 – 2005-12* | Telford, UK

Leading a cross functional European team with the objective to stabilize a 250 people process and assembly plant before the closure with the focus on customer PPM, scrap and efficiency.

### Johnson Controls — Technical & Launch Manager
*2003-09 – 2005-08* | Schweighouse, France

Leading and restructuring the departments Methods, Industrialization, Maintenance and Launch with 50 people in a 500 people automotive headliner plant.

### Johnson Controls — Black Belt in Program Management Office
*2001-05 – 2003-08* | Burscheid, Germany

Black Belt projects with focus on optimization of product development process and program management. Implementation of management information systems, PM trainings, change process optimization and development resource planning.

### Johnson Controls — Project Engineer Electrical / Electronics
*2000-04 – 2001-05* | Burscheid, Germany

Support of VW complete seat team with focus on the seat controller and all electrical and electronic components and wires harness routing incl. trouble shooting. Evaluation and test drives with and without customer with focus on seat function and comfort.

### Johnson Controls — Test Engineer / Test Coordinator
*1998-02 – 2000-04* | Burscheid, Germany

Building up new department "Interior Testing" incl. design and procurement of test machines. Creating test plans for various European vehicle interior projects, budget planning, supervising vibration measurements, durability tests and legal homologation tests. Extension of seating test lab to a full interiors system test lab (incl. FMVSS 201 FMH).

### Johnson Controls — Student in Testing
*1997-02 – 1998-02* | Burscheid, Germany

Part time job: QM system support VDA6.1, QS9000, design of test fixtures, test execution and evaluation.

### UB Dr. Hans Schiffer — Backoffice Assistant – Management Consulting
*1997-01 – 1998-01* | Bonn, Germany

Prepare, format, and update presentations, proposals, and project documents. Assist with the preparation of reports, analyses, and workshop materials. Maintain and organize client and project data. Support invoicing, time tracking, and monthly reporting.

## Education
### UEL University of East London / ELBS London
*MBA Master of Business Administration — International Management* | 2001-09 – 2003-11
Grade: 63
Thesis: Successful Implementation of Kaizen.

### Rheinische Fachhochschule Köln
*Dipl.-Ing. Mechanical Engineering — Mechanical Engineering, specialization: Design Engineering* | 1995-03 – 1998-05
Grade: 1,3
Thesis: Design and realization of a Test Rig for Headrest energy absorption and acceleration curves according to ECE-R17.

### Bonner Autohaus GmbH (Vertragswerkstatt der Daimler-Benz AG)
*Car Mechanic (Journeyman Certificate) — Automotive Mechanics* | 1992-10 – 1995-01

### Ernst-Moritz-Arndt-Gymnasium der Stadt Bonn
*High School Diploma (Abitur) — Focus on Mathematics and Physics* | 1988-06 – 1991-06
Grade: 3,2

## Skills
- **Operating Systems:** Windows (bis 11) (proficient), Linux (proficient)
- **Office:** MS Excel (advanced), MS PowerPoint (proficient), MS Word (proficient)
- **CAD:** OnShape (proficient), AutoCAD 3D (proficient), CATIA V5 (basic)
- **PDM:** Sherpa (basic), Matrix One (basic)
- **ERP/MRP:** SAP (basic)
- **Project Management Tools:** MS Project (advanced), DotProject (basic), eGroup (proficient), eRoom (proficient), BugZilla (proficient)
- **Databases:** MySQL (basic), PostgreSQL mit pgvector (advanced), Alembic / Schema-Migrationen (proficient), Access (basic), Lotus 1-2-3 (basic)
- **Programming:** Python (proficient), C# (basic), Visual Basic (basic), VB.NET (basic), Pascal (basic), C (basic)
- **AI & Automation:** N8N (proficient), Ollama & LM Studio (lokale KI) (proficient), Claude Code / Codex (advanced), GPT-OS:20B / Qwen etc. (proficient), Lokale Telefonagenten / Local Phone Agents (proficient)
- **LLM Infrastructure:** LLM-Serving (llama.cpp, vLLM, ollama, TEI) (advanced), Multi-GPU-Betrieb & GPU-Lastmanagement (advanced), RAG & Hybrid Retrieval (Vektor + BM25, RRF) (advanced), Embeddings & Cross-Encoder-Reranking (bge-m3, Cohere) (advanced), Azure OpenAI / EU-gehostete Cloud-Modelle (proficient), Azure Document Intelligence (proficient), Quantisierung & Modellauswahl (Qwen MoE, Gemma, MedGemma) (proficient), OCR & Vision-LLM (PaddleOCR, DeepSeek-OCR, Qwen-VL) (advanced), LLM-Evaluation & Benchmarking (Ground-Truth-Harness) (proficient)
- **Backend & DevOps:** FastAPI (async, SSE, WebSockets) (advanced), SQLAlchemy async / asyncpg (proficient), React + TypeScript (SPA, Live-Monitoring) (proficient), Docker / Docker Compose (advanced), Caddy Reverse Proxy & Security-Hardening (proficient), GitHub Actions CI / Container Registry (proficient), Kubernetes (Deployment-Manifeste) (basic)
- **Medical Technology:** qEEG-Messung und -Auswertung (19-Kanal / 2-Kanal, Normdatenbank-Abgleich) (proficient), Neurofeedback-Systeme (Messung und Protokolle) (proficient), Narkosemonitor-Anbindung GE / Mindray inkl. EKG-Daten (proficient), OpenEMR (Praxis- und Klinikinformationssystem) (proficient)

## Certifications
### AI & Data
- **EU AI Act Explained: What You Need to Know About the New AI Regulation from August** — WBS.LEGAL (Prof. Christian Solmecke) (2026-08)
- **Agentic AI with LangChain and LangGraph** — Coursera (IBM Skills Network) (2026-04)
- **Introduction to Deep Learning & Neural Networks with Keras (IBM)** — IBM / Coursera (2026-01)
- **Google AI Essentials (Specialization, 5 courses)** — Google / Coursera (2026-01)
- **Introduction to OpenAI Codex** — Scrimba / Coursera (2026-01)
- **Google Prompting Essentials (Specialization, 4 courses)** — Google / Coursera (2025-12)
- **Introduction to AI (Google)** — Google / Coursera (2025-12)
- **Vector Databases for RAG** — IBM / Coursera (2025-10)
- **Build Intelligent Agents using DeepSeek & N8N** — Board Infinity / Coursera (2025-07)
- **MySQL for Data Engineering** — Duke University / Coursera (2025-05)
- **Python for Everybody (Specialization, 5 courses)** — University of Michigan / Coursera (2025-04)

### AI Healthcare
- **Generative AI-Powered Solutions for Modern Healthcare (Specialization, 9 courses)** — Coursera (2025-11)

### Quality
- **Toyota Boshoku Business Practices (TBBP) - Solving Problems The TB Way** — Toyota Boshoku (2025-10)
- **Design and Process FMEA (5 days)** — Gabor Kulsar / Magna Steyr (2013-11)
- **Advanced Workshop QM per DIN EN ISO 9001:2008** — KMU-Berater Bundesverband / Gemeinschaft zertifizierter Unternehmensberater (2013-02)
- **Value Stream Engineering (4 days)** — Fraunhofer IAO, Stuttgart (2012-10)
- **JCI SixSigma Certified Black Belt** — Johnson Controls (2001-01)
- **Training for internal Audits according to VDA6.1 and QS9000 and BOS** — GFQ Akademie GmbH (firmeninternes Seminar bei Johnson Controls) (1998-01)
- **Measurement device studies** — Johnson Controls (on-the-job) (1998-01)
- **VDA6.1 and QS9000 new demands to the Automotive Industry** — Technische Akademie Wuppertal (TAW) (1997-05)
- **Work System Design** — REFA-Verband (1996-11)
- **Medical Device Act, EU Directives, CE Marking** — MUS Fortbildungsseminar, Köln (1996-10)
- **REFA Basic Certificate** — REFA-Verband Köln (1996-09)
- **EOQ Quality Auditor** — EOQ / DGQ (1996-06)
- **DGQ-Auditor / Lead Auditor (DIN EN ISO 10011-2)** — DGQ Bonn (1996-05)
- **Internal Auditor of Quality Systems** — DGQ (1996-05)
- **Quality Techniques II** — DGQ Bonn (1996-04)
- **EOQ Quality Systems Manager** — EOQ / DGQ (1996-01)
- **DGQ-Quality Manager** — DGQ Bonn (1995-10)

### Other
- **GDPR Live Webinar** — eRecht24 (2018-07)
- **Siemens NX Viewer / 3D Tool V12** — The Implementers GmbH (on-the-job) (2017-11)
- **TPG Microsoft Project Info Day** — TPG The Project Group (2012-10)
- **Data Protection 2012** — Luther Rechtsanwaltsgesellschaft mbH (2012-09)
- **English in Management and International Business** — None (2001-02)
- **CANoe Hands-on Workshop (1 day)** — Vector Informatik GmbH, Stuttgart (2000-09)
- **Internal trainings for project engineers - seats** — Johnson Controls (2000-01)
- **Environmental Simulation of Vibration and Shock Loads (Shaker Course)** — Technische Akademie Esslingen (TAE) (1999-01)
- **Training in Test methods and procedures** — Prince Automotive / Johnson Controls (on-the-job) (1998-08)
- **Rhetoric and Communication (Diploma)** — Institut für Rhetorik und Kommunikation, Bornheim bei Bonn (1996-11)
- **2x 3 days courses for Teambuilding** — None (1996-01)
- **DVS Welding Courses: Gas Welding (G-Schw) and MAG Thin Sheet Welding (MAG-St D)** — DVS / Handwerkszentrum Bonn (1993-04)

### Management
- **Strategy for Success (EKS Success Strategy)** — KMU-Akademie e.V. / Cord Tepelmann, UnternehmerCoach (2010-04)
- **Certified SME Restructuring Consultant** — KMU-Akademie e.V., Hamm (2010-03)
- **Certified Program Manager (PMU / JCI)** — Johnson Controls (2002-07)
- **Managing the company with key performance indicators** — RKW Rationalisierungs-Kuratorium der Deutschen Wirtschaft e.V., Bayern Büro Nürnberg (1996-10)

## Awards
- Pallas Athene Medal for final exam and best of term (1998)
- Best of term for the education to a Car Mechanic (1995)

## Driving Licenses
- Class II + III (Passenger car and semi truck >7.5t)
- Forklift license
- Motorboat license for coast and river
- UKW-Radio license
- CEPT-Novice amateur radio license (class E)

## Memberships
- BDS: German Sport Shooters Association
- DARC: German Amateur Radio Club

## Interests
Mobile homes, Travelling, Cooking, Walking Bouviers, Ham radio, Sport shooter

---
Last updated: 2026-08-27 05:00:04
Source: https://schifferm.de

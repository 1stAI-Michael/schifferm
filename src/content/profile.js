export const profileContent = {
  site: {
    name: "Michael Schiffer",
    fullName: "Dipl.-Ing. Michael Schiffer, MBA",
    baseUrl: "https://schifferm.de",
    sameAs: ["https://the-implementers.de"],
  },
  person: {
    name: "Dipl.-Ing. Michael Schiffer, MBA",
    location: "Spremberg, Deutschland",
    email: "Schiffer@TIUB.de",
    mobile: "+49 172 25 6 42 48",
    languages: [
      { code: "de", label: "DE", level: "native" },
      { code: "en", label: "EN", level: "very good" },
      { code: "fr", label: "FR", level: "basic" },
      { code: "es", label: "ES", level: "basic" },
      { code: "pl", label: "PL", level: "basic" },
    ],
  },
  positioning: {
    de: {
      headline: "Prozessoptimierung • Program Management • Generative AI • Healthcare Automation",
      oneLiner:
        "Prozessoptimierer & Program Manager mit 20+ Jahren Automobilindustrie, Serienanläufen und globalen Werksstrukturen. Seit 2024 verstärkt fokussiert auf Generative AI, Healthcare Automation, Datenanalyse, KI-gestützte Prozessoptimierung und Telemedizin-Workflows. Betrieb einer eigenen On-Premise-LLM-Infrastruktur auf heterogenem Multi-GPU-Verbund: zwei produktive RAG-Systeme mit rund 42.000 embeddeten Chunks (COBOL-Legacy-Korpus und Dokumenten-/Mail-Wissensbasis), 130.000+ geroutete Requests und 463 Mio. verarbeitete Input-Token in 14 Tagen. Fundierte Kenntnisse in Python/FastAPI, PostgreSQL mit pgvector, Hybrid-Retrieval und Reranking, GPU-Lastmanagement sowie Dokumenten-KI (OCR/Vision-LLM).",
      keywords: [
        "Prozessoptimierung",
        "Program Management",
        "Serienanlauf",
        "Lieferantenentwicklung",
        "Generative AI",
        "Healthcare Automation",
        "RAG",
        "n8n",
        "Python",
        "SQL",
        "Telemedizin Workflows",
      ],
    },
    en: {
      headline: "Process Optimization • Program Management • Generative AI • Healthcare Automation",
      oneLiner:
        "Process optimizer & Program Manager with 20+ years in automotive industry, production launches and global plant structures. Since 2024 increasingly focused on Generative AI, Healthcare Automation, data analysis, AI-driven process optimization and telemedicine workflows. Operates a self-hosted on-premise LLM infrastructure on a heterogeneous multi-GPU cluster: two production RAG systems with around 42,000 embedded chunks (COBOL legacy corpus and a document/mail knowledge base), 130,000+ routed requests and 463M processed input tokens in 14 days. Solid expertise in Python/FastAPI, PostgreSQL with pgvector, hybrid retrieval and reranking, GPU load management and document AI (OCR/vision LLM).",
      keywords: [
        "process optimization",
        "program management",
        "launch management",
        "supplier development",
        "generative AI",
        "healthcare automation",
        "RAG",
        "n8n",
        "Python",
        "SQL",
        "telemedicine workflows",
      ],
    },
  },
  coreDomains: [
    {
      title: {
        de: "Automotive- & Manufacturing Operations",
        en: "Automotive & Manufacturing Operations",
      },
      focus: {
        de: [
          "Serienanlauf",
          "globale Werke",
          "Ausschussreduzierung",
          "Lieferantenentwicklung",
          "Relocations",
          "Cost-Down",
        ],
        en: [
          "serial launches",
          "global plants",
          "scrap reduction",
          "supplier development",
          "relocations",
          "cost-down",
        ],
      },
    },
    {
      title: {
        de: "Healthcare Operations & Automation",
        en: "Healthcare Operations & Automation",
      },
      focus: {
        de: [
          "klinische Dokumentations-Workflows",
          "strukturierte Aufnahme/Frageboegen",
          "Evaluation/Reporting",
          "Telemedizin-Workflows",
        ],
        en: [
          "clinical documentation workflows",
          "structured intake/questionnaires",
          "evaluation/reporting",
          "telemedicine workflows",
        ],
      },
    },
    {
      title: {
        de: "AI / Data / Workflow Engineering",
        en: "AI / Data / Workflow Engineering",
      },
      focus: {
        de: [
          "RAG + Vector DBs",
          "LLM-Workflows",
          "Python+SQL Pipelines",
          "lokale LLMs (Ollama/LM Studio)",
          "n8n",
        ],
        en: [
          "RAG + vector DBs",
          "LLM workflows",
          "Python+SQL pipelines",
          "local LLMs (Ollama/LM Studio)",
          "n8n",
        ],
      },
    },
  ],
  // Skills, experience, education, certifications, workTypes → now from career_data.json via careerData.js
  publications: {
    de: [
      {
        title: "Diplomarbeit (Rheinische FH Koeln, 1998): Versuchsstand ECE-R17 Kopfstuetzenpruefung.",
        file: "00-DIP-Inhalt.pdf",
      },
      {
        title: "MBA-Thesis (UEL/ELBS London, 2003): Successful Implementation of Kaizen.",
        file: "Kaizen MR _Final.pdf",
      },
    ],
    en: [
      {
        title: "Diploma thesis (Rheinische FH Cologne, 1998): Versuchsstand ECE-R17 Kopfstuetzenpruefung.",
        file: "00-DIP-Inhalt.pdf",
      },
      {
        title: "MBA thesis (UEL/ELBS London, 2003): Successful Implementation of Kaizen.",
        file: "Kaizen MR _Final.pdf",
      },
    ],
  },
  diplomaFiles: [
    "00-DIP-Inhalt.pdf",
    "01-DIP-Einleitung.pdf",
    "02-DIP-Grundlagen.pdf",
    "03-Dip-Entwurf-eines-Pendels.pdf",
    "04-Dip-Entwurf-einer-linearen.pdf",
    "05-Dip-Bestaetigung-der-Theorie.pdf",
    "06-DIP-Ermittlung-der-Ko.pdf",
    "07-Dip-Bewertung-der-beiden-Loes.pdf",
    "08-DIP-Konstruktion-der-Posi.pdf",
    "09-DIP-Steuerung.pdf",
    "10-DIP-Bau-und-Inbetriebnahme.pdf",
    "11-DIP-Ist kosten.pdf",
    "12-DIP-Literaturn.pdf",
    "13-DIP-Erklaerung.pdf",
    "147-DIP-An_CFC 600.pdf",
    "148-DIP-An_Der-Lineare-Pruefstand.pdf",
  ],
  machineReadable: {
    profileMdTitle: "Michael Schiffer Profile (Machine-Readable)",
  },
};

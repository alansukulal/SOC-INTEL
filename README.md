# 🔐 SOC-INTEL

## AI-Powered Agentic SOC Investigation Platform

**Python · Microsoft Sentinel · KQL · OpenAI · LLMs · Pydantic · Agentic AI · Security Automation**

SOC-INTEL is an AI-assisted Security Operations Center investigation platform designed to explore how Large Language Models and agentic workflows can support security analysts during incident investigation.

The platform integrates with **Microsoft Sentinel** to retrieve incidents, alerts, entities, and security telemetry while using an LLM to assist with investigation planning, query generation, evidence analysis, and iterative investigation.

> **AI assists the investigation, while security data access, query execution, sensitive entity handling, and final analyst decisions remain controlled.**

---

## 🚧 Project Status

**Active Development**

The current implementation includes a working Microsoft Sentinel investigation foundation with:

- Incident ingestion and normalization
- Alert processing
- Security entity extraction and deduplication
- Microsoft Sentinel authentication
- AI-generated investigation planning
- KQL generation and execution
- Evidence collection
- Privacy-aware LLM interaction
- Local entity binding
- Evidence-context sanitization
- Bounded investigation retries
- Investigation state and history tracking
- Human analyst oversight

---

# 🎯 Project Goal

SOC analysts frequently perform repetitive investigation activities:

- Understanding incidents and alerts
- Identifying users, hosts, IP addresses, and other entities
- Determining what evidence is required
- Writing KQL queries
- Executing queries against Microsoft Sentinel
- Reviewing returned telemetry
- Correlating evidence
- Determining whether further investigation is required
- Producing investigation findings

SOC-INTEL explores how these activities can be orchestrated through an AI-assisted workflow while retaining security boundaries around sensitive operations.

The goal is **not**:

```text
Incident → LLM → Answer
```

Instead, SOC-INTEL follows a controlled investigation lifecycle:

```text
Security Incident
        │
        ▼
Incident / Alert Ingestion
        │
        ▼
Normalization & Entity Extraction
        │
        ▼
Sanitized Investigation Context
        │
        ▼
AI Investigation Planner
        │
        ▼
Investigation Tasks
        │
        ▼
Local Entity Binding
        │
        ▼
KQL Generation
        │
        ▼
Controlled Sentinel Execution
        │
        ▼
Evidence Collection
        │
        ▼
Evidence Sanitization
        │
        ▼
AI Evaluation
        │
        ▼
More Evidence Required?
      ┌─┴─┐
     Yes  No
      │    │
      ▼    ▼
  Re-plan  Findings
      │
      └────► Bounded Investigation Loop
                 │
                 ▼
           Analyst Review
```

---

# 🧠 Core Capabilities

## 1. Microsoft Sentinel Integration

SOC-INTEL currently uses **Microsoft Sentinel** as its primary security platform.

The integration supports:

- Sentinel authentication
- Incident retrieval
- Alert retrieval
- Security entity extraction
- KQL execution
- Security telemetry retrieval
- Evidence collection

Sentinel access remains behind controlled application components rather than allowing the LLM unrestricted access to the security platform.

---

## 2. Structured Security Models

SOC-INTEL uses Python and **Pydantic** models to provide structured representations of investigation data.

Current model areas include:

- Incidents
- Alerts
- Entities
- Customer / security profiles
- Sentinel configuration
- Credentials
- Platform capabilities
- Investigation sessions
- Investigation tasks
- Evidence

Structured models provide predictable interfaces between ingestion, investigation, LLM, and SIEM components.

---

## 3. Security Data Normalization

SIEM data is normalized before entering the investigation engine.

```text
Microsoft Sentinel
        │
        ▼
Raw Incident / Alert Data
        │
        ▼
Normalization Layer
        │
        ▼
SOC-INTEL Models
        │
        ▼
Investigation Engine
```

This reduces coupling between SIEM-specific data structures and the core investigation workflow.

It also provides an architectural foundation for supporting additional security platforms in the future.

---

## 4. Entity Extraction & Deduplication

Security investigations frequently reference the same entities across multiple alerts.

SOC-INTEL extracts, normalizes, and deduplicates investigation entities such as:

- User accounts
- IP addresses
- Hosts
- Devices
- Accounts
- Other SIEM-provided entities

This produces a cleaner investigation context and prevents unnecessary repeated work against the same target.

---

# 🤖 AI Investigation Planning

The LLM acts as an investigation planning and reasoning component.

The planner receives an appropriate investigation context and determines what evidence should be collected.

```text
Sanitized Incident Context
          │
          ▼
      LLM Planner
          │
          ▼
Investigation Objectives
          │
          ▼
 Investigation Tasks
          │
          ▼
Required Evidence
```

The planner determines **what should be investigated**.

Actual security platform execution remains controlled by the local application.

---

# 🔐 Privacy-Aware LLM Architecture

Security investigations can contain sensitive information including:

- User identifiers
- IP addresses
- Hostnames
- Customer-specific values
- Incident metadata
- Security telemetry
- Internal infrastructure information

SOC-INTEL therefore introduces a privacy boundary between the security environment and the external LLM.

```text
REAL SECURITY DATA
        │
        ▼
LOCAL SOC-INTEL APPLICATION
        │
        ├── Real entity values
        ├── Credentials
        ├── Query execution
        ├── SIEM connectivity
        └── Security evidence
        │
        ▼
SANITIZATION / PRIVACY BOUNDARY
        │
        ▼
LLM-SAFE CONTEXT
        │
        ▼
EXTERNAL LLM
```

The objective is to provide enough information for useful AI reasoning without unnecessarily transmitting real security entity values.

---

# 🔗 Local Entity Binding

Privacy-aware planning creates an important separation between **reasoning** and **execution**.

The LLM can reason using sanitized investigation targets.

The application retains the actual value and binds it locally before query execution.

```text
LLM TASK
"Investigate TARGET_USER"
        │
        ▼
Local SOC-INTEL Runtime
        │
        ▼
Resolve TARGET_USER
        │
        ▼
Actual Entity Value
        │
        ▼
Bind into KQL
        │
        ▼
Microsoft Sentinel
```

This allows the LLM to participate in investigation planning without requiring every real security entity value.

---

# 📊 KQL Investigation

Investigation tasks can generate queries for Microsoft Sentinel.

The execution flow separates AI reasoning from actual SIEM access:

```text
Investigation Task
        │
        ▼
Investigation Context
        │
        ▼
KQL Generation
        │
        ▼
Local Target Binding
        │
        ▼
Controlled Query Execution
        │
        ▼
Microsoft Sentinel
        │
        ▼
Query Results
        │
        ▼
Evidence
```

SOC-INTEL owns the actual Sentinel connection and execution process.

---

# 🔍 Evidence Collection

The investigation engine converts returned security telemetry into investigation evidence.

```text
KQL Query
    │
    ▼
Sentinel Results
    │
    ▼
Evidence Object
    │
    ▼
Investigation State
    │
    ▼
Evidence Analysis
```

This allows investigation reasoning to stay grounded in retrieved security data.

---

# 🛡️ Evidence Privacy

The privacy boundary applies to returned evidence as well as the initial incident.

Raw Sentinel query results may contain sensitive information.

SOC-INTEL therefore supports an evidence-processing boundary:

```text
RAW SENTINEL EVIDENCE
        │
        ▼
LOCAL PROCESSING
        │
        ▼
SANITIZATION
        │
        ▼
LLM-SAFE EVIDENCE CONTEXT
        │
        ▼
AI ANALYSIS
```

Real values can remain available locally for subsequent investigation tasks while the model works with an appropriate sanitized representation.

---

# 🔄 Bounded Investigation Loop

A security investigation may require several queries before sufficient evidence is available.

SOC-INTEL supports iterative investigation:

```text
Plan
 │
 ▼
Investigate
 │
 ▼
Collect Evidence
 │
 ▼
Evaluate
 │
 ▼
Enough Evidence?
   │
   ├── YES ──► Complete
   │
   └── NO
        │
        ▼
      Re-plan
        │
        ▼
Next Investigation Attempt
```

Agentic investigation is deliberately **bounded**.

A task cannot continuously generate queries indefinitely.

Previous attempts are retained so subsequent planning can consider what was already tried.

---

# 🧠 Investigation State & History

SOC-INTEL maintains runtime investigation state.

State can include:

- Investigation objectives
- Current task
- Previous attempts
- Generated queries
- Retrieved evidence
- Investigation history
- Task status
- Investigation results

This enables history-aware replanning.

```text
Attempt 1
    │
    ▼
Evidence Insufficient
    │
    ▼
Record Attempt
    │
    ▼
Attempt 2
    │
    ▼
Previous Context Available
    │
    ▼
Alternative Investigation
```

The system therefore avoids blindly repeating the same unsuccessful investigation.

---

# 👤 Human Analyst Oversight

SOC-INTEL is an analyst-assistance system rather than an autonomous remediation engine.

Responsibilities are deliberately separated:

### 🤖 AI

- Interpret sanitized investigation context
- Plan investigations
- Generate investigation tasks
- Assist with query generation
- Analyze sanitized evidence
- Recommend findings

### ⚙️ Application

- Protect credentials
- Resolve actual entities
- Control security tools
- Execute SIEM queries
- Retrieve evidence
- Enforce execution boundaries
- Maintain investigation state

### 👤 Security Analyst

- Review evidence
- Validate conclusions
- Make security decisions
- Determine appropriate remediation
- Approve downstream actions

> **The analyst remains responsible for final security judgment.**

---

# 🏗️ System Architecture

```text
                       SECURITY ANALYST
                              │
                              ▼
                         SOC-INTEL
                              │
                              ▼
                      INCIDENT INGESTION
                              │
                  ┌───────────┴───────────┐
                  │                       │
               ALERTS                  ENTITIES
                  │                       │
                  └───────────┬───────────┘
                              │
                              ▼
                        NORMALIZATION
                              │
                              ▼
                    INVESTIGATION STATE
                              │
                              ▼
                       PRIVACY BOUNDARY
                              │
                              ▼
                     SANITIZED CONTEXT
                              │
                              ▼
                        LLM PLANNER
                              │
                              ▼
                    INVESTIGATION TASK
                              │
                              ▼
                    LOCAL ENTITY BINDING
                              │
                              ▼
                       KQL GENERATION
                              │
                              ▼
                    SENTINEL QUERY TOOL
                              │
                              ▼
                     MICROSOFT SENTINEL
                              │
                              ▼
                      SECURITY EVIDENCE
                              │
                              ▼
                    EVIDENCE SANITIZATION
                              │
                              ▼
                       AI EVALUATION
                              │
                     ┌────────┴────────┐
                     │                 │
               More Evidence       Complete
                     │                 │
                     ▼                 ▼
                  Re-plan         Final Findings
                     │                 │
                     ▼                 ▼
                Bounded Loop        ANALYST
```

---

# 🧰 Technology Stack

| Category | Technology |
|---|---|
| Programming | Python |
| Data Models | Pydantic |
| SIEM | Microsoft Sentinel |
| Query Language | KQL |
| AI / LLM | OpenAI |
| Authentication | Azure Identity / Application Credentials |
| Orchestration | Custom Python Agentic Workflow |
| Security Telemetry | Microsoft Sentinel / Log Analytics |
| Configuration | Environment Variables |
| Source Control | Git / GitHub |

> SOC-INTEL uses its own Python orchestration architecture rather than depending on LangChain or LangGraph for the core investigation workflow.

---

# 📁 Project Structure

```text
SOC-INTEL/
│
├── data/
│   └── samples/
│       └── incident_001.json
│
├── src/
│   └── soc_intel/
│       │
│       ├── auth/
│       │   └── environment.py
│       │
│       ├── config/
│       │
│       ├── ingestion/
│       │   ├── loader.py
│       │   └── normalizers/
│       │
│       ├── investigation/
│       │
│       ├── llm/
│       │   └── providers/
│       │
│       ├── models/
│       │   ├── capabilities.py
│       │   ├── credentials.py
│       │   ├── customer.py
│       │   ├── enums.py
│       │   ├── evidence.py
│       │   ├── incident.py
│       │   ├── investigation.py
│       │   └── sentinel.py
│       │
│       ├── tools/
│       │   └── siem/
│       │
│       └── main.py
│
├── tests/
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Local Development

## Prerequisites

- Python
- Git
- Microsoft Sentinel workspace access
- Appropriate Azure application permissions
- OpenAI API credentials

## Clone

```bash
git clone https://github.com/alansukulal/SOC-INTEL.git
cd SOC-INTEL
```

## Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv socpro
```

Activate:

```powershell
.\socpro\Scripts\Activate.ps1
```

## Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔑 Environment Configuration

Real credentials should never be committed to Git.

Create a local `.env` using `.env.example` as a reference.

Example:

```env
SOC_INTEL_SENTINEL_TENANT_ID=
SOC_INTEL_SENTINEL_SUBSCRIPTION_ID=
SOC_INTEL_SENTINEL_WORKSPACE_ID=

SOC_INTEL_DEV_CLIENT_ID=
SOC_INTEL_DEV_CLIENT_SECRET=

SOC_INTEL_OPENAI_API_KEY=
```

```text
.env           ❌ NEVER COMMIT
.env.example   ✅ SAFE PLACEHOLDERS ONLY
```

---

# 🔐 Security Considerations

SOC-INTEL interacts with security telemetry and external AI services, making data exposure an important architectural concern.

Current design principles include:

- Secrets loaded from environment variables
- Credentials excluded from source control
- Controlled SIEM access
- Local entity resolution
- Privacy-aware LLM context
- Evidence sanitization
- Bounded investigation attempts
- Structured input and state validation
- Separation between AI reasoning and security execution
- Human analyst oversight

Public development and testing data should remain synthetic.

---

# 🧪 Testing

Important test areas include:

- Incident JSON validation
- Alert normalization
- Entity normalization
- Entity deduplication
- Azure authentication
- Sentinel incident retrieval
- Sentinel alert retrieval
- Entity extraction
- KQL execution
- AI investigation planning
- Local entity binding
- Evidence collection
- Evidence sanitization
- Investigation retries
- Investigation history
- Investigation-state preservation
- End-to-end AI-assisted investigation

---

# 🗺️ Development Roadmap

## ✅ Foundation

- Python project structure
- Pydantic security models
- Incident ingestion
- Alert models
- Entity models
- Sentinel configuration
- Investigation models
- Evidence models

## ✅ Sentinel Investigation Foundation

- Sentinel authentication
- Incident retrieval
- Alert retrieval
- Entity extraction
- Entity normalization
- Entity deduplication
- KQL execution
- Evidence retrieval

## ✅ AI Investigation Foundation

- OpenAI integration
- Investigation planning
- AI-generated investigation tasks
- Query generation
- Local entity binding
- Evidence-aware reasoning
- Investigation history
- Bounded investigation retries

## ✅ Privacy Architecture

- Sanitized incident context
- Local retention of actual entity values
- LLM-safe investigation context
- Evidence-context sanitization
- Separation between reasoning and execution

## 🚧 Current Development

- Improve investigation planning
- Expand evidence evaluation
- Strengthen validation and failure handling
- Increase test coverage
- Improve investigation summaries
- Improve analyst-facing output
- Add better observability

## 🔭 Future Direction

Potential future capabilities include:

- Additional SIEM adapters
- EDR integrations
- Threat intelligence enrichment
- IOC reputation analysis
- MITRE ATT&CK mapping
- Security knowledge retrieval
- Attack timeline generation
- Cross-source evidence correlation
- Analyst feedback loops
- Web-based analyst interface
- Investigation-quality evaluation
- Additional human approval controls

> Future items are architectural directions and are not presented as currently implemented capabilities.

---

# 🧭 Design Philosophy

SOC-INTEL is not simply a demonstration of using an LLM to generate KQL.

The broader engineering problem is:

> **How can probabilistic AI reasoning be safely combined with deterministic security tools, sensitive security data, evidence, investigation state, and human judgment?**

SOC-INTEL therefore focuses on six principles:

### 🔐 Privacy

Sensitive security information should remain local wherever practical.

### 🛡️ Control

LLM reasoning should not provide unrestricted access to security tooling.

### 🔍 Evidence

Investigation conclusions should be supported by retrieved security telemetry.

### 🔄 Bounded Autonomy

Agentic investigation should operate within defined execution limits.

### 🔌 Extensibility

Security-platform-specific logic should remain separate from core investigation orchestration wherever possible.

### 👤 Human Oversight

Final security decisions belong to the analyst.

---
### Areas of Focus

**Microsoft Sentinel · KQL · SOC Operations · Python · LLMs · Agentic AI · Security Automation · AI Security Engineering**

---

# 📌 Project Status

🚧 **Active Development**

The current implementation establishes the core Microsoft Sentinel and AI-assisted investigation workflow.

SOC-INTEL will continue evolving through incremental engineering, testing, and security-focused improvements.

---

# 🔐 SOC-INTEL

### From Security Incident to Evidence-Driven AI-Assisted Investigation

> **AI investigates. Tools execute. Evidence supports. Analysts decide.**

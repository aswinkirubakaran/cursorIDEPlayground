# Use Case: AI-Powered Monitoring Assistant and System Check Agent

## Goal
Transform system health checks and triage in Blue Yonder Dispatcher WMS by deploying a chat-based AI agent that enables instant, expert-level diagnostics for any issues (e.g., pack bench freezing, system slowness, order volume drop) to user (operator), manager, or IT—eliminating technical barriers, cutting delays, and reducing dependence on manual expertise.

---

## Current Workflow (As-Is)

- When users encounter performance issues (e.g., slowness, order drops, pack bench freezes), they:
  - Report the issue to IT through tickets, calls, or emails.
  - Wait for an IT engineer to become available, often outside normal hours.
- IT engineers must:
  - Manually check monitoring dashboards (e.g., Dynatrace), review system logs, query databases, and dig into product diagnostics.
  - Collaborate with other teams if the issue lies outside the product (infra, DB, network).
  - Resolve the issue if possible, or determine it as a false alarm.
  - Communicate updates back to the user or management, often after several handoffs.
- **Challenges:**
  - Slow and inconsistent incident triage.
  - Heavy reliance on domain knowledge and manual effort.
  - High risk of misdirection or missed context, especially with false alarms.
  - Non-technical users always depend on IT for insights.

---

## Future Workflow (To-Be, with AI Agent)

- Any user reports a problem directly to a chat-based AI agent, using simple, business language.
- The AI agent:
  - Instantly interprets and classifies the issue based on user description.
  - Queries relevant monitoring systems, logs, and databases in real time.
  - Correlates current telemetry data with historical incidents for rapid context-building.
  - Provides immediate, actionable insights—root cause, next steps, and recommended solutions.
  - Clearly states if escalation is needed and routes it to the appropriate team with a rich context summary.
  - Notifies all stakeholders (user, IT, management) with status updates and outcomes.
- **Resulting Experience:**
  - Anyone, regardless of technical background, can get fast, accurate diagnostics and guidance.
  - IT engineers can focus on complex problems instead of repetitive checks.
  - Management gains visibility and control without waiting for IT translation.

---

## Key Value Hypothesis

- **Speed:**
  - Triage and resolution times are reduced by 10×, with instant response for known issues.
- **Effort:**
  - Manual analysis and troubleshooting drop by 90% for engineers.
- **Quality & Performance:**
  - Consistent, AI-driven recommendations leverage both current data and past incident resolution paths.
  - Much lower risk of misdiagnosis or escalation delays—false positives/alarms are filtered out with up to 80% accuracy.
- **Experience:**
  - Accessible, transparent, and empowering for all business and operations staff.
  - IT resources are freed up for strategic work, and every incident is documented and auditable.

---

## Early Proposed Tech Stack

- Inferencing Groq’s Gemma Model (LLM model)
- Tech Stack: Python: Core agent orchestration and integrations.
- Further to be added.

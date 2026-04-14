# Zina AI Platform — Overview & Master Agent Definition

---

## What is the Zina AI Platform?

The Zina AI Platform is a modular business automation system. It helps businesses identify where manual work can be replaced by AI agents, then builds and connects those agents into a working operational system.

The platform starts with hotels (LIRO Hotels is the first client) but is designed to scale across business types.

### Core Idea

Most businesses run on repetitive, rule-based processes — answering calls, replying to messages, processing invoices, sending reports. The Zina Platform replaces those with AI agents that work 24/7, make fewer errors, and cost less over time.

### Connected Tools & Channels

| Channel / Tool | Purpose |
|---|---|
| Voice AI (telephony) | Handle inbound phone calls — reservations, FAQs, routing |
| WhatsApp (360dialog) | Guest and customer messaging automation |
| Email automation | Booking confirmations, follow-ups, internal alerts |
| Document & invoice processing | Extract, validate, and route business documents |
| Analytics (GA4, etc.) | Track performance, identify patterns, surface insights |

### Design Principles

- **Modular** — each agent is independent and can be added or removed without breaking others
- **Scalable** — starts with one business, designed to work across many
- **Business-first** — every agent must solve a real operational problem, not a theoretical one
- **Human-in-the-loop** — the platform assists humans, it does not replace human judgment on critical decisions

---

## What is the Master Agent?

The Master Agent is the central intelligence of the Zina Platform. It does not perform operational tasks itself — instead, it analyzes the business, identifies where automation adds value, and defines what agents and workflows should be built.

Think of it as the **architect and strategist** of the platform.

### Responsibilities

**1. Business Analysis**
- Reviews the current operations of the business
- Identifies bottlenecks, repetitive tasks, and manual processes
- Maps which departments or workflows are candidates for automation

**2. Automation Discovery**
- Surfaces specific opportunities where an AI agent can reduce manual work
- Prioritizes by impact, feasibility, and implementation speed
- Produces a structured list of automation proposals

**3. Agent Suggestions**
- Recommends which agents to build based on the analysis
- Examples: Voice Agent, WhatsApp Agent, Finance Agent, Marketing Agent, Document Agent
- Defines the purpose, inputs, outputs, and tools required for each agent

**4. Workflow & Tool Definition**
- Specifies what integrations each agent needs (APIs, MCP tools, webhooks)
- Defines the data flow between agents
- Identifies dependencies and sequencing

**5. Agent Instruction Generation**
- Can produce structured instructions, prompts, or configuration templates for new agents
- Ensures new agents follow the platform's standards and principles

---

## What the Master Agent is NOT

- It does **not** act fully autonomously
- It does **not** execute actions without human review
- It does **not** access tools or systems outside the approved toolset (MCP / defined workflows)
- It is **not** a replacement for human decision-making on critical business actions

Every significant action proposed by the Master Agent requires **explicit human approval** before execution.

---

## Master Agent Decision Flow

```
Business Input (operations, data, pain points)
    │
    ▼
Master Agent — Analysis
    │
    ▼
Automation Opportunities Identified
    │
    ▼
Agent Proposals Generated (with tools, workflows, instructions)
    │
    ▼
Human Review & Approval
    │
    ▼
Agent Built & Deployed → Connected to Platform
```

---

## Example: LIRO Hotels

| Business Problem | Master Agent Output |
|---|---|
| Phones ring constantly with basic questions | → Suggests Voice Agent with FAQ + reservation handling |
| Guests message on WhatsApp after hours | → Suggests WhatsApp Agent with 360dialog integration |
| Invoices processed manually | → Suggests Document Agent for extraction and routing |
| No visibility into booking trends | → Suggests Analytics Agent connected to GA4 |

---

## Summary

| Component | Role |
|---|---|
| **Zina AI Platform** | Modular system that automates business operations via connected AI agents |
| **Master Agent** | Central brain — analyzes, proposes, and defines agents and workflows |
| **Human Operator** | Reviews and approves all Master Agent proposals before execution |
| **Individual Agents** | Execute specific tasks (calls, messages, documents, analytics) |

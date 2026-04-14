# Voice AI Telephony Provider — Decision Document
**Project:** LIRO Hotels Voice AI System
**Date:** 2026-03-30
**Author:** AI Systems Architect

---

## 1. What a Telephony Provider Does

A telephony provider bridges the public phone network (PSTN) and your software. When a guest calls, the provider:

1. Receives the call on a virtual phone number
2. Streams the audio to your application (via WebSocket or webhook)
3. Sends your synthesized response back as audio
4. Handles call routing, recording, and DTMF (keypad input)

In a Voice AI system, the provider is the entry point — it is not the brain. Your STT, LLM, and TTS handle intelligence. The provider handles connectivity.

---

## 2. Comparison Table

| Criteria | Twilio | Vapi | Sipgate |
|---|---|---|---|
| **Ease of setup** | Medium — requires assembling components | Very easy — opinionated, batteries-included | Hard — SIP-focused, developer-unfriendly for AI |
| **Cost** | Pay-per-use, predictable, can get expensive at scale | Higher per-minute cost, but fewer moving parts | Cheapest base cost, but hidden integration cost |
| **AI integration** | DIY — flexible but manual | Native — built for AI voice agents | None native — full DIY via SIP |
| **Flexibility** | High — full control over pipeline | Low-Medium — constrained to Vapi's model | High — SIP is universal, but complex |
| **Speed to MVP** | Medium — 1–3 days to wire up properly | Fast — hours to a working demo | Slow — days to weeks for AI integration |
| **Scalability** | Excellent — enterprise-grade | Good — cloud-managed, but vendor lock-in | Good infrastructure, poor AI tooling at scale |

---

## 3. Detailed Analysis

---

### Twilio

**Strengths**
- Industry standard with massive documentation and community
- WebSocket streaming (Media Streams API) integrates cleanly with custom STT pipelines like faster-whisper
- Full control over every step: STT, LLM, TTS, routing logic
- Programmable voice, SMS, and SIP in one platform
- Reliable 99.95%+ uptime SLA
- Supports BYOC (Bring Your Own Carrier) for cost optimization later

**Weaknesses**
- No AI orchestration layer — you build it yourself
- Latency management (turn-taking, interruption handling) is your responsibility
- Costs stack up: per-minute + per-message + phone number fees
- More moving parts means more failure points during development

**Best use case**
Teams with backend engineering capacity who want full ownership of the AI pipeline and need long-term flexibility.

**When NOT to use it**
If you have no developer bandwidth or need a working demo in under 24 hours.

---

### Vapi

**Strengths**
- Purpose-built for AI voice agents — fastest path to a working call bot
- Handles WebSocket streaming, turn detection, interruption, and barge-in out of the box
- Supports custom LLMs, custom STT (can point to your own faster-whisper endpoint), and custom TTS
- Dashboard with call logs, transcripts, and analytics
- Simple REST API and good documentation
- Phone number provisioning included

**Weaknesses**
- Higher per-minute cost (~$0.05–0.10/min on top of model costs)
- Vendor lock-in: your pipeline runs through Vapi's infrastructure
- Less control over low-level audio handling
- Custom STT integration (e.g., self-hosted faster-whisper) requires exposing your STT as an HTTP endpoint — adds latency hop
- Relatively new company — long-term reliability not yet proven at enterprise scale

**Best use case**
Fast MVP with minimal engineering overhead. Ideal when time-to-demo matters more than cost optimization.

**When NOT to use it**
When you need sub-300ms end-to-end latency, or when regulatory/data residency requirements prohibit sending audio through a third-party intermediary.

---

### Sipgate

**Strengths**
- Solid European SIP/VoIP infrastructure, strong in DACH region
- Very low call termination costs
- GDPR-compliant by default (EU-based)
- Good for traditional PBX-style routing

**Weaknesses**
- No AI-native features whatsoever
- SIP integration requires a SIP server (e.g., FreeSWITCH, Asterisk) to bridge to your AI pipeline — significant operational complexity
- Poor English documentation
- Not designed for real-time WebSocket audio streaming to AI pipelines
- Slow support cycle for developer use cases

**Best use case**
Traditional business telephony, call forwarding, or as a carrier layer under a more capable platform.

**When NOT to use it**
For any AI voice agent use case. Sipgate is a carrier, not an AI platform. Using it as your primary AI telephony layer would require building the entire bridge layer yourself, negating its cost advantage.

---

## 4. Final Recommendation

### Best Provider for MVP: **Vapi**

Vapi wins at MVP stage because:

- You can have a working call flow in hours, not days
- It handles the hardest problems in voice AI (barge-in, turn detection, low-latency streaming) out of the box
- Your existing MCP knowledge system and Telegram escalation can be wired in via Vapi's function-calling hooks
- You avoid building WebSocket audio infrastructure from scratch
- The cost delta over Twilio is acceptable at low call volume (early hotel deployment)

The tradeoff is vendor dependency and slightly less control over your STT pipeline. For a hotel at MVP stage, this is acceptable.

---

### Best Provider Long-term: **Twilio**

Once call volume grows and the pipeline is proven, migrate to Twilio because:

- Cost per minute drops significantly at volume (negotiated rates, BYOC)
- Full pipeline ownership means you can optimize every latency bottleneck
- Your local faster-whisper STT integrates directly via Media Streams WebSocket — no external hop
- No dependency on Vapi's pricing or uptime
- Twilio's infrastructure is battle-tested at enterprise hotel chains

The migration path is clean: Vapi lets you prototype the conversation logic; Twilio lets you own it in production.

**Do not build on Sipgate.** It is a carrier, not a platform. It would require building everything Vapi gives you for free, without the AI tooling to show for it.

---

## 5. Suggested Setup

### MVP Flow (Vapi)

```
Guest Call
    │
    ▼
Vapi (phone number, call handling, WebSocket stream)
    │
    ├─► STT: faster-whisper (self-hosted, exposed as HTTP endpoint)
    │         └─► Transcript
    │
    ├─► LLM: Claude / GPT-4o (via Vapi assistant config)
    │         └─► Uses MCP knowledge base for hotel FAQs, reservations
    │         └─► Function calls: check availability, create booking, escalate
    │
    ├─► Escalation: Telegram bot (triggered via function call when confidence low)
    │
    └─► TTS: ElevenLabs / Azure (configured in Vapi)
              └─► Audio response streamed back to caller
```

**Key integration points:**
- Vapi calls your faster-whisper endpoint via `transcriber.url` (custom STT)
- MCP knowledge system is called by the LLM during tool use
- Telegram escalation fires when the LLM invokes an `escalate_to_human` function
- Call recordings and transcripts stored via Vapi webhook to your backend

---

### Production Flow (Twilio, post-MVP)

```
Guest Call
    │
    ▼
Twilio (phone number, Media Streams WebSocket)
    │
    ▼
Your WebSocket Server (Node.js / Python)
    │
    ├─► faster-whisper (local, direct — no HTTP hop)
    │         └─► Transcript
    │
    ├─► LLM (Claude via Anthropic API)
    │         └─► MCP knowledge base
    │         └─► Tool calls: reservations, routing, escalation
    │
    ├─► Telegram escalation
    │
    └─► TTS → PCM audio → Twilio Media Stream → Caller
```

**Advantage over Vapi in production:**
- STT runs locally with no external API hop — lower latency
- Full control over silence detection, barge-in, and turn-taking logic
- Cost: ~$0.013/min (Twilio) vs ~$0.05–0.10/min (Vapi) at scale

---

## Summary

| Decision | Choice | Reason |
|---|---|---|
| **Start with** | Vapi | Fastest path to working hotel call flow |
| **Scale with** | Twilio | Cost efficiency + full pipeline ownership |
| **Avoid** | Sipgate | Wrong tool for AI voice use case |

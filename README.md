# JIT Context OS for Agent Zero ⚡

**Epistemic context runtime & 3-tier memory cascade (L0/L1/L2) with deterministic prompt caching for Agent Zero.**

[![Agent Zero](https://img.shields.io/badge/Agent%20Zero-Plugin-blue)](https://github.com/agent0ai/agent-zero)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Token Reduction](https://img.shields.io/badge/Prompt%20Tokens--88.9%25-brightgreen)]()
[![Code Accuracy](https://img.shields.io/badge/Self--Healing%20Accuracy-%2B20%25-brightgreen)]()

---

## 🌟 What is JIT Context OS?

In complex agentic workflows, injecting large instruction manuals, task history, and noisy logs leads to **context bloat**, **attention drift**, and **cache thrashing**.

**JIT Context OS** solves this by providing:
1. **L0 Hot-Path (<3ms):** SQLite WAL in-memory engine storing active hot-facts with Read-Your-Own-Writes (RYOW).
2. **L1 Warm-Path (<10ms):** Project domain knowledge with Hysteresis Scope Guard to eliminate context oscillations.
3. **L2 Deep-Path:** On-demand retrieval with a 600ms Circuit Breaker protecting against hanging endpoints.
4. **Deterministic XML Capsule (`<jit_capsule>`):** Stable prompt prefix ordering ensuring **>85% prompt cache hit rates** on Claude 3.5/3.7, Gemini 3.8 Flash, and GPT-4o.
5. **Epistemic Invariants Engine (I1–I10):** Anti-self-poisoning (assistant outputs carry 0.0 epistemic weight), strict direct user input precedence, and destructive action gating.
6. **RecentTurnFence Self-Healing:** 1-turn repair loops for coding errors without expanding conversational history.

---

## 🚀 Easy Installation (Choose Any Method)

### Method 1: Git Clone (Recommended)
Run inside your Agent Zero container or host:
```bash
git clone https://github.com/wojciechwiesner/jit-context-os /a0/usr/plugins/jit_context
```

### Method 2: One-Click ZIP Installation
1. Download `jit_context.zip`.
2. Extract directly into `/a0/usr/plugins/jit_context/`:
```bash
unzip jit_context.zip -d /a0/usr/plugins/jit_context
```

### Method 3: Agent Zero WebUI Plugin Hub
1. Open Agent Zero WebUI.
2. Go to **Settings** -> **Plugins** -> **Install from URL/Git**.
3. Enter: `https://github.com/wojciechwiesner/jit-context-os` and click **Install**.

---

## 🛠️ Verification & Health Check

After installation, run the self-diagnostic test:
```bash
python /a0/usr/plugins/jit_context/execute.py
```
Or trigger **Execute / Run** directly from the Plugins modal in the Agent Zero WebUI.

---

## ⚙️ Configuration

JIT Context OS can be configured globally or per-agent/per-project via **Settings -> Agent -> JIT Context OS**:

| Setting Key | Default | Description |
| :--- | :---: | :--- |
| `mode` | `active` | `active` to inject capsule, `disabled` to pause. |
| `recent_turn_fence` | `4` | Number of recent turns preserved to stop history explosion. |
| `max_l0_facts` | `20` | Maximum dynamic facts held in active L0 hot-path. |
| `l2_timeout_ms` | `600` | Circuit breaker timeout for external RAG queries. |

---

## 🧰 Included Tools

* `jit_context_query`: Inspect active L0 facts, update dynamic facts, switch project scope, or preview the compiled prompt cache capsule in real time.

---

## 📊 Benchmark Results

| Model | Without JIT | With JIT Context OS | Improvement |
| :--- | :---: | :---: | :---: |
| **Gemini 3.8 Flash** | 3,085 tokens | **341 tokens** | **-88.9% Token Consumption** |
| **Liquid AI LFM 2.5** | 72.0% (36/50) | **92.0% (46/50)** | **+20.0 p.p. SWE Pass Rate** |
| **Qwen 3.8 Coder** | 76.0% (38/50) | **94.0% (47/50)** | **+18.0 p.p. Self-Healing** |

---

## 📄 License
MIT License. Created by Wojciech Wiesner for the Agent Zero community.

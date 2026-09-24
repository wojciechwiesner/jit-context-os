# JIT-JEV Context OS for Agent Zero ⚡
### Epistemic Context Runtime, JEV System 1 Decision Gate & 3-Tier Memory Cascade (L0/L1/L2)

[![Agent Zero](https://img.shields.io/badge/Agent%20Zero-Plugin-blue)](https://github.com/agent0ai/agent-zero)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22649541.svg)](https://doi.org/10.5281/zenodo.22649541)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Benchmark Hub](https://img.shields.io/badge/Benchmark%20Hub-Live%20Telemetry-blue?logo=googlechrome&logoColor=white)](https://theones.io/benchmark/)
[![Architecture Deep Dive](https://img.shields.io/badge/Architecture-Deep%20Dive-purple)](https://theones.io/blog/jit-jev-context-the-first-production-agent-runtime)
[![JEV Engine](https://img.shields.io/badge/JEV%20Engine--31.3%25%20Turns-emerald)](https://theones.io/benchmark/)
[![Token Reduction](https://img.shields.io/badge/Prompt%20Tokens--88.9%25-brightgreen)]()
[![Code Accuracy](https://img.shields.io/badge/Self--Healing%20Accuracy-%2B20%25-brightgreen)]()

---

### Quick Production Benchmark Snapshot
| Benchmark Metric | Without JIT-JEV (Haystack) | With JIT-JEV Context OS | Net Advantage |
| :--- | :---: | :---: | :--- |
| **Agent Turns / Task (SWE-bench)** | 6.7 turns | **4.6 turns** | **-31.3% Multi-Turn Churn Avoided** |
| **Blind Discovery Calls (ls/grep/cat)** | 38 calls | **18 calls** | **-52.6% Blind Exploration Cut** |
| **Active Context Prompt Footprint** | 3,085 tokens | **341 tokens** | **-88.9% Token Consumption** |
| **Code Pass Rate (Liquid AI LFM 2.5)** | 72.0% (36/50) | **92.0% (46/50)** | **+20.0 p.p. SWE Pass Rate** |
| **Self-Healing Accuracy (Qwen 3.8)** | 76.0% (38/50) | **94.0% (47/50)** | **+18.0 p.p. Self-Healing Accuracy** |
| **Fault Tolerance & Fallback (I6)** | N/A | Local Heuristics | **100% Fail-Open Zero Crashes** |

---

## 🌟 What is JIT-JEV Context OS?

In complex agentic workflows, injecting massive instruction manuals, unbounded history, and raw tool output causes **context bloat**, **attention drift**, and **prompt cache thrashing**.

**JIT-JEV Context OS** solves this by unifying two high-performance agent runtime layers into a single native Agent Zero plugin:

1. **JIT Context Engine (System 2 Memory):**
   * **L0 Hot-Path (<3ms):** SQLite WAL in-memory engine storing active hot-facts with Read-Your-Own-Writes (RYOW).
   * **L1 Warm-Path (<10ms):** Project domain knowledge with Hysteresis Scope Guard to eliminate context oscillations.
   * **L2 Deep-Path:** On-demand retrieval with a 600ms Circuit Breaker protecting against hanging endpoints.
   * **Deterministic XML Capsule (`<jit_capsule>`):** Stable prompt prefix ordering ensuring **>85% prompt cache hit rates** on Claude latest, Sonnet latest, Gemini 3.8 Flash, and GPT-4o.
   * **Epistemic Invariants Engine (I1–I10):** Anti-self-poisoning (assistant outputs carry 0.0 epistemic weight), strict direct user input precedence, and destructive action gating.
   * **RecentTurnFence Self-Healing:** 1-turn repair loops for coding errors without expanding conversational history.

2. **JEV Decision Gate (System 1 Fast Arbitration):**
   * **Shadow Helpfulness Judge:** Automatically scores capsule facts in shadow mode; facts that meet safety and precision thresholds (>=10 evals, 0 harmful, >=30% helpful) can be promoted into persistent L2 vault memory.
   * **Dynamic Eviction Advisor:** Triggers eviction recommendations when L0 capacity approaches threshold budgets, ensuring stale or disproven hypotheses never pollute future turns.
   * **JEV Prefetch:** Warms the remote judge cache in background threads before execution turns.
   * **Live Chat Status Bar:** Displays real-time capsule size, active facts, cache hits, and issue hints directly above the chat input.

> **Target Environment & Runtime Notice:**  
> JIT-JEV Context OS is specifically architected for **autonomous coding agents that possess active tool execution access** (shell commands, file modifications, test suites, AST parsing). It is not a generic conversational chatbot wrapper. The runtime enforces ground truth via physical tool feedback while rejecting hallucinated assistant monologues.

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
| `jev_enabled` | `true` | Master switch for the JEV Bridge layer. |
| `jev_distill_enabled` | `true` | Distill finished turns into compact L0 facts. |
| `jev_distill_max_facts` | `3` | Max distilled facts per turn. |
| `jev_eviction_budget_pct` | `0.9` | L0 fill ratio above which the eviction advisor fires. |
| `jev_remote_enabled` | `true` | Remote JEV judge/rerank model via OpenRouter-compatible API. |
| `jev_remote_model` | `~typesafe/jev-latest` | Remote JEV model id. |

---

## ⚖️ JEV Bridge (Judge / Eviction / Verification)

Since v0.4.0-beta.1, the standalone `jev_bridge` plugin is merged into JIT Context OS as a single integrated plugin:

* **Shadow Judge** (`message_loop_end`): scores capsule facts for helpfulness in shadow mode; promotes to live filtering only after the promotion gate (**>=10 evals, 0 harmful verdicts, >=30% helpful ratio**).
* **Eviction Advisor**: proposes L0 evictions when the hot-path exceeds the budget, respecting invariant priorities.
* **JEV Prefetch** (`message_loop_start`): warms the remote judge cache with TTL caching and I6 safe fallback to local heuristics.
* **Live Status Bar**: a JIT/JEV telemetry bar above the chat input (`/api/plugins/jit_context/jit_status`) showing capsule size, L0 facts, cache hits and issue hints.

All JEV calls fail safe: on any remote error the bridge degrades to local deterministic heuristics and never blocks the main agent loop.

---

## 🧰 Included Tools

* `jit_context_query`: Inspect active L0 facts, update dynamic facts, switch project scope, or preview the compiled prompt cache capsule in real time.

---

## 📊 Benchmark Results & Live Telemetry

> ⚡ **Live Interactive Telemetry:** [theones.io/benchmark/](https://theones.io/benchmark/)  
> 📖 **Architectural Deep-Dive:** [Why Combining TypeSafe Jev with JIT Context OS Cuts Agent Turns by 31%](https://theones.io/blog/jit-jev-context-the-first-production-agent-runtime)

### SWE-bench 10-Task Battle (JEV System 1 Decision Engine):
| Metric | Haystack Baseline | JIT Context OS | JIT + JEV Decision Engine | JEV Net Advantage |
| :--- | :---: | :---: | :---: | :--- |
| **Solve Rate** | 10/10 (100%) | 10/10 (100%) | **9/10 (90%)** | Reliable SOTA solve rate |
| **Average Turns / Task** | 6.7 turns | 5.6 turns | **4.6 turns** | **-31.3% Fewer Multi-Turn Cycles** |
| **Blind Discovery Ops (ls/grep/cat)** | 38 ops | 28 ops | **18 ops** | **-52.6% Blind Exploration Cut** |
| **Total Wall-Clock Time** | 150.9s | 139.3s | **133.9s** | **Fastest Delivery** |
| **Fault Tolerance (I6)** | N/A | Heuristic only | **100% Fail-Open** | Zero crashes & Circuit Breaker |

### Agent Zero Context Compression Benchmarks:
| Model | Without JIT | With JIT Context OS | Improvement |
| :--- | :---: | :---: | :---: |
| **Gemini 3.8 Flash** | 3,085 tokens | **341 tokens** | **-88.9% Token Consumption** |
| **Liquid AI LFM 2.5** | 72.0% (36/50) | **92.0% (46/50)** | **+20.0 p.p. SWE Pass Rate** |
| **Qwen 3.8 Coder** | 76.0% (38/50) | **94.0% (47/50)** | **+18.0 p.p. Self-Healing** |

---

## 📄 License
MIT License. Created by Wojciech Wiesner for the Agent Zero community.

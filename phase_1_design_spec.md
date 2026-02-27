# Phase 1: Total System Decomposition - Architecture Design

**System:** Monolith v4.5 Immortal
**Phase:** 1 (Design & Decomposition)

## 1. Operator Intelligence Layer (The "Brain")

The current `monolith_core.py` is a *Scheduler*, not an *Operator*. It executes tasks but does not invent them.
**New Component:** `System.Core.Operator`

- **Goal Engine:** Accepts high-level Axioms (e.g., "Survive", "Get Rich").
- **Planner:** Decomposes Goals into Tasks using LLM (Ollama/Gemini).
- **Feedback Loop:** Analyzes Task Results to update Strategy.

### Workflow

`Axiom -> Goal -> Plan -> Task Queue -> Scheduler -> Execution -> Result -> Memory -> Planner`

## 2. Memory Systems (The "Context")

To end "Goldfish Mode", the system requires four distinct memory types:

### A. Short-Term Memory (Context Window)

- **Implementation:** Runtime Dictionary / In-Memory list of recent logs.
- **Purpose:** Immediate context for the current cycle.

### B. Long-Term Memory (Semantic)

- **Implementation:** Vector Database (ChromaDB or FAISS) + JSON Archives.
- **Purpose:** Recall "How did I fix this bug last time?" or "What is my strategy?"

### C. Persistent Memory (State)

- **Implementation:** SQLite (`ledger.db`, `state.db`).
- **Purpose:** Financial transactions, active task IDs, agent registry.

### D. Immutable Memory (The "Black Box")

- **Implementation:** Append-only Log Files + Hash Chain (Simulated Blockchain).
- **Purpose:** Audit trail that cannot be deleted, even by the Operator.

## 3. Execution & Sandboxing (The "Body")

**Component:** `System.Core.sandbox_win` (Existing & Verified)

- **Mechanism:** Windows Job Objects.
- **Constraints:** 512MB RAM Limit, CPU Throttling, Kill-on-Close.
- **Upgrade:** Add **Network Access Control** (Allow-list domains only via local proxy or firewall rules).

## 4. Agent Lifecycle (The "Population")

**Component:** `System.Agents.Factory`

- **Genesis:** Operator requests new capability.
- **Construction:** Factory generates code based on `Template`.
- **Validation:** Sandbox Test Run (Simulated).
- **Deployment:** Registered to `monolith_core`.
- **Termination:** Pruning underperforming agents ($0 revenue).

## 5. Security Boundaries

- **Ring 0 (Kernel):** `monolith_omega.py`, `monolith_core.py`, `monolith_sentinel.py`. (Read-Only to Agents).
- **Ring 1 (Services):** `Operator`, `Memory`, `Finance`.
- **Ring 2 (Agents):** `Scout`, `Builder`, `Sales`. (Sandboxed).

# Psiquis Genesis Framework
### Autonomous Agent Generation and Self-Correction at Enterprise Scale

---

## The Challenge: The Brittleness of Modern AI Agents

Enterprise-grade AI initiatives are consistently hampered by a core technical challenge: the operational fragility of autonomous agents. Standard agentic systems are static, require continuous human-in-the-loop intervention for error handling, and lack the intrinsic capability to adapt to novel scenarios or self-heal from failures. This results in escalating maintenance costs, operational bottlenecks, and a failure to realize the full potential of autonomous systems at scale.

## The Solution: The Genesis Meta-Orchestration Layer

The Psiquis Genesis Framework introduces a paradigm shift from static agents to a dynamic, self-correcting ecosystem. At its core, the `Genesis` meta-agent orchestrates a hierarchy of specialized agents, treating them as dynamic, replaceable components.

When a subordinate agent encounters an error it cannot resolve, the event is escalated. The `CorrectorAgent` is then tasked by `Genesis` to perform a root-cause analysis, introspect the failed agent's source code, and programmatically generate a patch. The corrected code is then validated and redeployed, often without any human intervention. For new tasks, the `ScaffolderAgent` can be invoked to generate boilerplate code and operational structures for entirely new agents, dramatically accelerating development cycles.

This architecture transforms the traditional "fail-and-fix" model into a "fail-and-evolve" system, delivering unprecedented operational resilience and scalability.

## Core Capabilities

*   **Dynamic Agent Generation:** `ScaffolderAgent` autonomously generates the necessary boilerplate, dependencies, and configuration for new agent classes based on high-level objectives.
*   **Autonomous Self-Correction:** `CorrectorAgent` performs real-time code analysis and patch generation in response to runtime errors, leveraging LLMs for code-level introspection and repair.
*   **Hierarchical Meta-Orchestration:** The `Genesis` agent manages the entire agent lifecycle, from instantiation and tasking to monitoring and decommissioning, ensuring system-wide goal alignment.
*   **Stateful Persistence & Recovery:** Agents persist their state, allowing for seamless recovery and task resumption after a system restart or a self-correction-induced redeployment.
*   **Extensible Tooling API:** A modular interface allows for the rapid integration of new tools, data sources, and proprietary capabilities into the agent ecosystem.
*   **Enterprise-Grade Monitoring & Logging:** Comprehensive, structured logging provides a clear audit trail of all agent actions, decisions, and self-correction events for robust oversight and diagnostics.

## Genesis in Action

The following demonstration illustrates the self-correction loop. An agent is tasked with a function containing a deliberate bug. The framework detects the failure, invokes the `CorrectorAgent` to patch the code, and successfully re-runs the task.

![Genesis Framework Self-Correction Demo](assets/genesis-demo.gif)

## Quickstart

### Prerequisites
*   Python 3.10+
*   Access to a compatible LLM API (e.g., OpenAI, Anthropic, or a Psiquis-X hosted model)

### 1. Clone the Repository
```bash
git clone https://github.com/psiquis-x/psiquis-genesis-framework.git
cd psiquis-genesis-framework
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Copy the `.env.example` file to `.env` and populate it with the required API keys and configuration parameters.
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 4. Initiate the Orchestrator
```bash
python main.py --task "Your initial high-level objective here"
```

---

## Deploying Genesis at Enterprise Scale

This repository provides the core engine of the Genesis Framework. For enterprise deployments, Psiquis-X offers tailored architecture design, hardened security implementations, proprietary model fine-tuning, and dedicated support to integrate Genesis into your mission-critical workflows.

**[Contact Psiquis-X to deploy this architecture and redefine your organization's AI capabilities.](mailto:orquestadrop6@gmail.com)**
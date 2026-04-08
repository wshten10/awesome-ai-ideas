# AutoGPT + n8n Integration - Autonomous Workflow Orchestration

> **Issue:** #869 | **Status:** Proposal | **Difficulty:** Advanced
> **Target Markets:** AutoGPT (183k⭐) + n8n (183k⭐) = 366k potential users

---

## 1. Overview

### Problem Statement

AutoGPT excels at autonomous task execution but lacks visual workflow orchestration. n8n provides powerful visual workflow building but lacks deep AI agent integration. Bridging these two ecosystems enables:

- **Visual AI pipelines** — Design complex multi-agent workflows with drag-and-drop
- **Production-grade reliability** — Retry logic, error handling, conditional branching for agent tasks
- **Enterprise adoption** — n8n's self-hosted model aligns with enterprise security requirements
- **Rapid prototyping** — Test agent workflows visually before deploying autonomously

### Value Proposition

| Dimension | AutoGPT Alone | n8n Alone | Combined |
|-----------|--------------|-----------|----------|
| Visual Workflow | ❌ CLI-only | ✅ Canvas editor | ✅ AI-aware canvas |
| Error Recovery | ⚠️ Manual | ✅ Built-in | ✅ Agent-aware retries |
| Human-in-the-loop | ⚠️ Limited | ✅ Webhooks | ✅ Smart approval nodes |
| Scaling | ⚠️ Single agent | ✅ Queue-based | ✅ Multi-agent orchestration |
| Monitoring | ⚠️ Logs | ✅ Dashboard | ✅ Agent telemetry |

### Target Audience

1. **AutoGPT power users** wanting workflow reliability and visual debugging
2. **n8n users** wanting autonomous AI agent capabilities in their pipelines
3. **Enterprise teams** needing governed AI agent deployment with audit trails
4. **AI developers** building production agent systems requiring orchestration

---

## 2. Competitor Analysis

### Existing Solutions Landscape

| Competitor | Integration Type | Strengths | Weaknesses | Price |
|-----------|-----------------|-----------|------------|-------|
| LangGraph + n8n | Community plugin | LangChain ecosystem | Complex setup, limited | Free |
| CrewAI + n8n | Webhook-based | Multi-agent focus | No native nodes, fragile | Free |
| Flowise | Self-hosted | Visual AI builder | Limited agent autonomy | Free/Pro |
| Dify | Self-hosted | Full AI platform | Lock-in, not n8n native | Free/Cloud |
| Zapier + OpenAI | SaaS | Easy setup | No agent autonomy, expensive | $$$ |
| Make + OpenAI | SaaS | Visual builder | Limited agent control | $$ |
| ComfyUI | Self-hosted | Visual AI pipelines | Image-focused, not general | Free |

### Market Positioning

Our integration occupies a unique position:

- **Deeper than webhooks** — Native nodes with agent state awareness
- **More flexible than Flowise** — Leverages both AutoGPT and n8n ecosystems
- **More autonomous than Zapier/Make** — True agent-driven execution
- **More general than ComfyUI** — Works with any AutoGPT agent, not just image gen

### Competitive Advantages

1. **Bidirectional integration** — Not just "trigger agent from n8n" but also "agent triggers n8n workflows as tools"
2. **Stateful orchestration** — Agent memory persists across n8n workflow steps
3. **Visual debugging** — Real-time agent state visualization on n8n canvas
4. **Community scale** — Combined 366k GitHub stars provide massive distribution

---

## 3. Feature Design

### 3.1 n8n Custom Node: AutoGPT Agent

The core n8n node that brings AutoGPT capabilities into workflows.

```
┌─────────────────────────────────────────────┐
│           AutoGPT Agent Node                │
├─────────────────────────────────────────────┤
│  Agent Config:                              │
│    [Agent Name: research-agent       ▼]     │
│    [Agent Mode: autonomous           ▼]     │
│                                             │
│  Task Configuration:                        │
│    [Task Prompt: _______________________]   │
│    [Max Iterations: 25              ]       │
│    [Timeout: 300s                  ]        │
│                                             │
│  Parameters:                                │
│    [Model: gpt-4-turbo              ▼]     │
│    [Temperature: 0.7               ]        │
│    [Memory: persistent              ▼]      │
│                                             │
│  Advanced:                                  │
│    [☑] Enable human-in-the-loop             │
│    [☑] Stream intermediate results          │
│    [  ] Allow tool creation                 │
│    [Fallback: retry | fail | skip    ▼]     │
└─────────────────────────────────────────────┘
```

**Node Properties:**

```json
{
  "name": "AutoGPT Agent",
  "version": "1.0.0",
  "description": "Execute AutoGPT agents within n8n workflows",
  "icon": "file:autogpt.svg",
  "properties": [
    {
      "name": "agentName",
      "type": "string",
      "required": true,
      "default": "default"
    },
    {
      "name": "taskPrompt",
      "type": "string",
      "required": true,
      "displayOptions": { "show": { "mode": ["single", "autonomous"] } }
    },
    {
      "name": "maxIterations",
      "type": "number",
      "default": 25,
      "validateType": "number"
    },
    {
      "name": "timeout",
      "type": "number",
      "default": 300,
      "description": "Maximum execution time in seconds"
    },
    {
      "name": "mode",
      "type": "options",
      "options": [
        { "name": "Single Task", "value": "single" },
        { "name": "Autonomous", "value": "autonomous" },
        { "name": "Chat", "value": "chat" }
      ]
    },
    {
      "name": "humanInLoop",
      "type": "boolean",
      "default": false,
      "description": "Require human approval for agent actions"
    },
    {
      "name": "onError",
      "type": "options",
      "options": [
        { "name": "Retry (3x)", "value": "retry" },
        { "name": "Fail Workflow", "value": "fail" },
        { "name": "Skip to Next", "value": "skip" },
        { "name": "Fallback Node", "value": "fallback" }
      ]
    }
  ]
}
```

**Output Schema:**

```json
{
  "result": {
    "finalAnswer": "string",
    "taskCompleted": "boolean",
    "iterationsUsed": "number",
    "executionTime": "number",
    "toolsUsed": ["string"],
    "memorySnapshot": {
      "messages": "number",
      "filesAccessed": "number",
      "apiCalls": "number"
    },
    "intermediateResults": [
      {
        "iteration": "number",
        "thought": "string",
        "action": "string",
        "observation": "string"
      }
    ]
  },
  "metadata": {
    "agentId": "string",
    "sessionId": "string",
    "model": "string",
    "totalTokens": "number",
    "estimatedCost": "number"
  }
}
```

### 3.2 n8n Trigger Node: AutoGPT Event

Listens for events from running AutoGPT agents.

```
┌─────────────────────────────────────────────┐
│         AutoGPT Event Trigger               │
├─────────────────────────────────────────────┤
│  Event Types:                               │
│    [☑] Agent Started                        │
│    [☑] Task Completed                       │
│    [☑] Task Failed                          │
│    [☑] Human Approval Required              │
│    [☑] Intermediate Checkpoint              │
│    [  ] Memory Threshold Exceeded           │
│                                             │
│  Filter:                                    │
│    [Agent Name: __all__              ▼]     │
│    [Min Confidence: 0.0             ]       │
│                                             │
│  Webhook URL:                               │
│    https://n8n.example.com/webhook/ag-xxx   │
└─────────────────────────────────────────────┘
```

### 3.3 AutoGPT Plugin: n8n Workflow Tool

Allows AutoGPT agents to execute n8n workflows as tools during autonomous operation.

```python
class N8nWorkflowTool(Tool):
    """Tool that allows AutoGPT to execute n8n workflows."""

    name = "n8n_workflow"
    description = (
        "Execute an n8n workflow with given parameters. "
        "Useful for multi-step data processing, API integrations, "
        "and complex operations that benefit from visual workflow design."
    )
    parameters = {
        "type": "object",
        "properties": {
            "workflow_id": {
                "type": "string",
                "description": "The n8n workflow ID to execute"
            },
            "parameters": {
                "type": "object",
                "description": "Input parameters for the workflow"
            },
            "wait_for_completion": {
                "type": "boolean",
                "default": True,
                "description": "Whether to wait for workflow completion"
            },
            "timeout": {
                "type": "number",
                "default": 120,
                "description": "Timeout in seconds"
            }
        },
        "required": ["workflow_id"]
    }

    def execute(self, workflow_id: str, parameters: dict = None,
                wait_for_completion: bool = True, timeout: int = 120):
        """Execute an n8n workflow."""
        n8n_client = N8nClient(self.config.n8n_base_url, self.config.n8n_api_key)

        execution = n8n_client.execute_workflow(
            workflow_id=workflow_id,
            data=parameters or {}
        )

        if wait_for_completion:
            result = execution.wait(timeout=timeout)
            return {
                "status": result.status,
                "output_data": result.data,
                "execution_time": result.execution_time,
                "error": result.error if result.error else None
            }

        return {
            "status": "submitted",
            "execution_id": execution.id,
            "check_url": f"{self.config.n8n_base_url}/executions/{execution.id}"
        }

    def list_workflows(self, search: str = None) -> list:
        """List available n8n workflows."""
        n8n_client = N8nClient(self.config.n8n_base_url, self.config.n8n_api_key)
        workflows = n8n_client.list_workflows(active=True, search=search)
        return [
            {
                "id": w.id,
                "name": w.name,
                "description": w.description or "",
                "tags": w.tags
            }
            for w in workflows
        ]
```

**Agent Configuration:**

```yaml
# autogpt_config.yaml
ai_settings:
  agent_name: "orchestrator"
  role: "AI workflow orchestrator"
  goals:
    - "Coordinate complex multi-step tasks using n8n workflows"
    - "Monitor workflow execution and handle failures"
    - "Report results and insights"

plugins:
  n8n_integration:
    enabled: true
    config:
      base_url: "http://n8n:5678"
      api_key: "${N8N_API_KEY}"
      available_workflows:
        - id: "web-research"
          description: "Research a topic and return structured findings"
        - id: "data-analysis"
          description: "Analyze data and generate reports"
        - id: "content-generation"
          description: "Generate content based on research findings"
        - id: "notification"
          description: "Send notifications via email/Slack/Discord"

      max_concurrent_workflows: 5
      default_timeout: 120
      retry_policy:
        max_retries: 3
        backoff: "exponential"
        retryable_errors:
          - "TIMEOUT"
          - "RATE_LIMIT"
          - "CONNECTION_ERROR"
```

### 3.4 Orchestration Engine

The brain that maps n8n workflow steps to AutoGPT agent capabilities.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION ENGINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐      │
│  │  n8n      │───▶│  Capability  │───▶│  Agent           │      │
│  │  Workflow │    │  Mapper      │    │  Dispatcher      │      │
│  │  Steps    │    │              │    │                  │      │
│  └──────────┘    └──────────────┘    └──────────────────┘      │
│                         │                      │                │
│                         ▼                      ▼                │
│                  ┌──────────────┐    ┌──────────────────┐      │
│                  │  State       │    │  Visual          │      │
│                  │  Manager     │    │  Debugger        │      │
│                  │              │    │                  │      │
│                  └──────────────┘    └──────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Capability Mapping Table:**

| n8n Step Type | Mapped Agent Capability | Execution Mode |
|--------------|------------------------|----------------|
| HTTP Request | API calls + web search | Direct execution |
| Code Node | Python/JS execution sandbox | Sandboxed |
| IF/Switch | Conditional branching | Agent reasoning |
| Loop | Iterative processing | Agent iteration |
| Set/Function | Data transformation | Agent memory update |
| Webhook | External triggers | Event subscription |
| Wait | Delay/polling | Agent scheduled check |
| Sub-Workflow | Nested workflows | Agent sub-task dispatch |
| Error Trigger | Error handling | Agent self-correction |
| Merge | Data joining | Agent synthesis |

**State Management:**

```typescript
interface OrchestrationState {
  sessionId: string;
  workflowId: string;
  currentStep: string;
  agentState: {
    memory: ConversationMemory;
    taskQueue: Task[];
    completedTasks: TaskResult[];
    failedTasks: FailedTask[];
  };
  executionContext: {
    variables: Record<string, unknown>;
    sharedData: Record<string, unknown>;
    checkpoint?: Checkpoint;
  };
  monitoring: {
    startTime: number;
    lastActivity: number;
    tokenUsage: TokenUsage;
    estimatedCost: number;
    progress: number; // 0-100
  };
}
```

---

## 4. User Acquisition Strategy

### Phase 1: Community Launch (Weeks 1-4)

| Channel | Action | Expected Reach |
|---------|--------|---------------|
| AutoGPT Discord | Post demo + tutorial | 50k members |
| n8n Community Forum | Integration guide post | 30k members |
| Reddit r/AutoGPT | Video demo + benchmark | 120k members |
| Reddit r/n8n | Workflow template pack | 45k members |
| Twitter/X | Thread: "AutoGPT meets n8n" | 100k impressions |
| Dev.to | Technical deep-dive article | 20k views |
| GitHub README | Featured in both repos | 366k combined stars |

### Phase 2: Content Marketing (Weeks 5-12)

1. **Video Tutorial Series** (YouTube)
   - "Build an autonomous research pipeline" — AutoGPT + n8n
   - "Enterprise AI workflows with human approval"
   - "Multi-agent coordination with visual debugging"

2. **Workflow Template Gallery**
   - 20+ pre-built templates for common use cases
   - Customer research automation
   - Content creation pipeline
   - Data analysis workflows
   - Notification and reporting

3. **Case Studies**
   - Enterprise deployment story
   - Startup MVP acceleration
   - Research lab automation

### Phase 3: Partnership & Integration (Weeks 8-16)

| Partner | Integration Type | Value |
|---------|-----------------|-------|
| n8n Inc. | Official community node | Verified badge, discoverability |
| AutoGPT team | Recommended plugin | Featured in docs |
| LangChain | Compatible tool interface | Ecosystem leverage |
| Supabase | Template for persistent state | Data layer |

### Growth Metrics

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| GitHub Stars | 500 | 3,000 | 10,000 |
| npm Downloads | 1,000 | 15,000 | 50,000 |
| Active Users | 100 | 1,500 | 5,000 |
| Template Downloads | 200 | 3,000 | 15,000 |

---

## 5. Technical Plan

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER LAYER                            │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  n8n Canvas  │  │  AutoGPT CLI │  │  Web Dashboard │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
└─────────┼────────────────┼──────────────────┼───────────┘
          │                │                  │
┌─────────┼────────────────┼──────────────────┼───────────┐
│         ▼                ▼                  ▼            │
│                 INTEGRATION LAYER                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │           Orchestration Engine (Core)             │   │
│  │  ┌──────────┐ ┌───────────┐ ┌───────────────┐   │   │
│  │  │  n8n     │ │  AutoGPT  │ │  State        │   │   │
│  │  │  Adapter │ │  Adapter  │ │  Manager      │   │   │
│  │  └──────────┘ └───────────┘ └───────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│                 COMMUNICATION LAYER                      │
│  ┌────────────────┐  ┌──────────────────────────────┐  │
│  │  REST API      │  │  WebSocket (real-time)       │  │
│  │  /api/v1/*     │  │  ws://localhost:8765         │  │
│  └────────────────┘  └──────────────────────────────┘  │
│                                                         │
│                 PERSISTENCE LAYER                        │
│  ┌────────────────┐  ┌──────────────────────────────┐  │
│  │  SQLite/PG     │  │  Redis (caching/sessions)    │  │
│  │  (state/logs)  │  │                              │  │
│  └────────────────┘  └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| n8n Node SDK | TypeScript | Official n8n node development |
| AutoGPT Plugin | Python | AutoGPT's native language |
| Orchestration Engine | TypeScript | Shared language with n8n |
| State Storage | SQLite (default) / PostgreSQL | Portable, scalable |
| Real-time Updates | WebSocket | Agent status streaming |
| API Layer | FastAPI (Python) + Express (Node) | Native to each ecosystem |
| Configuration | YAML + Environment variables | AutoGPT convention |
| Testing | Jest + Pytest | Industry standard |
| CI/CD | GitHub Actions | Repository standard |

### API Endpoints

```
# Orchestration Engine API
POST   /api/v1/workflows/execute          # Execute workflow with agent
GET    /api/v1/sessions/{id}              # Get session state
POST   /api/v1/sessions/{id}/approve      # Human approval
GET    /api/v1/sessions/{id}/debug        # Visual debug data
WebSocket /ws/sessions/{id}               # Real-time updates

# n8n Node API (internal)
POST   /internal/agent/execute            # Execute agent task
POST   /internal/agent/status             # Check agent status
POST   /internal/workflow/trigger         # Agent triggers workflow
GET    /internal/capabilities             # List agent capabilities
```

---

## 6. Implementation Steps

### Phase 1: Foundation (Weeks 1-3)

| Week | Task | Deliverable |
|------|------|-------------|
| 1.1 | Project scaffolding, monorepo setup | Repo with packages: node, plugin, engine |
| 1.2 | Define shared types and interfaces | `@autogpt-n8n/types` package |
| 1.3 | Basic n8n node skeleton | Node appears in n8n, accepts config |
| 2.1 | AutoGPT plugin skeleton | Plugin loads, registers as tool |
| 2.2 | REST API for communication | Agent ↔ n8n basic communication |
| 2.3 | Docker Compose setup | One-command dev environment |
| 3.1 | State management foundation | Session persistence in SQLite |
| 3.2 | Basic integration test | End-to-end: n8n triggers agent, gets result |
| 3.3 | Documentation site setup | Docusaurus with getting started guide |

### Phase 2: Core Features (Weeks 4-8)

| Week | Task | Deliverable |
|------|------|-------------|
| 4.1 | Agent node: single-task mode | Execute one task, return result |
| 4.2 | Agent node: autonomous mode | Multi-iteration execution |
| 4.3 | Error handling & retry logic | Configurable failure strategies |
| 5.1 | n8n Workflow tool in AutoGPT | Agent can trigger n8n workflows |
| 5.2 | Bidirectional communication | Agent ↔ n8n real-time status |
| 5.3 | Parameter passing & data mapping | Complex data flows between systems |
| 6.1 | Human-in-the-loop node | Approval workflow in n8n canvas |
| 6.2 | Intermediate result streaming | Real-time agent output in n8n |
| 6.3 | Event trigger node | AutoGPT events trigger n8n workflows |
| 7.1 | Orchestration engine: capability mapper | Map n8n steps to agent capabilities |
| 7.2 | State manager: checkpointing | Resume workflows from checkpoints |
| 7.3 | Visual debugger: WebSocket streaming | Live agent state on n8n canvas |
| 8.1 | Template system | Import/export workflow templates |
| 8.2 | 10 starter templates | Common use case workflows |
| 8.3 | Performance optimization | Concurrent execution, caching |

### Phase 3: Polish & Launch (Weeks 9-12)

| Week | Task | Deliverable |
|------|------|-------------|
| 9.1 | Comprehensive test suite | 90%+ coverage on both packages |
| 9.2 | Security audit | Input validation, auth, secrets management |
| 9.3 | Logging & monitoring integration | Structured logs, OpenTelemetry |
| 10.1 | Documentation complete | API docs, tutorials, troubleshooting |
| 10.2 | Video tutorial: getting started | 15-min setup walkthrough |
| 10.3 | Contribution guidelines | CLA, PR template, issue forms |
| 11.1 | Beta release (v0.9.0) | npm + PyPI beta packages |
| 11.2 | Community feedback collection | GitHub Discussions, Discord |
| 11.3 | Bug fixes from beta | Stability improvements |
| 12.1 | v1.0.0 release | Stable release with full docs |
| 12.2 | Launch blog post & social media | Announcement across all channels |
| 12.3 | Submit to n8n community nodes | Official review process |

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| AutoGPT API breaking changes | Medium | High | Abstraction layer, version pinning |
| n8n SDK deprecation | Low | High | Follow n8n releases, community monitoring |
| Performance at scale | Medium | Medium | Async processing, queue-based execution |
| Security vulnerabilities | Low | Critical | Security audit, dependency scanning |
| Community adoption slow | Medium | Medium | Template gallery, content marketing |

---

## 7. Success Metrics

| KPI | Target (6 months) | Measurement |
|-----|-------------------|-------------|
| GitHub Stars | 10,000 | GitHub API |
| npm Downloads/month | 50,000 | npm registry |
| Active installations | 5,000 | Telemetry (opt-in) |
| Community templates | 50+ | Template gallery |
| Discord/community members | 2,000 | Server count |
| Bug resolution time | < 48 hours | GitHub issues |
| Test coverage | > 85% | Codecov |

---

## 8. Conclusion

The AutoGPT + n8n integration represents a unique opportunity to bridge two of the most popular open-source AI/automation projects. By providing deep bidirectional integration with visual debugging, stateful orchestration, and enterprise-grade reliability, this project can become the de facto standard for production AI agent workflows.

The combined community of 366k GitHub stars provides an unprecedented launch pad, and the technical architecture ensures extensibility for future integrations with other agent frameworks (CrewAI, LangGraph, etc.).

**Next Steps:**
1. ✅ Community feedback on this proposal
2. 🔲 Set up monorepo and CI/CD
3. 🔲 Begin Phase 1 implementation
4. 🔲 Recruit maintainers from both communities

---

*This proposal is open for community feedback. Please comment on #869 with suggestions, questions, or expressions of interest in contributing.*
"@

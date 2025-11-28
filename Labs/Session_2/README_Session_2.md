# Session 2: Advanced Agent Patterns

**Duration:** 3 hours
**Format:** ~80% hands-on, ~20% lecture

## Session Overview

In this session, you'll learn advanced agent patterns using LangGraph for stateful workflows. You'll also build a capstone project using your preferred framework.

---

## Agenda

| Time | Activity | Description |
|------|----------|-------------|
| 0:00-0:30 | Advanced Frameworks | LangGraph intro, SmolAgents demo, ADK overview |
| 0:30-1:15 | **Lab 3: LangGraph Workflows** | Build stateful agent with conditional routing |
| 1:15-1:30 | Break | - |
| 1:30-1:45 | Framework Selection Guide | Decision framework, choosing for your use case |
| 1:45-2:30 | **Lab 4: Capstone Project** | Build your own agent with framework of choice |
| 2:30-3:00 | Demo & Wrap-up | Participants demo their agents |

---

## Learning Objectives

By the end of Session 2, you will be able to:

1. **Build** stateful workflows with LangGraph
2. **Implement** conditional routing between agent steps
3. **Use** cycles and loops in agent workflows
4. **Design** human-in-the-loop patterns
5. **Choose** the right framework for any use case
6. **Build** a complete agent for a real-world scenario

---

## Key Concepts

### Why LangGraph?

LangGraph addresses limitations of simple ReAct agents:

| Simple Agent | LangGraph |
|--------------|-----------|
| Linear execution | Graph-based workflows |
| Implicit state | Explicit state management |
| Hard to debug | Visual, traceable flow |
| No persistence | Built-in checkpointing |
| Limited control | Fine-grained routing |

### LangGraph Core Concepts

```
┌─────────────────────────────────────────────────┐
│                  StateGraph                      │
│                                                  │
│   ┌──────────┐     ┌──────────┐     ┌────────┐  │
│   │  START   │────►│  Node A  │────►│ Node B │  │
│   └──────────┘     └──────────┘     └────────┘  │
│                          │                │      │
│                          │ conditional    │      │
│                          ▼                ▼      │
│                    ┌──────────┐     ┌────────┐  │
│                    │  Node C  │────►│  END   │  │
│                    └──────────┘     └────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘

State = { messages: [], context: {}, ... }
```

1. **State**: A TypedDict that flows through the graph
2. **Nodes**: Functions that process and update state
3. **Edges**: Connections between nodes (can be conditional)
4. **Checkpoints**: Saved state for persistence/resumption

### When to Use LangGraph

**Use LangGraph when you need:**
- Complex workflows with multiple paths
- State that persists across steps
- Human-in-the-loop approval
- Cycles (agent can loop back)
- Detailed control over execution

**Stick with simpler agents when:**
- Linear, straightforward tasks
- Simple tool calling
- No state management needed

---

## Other Frameworks (Brief Overview)

### SmolAgents (Hugging Face)

**Philosophy**: Minimal, code-focused agents that write and execute code directly.

```python
from smolagents import CodeAgent, tool

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    # Implementation here
    return f"Search results for: {query}"

agent = CodeAgent(tools=[search_web])
result = agent.run("Find the latest news about AI agents")
print(result)
```

**Best for**: Lightweight tasks, learning, HuggingFace ecosystem.

📖 **Deep dive**: See [Supporting_Materials/SmolAgents_Guide.md](../../Supporting_Materials/SmolAgents_Guide.md)

### Google ADK (Agent Development Kit)

**Philosophy**: Production-ready agents for Google Cloud deployment.

```python
from google.adk.agents import Agent
from google.adk.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: Sunny, 72°F"

agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    tools=[get_weather]
)

# Run locally or deploy to Cloud Run
```

**CLI Commands**:
- `adk create my_agent` - Create new agent project
- `adk run` - Run agent locally
- `adk web` - Launch web UI for testing
- `adk deploy` - Deploy to Google Cloud

📖 **Deep dive**: See [Supporting_Materials/Google_ADK_Guide.md](../../Supporting_Materials/Google_ADK_Guide.md)

### A2A Protocol (Agent-to-Agent)

**Philosophy**: Open standard for agent interoperability across frameworks.

A2A enables agents built with different frameworks (LangGraph, AutoGen, ADK, etc.) to communicate using a common protocol.

**Core Concepts**:
- **Agent Card**: JSON describing agent capabilities
- **Tasks**: Units of work sent between agents
- **Messages/Parts**: Structured communication format

```python
# Discovering another agent's capabilities
import requests

response = requests.get("https://agent.example.com/.well-known/agent.json")
agent_card = response.json()
print(f"Agent: {agent_card['name']}")
print(f"Skills: {[s['name'] for s in agent_card['skills']]}")

# Sending a task to the agent
task_response = requests.post(
    "https://agent.example.com/tasks",
    json={
        "message": {
            "role": "user",
            "parts": [{"type": "text", "text": "Analyze this document..."}]
        }
    }
)
```

**When to use A2A**:
- Multiple teams using different frameworks
- Enterprise multi-agent orchestration
- Cross-organization agent communication

📖 **Deep dive**: See [Supporting_Materials/A2A_Protocol_Guide.md](../../Supporting_Materials/A2A_Protocol_Guide.md)

---

## Framework Selection Guide

### Decision Tree

```
Start
  │
  ├─► Single agent with tools?
  │     ├─► Yes ──► LangChain Agents
  │     └─► No ───┐
  │               │
  ├─► Need conversation between agents?
  │     ├─► Yes ──► AutoGen
  │     └─► No ───┐
  │               │
  ├─► Role-based pipeline?
  │     ├─► Yes ──► CrewAI
  │     └─► No ───┐
  │               │
  ├─► Complex stateful workflow?
  │     ├─► Yes ──► LangGraph
  │     └─► No ───┐
  │               │
  ├─► Minimal overhead needed?
  │     ├─► Yes ──► SmolAgents
  │     └─► No ───┐
  │               │
  └─► Google Cloud deployment?
        ├─► Yes ──► Google ADK
        └─► No ──► LangChain or LangGraph
```

### Quick Reference Table

| Use Case | Recommended Framework |
|----------|----------------------|
| Simple tool-using agent | LangChain |
| Research/writing pipeline | CrewAI |
| Code generation with execution | AutoGen |
| Customer support chat | AutoGen |
| Document processing workflow | LangGraph |
| Approval workflows | LangGraph |
| Learning/education | SmolAgents |
| Production on GCP | Google ADK |

---

## Labs Overview

### Lab 3: LangGraph Workflows (~45 min)

Build a document processing agent with:
- State management
- Conditional routing based on content
- Human-in-the-loop approval
- Error handling and retries

**Key Learnings:**
- Creating `StateGraph` with TypedDict state
- Adding nodes and edges
- Implementing conditional routing
- Using checkpoints for persistence

### Lab 4: Capstone Project (~45 min)

Choose your agent type and framework:
- **Code Assistant**: Analyze, explain, and improve code
- **Research Agent**: Gather, analyze, and summarize information
- **Data Analyst**: Process and visualize data
- **Custom Agent**: Your own idea!

---

## Prerequisites Checklist

Before starting the labs, ensure you have:

- [ ] Completed Session 1 labs
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] API keys configured

### Verify LangGraph Installation

```bash
python -c "from langgraph.graph import StateGraph; print('LangGraph OK')"
```

---

## Troubleshooting

### Common Issues

**Issue:** LangGraph state not updating
- **Solution:** Ensure your node functions return state updates correctly

**Issue:** Conditional edge not working
- **Solution:** Make sure the routing function returns valid node names

**Issue:** Graph enters infinite loop
- **Solution:** Add proper termination conditions and max iterations

**Issue:** Checkpointing errors
- **Solution:** Use SQLite checkpointer for persistent storage

---

## Resources

### Official Documentation
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)
- [SmolAgents Guide](https://huggingface.co/docs/smolagents/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol Specification](https://github.com/google-a2a/A2A)

### Workshop Materials
- [STUDENT_GUIDE.md](../../Supporting_Materials/STUDENT_GUIDE.md) - Comprehensive learner guide
- [SmolAgents_Guide.md](../../Supporting_Materials/SmolAgents_Guide.md) - SmolAgents deep-dive
- [Google_ADK_Guide.md](../../Supporting_Materials/Google_ADK_Guide.md) - ADK documentation
- [A2A_Protocol_Guide.md](../../Supporting_Materials/A2A_Protocol_Guide.md) - A2A protocol guide

---

## Capstone Project Guidelines

### Requirements

1. **Functional Agent**: Must perform a useful task
2. **Multiple Tools**: At least 2-3 tools
3. **Clear Documentation**: Code comments and README
4. **Demo Ready**: Be prepared to show it working

### Evaluation Criteria

- Does the agent accomplish its goal?
- Is the code well-organized?
- Are tools well-designed?
- Does it handle errors gracefully?
- Is it demo-able in 2-3 minutes?

### Ideas for Projects

1. **Code Assistant**
   - Analyze code for bugs
   - Suggest improvements
   - Generate documentation

2. **Research Agent**
   - Search multiple sources
   - Synthesize findings
   - Generate reports

3. **Data Analyst**
   - Load and process CSV
   - Calculate statistics
   - Create visualizations

4. **Meeting Assistant**
   - Summarize transcripts
   - Extract action items
   - Schedule follow-ups

5. **Your Own Idea!**
   - What problem would you solve?
   - What tools would you need?

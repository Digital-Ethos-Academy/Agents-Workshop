# Student Guide: Crafting Custom Agents Workshop

Welcome! This guide will help you navigate the workshop, understand key concepts, and get the most out of your learning experience.

---

## Learning Path Overview

```
Session 1: Foundations          Session 2: Advanced Patterns
┌─────────────────────────┐     ┌─────────────────────────┐
│ Lab 1: LangChain Basics │     │ Lab 3: LangGraph        │
│ - Tools & prompts       │     │ - State machines        │
│ - ReAct pattern         │     │ - Conditional routing   │
├─────────────────────────┤     │ - Cycles in graphs      │
│ Lab 2: AutoGen & CrewAI │     ├─────────────────────────┤
│ - Multi-agent systems   │     │ Lab 4: Capstone Project │
│ - Agent collaboration   │     │ - Build your own agent  │
│ - Role-based crews      │     │ - Framework of choice   │
└─────────────────────────┘     └─────────────────────────┘
```

---

## Before You Start

### Prerequisites Checklist
- [ ] Python 3.10+ installed
- [ ] OpenAI API key (with credits)
- [ ] IDE or Jupyter environment ready
- [ ] Basic Python knowledge (functions, classes, async)

### Environment Setup
Run the environment checker to verify your setup:
```bash
python check_environment.py
```

### API Cost Estimates
| Lab | Estimated Cost | Notes |
|-----|---------------|-------|
| Lab 1 | $0.10 - $0.30 | Basic tool use, few iterations |
| Lab 2 | $0.15 - $0.40 | Multi-agent conversations |
| Lab 3 | $0.20 - $0.50 | State graph with multiple nodes |
| Lab 4 | $0.40 - $1.00 | Complex workflows, more tokens |
| **Total** | **$0.85 - $2.20** | Conservative estimate |

**Tips to minimize costs:**
- Use `gpt-4o-mini` for development/testing
- Switch to `gpt-4o` only for final runs
- Reuse cached results when possible

---

## Lab-by-Lab Walkthrough

### Lab 1: Building Your First Agent (LangChain)

**Goal**: Understand how agents use tools to accomplish tasks.

**Key Concepts**:
- **Tools**: Functions the agent can call (search, calculate, etc.)
- **ReAct Pattern**: Reason → Act → Observe loop
- **Prompts**: Instructions that guide agent behavior

**What You'll Build**: A research assistant that can search and summarize.

**Checkpoint Questions**:
1. What happens if the agent can't find an appropriate tool?
2. How does the agent decide which tool to use?
3. What's the role of the system prompt?

---

### Lab 2: Multi-Agent Systems (AutoGen & CrewAI)

**Goal**: Coordinate multiple specialized agents using two frameworks.

**Key Concepts**:
- **Agent Roles**: Specialized agents for different tasks
- **Group Chat**: Multi-agent conversation management (AutoGen)
- **Crews & Tasks**: Role-based collaboration (CrewAI)
- **Handoffs**: Passing tasks between agents

**What You'll Build**: A team of agents (researcher, analyst, writer) working together.

**Checkpoint Questions**:
1. How do agents know when to speak?
2. What happens when agents disagree?
3. When is multi-agent better than a single agent?

---

### Lab 3: Stateful Workflows with LangGraph

**Goal**: Build agents with controlled, predictable workflows.

**Key Concepts**:
- **State Graph**: Nodes (actions) connected by edges (transitions)
- **TypedDict State**: Structured data passed between nodes
- **Conditional Edges**: Dynamic routing based on state
- **Human-in-the-Loop**: Checkpoints for human review

**What You'll Build**: A document analysis pipeline with branching logic and approval gates.

**Checkpoint Questions**:
1. When would you use a cycle vs. a linear graph?
2. How do you prevent infinite loops?
3. What information should be stored in state?

---

### Lab 4: Capstone - Build Your Own Agent

**Goal**: Apply everything you've learned to build a complete, functional agent.

**Key Concepts**:
- **Framework Selection**: Choose the right tool for your use case
- **Agent Design**: Define tools, state, and workflow
- **Testing & Iteration**: Validate and refine your agent

**What You'll Build**: Your choice of Code Assistant, Research Agent, Data Analyst, or custom agent.

**Checkpoint Questions**:
1. Why did you choose this framework for your use case?
2. What tools does your agent need to accomplish its goal?
3. How would you extend your agent for production use?

---

## Key Concepts Glossary

### Agent Fundamentals

| Term | Definition |
|------|------------|
| **Agent** | An LLM that can reason and take actions via tools |
| **Tool** | A function the agent can call (API, search, calculator) |
| **ReAct** | Reasoning + Acting pattern: think, act, observe, repeat |
| **Chain** | A sequence of LLM calls, fixed order |
| **Graph** | A flexible workflow with conditional paths |

### LangGraph Specific

| Term | Definition |
|------|------------|
| **State** | TypedDict holding all workflow data |
| **Node** | A function that transforms state |
| **Edge** | Connection between nodes |
| **Conditional Edge** | Edge that routes based on state |
| **Checkpoint** | Saved state for resumption or human review |
| **START/END** | Special nodes marking workflow boundaries |

### Multi-Agent

| Term | Definition |
|------|------------|
| **Orchestrator** | Agent that coordinates other agents |
| **Specialist** | Agent focused on one domain/task |
| **Handoff** | Passing control from one agent to another |
| **Group Chat** | Multi-agent conversation pattern |
| **Round Robin** | Agents speak in fixed order |

### Protocols

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - connects agents to tools/data |
| **A2A** | Agent-to-Agent Protocol - inter-agent communication |
| **Agent Card** | JSON document describing agent capabilities (A2A) |

---

## Common Pitfalls & Solutions

### 1. "Agent keeps looping forever"
**Cause**: No termination condition or unclear goal.
**Solution**: Add max iterations, clear success criteria, and explicit END conditions.

```python path=null start=null
# Bad: No clear end
while True:
    result = agent.run(task)

# Good: Clear termination
for i in range(max_iterations):
    result = agent.run(task)
    if result.status == "complete":
        break
```

### 2. "Agent isn't using the right tool"
**Cause**: Tool descriptions are unclear.
**Solution**: Write detailed, specific tool descriptions.

```python path=null start=null
# Bad: Vague description
@tool
def search(query: str):
    """Search for information."""
    
# Good: Specific description
@tool  
def search_recent_news(query: str):
    """Search news articles from the last 7 days. 
    Use for current events, recent announcements, or breaking news.
    NOT for historical facts or general knowledge."""
```

### 3. "State isn't updating correctly"
**Cause**: Returning new dict instead of updating existing state.
**Solution**: Return only changed fields (LangGraph merges automatically).

```python path=null start=null
# Bad: Overwrites entire state
def my_node(state):
    return {"messages": state["messages"] + [new_msg]}

# Good: Uses reducer properly (if defined)
def my_node(state):
    return {"messages": [new_msg]}  # Will be appended if using add_messages
```

### 4. "API rate limit errors"
**Cause**: Too many rapid requests.
**Solution**: Add delays, use exponential backoff, or batch requests.

```python path=null start=null
import time
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(min=1, max=60))
def call_api_with_retry(prompt):
    return llm.invoke(prompt)
```

### 5. "Agent output is inconsistent"
**Cause**: Temperature too high or prompt too vague.
**Solution**: Lower temperature for determinism, add output format instructions.

```python path=null start=null
# For consistent outputs
llm = ChatOpenAI(temperature=0)

# Add format instructions
prompt = """Analyze this document and respond in JSON:
{
    "summary": "...",
    "key_points": ["...", "..."],
    "sentiment": "positive|negative|neutral"
}"""
```

---

## Framework Decision Guide

When should you use which framework?

### Use LangChain (Lab 1) When:
- ✅ Building simple tool-using agents
- ✅ Quick prototyping
- ✅ Straightforward Q&A or RAG
- ❌ Complex multi-step workflows

### Use AutoGen & CrewAI (Lab 2) When:
- ✅ Need multiple specialized agents
- ✅ Want agents to debate/critique each other
- ✅ Building agent "teams" with roles
- ❌ Need fine-grained workflow control

### Use LangGraph (Lab 3) When:
- ✅ Need controlled, predictable workflows
- ✅ Require human-in-the-loop approvals
- ✅ Building stateful, resumable processes
- ✅ Want visual representation of logic
- ❌ Simple one-shot tasks

### Use SmolAgents When:
- ✅ Want minimal dependencies
- ✅ Prefer code-first approach
- ✅ Building in HuggingFace ecosystem
- See: [SmolAgents Guide](SmolAgents_Guide.md)

### Use Google ADK When:
- ✅ Deploying to Google Cloud
- ✅ Need production-ready infrastructure
- ✅ Want managed agent hosting
- See: [Google ADK Guide](Google_ADK_Guide.md)

### Use A2A Protocol When:
- ✅ Agents from different frameworks need to talk
- ✅ Enterprise multi-vendor environments
- ✅ Cross-organization agent systems
- See: [A2A Protocol Guide](A2A_Protocol_Guide.md)

---

## Using the Utils Package

The repository includes a `utils/` package with convenience helpers for LLM initialization and model configuration. **The labs do not require it** — each notebook sets up its own LLM directly — but you can optionally use it to reduce boilerplate:

```python path=null start=null
# Optional: use utils helpers instead of manual ChatOpenAI() setup
import sys
sys.path.insert(0, "../..")

from utils import (
    load_environment,       # Load .env and validate keys
    get_langchain_llm,      # Get configured LLM for LangChain
    get_autogen_config,     # Get config for AutoGen
)

load_environment()
llm = get_langchain_llm("gpt-4o-mini", temperature=0)
```

See [Understanding Utils Package](Understanding_Utils_Package.md) for details.

---

## Tips for Success

1. **Start Simple**: Get basic version working before adding complexity
2. **Print Everything**: Add logging to understand agent reasoning
3. **Test Incrementally**: Test each node/tool before combining
4. **Read Error Messages**: They often tell you exactly what's wrong
5. **Use Playground First**: Test prompts in ChatGPT before coding
6. **Save API Calls**: Cache results during development

---

## Getting Help

- **During Workshop**: Raise your hand, use chat
- **After Workshop**: 
  - LangChain Discord: discord.gg/langchain
  - AutoGen Discord: discord.gg/autogen
  - Stack Overflow: tag with framework name

---

## Next Steps After Workshop

1. **Build Something Real**: Apply patterns to your own problem
2. **Explore Streaming**: Add real-time output to your agents
3. **Add Observability**: Try LangSmith or similar tools
4. **Study Security**: Learn about prompt injection defenses
5. **Try Other Frameworks**: Explore SmolAgents, ADK, CrewAI
6. **Read the Docs**: Each framework has extensive documentation

Good luck, and enjoy building agents! 🤖

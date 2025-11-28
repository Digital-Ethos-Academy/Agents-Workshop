# Session 1: Agent Foundations

**Duration:** 3 hours
**Format:** ~80% hands-on, ~20% lecture

## Session Overview

In this session, you'll learn the fundamentals of AI agents and build agents using multiple frameworks. By the end, you'll have working agents with custom tools, memory, and multi-agent collaboration.

---

## Agenda

| Time | Activity | Description |
|------|----------|-------------|
| 0:00-0:30 | Introduction to AI Agents | ReAct loop, tool use, when to use agents |
| 0:30-1:15 | **Lab 1: LangChain Agents** | Build tool-using agent with custom tools and memory |
| 1:15-1:30 | Break | - |
| 1:30-1:45 | Multi-Agent Systems Intro | Patterns: sequential, hierarchical, collaborative |
| 1:45-2:30 | **Lab 2: AutoGen & CrewAI** | Build multi-agent systems, compare approaches |
| 2:30-3:00 | Framework Comparison | When to use what, trade-offs, Q&A |

---

## Learning Objectives

By the end of Session 1, you will be able to:

1. **Explain** the ReAct (Reason-Act-Observe) loop that powers AI agents
2. **Build** single agents with LangChain using custom tools
3. **Implement** conversational memory in agents
4. **Debug** agent behavior using verbose mode and tracing
5. **Construct** multi-agent systems with AutoGen and CrewAI
6. **Compare** frameworks and understand their trade-offs

---

## Key Concepts

### What is an AI Agent?

An AI agent is an LLM-powered system that can:
- **Reason** about a task and plan steps
- **Act** by using tools (APIs, databases, code execution)
- **Observe** the results and adjust its approach
- **Iterate** until the task is complete

### The ReAct Loop

```
┌─────────────────────────────────────────┐
│                                         │
│   User Query                            │
│       │                                 │
│       ▼                                 │
│   ┌───────────┐                         │
│   │  Reason   │ ◄── What should I do?   │
│   └─────┬─────┘                         │
│         │                               │
│         ▼                               │
│   ┌───────────┐                         │
│   │   Act     │ ◄── Call a tool         │
│   └─────┬─────┘                         │
│         │                               │
│         ▼                               │
│   ┌───────────┐                         │
│   │  Observe  │ ◄── Process result      │
│   └─────┬─────┘                         │
│         │                               │
│         ▼                               │
│   Done? ─── No ──► Loop back to Reason  │
│     │                                   │
│    Yes                                  │
│     │                                   │
│     ▼                                   │
│   Final Response                        │
│                                         │
└─────────────────────────────────────────┘
```

### When to Use Agents

**Good Use Cases:**
- Tasks requiring multiple steps with decisions
- Dynamic tool selection based on context
- Complex reasoning with external data
- Tasks where the path isn't predetermined

**Avoid Agents When:**
- The workflow is fixed and predictable
- Simple input → output transformations
- Real-time latency is critical
- You need 100% deterministic behavior

### Multi-Agent Patterns

1. **Sequential**: Agents work in a pipeline (Agent A → Agent B → Agent C)
2. **Hierarchical**: Manager agent delegates to worker agents
3. **Collaborative**: Agents work together, discussing and refining

---

## Framework Overview

### LangChain
- **Best for:** Single agents with tools
- **Strengths:** Extensive tool ecosystem, good debugging
- **Approach:** ReAct loop with customizable prompts

### AutoGen
- **Best for:** Conversational multi-agent systems
- **Strengths:** Code execution, human-in-the-loop
- **Approach:** Message-passing between agents

### CrewAI
- **Best for:** Role-based collaboration
- **Strengths:** Intuitive role/task/crew abstractions
- **Approach:** Agents with defined roles work on tasks

---

## Labs Overview

### Lab 1: LangChain Agents (~45 min)

Build a research assistant agent with:
- Custom tools (web search, calculator, Wikipedia)
- Conversational memory
- Verbose debugging

**Key Learnings:**
- Creating tools with `@tool` decorator
- Binding tools to LLMs
- Using `create_react_agent` for ReAct loop
- Adding memory with `ConversationBufferMemory`

### Lab 2: AutoGen & CrewAI (~45 min)

Build the same multi-agent system in both frameworks:
- Research analyst agent
- Writer agent
- Critic agent

**Key Learnings:**
- AutoGen's `AssistantAgent` and `UserProxyAgent`
- CrewAI's Agent/Task/Crew pattern
- Comparing conversation flow vs. role-based approaches

---

## Prerequisites Checklist

Before starting the labs, ensure you have:

- [ ] Python 3.10+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with API keys:
  - [ ] `OPENAI_API_KEY` (required)
  - [ ] `TAVILY_API_KEY` (for web search)

### Verify Installation

```bash
python -c "from langchain_openai import ChatOpenAI; print('LangChain OK')"
python -c "import autogen; print('AutoGen OK')"
python -c "from crewai import Agent; print('CrewAI OK')"
```

---

## Troubleshooting

### Common Issues

**Issue:** `TAVILY_API_KEY` not found
- **Solution:** Get a free key at [tavily.com](https://tavily.com) and add to `.env`

**Issue:** Agent loops infinitely
- **Solution:** Add `max_iterations` parameter or adjust stopping conditions

**Issue:** Import errors for frameworks
- **Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`

**Issue:** OpenAI rate limits
- **Solution:** Add delays between calls or use `max_iterations` to limit agent steps

---

## Next Session Preview

In Session 2, you'll learn:
- LangGraph for stateful workflows
- Conditional routing and cycles
- Human-in-the-loop patterns
- Build your own capstone agent

---

## Resources

- [LangChain Agents Documentation](https://python.langchain.com/docs/modules/agents/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)

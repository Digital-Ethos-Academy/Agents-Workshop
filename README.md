# Crafting Custom Agents Workshop

Welcome to the Crafting Custom Agents Workshop! This 6-hour intensive workshop teaches you how to build AI agents using multiple frameworks, understand their trade-offs, and choose the right tool for your use case.

## Workshop Overview

**Duration:** 6 hours (2 sessions × 3 hours)
**Format:** ~80% hands-on labs, ~20% lecture
**Prerequisites:** Python experience (1-3 years), familiarity with LLMs and APIs

### What You'll Learn

- Understand AI agent fundamentals: ReAct loop, tool use, memory
- Build single agents with LangChain (custom tools, memory, debugging)
- Create multi-agent systems with AutoGen and CrewAI
- Implement stateful workflows with LangGraph
- Compare frameworks and know when to use each one
- Build production-ready agents for real-world use cases

### What You'll Build

By the end of this workshop, you will have built agents using multiple frameworks and completed a **Capstone Project** where you choose your preferred framework to build an agent for a real use case (code assistant, research agent, data analyst, etc.).

---

## Agenda

### Session 1: Foundations (3 hours)

| Time | Activity | Description |
|------|----------|-------------|
| 0:00-0:30 | Introduction to AI Agents | ReAct loop, tool use, when to use agents |
| 0:30-1:15 | **Lab 1: LangChain Agents** | Build tool-using agent with custom tools and memory |
| 1:15-1:30 | Break | - |
| 1:30-1:45 | Multi-Agent Systems Intro | Patterns: sequential, hierarchical, collaborative |
| 1:45-2:30 | **Lab 2: AutoGen & CrewAI** | Build multi-agent systems, compare approaches |
| 2:30-3:00 | Framework Comparison | When to use what, trade-offs, Q&A |

### Session 2: Advanced (3 hours)

| Time | Activity | Description |
|------|----------|-------------|
| 0:00-0:30 | Advanced Frameworks | LangGraph, SmolAgents demo, ADK overview |
| 0:30-1:15 | **Lab 3: LangGraph Workflows** | Build stateful agent with conditional routing |
| 1:15-1:30 | Break | - |
| 1:30-1:45 | Framework Selection Guide | Decision framework, SmolAgents demo |
| 1:45-2:30 | **Lab 4: Capstone** | Build your own agent with framework of choice |
| 2:30-3:00 | Demo & Wrap-up | Participants demo their agents |

---

## Repository Structure

```
Agents-Workshop/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .env.example                   # API key template
├── check_environment.py           # Environment verification script
├── utils/                         # Shared utilities (LLM helpers, model configs)
├── Labs/
│   ├── Session_1/
│   │   ├── README_Session_1.md    # Session 1 guide
│   │   ├── Lab_1_LangChain_Agents.ipynb
│   │   └── Lab_2_AutoGen_and_CrewAI.ipynb
│   └── Session_2/
│       ├── README_Session_2.md    # Session 2 guide
│       ├── Lab_3_LangGraph_Workflows.ipynb
│       └── Lab_4_Capstone_Build_Your_Agent.ipynb
├── Solutions/                     # Reference implementations
│   └── lab4_capstone_compliance_agent.py  # Capstone example
├── Slides/                        # Presentation decks
└── Supporting_Materials/
    ├── Environment_Setup_Guide.md
    ├── STUDENT_GUIDE.md           # Comprehensive learner guide
    ├── INSTRUCTOR_GUIDE.md        # Teaching tips & rubrics
    ├── SmolAgents_Guide.md        # SmolAgents deep-dive
    ├── Google_ADK_Guide.md        # Google ADK documentation
    ├── A2A_Protocol_Guide.md      # Agent-to-Agent protocol guide
    └── Understanding_Utils_Package.md
```

---

## Getting Started

### 1. Prerequisites

- **Python 3.10+**
- **VS Code** or your preferred IDE
- **Git** for version control
- **OpenAI API Key** (required)
- **Tavily API Key** (for web search tools - free tier available)

### 2. Clone the Repository

```bash
git clone https://github.com/Digital-Ethos-Academy/Agents-Workshop.git
cd Agents-Workshop
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure API Keys

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

### 6. Verify Installation

Run the environment checker:

```bash
python check_environment.py
```

Or verify manually:

```bash
python -c "from langchain_openai import ChatOpenAI; print('LangChain OK')"
python -c "import autogen; print('AutoGen OK')"
python -c "from crewai import Agent; print('CrewAI OK')"
```

---

## API Cost Estimates

This workshop uses OpenAI APIs. Estimated costs per lab (using `gpt-4o-mini`):

| Lab | Estimated Cost | Notes |
|-----|---------------|-------|
| Lab 1 | $0.10 - $0.30 | Basic tool use, few iterations |
| Lab 2 | $0.15 - $0.40 | Multi-agent conversations |
| Lab 3 | $0.20 - $0.50 | State graph with multiple nodes |
| Lab 4 | $0.40 - $1.00 | Complex workflows, more tokens |
| **Total** | **$0.85 - $2.20** | Conservative estimate |

**Tips to minimize costs:**
- Use `gpt-4o-mini` for development (10-20x cheaper than `gpt-4o`)
- Reuse cached results during iteration
- Set `max_tokens` to reasonable limits

---

## Framework Overview

### Frameworks Covered

| Framework | Best For | Key Strength |
|-----------|----------|--------------|
| **LangChain** | Single agents with tools | Extensive tool ecosystem, ReAct loop |
| **AutoGen** | Conversational multi-agent | Code execution, human-in-the-loop |
| **CrewAI** | Role-based collaboration | Intuitive role/task/crew abstractions |
| **LangGraph** | Complex stateful workflows | Conditional routing, cycles, checkpoints |
| **SmolAgents** | Lightweight agents | Simple, minimal overhead |
| **Google ADK** | Google ecosystem | Production deployment, Vertex AI |
| **A2A Protocol** | Agent interoperability | Cross-framework communication standard |

### Decision Framework

Choose your framework based on:

1. **Single vs. Multi-Agent**: LangChain for single, AutoGen/CrewAI for multi
2. **Conversation vs. Workflow**: AutoGen for chat, LangGraph for DAGs
3. **Simplicity vs. Control**: SmolAgents for simple, LangGraph for complex
4. **Ecosystem**: ADK if heavily invested in Google Cloud

---

## Labs Overview

### Lab 1: LangChain Agents
Deep dive into LangChain agent construction. Create custom tools with the `@tool` decorator, add conversational memory, and debug agent behavior with verbose mode.

### Lab 2: AutoGen & CrewAI
Build the same multi-agent problem with both frameworks. Compare AutoGen's conversational approach with CrewAI's role-based collaboration.

### Lab 3: LangGraph Workflows
Master stateful agent workflows. Build agents with StateGraph, conditional routing, cycles, and human-in-the-loop checkpoints.

### Lab 4: Capstone - Build Your Agent
Choose your preferred framework and build an agent for a real use case:
- Code Assistant Agent
- Research Agent
- Data Analyst Agent
- Customer Support Agent
- Or your own idea!

---

## Key Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [SmolAgents Guide](https://huggingface.co/docs/smolagents/)
- [Google ADK](https://google.github.io/adk-docs/)

---

## Troubleshooting

### Common Issues

**Issue:** `Tavily` authentication error
- **Solution:** Ensure `TAVILY_API_KEY` is set in your `.env` file. Get a free key at [tavily.com](https://tavily.com)

**Issue:** AutoGen agents stuck in infinite loop
- **Solution:** Use `max_consecutive_auto_reply` parameter or adjust termination conditions

**Issue:** `ModuleNotFoundError` for any framework
- **Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`

See `Supporting_Materials/Environment_Setup_Guide.md` for detailed troubleshooting.

---

## Student Resources

For a comprehensive learning guide including:
- Lab-by-lab walkthrough
- Key concepts glossary
- Common pitfalls & solutions
- Framework decision guide

See **[Supporting_Materials/STUDENT_GUIDE.md](Supporting_Materials/STUDENT_GUIDE.md)**

---

## Next Steps After Workshop

Once you've completed the workshop, consider exploring:

### 1. **Streaming & Async**
Add real-time output streaming to your agents for better UX.

### 2. **Deployment**
Deploy your agents to production using:
- FastAPI for REST endpoints
- Google Cloud Run for serverless
- Modal or Railway for quick deployments

### 3. **Security**
Learn about prompt injection defenses, input validation, and secure tool design.

### 4. **Observability**
Add monitoring with [LangSmith](https://smith.langchain.com/) or similar tools to debug and improve agents.

### 5. **Explore More Frameworks**
- **SmolAgents**: See [Supporting_Materials/SmolAgents_Guide.md](Supporting_Materials/SmolAgents_Guide.md)
- **Google ADK**: See [Supporting_Materials/Google_ADK_Guide.md](Supporting_Materials/Google_ADK_Guide.md)
- **A2A Protocol**: See [Supporting_Materials/A2A_Protocol_Guide.md](Supporting_Materials/A2A_Protocol_Guide.md)

### 6. **Enterprise Interoperability**
Learn the A2A (Agent-to-Agent) Protocol for building agents that communicate across frameworks and organizations.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute these materials with attribution.

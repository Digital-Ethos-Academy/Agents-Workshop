# Agents Workshop Solutions

This directory contains reference implementations for all workshop labs.

## Solution Files

### Lab 1: LangChain Research Agent
- **File:** `lab1_langchain_research_agent.py`
- **Description:** Complete research assistant with tools for search, notes, calculation, and summarization.
- **Key Features:**
  - Custom tools with `@tool` decorator
  - Conversational memory
  - ReAct pattern implementation

### Lab 2: Multi-Agent Systems

#### AutoGen Version
- **File:** `lab2_autogen_research_team.py`
- **Description:** Conversational multi-agent research team.
- **Agents:** Researcher, Writer, Critic
- **Key Features:**
  - GroupChat for agent collaboration
  - Round-robin speaker selection
  - Automatic termination

#### CrewAI Version
- **File:** `lab2_crewai_research_team.py`
- **Description:** Role-based research crew.
- **Agents:** Research Analyst, Content Writer, Content Reviewer
- **Key Features:**
  - Task dependencies with context
  - Sequential process
  - Clear role/goal/backstory pattern

### Lab 3: LangGraph Document Workflow
- **File:** `lab3_langgraph_document_workflow.py`
- **Description:** Stateful document processing workflow with conditional routing.
- **Key Features:**
  - TypedDict state management
  - Conditional routing based on urgency
  - Multiple processing nodes
  - Checkpointing with MemorySaver

## Running the Solutions

1. Ensure your virtual environment is activated:
   ```bash
   source .venv/bin/activate  # macOS/Linux
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Run any solution:
   ```bash
   python Solutions/lab1_langchain_research_agent.py
   python Solutions/lab2_autogen_research_team.py
   python Solutions/lab2_crewai_research_team.py
   python Solutions/lab3_langgraph_document_workflow.py
   ```

## Framework Comparison Summary

| Aspect | LangChain | AutoGen | CrewAI | LangGraph |
|--------|-----------|---------|--------|-----------|
| Approach | ReAct agent | Conversations | Role-based | State graph |
| Best for | Single agents | Dynamic chat | Pipelines | Complex workflows |
| Control | Medium | Low | Medium | High |
| Complexity | Low | Medium | Low | High |

## Notes

- These are reference implementations - there may be multiple valid approaches
- In production, add proper error handling and logging
- Configure API rate limiting for production use
- Consider cost optimization (e.g., using smaller models where appropriate)

## Extending the Solutions

### Adding Real Search
Replace mock search with Tavily:
```python
from langchain_community.tools.tavily_search import TavilySearchResults
search_tool = TavilySearchResults(max_results=5)
```

### Adding Persistence
For LangGraph, use SQLite checkpointer:
```python
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver.from_conn_string("checkpoints.db")
```

### Adding Tracing
Enable LangSmith for debugging:
```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"
```

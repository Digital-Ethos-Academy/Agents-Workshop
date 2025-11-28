# Crafting Custom Agents - Quick Reference

**Keep this open during the workshop!**

---

## 🚀 Getting Started

```bash
# Activate environment (if not already active)
source .venv/bin/activate

# Open notebooks
jupyter lab
# OR
code Labs/Session_1/Lab_1_LangChain_Agents.ipynb
```

---

## 📁 Workshop Structure

| Session | Lab | Topic | Notebook |
|---------|-----|-------|----------|
| 1 | Lab 1 | LangChain Agents | `Labs/Session_1/Lab_1_LangChain_Agents.ipynb` |
| 1 | Lab 2 | AutoGen & CrewAI | `Labs/Session_1/Lab_2_AutoGen_and_CrewAI.ipynb` |
| 2 | Lab 3 | LangGraph Workflows | `Labs/Session_2/Lab_3_LangGraph_Workflows.ipynb` |
| 2 | Lab 4 | Capstone Project | `Labs/Session_2/Lab_4_Capstone_Build_Your_Agent.ipynb` |

---

## 🔧 Key Imports

### LangChain (Lab 1)
```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain import hub
```

### AutoGen (Lab 2)
```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
```

### CrewAI (Lab 2)
```python
from crewai import Agent, Task, Crew, Process
```

### LangGraph (Labs 3 & 4)
```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Literal
```

---

## 🛠️ Creating Tools

```python
from langchain.tools import tool

@tool
def my_tool(query: str) -> str:
    """Description of what this tool does.
    
    Args:
        query: What the input represents
    """
    # Your implementation
    return f"Result for {query}"
```

---

## 📊 LangGraph State Pattern

```python
from typing import TypedDict

class MyState(TypedDict):
    """Define your workflow state."""
    input: str
    result: str
    step: int

def my_node(state: MyState) -> dict:
    """Process state and return updates."""
    return {"result": "processed", "step": state["step"] + 1}

# Build graph
graph = StateGraph(MyState)
graph.add_node("process", my_node)
graph.add_edge(START, "process")
graph.add_edge("process", END)
app = graph.compile()
```

---

## 🔄 Common Patterns

### ReAct Loop (LangChain)
```
User Query → Reason → Act (tool) → Observe → Repeat or Answer
```

### Multi-Agent Chat (AutoGen)
```python
groupchat = GroupChat(agents=[agent1, agent2], messages=[], max_round=10)
manager = GroupChatManager(groupchat=groupchat)
agent1.initiate_chat(manager, message="Start task")
```

### Conditional Routing (LangGraph)
```python
def router(state: MyState) -> Literal["path_a", "path_b"]:
    if state["condition"]:
        return "path_a"
    return "path_b"

graph.add_conditional_edges("node", router, {"path_a": "a", "path_b": "b"})
```

---

## 💡 Framework Cheat Sheet

| Need | Use |
|------|-----|
| Single agent + tools | **LangChain** |
| Agents chatting/debating | **AutoGen** |
| Role-based pipeline | **CrewAI** |
| Complex workflow with state | **LangGraph** |
| Human approval needed | **LangGraph** (interrupt_before) |

---

## ⚠️ Common Mistakes

| Problem | Solution |
|---------|----------|
| Agent loops forever | Add `max_iterations=10` |
| Tool not being called | Improve tool description |
| State not updating | Return dict with changed fields only |
| Import error | Run `source .venv/bin/activate` |
| API rate limit | Wait 60s or use `gpt-4o-mini` |

---

## 🔍 Debugging

```python
# LangChain - verbose mode
agent = AgentExecutor(..., verbose=True)

# LangGraph - print state
for event in app.stream(initial_state):
    print(event)

# Check API key
import os
print(os.getenv("OPENAI_API_KEY")[:10] + "...")
```

---

## 💰 Cost-Saving Tips

- Use `gpt-4o-mini` for development (10-20x cheaper)
- Set `max_tokens` to limit responses
- Cache results during iteration
- Estimated workshop cost: **$1-3 total**

---

## 📚 Solutions & Help

| Resource | Location |
|----------|----------|
| Lab 1 Solution | `Solutions/lab1_langchain_research_agent.py` |
| Lab 2 Solutions | `Solutions/lab2_autogen_research_team.py` |
| Lab 3 Solution | `Solutions/lab3_langgraph_document_workflow.py` |
| Capstone Example | `Solutions/lab4_capstone_compliance_agent.py` |
| Full Student Guide | `Supporting_Materials/STUDENT_GUIDE.md` |

---

## 🆘 Quick Fixes

```bash
# Restart kernel if stuck
# In Jupyter: Kernel → Restart

# Reinstall packages
pip install -r requirements.txt

# Check environment
python check_environment.py

# Verify API connection
python -c "from langchain_openai import ChatOpenAI; llm = ChatOpenAI(); print(llm.invoke('Hi'))"
```

---

## 📝 Capstone Ideas

1. **Code Assistant** - Analyze and improve code
2. **Research Agent** - Search and summarize topics
3. **Data Analyst** - Process CSV and generate insights
4. **Customer Support** - Answer questions from knowledge base
5. **Document Reviewer** - Flag compliance issues (see reference solution)

---

**Questions?** Raise your hand or ask in chat!

**After Workshop:** See `README.md` → "Next Steps After Workshop"

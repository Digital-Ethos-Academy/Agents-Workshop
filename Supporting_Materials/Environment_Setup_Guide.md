# Agents Workshop Environment Setup Guide

This guide helps you set up your development environment for the Crafting Custom Agents Workshop.

## Prerequisites

- **Python 3.10+**
- **VS Code** or your preferred IDE
- **Git** for version control
- **API Keys** (see below)

---

## Step 1: Install Python

### macOS
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

### Windows
1. Download from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify in PowerShell: `python --version`

### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv

# Verify
python3 --version
```

---

## Step 2: Clone the Repository

```bash
git clone https://github.com/Digital-Ethos-Academy/Agents-Workshop.git
cd Agents-Workshop
```

---

## Step 3: Create Virtual Environment

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the start of your terminal prompt.

---

## Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

This installs:
- LangChain and LangGraph
- AutoGen
- CrewAI
- OpenAI and Anthropic clients
- Tavily (web search)
- And supporting libraries

### Verify Installation
```bash
python -c "from langchain_openai import ChatOpenAI; print('LangChain OK')"
python -c "import autogen; print('AutoGen OK')"
python -c "from crewai import Agent; print('CrewAI OK')"
python -c "from langgraph.graph import StateGraph; print('LangGraph OK')"
```

---

## Step 5: Configure API Keys

### Create .env file
```bash
cp .env.example .env
```

### Edit .env with your keys
```env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-...

# Required for web search: Tavily API Key
TAVILY_API_KEY=tvly-...

# Optional: Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-...
```

### Getting API Keys

#### OpenAI (Required)
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign in or create account
3. Navigate to API Keys
4. Create new secret key

#### Tavily (Required for web search)
1. Go to [tavily.com](https://tavily.com)
2. Sign up for free account
3. Get your API key from dashboard

#### Anthropic (Optional)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in or create account
3. Navigate to API Keys
4. Create new key

---

## Step 6: Configure VS Code (Recommended)

### Install Extensions
1. Open VS Code
2. Go to Extensions (Cmd/Ctrl+Shift+X)
3. Install:
   - **Python**
   - **Jupyter**
   - **Python Environment Manager** (optional)

### Configure Python Interpreter
1. Open Command Palette (Cmd/Ctrl+Shift+P)
2. Type "Python: Select Interpreter"
3. Choose the interpreter from your `.venv`

### Enable Notebook Support
1. Open any `.ipynb` file
2. VS Code will prompt to install Jupyter support
3. Accept and wait for installation

---

## Step 7: Test Your Setup

### Test Basic Setup
```python
# Run this in Python or a notebook
import os
from dotenv import load_dotenv

load_dotenv()

# Check API keys
assert os.getenv("OPENAI_API_KEY"), "OpenAI key missing"
print("OpenAI key configured!")

if os.getenv("TAVILY_API_KEY"):
    print("Tavily key configured!")
else:
    print("Warning: Tavily key not set (web search won't work)")
```

### Test LangChain
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke("Say hello!")
print(response.content)
```

### Test AutoGen
```python
from autogen import AssistantAgent
import os

config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]}
agent = AssistantAgent(name="Test", llm_config=config)
print("AutoGen agent created successfully!")
```

### Test CrewAI
```python
from crewai import Agent

agent = Agent(
    role="Test Agent",
    goal="Testing setup",
    backstory="A test agent"
)
print("CrewAI agent created successfully!")
```

### Test LangGraph
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    value: str

graph = StateGraph(State)
graph.add_node("test", lambda x: {"value": "success"})
graph.set_entry_point("test")
graph.add_edge("test", END)
app = graph.compile()

result = app.invoke({"value": "start"})
print(f"LangGraph test: {result['value']}")
```

---

## Troubleshooting

### Import errors for any framework
```bash
# Make sure venv is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### AutoGen "config_list" errors
```python
# Use this format for config
config = {
    "config_list": [{
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY")
    }]
}
```

### CrewAI execution errors
```bash
# CrewAI sometimes needs specific versions
pip install crewai==0.30.0 --upgrade
```

### LangGraph state errors
- Ensure state is defined as `TypedDict`
- All node functions must return dict updates

### Tavily "authentication error"
1. Verify key in `.env` file
2. No spaces around the `=` sign
3. Try regenerating key at tavily.com

### Jupyter kernel not found
```bash
# Install ipykernel
pip install ipykernel

# Register kernel
python -m ipykernel install --user --name=agents-workshop
```

### Rate limiting errors
- OpenAI has rate limits on free tier
- Add delays between API calls:
```python
import time
time.sleep(1)  # Wait 1 second between calls
```

---

## Quick Reference

### Activate Environment
```bash
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\Activate.ps1  # Windows
```

### Run Jupyter Notebook
```bash
jupyter notebook
# Or in VS Code, just open .ipynb files
```

### Run Python Scripts
```bash
python Solutions/lab1_langchain_research_agent.py
```

### Check Installed Packages
```bash
pip list | grep -E "langchain|autogen|crewai|langgraph"
```

---

## Framework Versions (Tested)

These versions are known to work together:
```
langchain>=0.2.0
langchain-openai>=0.1.0
langgraph>=0.1.0
pyautogen>=0.2.0
crewai>=0.30.0
```

---

## Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Make sure virtual environment is activated
4. Check API keys are correctly set
5. Ask your instructor for assistance

---

## Useful Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [CrewAI Documentation](https://docs.crewai.com/)

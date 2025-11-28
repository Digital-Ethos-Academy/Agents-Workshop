# Google Agent Development Kit (ADK) Guide

Google ADK is a production-ready framework for building, deploying, and managing AI agents. It's designed for enterprise-scale deployments, particularly within the Google Cloud ecosystem.

## Overview

### What is Google ADK?

The Agent Development Kit (ADK) is an open-source framework from Google for developing and deploying AI agents. While optimized for Gemini and Google Cloud, it's model-agnostic and deployment-agnostic.

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Philosophy** | Production-ready, enterprise-grade |
| **Deployment** | Cloud Run, Agent Engine, GKE, Docker |
| **Best For** | Production systems on Google Cloud |
| **Key Strength** | Scalable deployment and observability |

### When to Use Google ADK

✅ **Use ADK when:**
- Building for Google Cloud production deployment
- You need enterprise-grade observability and tracing
- You want native Vertex AI integration
- You need scalable, containerized agents
- You're building for production, not just prototyping

❌ **Consider alternatives when:**
- You're prototyping or learning (→ LangChain, SmolAgents)
- You need complex multi-agent conversations (→ AutoGen)
- You're not using Google Cloud infrastructure
- You want the simplest possible setup

---

## Installation

```bash
# Install ADK
pip install google-adk

# Verify installation
adk --version
```

**Requirements:**
- Python 3.10 or later
- pip for package management

---

## Quick Start

### 1. Create an Agent Project

```bash
# Create a new agent project
adk create my_agent

# This creates:
# my_agent/
#     agent.py      # Main agent code
#     .env          # API keys
#     __init__.py
```

### 2. Configure Your Agent

Edit `my_agent/agent.py`:

```python
from google.adk.agents.llm_agent import Agent

# Define a tool
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.
    
    Args:
        city: The name of the city to get the time for.
    """
    # In production, you'd call a real time API
    import datetime
    return {
        "status": "success",
        "city": city,
        "time": datetime.datetime.now().strftime("%I:%M %p")
    }

# Define the agent
root_agent = Agent(
    model='gemini-1.5-flash',
    name='time_agent',
    description="An agent that tells the current time in cities.",
    instruction="You are a helpful assistant that tells the current time. "
                "Use the 'get_current_time' tool when asked about time.",
    tools=[get_current_time],
)
```

### 3. Set Your API Key

```bash
# Create .env file
echo 'GOOGLE_API_KEY="your-api-key-here"' > my_agent/.env
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Run Your Agent

```bash
# Command-line interface
adk run my_agent

# Web interface (for testing)
adk web --port 8000
```

---

## Core Concepts

### 1. Agent Definition

The core of ADK is the `Agent` class:

```python
from google.adk.agents.llm_agent import Agent

agent = Agent(
    model='gemini-1.5-flash',      # The LLM to use
    name='my_agent',                # Unique identifier
    description='What this agent does',
    instruction='System prompt / behavior instructions',
    tools=[tool1, tool2],           # Available tools
)
```

### 2. Tools

Tools are Python functions that agents can call:

```python
def search_database(query: str, limit: int = 10) -> dict:
    """
    Search the database for records matching the query.
    
    Args:
        query: The search query string.
        limit: Maximum number of results to return.
        
    Returns:
        A dictionary containing search results.
    """
    # Your implementation
    return {"results": [...], "count": 5}

def send_notification(user_id: str, message: str) -> dict:
    """
    Send a notification to a user.
    
    Args:
        user_id: The ID of the user to notify.
        message: The notification message.
    """
    # Your implementation
    return {"status": "sent", "user_id": user_id}
```

### 3. Using Other LLM Providers

ADK supports multiple providers:

```python
from google.adk.agents.llm_agent import Agent

# Using OpenAI
agent = Agent(
    model='openai/gpt-4o-mini',
    name='openai_agent',
    # ... rest of config
)

# Using Anthropic
agent = Agent(
    model='anthropic/claude-3-5-sonnet-20241022',
    name='claude_agent',
    # ... rest of config
)
```

---

## Practical Examples

### Example 1: Financial Data Agent

```python
from google.adk.agents.llm_agent import Agent
import json

def get_stock_price(symbol: str) -> dict:
    """
    Get the current stock price for a symbol.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'GOOGL')
    """
    # Mock implementation - replace with real API
    prices = {"AAPL": 178.50, "GOOGL": 141.25, "MSFT": 378.90}
    if symbol in prices:
        return {"symbol": symbol, "price": prices[symbol], "currency": "USD"}
    return {"error": f"Unknown symbol: {symbol}"}

def calculate_portfolio_value(holdings: str) -> dict:
    """
    Calculate total portfolio value.
    
    Args:
        holdings: JSON string of holdings like '{"AAPL": 10, "GOOGL": 5}'
    """
    try:
        portfolio = json.loads(holdings)
        # Mock calculation
        total = sum(qty * 150 for qty in portfolio.values())  # Simplified
        return {"total_value": total, "currency": "USD"}
    except json.JSONDecodeError:
        return {"error": "Invalid holdings format"}

root_agent = Agent(
    model='gemini-1.5-flash',
    name='financial_advisor',
    description="A financial data assistant",
    instruction="""You are a financial data assistant. You can:
    1. Look up stock prices
    2. Calculate portfolio values
    Always provide clear, accurate information.""",
    tools=[get_stock_price, calculate_portfolio_value],
)
```

### Example 2: Document Processing Agent

```python
from google.adk.agents.llm_agent import Agent

def classify_document(content: str) -> dict:
    """
    Classify a document by type.
    
    Args:
        content: The document content to classify
    """
    # Simple keyword-based classification
    content_lower = content.lower()
    if "invoice" in content_lower or "payment" in content_lower:
        return {"type": "invoice", "confidence": 0.85}
    elif "contract" in content_lower or "agreement" in content_lower:
        return {"type": "contract", "confidence": 0.90}
    elif "report" in content_lower:
        return {"type": "report", "confidence": 0.80}
    return {"type": "unknown", "confidence": 0.50}

def extract_entities(content: str) -> dict:
    """
    Extract key entities from document content.
    
    Args:
        content: The document content to analyze
    """
    # Simplified extraction - in production use NER
    return {
        "dates": ["2024-01-15"],
        "amounts": ["$10,000"],
        "organizations": ["Acme Corp"],
    }

root_agent = Agent(
    model='gemini-1.5-flash',
    name='document_processor',
    description="Processes and analyzes documents",
    instruction="""You are a document processing assistant for a financial institution.
    Your job is to:
    1. Classify incoming documents
    2. Extract key information
    3. Flag any compliance concerns
    Be thorough and accurate.""",
    tools=[classify_document, extract_entities],
)
```

### Example 3: Multi-Agent Team

ADK supports hierarchical multi-agent systems:

```python
from google.adk.agents.llm_agent import Agent

# Specialist agents
researcher = Agent(
    model='gemini-1.5-flash',
    name='researcher',
    description="Researches and gathers information",
    instruction="You are a research specialist. Gather comprehensive information.",
    tools=[web_search, read_document],
)

analyst = Agent(
    model='gemini-1.5-flash',
    name='analyst',
    description="Analyzes data and provides insights",
    instruction="You are a data analyst. Provide clear insights from data.",
    tools=[calculate_stats, create_chart],
)

# Coordinator agent that delegates to specialists
coordinator = Agent(
    model='gemini-1.5-pro',
    name='coordinator',
    description="Coordinates research and analysis tasks",
    instruction="""You are a team coordinator. 
    Delegate research to the researcher and analysis to the analyst.
    Synthesize their outputs into a cohesive response.""",
    tools=[researcher, analyst],  # Agents can be tools!
)
```

---

## Deployment

### Local Development

```bash
# Run with CLI
adk run my_agent

# Run with web UI
adk web --port 8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY my_agent/ ./my_agent/
CMD ["adk", "run", "my_agent"]
```

### Google Cloud Run

```bash
# Build and deploy
gcloud run deploy my-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Vertex AI Agent Engine

For enterprise deployments, use Agent Engine:

```python
from google.adk.deploy import AgentEngine

# Deploy to Agent Engine
engine = AgentEngine(project_id="your-project")
deployment = engine.deploy(
    agent=root_agent,
    region="us-central1",
    scaling_config={"min_instances": 1, "max_instances": 10}
)
```

---

## Observability

ADK integrates with various observability tools:

### Cloud Trace

```python
from google.adk.observability import enable_tracing

enable_tracing(project_id="your-project")
```

### Logging

```python
from google.adk.observability import configure_logging

configure_logging(level="INFO", format="json")
```

### Third-Party Integrations

ADK supports:
- AgentOps
- Arize AX
- Phoenix (Arize)
- Weights & Biases (Weave)

---

## Comparison with Other Frameworks

| Feature | ADK | LangChain | AutoGen | LangGraph |
|---------|-----|-----------|---------|-----------|
| **Production Ready** | ✅ Native | ✅ With setup | ⚠️ Limited | ✅ With setup |
| **Cloud Deployment** | ✅ Native | Manual | Manual | Manual |
| **Observability** | ✅ Built-in | Add-on | Limited | Add-on |
| **Multi-Agent** | ✅ Hierarchical | Limited | ✅ Native | Manual |
| **Learning Curve** | Medium | Medium | Medium | Steep |

---

## Financial Services Use Cases

ADK is ideal for:

1. **Compliance Automation**: Document classification and review at scale
2. **Customer Service**: Production-grade support agents
3. **Risk Analysis**: Scalable analysis pipelines
4. **Report Generation**: Automated financial reporting

---

## CLI Reference

```bash
# Create a new project
adk create <project_name>

# Run an agent
adk run <project_name>

# Start web interface
adk web --port <port>

# Evaluate agent performance
adk eval <project_name> --test-file tests.json
```

---

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Python Quickstart](https://google.github.io/adk-docs/get-started/python/)
- [GitHub Repository](https://github.com/google/adk-python)
- [Tutorials](https://google.github.io/adk-docs/tutorials/)
- [API Reference](https://google.github.io/adk-docs/api-reference/python/)

---

## Workshop Integration

ADK is mentioned in Session 2 as a production deployment option. While we don't have a dedicated lab (due to time constraints), you can explore ADK for your capstone project if you're interested in production deployment patterns.

### Quick Experiment

```bash
# Install
pip install google-adk

# Create project
adk create my_capstone_agent

# Edit my_capstone_agent/agent.py with your logic

# Run
adk run my_capstone_agent
```

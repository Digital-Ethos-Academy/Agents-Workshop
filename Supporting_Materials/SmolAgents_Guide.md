# SmolAgents Guide

SmolAgents is a lightweight, code-first agent framework from Hugging Face. It takes a unique approach where agents write and execute Python code directly, rather than using structured tool calls.

## Overview

### What is SmolAgents?

SmolAgents is designed around a simple philosophy: **agents should write code**. Instead of structured JSON tool calls, SmolAgents agents generate Python code that directly manipulates tools and data.

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Philosophy** | Code as the action language |
| **Overhead** | Very low - minimal abstractions |
| **Best For** | Prototyping, learning, lightweight tasks |
| **Key Strength** | Transparency and simplicity |

### When to Use SmolAgents

✅ **Use SmolAgents when:**
- You want to prototype quickly
- You need transparency in agent reasoning
- Your task involves data manipulation or calculations
- You're learning about agent architectures
- You want minimal framework overhead

❌ **Consider alternatives when:**
- You need complex multi-agent orchestration (→ AutoGen, CrewAI)
- You need stateful workflows with checkpoints (→ LangGraph)
- You're deploying to production at scale (→ Google ADK)
- You need extensive tool ecosystems (→ LangChain)

---

## Installation

```bash
# Basic installation
pip install smolagents

# With LiteLLM support for multiple providers
pip install smolagents[litellm]
```

---

## Quick Start

### Basic Code Agent

```python
from smolagents import CodeAgent, tool, LiteLLMModel

# Define a custom tool
@tool
def calculate(expression: str) -> float:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: A mathematical expression like "2 + 2" or "15 * 0.15"
    """
    return eval(expression)

# Create the model (uses LiteLLM for provider flexibility)
model = LiteLLMModel(model_id="gpt-4o-mini")

# Create the agent
agent = CodeAgent(
    tools=[calculate],
    model=model,
    max_steps=5
)

# Run the agent
result = agent.run("What is 15% of 250?")
print(result)
```

### How It Works

When you ask "What is 15% of 250?", the agent generates and executes code like:

```python
# Agent's generated code
result = calculate("250 * 0.15")
final_answer(result)
```

This is different from other frameworks where the agent would make a structured tool call. The code-first approach makes the agent's reasoning transparent and debuggable.

---

## Core Concepts

### 1. Tools

Tools in SmolAgents are Python functions decorated with `@tool`:

```python
from smolagents import tool

@tool
def search_web(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: The search query
    """
    # Your implementation here
    return f"Search results for: {query}"

@tool
def save_file(filename: str, content: str) -> str:
    """
    Save content to a file.
    
    Args:
        filename: Name of the file to create
        content: Content to write to the file
    """
    with open(filename, 'w') as f:
        f.write(content)
    return f"Saved to {filename}"
```

### 2. Models

SmolAgents supports multiple LLM providers through LiteLLM:

```python
from smolagents import LiteLLMModel

# OpenAI
model = LiteLLMModel(model_id="gpt-4o-mini")

# Anthropic
model = LiteLLMModel(model_id="claude-3-5-sonnet-20241022")

# Local models via Ollama
model = LiteLLMModel(model_id="ollama/llama3.2")
```

### 3. Agent Types

```python
from smolagents import CodeAgent, ToolCallingAgent

# CodeAgent: Writes and executes Python code
code_agent = CodeAgent(tools=[...], model=model)

# ToolCallingAgent: Uses structured tool calls (like other frameworks)
tool_agent = ToolCallingAgent(tools=[...], model=model)
```

---

## Practical Examples

### Example 1: Data Analysis Agent

```python
from smolagents import CodeAgent, tool, LiteLLMModel
import json

@tool
def load_data(filename: str) -> str:
    """Load JSON data from a file."""
    with open(filename, 'r') as f:
        return json.dumps(json.load(f))

@tool
def calculate_stats(numbers: str) -> str:
    """
    Calculate statistics for a list of numbers.
    
    Args:
        numbers: Comma-separated numbers like "1,2,3,4,5"
    """
    nums = [float(n.strip()) for n in numbers.split(',')]
    return json.dumps({
        "count": len(nums),
        "sum": sum(nums),
        "mean": sum(nums) / len(nums),
        "min": min(nums),
        "max": max(nums)
    })

model = LiteLLMModel(model_id="gpt-4o-mini")
agent = CodeAgent(tools=[load_data, calculate_stats], model=model)

result = agent.run("Calculate the average of 10, 20, 30, 40, 50")
```

### Example 2: Research Agent with Web Search

```python
from smolagents import CodeAgent, tool, LiteLLMModel
from tavily import TavilyClient
import os

@tool
def web_search(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: What to search for
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query, max_results=3)
    return "\n".join([r["content"] for r in results["results"]])

@tool
def summarize_notes(notes: str) -> str:
    """
    Create a summary of research notes.
    
    Args:
        notes: The notes to summarize
    """
    return f"Summary: {notes[:500]}..."

model = LiteLLMModel(model_id="gpt-4o-mini")
agent = CodeAgent(
    tools=[web_search, summarize_notes],
    model=model,
    max_steps=10
)

result = agent.run("Research the benefits of microservices architecture")
```

### Example 3: Code Assistant

```python
from smolagents import CodeAgent, tool, LiteLLMModel
import ast

@tool
def analyze_code(code: str) -> str:
    """
    Analyze Python code for potential issues.
    
    Args:
        code: Python code to analyze
    """
    try:
        tree = ast.parse(code)
        # Count functions, classes, etc.
        functions = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
        classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        return f"Code analysis: {functions} functions, {classes} classes"
    except SyntaxError as e:
        return f"Syntax error: {e}"

@tool
def explain_code(code: str) -> str:
    """
    Return the code for the LLM to explain.
    
    Args:
        code: Code to explain
    """
    return f"Code to explain:\n```python\n{code}\n```"

model = LiteLLMModel(model_id="gpt-4o-mini")
agent = CodeAgent(tools=[analyze_code, explain_code], model=model)

result = agent.run("Analyze this code: def factorial(n): return 1 if n <= 1 else n * factorial(n-1)")
```

---

## Advanced Features

### Memory and Context

```python
from smolagents import CodeAgent, LiteLLMModel

model = LiteLLMModel(model_id="gpt-4o-mini")
agent = CodeAgent(tools=[], model=model)

# First interaction
result1 = agent.run("My name is Alice")

# Agent remembers context for follow-up
result2 = agent.run("What's my name?")
```

### Custom System Prompts

```python
agent = CodeAgent(
    tools=[...],
    model=model,
    system_prompt="""You are a financial analyst assistant. 
    Always be precise with numbers and cite your sources."""
)
```

### Verbose Mode for Debugging

```python
# See the agent's thought process and generated code
agent = CodeAgent(tools=[...], model=model, verbosity_level=2)
result = agent.run("Calculate compound interest")
```

---

## Comparison with Other Frameworks

| Feature | SmolAgents | LangChain | AutoGen | LangGraph |
|---------|------------|-----------|---------|-----------|
| **Approach** | Code generation | Tool calling | Conversations | State graphs |
| **Complexity** | Low | Medium | Medium | High |
| **Multi-agent** | Limited | Limited | Native | Manual |
| **Transparency** | High | Medium | Medium | High |
| **Learning curve** | Easy | Medium | Medium | Steep |
| **Production ready** | Prototype | Yes | Yes | Yes |

---

## Financial Services Use Cases

SmolAgents is particularly useful for:

1. **Transaction Analysis**: Quick data analysis and calculations
2. **Report Generation**: Transparent, auditable code execution
3. **Prototyping**: Fast iteration on agent ideas
4. **Education**: Teaching agent concepts with visible code

---

## Resources

- [SmolAgents Documentation](https://huggingface.co/docs/smolagents/)
- [GitHub Repository](https://github.com/huggingface/smolagents)
- [Hugging Face Blog Post](https://huggingface.co/blog/smolagents)

---

## Workshop Integration

While we don't have a dedicated SmolAgents lab, you can experiment with it during the Capstone project. SmolAgents is mentioned in Session 2 slides as an alternative for lightweight prototyping.

To try SmolAgents in your capstone:

```python
# Install
!pip install smolagents[litellm]

# Quick test
from smolagents import CodeAgent, tool, LiteLLMModel

@tool
def my_tool(input: str) -> str:
    """Your custom tool."""
    return f"Processed: {input}"

model = LiteLLMModel(model_id="gpt-4o-mini")
agent = CodeAgent(tools=[my_tool], model=model)
result = agent.run("Your task here")
```

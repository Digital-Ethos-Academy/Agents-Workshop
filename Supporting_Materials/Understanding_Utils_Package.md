# Understanding the Utils Package

The `utils/` package provides a clean abstraction layer for common workshop tasks. This guide explains what's available and how to extend it.

---

## Why Utils?

Without utils, every notebook starts with:

```python path=null start=null
# Repetitive boilerplate in every notebook
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY")
    
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

With utils:

```python path=null start=null
from utils import load_environment, get_langchain_llm

load_environment()
llm = get_langchain_llm("gpt-4o-mini")
```

**Benefits:**
- Less boilerplate in notebooks
- Consistent configuration across labs
- Centralized model management
- Easier to update when APIs change

---

## Available Functions

### Environment Loading

```python path=null start=null
from utils import load_environment

# Load .env and validate required keys
load_environment()  # Raises error if OPENAI_API_KEY missing
```

### LangChain LLM

```python path=null start=null
from utils import get_langchain_llm

# Basic usage
llm = get_langchain_llm("gpt-4o-mini")

# With options
llm = get_langchain_llm(
    "gpt-4o",
    temperature=0.7,
    max_tokens=2000
)
```

### AutoGen Configuration

```python path=null start=null
from utils import get_autogen_config

# Get config dict for AutoGen agents
config = get_autogen_config("gpt-4o-mini", temperature=0)

# Use in AutoGen
assistant = AssistantAgent(
    "assistant",
    llm_config={"config_list": [config]}
)
```

### Model Constants

```python path=null start=null
from utils import OPENAI_MODELS, ANTHROPIC_MODELS

# Available models
print(OPENAI_MODELS)
# {'gpt-4o': {...}, 'gpt-4o-mini': {...}, ...}

# Check if model exists
if "gpt-4o" in OPENAI_MODELS:
    print("Model available")
```

---

## Package Structure

```
utils/
├── __init__.py      # Public exports
├── environment.py   # Environment loading
├── llm.py           # LLM factory functions
└── models.py        # Model definitions
```

### models.py

Defines available models with metadata:

```python path=null start=null
OPENAI_MODELS = {
    "gpt-4o": {
        "description": "Most capable model",
        "context_window": 128000,
        "cost_per_1k_input": 0.005,
        "cost_per_1k_output": 0.015,
    },
    # ...
}
```

### environment.py

Handles `.env` loading and validation:

```python path=null start=null
def load_environment():
    """Load .env file and validate required keys."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found")
```

### llm.py

Factory functions for creating LLMs:

```python path=null start=null
def get_langchain_llm(model_name, **kwargs):
    """Create a LangChain ChatOpenAI instance."""
    load_environment()
    validate_model(model_name)
    return ChatOpenAI(model=model_name, **kwargs)
```

---

## Using Utils in Notebooks

Add this to your notebook's first cell:

```python path=null start=null
# Standard workshop setup
import sys
sys.path.insert(0, "../..")  # Adjust based on notebook location

from utils import (
    load_environment,
    get_langchain_llm,
    OPENAI_MODELS
)

# Initialize
load_environment()
print("Environment loaded successfully!")
print(f"Available models: {list(OPENAI_MODELS.keys())}")
```

---

## Extending Utils

### Adding a New Model

Edit `utils/models.py`:

```python path=null start=null
OPENAI_MODELS = {
    # ... existing models ...
    "gpt-4-new": {
        "description": "New model description",
        "context_window": 128000,
        "cost_per_1k_input": 0.01,
        "cost_per_1k_output": 0.03,
    },
}
```

### Adding a New Provider

1. Add to `models.py`:
```python path=null start=null
GOOGLE_MODELS = {
    "gemini-1.5-pro": {...},
    "gemini-1.5-flash": {...},
}
```

2. Add helper to `llm.py`:
```python path=null start=null
def get_google_llm(model_name, **kwargs):
    from langchain_google_genai import ChatGoogleGenerativeAI
    load_environment()  # Should check GOOGLE_API_KEY
    return ChatGoogleGenerativeAI(model=model_name, **kwargs)
```

3. Export in `__init__.py`:
```python path=null start=null
from .llm import get_google_llm
from .models import GOOGLE_MODELS
```

### Adding Utility Functions

Add to appropriate module or create new one:

```python path=null start=null
# utils/prompts.py
def format_system_prompt(role: str, context: str) -> str:
    """Create consistent system prompts."""
    return f"You are a {role}.\n\nContext:\n{context}"
```

---

## Best Practices

1. **Always use utils** in notebooks for consistency
2. **Don't hardcode models** - use constants from `models.py`
3. **Validate early** - call `load_environment()` at notebook start
4. **Keep utils focused** - only workshop-relevant abstractions
5. **Document additions** - update this guide when extending

---

## Troubleshooting

### "Module 'utils' not found"
```python path=null start=null
# Make sure path is correct for your notebook location
import sys
sys.path.insert(0, "../..")  # From Labs/Session_1/
# or
sys.path.insert(0, "..")     # From Labs/
```

### "Model not in OPENAI_MODELS"
The model might be new or misspelled. Check `utils/models.py` for available models.

### "OPENAI_API_KEY not found"
1. Check `.env` file exists in repo root
2. Check key name is exactly `OPENAI_API_KEY`
3. Restart kernel after adding `.env`

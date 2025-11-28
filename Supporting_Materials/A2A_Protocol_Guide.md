# Agent-to-Agent (A2A) Protocol Guide

## Overview

The **Agent-to-Agent (A2A) Protocol** is an open standard developed by Google that enables AI agents built on different frameworks to communicate and collaborate. Think of it as a "universal translator" for AI agents—regardless of whether an agent is built with LangGraph, AutoGen, CrewAI, or any other framework, A2A provides a common language for them to work together.

### Why A2A Matters

In enterprise environments, you'll often encounter:
- Different teams using different agent frameworks
- Legacy systems with existing AI capabilities
- Third-party agents from vendors or partners
- The need to orchestrate complex workflows across boundaries

A2A solves the interoperability problem by providing:
- **Framework Agnosticism**: Any agent can participate regardless of how it's built
- **Discoverable Capabilities**: Agents advertise what they can do via Agent Cards
- **Standardized Communication**: Common message formats and task lifecycles
- **Enterprise Ready**: Built with security, authentication, and scalability in mind

---

## Core Concepts

### 1. Agent Card

An **Agent Card** is a JSON document that describes an agent's capabilities, similar to an API specification. It's hosted at a well-known URL (`/.well-known/agent.json`).

```json path=null start=null
{
  "name": "Document Analyzer",
  "description": "Analyzes documents for compliance and risk factors",
  "url": "https://agent.example.com",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "analyze-compliance",
      "name": "Compliance Analysis",
      "description": "Analyzes documents for regulatory compliance",
      "inputModes": ["text/plain", "application/pdf"],
      "outputModes": ["application/json"]
    }
  ],
  "authentication": {
    "schemes": ["bearer"]
  }
}
```

### 2. Tasks

A **Task** represents a unit of work sent to an agent. Tasks have a lifecycle:

```
┌─────────┐    ┌────────────┐    ┌───────────┐    ┌───────────┐
│ Created │ -> │ Processing │ -> │ Completed │ or │  Failed   │
└─────────┘    └────────────┘    └───────────┘    └───────────┘
                     │
                     v
              ┌─────────────────┐
              │ Input Required  │ (for human-in-the-loop)
              └─────────────────┘
```

### 3. Messages and Parts

Communication uses **Messages** containing **Parts**:

- **TextPart**: Plain text content
- **FilePart**: Binary files (documents, images)
- **DataPart**: Structured JSON data

### 4. Artifacts

**Artifacts** are the outputs produced by an agent—documents, analysis results, generated content, etc.

---

## A2A vs MCP: Understanding the Difference

| Aspect | A2A Protocol | Model Context Protocol (MCP) |
|--------|--------------|------------------------------|
| **Purpose** | Agent-to-agent communication | Model-to-tool communication |
| **Scope** | Inter-agent orchestration | Single agent's tool access |
| **Use Case** | "Agent A asks Agent B to do something" | "Agent uses a tool to get data" |
| **Analogy** | Colleagues collaborating | Worker using their toolbox |

**When to use A2A:**
- Multiple autonomous agents need to collaborate
- Cross-organization agent communication
- Enterprise multi-agent systems

**When to use MCP:**
- Single agent needs to access external tools/data
- Integrating APIs, databases, file systems
- Extending an agent's capabilities

**They're complementary!** An agent might use MCP to access its tools, while using A2A to communicate with other agents.

---

## Sample Implementation

### A2A Server (Agent Provider)

```python path=null start=null
"""
A2A Server Example - Document Analysis Agent
This agent receives documents and returns compliance analysis.
"""

from typing import Any
import json
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler


class Task:
    """Represents an A2A task."""
    
    def __init__(self, task_id: str, message: dict):
        self.id = task_id
        self.status = "processing"
        self.message = message
        self.artifacts = []
        self.created_at = datetime.utcnow().isoformat()
    
    def complete(self, result: dict):
        self.status = "completed"
        self.artifacts.append({
            "type": "data",
            "data": result
        })
    
    def fail(self, error: str):
        self.status = "failed"
        self.error = error
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status,
            "artifacts": self.artifacts,
            "createdAt": self.created_at
        }


# Agent Card describing our capabilities
AGENT_CARD = {
    "name": "Compliance Analyzer",
    "description": "Analyzes text for compliance issues and risk factors",
    "url": "http://localhost:8080",
    "version": "1.0.0",
    "capabilities": {
        "streaming": False,
        "pushNotifications": False
    },
    "skills": [
        {
            "id": "analyze-compliance",
            "name": "Compliance Analysis",
            "description": "Identifies compliance risks in text content",
            "inputModes": ["text/plain"],
            "outputModes": ["application/json"]
        }
    ]
}


def analyze_compliance(text: str) -> dict:
    """
    Simple compliance analysis logic.
    In production, this would use an LLM or specialized model.
    """
    risks = []
    
    # Simple keyword-based detection (demo purposes)
    risk_keywords = {
        "guarantee": "Potential misleading claim",
        "unlimited": "May violate advertising standards",
        "confidential": "Data handling review needed",
        "insider": "Potential securities concern"
    }
    
    text_lower = text.lower()
    for keyword, risk_type in risk_keywords.items():
        if keyword in text_lower:
            risks.append({
                "keyword": keyword,
                "risk_type": risk_type,
                "severity": "medium"
            })
    
    return {
        "analyzed_length": len(text),
        "risk_count": len(risks),
        "risks": risks,
        "recommendation": "Review required" if risks else "No immediate concerns"
    }


class A2AHandler(BaseHTTPRequestHandler):
    """HTTP handler for A2A protocol endpoints."""
    
    tasks: dict[str, Task] = {}
    
    def do_GET(self):
        # Serve Agent Card at well-known URL
        if self.path == "/.well-known/agent.json":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(AGENT_CARD).encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == "/tasks":
            # Create new task
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length))
            
            task_id = str(uuid.uuid4())
            task = Task(task_id, body.get("message", {}))
            
            # Extract text from message parts
            text_content = ""
            for part in body.get("message", {}).get("parts", []):
                if part.get("type") == "text":
                    text_content += part.get("text", "")
            
            # Process the task
            if text_content:
                result = analyze_compliance(text_content)
                task.complete(result)
            else:
                task.fail("No text content provided")
            
            self.tasks[task_id] = task
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(task.to_dict()).encode())
        
        elif self.path.startswith("/tasks/") and self.path.endswith("/send"):
            # Send additional message to existing task
            task_id = self.path.split("/")[2]
            if task_id in self.tasks:
                # Handle follow-up messages
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(self.tasks[task_id].to_dict()).encode())
            else:
                self.send_error(404, "Task not found")
        else:
            self.send_error(404)


def run_server(port: int = 8080):
    """Run the A2A agent server."""
    server = HTTPServer(("localhost", port), A2AHandler)
    print(f"A2A Agent running at http://localhost:{port}")
    print(f"Agent Card: http://localhost:{port}/.well-known/agent.json")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
```

### A2A Client (Agent Consumer)

```python path=null start=null
"""
A2A Client Example - Calling another agent via A2A protocol.
"""

import requests
from typing import Optional


class A2AClient:
    """Client for communicating with A2A-compatible agents."""
    
    def __init__(self, agent_url: str):
        self.agent_url = agent_url.rstrip("/")
        self.agent_card = None
    
    def discover(self) -> dict:
        """Fetch the agent's capabilities via Agent Card."""
        response = requests.get(f"{self.agent_url}/.well-known/agent.json")
        response.raise_for_status()
        self.agent_card = response.json()
        return self.agent_card
    
    def create_task(self, text: str, skill_id: Optional[str] = None) -> dict:
        """
        Create a new task for the agent.
        
        Args:
            text: The text content to send
            skill_id: Optional skill to invoke
            
        Returns:
            Task response with status and artifacts
        """
        payload = {
            "message": {
                "role": "user",
                "parts": [
                    {"type": "text", "text": text}
                ]
            }
        }
        
        if skill_id:
            payload["skill"] = skill_id
        
        response = requests.post(
            f"{self.agent_url}/tasks",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    
    def get_task(self, task_id: str) -> dict:
        """Get the status of a task."""
        response = requests.get(f"{self.agent_url}/tasks/{task_id}")
        response.raise_for_status()
        return response.json()


def main():
    """Example: Using A2A to communicate with a compliance agent."""
    
    # Connect to the agent
    client = A2AClient("http://localhost:8080")
    
    # Discover capabilities
    print("Discovering agent capabilities...")
    card = client.discover()
    print(f"Connected to: {card['name']}")
    print(f"Skills: {[s['name'] for s in card['skills']]}")
    
    # Send a task
    document = """
    Dear Investor,
    
    We guarantee a 20% return on your investment within 6 months.
    This is confidential information not available to the public.
    Act now for unlimited profit potential!
    """
    
    print("\nSending document for analysis...")
    result = client.create_task(document, skill_id="analyze-compliance")
    
    print(f"\nTask Status: {result['status']}")
    if result['artifacts']:
        analysis = result['artifacts'][0]['data']
        print(f"Risks Found: {analysis['risk_count']}")
        for risk in analysis['risks']:
            print(f"  - {risk['keyword']}: {risk['risk_type']} ({risk['severity']})")
        print(f"Recommendation: {analysis['recommendation']}")


if __name__ == "__main__":
    main()
```

---

## Running the Example

1. **Start the server** (in one terminal):
```bash path=null start=null
python a2a_server.py
```

2. **Run the client** (in another terminal):
```bash path=null start=null
python a2a_client.py
```

Expected output:
```
Discovering agent capabilities...
Connected to: Compliance Analyzer
Skills: ['Compliance Analysis']

Sending document for analysis...

Task Status: completed
Risks Found: 3
  - guarantee: Potential misleading claim (medium)
  - confidential: Data handling review needed (medium)
  - unlimited: May violate advertising standards (medium)
Recommendation: Review required
```

---

## Using the Official A2A SDK

Google provides official SDKs for easier implementation:

```bash path=null start=null
pip install a2a-sdk
```

```python path=null start=null
from a2a import A2AClient, AgentCard, Task

# The SDK handles protocol details automatically
client = A2AClient()
agent = client.connect("https://agent.example.com")

# Check capabilities
print(agent.card.skills)

# Create task with streaming support
async for event in agent.stream_task("Analyze this document..."):
    if event.type == "progress":
        print(f"Progress: {event.progress}%")
    elif event.type == "artifact":
        print(f"Result: {event.artifact}")
```

---

## Best Practices

### 1. Design Clear Agent Cards
- Be specific about what each skill does
- Document input/output formats clearly
- Include example payloads in descriptions

### 2. Handle Task Lifecycles
- Implement proper status transitions
- Support long-running tasks with polling or streaming
- Handle failures gracefully

### 3. Security Considerations
- Always use HTTPS in production
- Implement proper authentication (OAuth2, API keys)
- Validate input data before processing
- Rate limit task creation

### 4. Interoperability
- Follow the spec strictly for maximum compatibility
- Test with multiple client implementations
- Version your agent cards

---

## Resources

- **Official Specification**: [google-a2a/A2A on GitHub](https://github.com/google-a2a/A2A)
- **Python SDK**: [google-a2a/a2a-python](https://github.com/google-a2a/a2a-python)
- **Sample Agents**: Check the official repo for reference implementations
- **Blog Post**: [Announcing A2A Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)

---

## Workshop Connection

In this workshop, we've built agents that could benefit from A2A:
- **Lab 4's State Machine**: Could expose its analysis as an A2A skill
- **Multi-Agent Systems**: Use A2A instead of framework-specific delegation
- **The Capstone Agent**: Perfect candidate for A2A exposure in enterprise settings

A2A represents the future of enterprise AI—where agents from different vendors, teams, and frameworks work together seamlessly.

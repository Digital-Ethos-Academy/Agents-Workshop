"""
Lab 1 Solution: LangChain Research Agent

A complete research assistant agent with tools, memory, and debugging.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain import hub
from langchain.memory import ConversationBufferMemory

# Load environment
load_dotenv()

# Storage for notes
notes_storage = []


# ============ TOOLS ============

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result.

    Args:
        expression: A mathematical expression like '2 + 2' or '15 * 7'
    """
    try:
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


@tool
def get_current_datetime() -> str:
    """Returns the current date and time."""
    now = datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def save_note(note: str) -> str:
    """Save a research note for later reference.

    Args:
        note: The note content to save
    """
    notes_storage.append({
        "content": note,
        "timestamp": datetime.now().isoformat()
    })
    return f"Note saved! You now have {len(notes_storage)} note(s)."


@tool
def get_notes() -> str:
    """Retrieve all saved research notes."""
    if not notes_storage:
        return "No notes saved yet."

    result = "Saved notes:\n"
    for i, note in enumerate(notes_storage, 1):
        result += f"\n{i}. [{note['timestamp'][:10]}] {note['content']}"
    return result


@tool
def summarize_research() -> str:
    """Summarize all research findings from saved notes.

    Use this after gathering information to create a summary.
    """
    if not notes_storage:
        return "No notes to summarize. Save some notes first."

    result = "Research Summary:\n"
    result += "=" * 40 + "\n"
    result += f"Total findings: {len(notes_storage)}\n\n"

    for i, note in enumerate(notes_storage, 1):
        result += f"Finding {i}:\n{note['content']}\n\n"

    return result


@tool
def web_search(query: str) -> str:
    """Search the web for information (simulated).

    Args:
        query: The search query
    """
    # In production, use Tavily or another search API
    return f"""Search results for "{query}":

1. [Article 1] Key findings about {query} from recent studies...
2. [Article 2] Expert analysis on {query} trends and implications...
3. [Article 3] Practical guide to understanding {query}...

Note: This is simulated. Configure TAVILY_API_KEY for real search."""


def build_research_agent():
    """Build and return the research agent."""

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Define tools
    tools = [
        calculator,
        get_current_datetime,
        save_note,
        get_notes,
        summarize_research,
        web_search
    ]

    # Get conversational ReAct prompt
    prompt = hub.pull("hwchase17/react-chat")

    # Create memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # Create agent
    agent = create_react_agent(llm, tools, prompt)

    # Create executor
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

    return executor


def main():
    """Demo the research agent."""
    print("=" * 60)
    print("Research Agent Demo")
    print("=" * 60)

    agent = build_research_agent()

    # Demo queries
    queries = [
        "My name is Alex. Search for information about Python async programming.",
        "Save a note: Python async uses asyncio library and await/async keywords",
        "What's my name? Also calculate 15 * 7 + 23",
        "What notes do we have so far? Summarize our research."
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print("=" * 60)

        result = agent.invoke({"input": query})
        print(f"\nResponse: {result['output']}")


if __name__ == "__main__":
    main()

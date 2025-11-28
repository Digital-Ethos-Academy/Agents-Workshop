"""
Lab 3 Solution: LangGraph Document Processing Workflow

A stateful workflow for document processing with conditional routing.
"""

import os
from typing import TypedDict, Annotated, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ============ STATE DEFINITION ============

class DocumentState(TypedDict):
    """State for document processing workflow."""
    document: str
    doc_type: str  # email, report, memo, unknown
    extracted_info: dict
    summary: str
    urgency: str  # high, medium, low
    response: str


# ============ NODE FUNCTIONS ============

def classify_document(state: DocumentState) -> dict:
    """Classify the document type."""
    document = state["document"]

    messages = [
        SystemMessage(content="""Classify the document type. Return ONLY one word:
        - email (if it's an email or message)
        - report (if it's a report or analysis)
        - memo (if it's a memo or announcement)
        - unknown (if unclear)"""),
        HumanMessage(content=f"Document:\n{document}")
    ]

    response = llm.invoke(messages)
    doc_type = response.content.strip().lower()

    # Validate
    if doc_type not in ["email", "report", "memo"]:
        doc_type = "unknown"

    print(f"[classify] Document type: {doc_type}")
    return {"doc_type": doc_type}


def extract_info(state: DocumentState) -> dict:
    """Extract key information from the document."""
    document = state["document"]
    doc_type = state["doc_type"]

    extraction_prompts = {
        "email": "Extract: sender, recipient, subject, main request, deadline (if any)",
        "report": "Extract: title, date, key findings, recommendations",
        "memo": "Extract: from, to, subject, key points, action items",
        "unknown": "Extract: main topic, key points, any action items"
    }

    prompt = extraction_prompts.get(doc_type, extraction_prompts["unknown"])

    messages = [
        SystemMessage(content=f"You are an information extractor. {prompt}. Return as JSON."),
        HumanMessage(content=f"Document:\n{document}")
    ]

    response = llm.invoke(messages)

    print(f"[extract] Extracted key information")
    return {"extracted_info": {"raw": response.content}}


def determine_urgency(state: DocumentState) -> dict:
    """Determine the urgency level of the document."""
    document = state["document"]
    extracted_info = state.get("extracted_info", {})

    messages = [
        SystemMessage(content="""Determine the urgency level. Return ONLY one word:
        - high (immediate action needed, critical issues, deadlines today)
        - medium (action needed soon, important but not critical)
        - low (informational, no immediate action needed)"""),
        HumanMessage(content=f"Document:\n{document}\n\nExtracted info:\n{extracted_info}")
    ]

    response = llm.invoke(messages)
    urgency = response.content.strip().lower()

    # Validate
    if urgency not in ["high", "medium", "low"]:
        urgency = "medium"

    print(f"[urgency] Urgency level: {urgency}")
    return {"urgency": urgency}


def summarize_document(state: DocumentState) -> dict:
    """Create a brief summary of the document."""
    document = state["document"]
    doc_type = state["doc_type"]
    extracted_info = state.get("extracted_info", {})

    messages = [
        SystemMessage(content="""Create a brief 2-3 sentence summary of the document.
        Focus on the most important information."""),
        HumanMessage(content=f"Document type: {doc_type}\nExtracted info: {extracted_info}\n\nDocument:\n{document}")
    ]

    response = llm.invoke(messages)

    print(f"[summarize] Created summary")
    return {"summary": response.content}


def handle_urgent(state: DocumentState) -> dict:
    """Handle urgent documents with immediate response."""
    summary = state["summary"]
    extracted_info = state.get("extracted_info", {})

    messages = [
        SystemMessage(content="""This is an URGENT document. Create a brief response that:
        1. Acknowledges the urgency
        2. Outlines immediate next steps
        3. Identifies who needs to be notified"""),
        HumanMessage(content=f"Summary: {summary}\nExtracted info: {extracted_info}")
    ]

    response = llm.invoke(messages)

    print(f"[handle_urgent] Created urgent response")
    return {"response": f"[URGENT HANDLING]\n{response.content}"}


def handle_normal(state: DocumentState) -> dict:
    """Handle normal documents with standard response."""
    summary = state["summary"]
    doc_type = state["doc_type"]

    messages = [
        SystemMessage(content="""Create a brief response that:
        1. Acknowledges receipt
        2. Notes key points
        3. Suggests next steps if applicable"""),
        HumanMessage(content=f"Document type: {doc_type}\nSummary: {summary}")
    ]

    response = llm.invoke(messages)

    print(f"[handle_normal] Created standard response")
    return {"response": f"[STANDARD HANDLING]\n{response.content}"}


# ============ ROUTING FUNCTION ============

def route_by_urgency(state: DocumentState) -> Literal["urgent", "normal"]:
    """Route based on urgency level."""
    urgency = state.get("urgency", "medium")

    if urgency == "high":
        print("[router] Routing to urgent handler")
        return "urgent"
    else:
        print("[router] Routing to normal handler")
        return "normal"


# ============ BUILD GRAPH ============

def build_document_workflow():
    """Build and return the document processing workflow."""

    # Create graph
    graph = StateGraph(DocumentState)

    # Add nodes
    graph.add_node("classify", classify_document)
    graph.add_node("extract", extract_info)
    graph.add_node("urgency", determine_urgency)
    graph.add_node("summarize", summarize_document)
    graph.add_node("urgent", handle_urgent)
    graph.add_node("normal", handle_normal)

    # Add edges
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "extract")
    graph.add_edge("extract", "urgency")
    graph.add_edge("urgency", "summarize")

    # Conditional routing after summarize
    graph.add_conditional_edges(
        "summarize",
        route_by_urgency,
        {
            "urgent": "urgent",
            "normal": "normal"
        }
    )

    # Both handlers go to END
    graph.add_edge("urgent", END)
    graph.add_edge("normal", END)

    # Compile with memory for checkpointing
    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)

    return app


def process_document(document: str, thread_id: str = "default"):
    """Process a document through the workflow."""
    app = build_document_workflow()
    config = {"configurable": {"thread_id": thread_id}}

    result = app.invoke({"document": document}, config)

    return result


def main():
    """Demo the document processing workflow."""
    test_documents = [
        """URGENT: Production server is down!

From: DevOps Team
To: All Engineers
Subject: CRITICAL - Production Outage

Our main production database became unreachable at 14:32 UTC.
All services are affected. We need immediate assistance from the database team.

This is a P0 incident. Please join the war room immediately.
ETA for resolution needed ASAP.""",

        """Weekly Status Report - Q4 Week 3

From: Project Management
To: Leadership Team
Date: November 15, 2024

Key Highlights:
- Sprint velocity increased by 15%
- All milestone deliverables on track
- New hire onboarding completed

Upcoming:
- Feature freeze on Friday
- UAT begins next Monday

No blockers at this time.""",

        """Meeting Request

Hi Team,

Would like to schedule a quick sync about the Q1 roadmap.
How does next Tuesday at 2pm work for everyone?

Let me know your availability.

Thanks,
Sarah"""
    ]

    for i, doc in enumerate(test_documents, 1):
        print("\n" + "=" * 70)
        print(f"DOCUMENT {i}")
        print("=" * 70)
        print(doc[:100] + "..." if len(doc) > 100 else doc)

        result = process_document(doc, f"doc-{i}")

        print("\n" + "-" * 40)
        print("RESULT:")
        print(f"Type: {result['doc_type']}")
        print(f"Urgency: {result['urgency']}")
        print(f"Summary: {result['summary'][:200]}...")
        print(f"\nResponse:\n{result['response']}")


if __name__ == "__main__":
    main()

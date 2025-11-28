"""
Capstone Solution: Compliance Document Reviewer

A LangGraph-based agent that analyzes documents for regulatory compliance in
financial services. This demonstrates:
- State machine architecture
- Document classification
- Entity extraction
- Risk flagging
- Human-in-the-loop for high-risk documents

Usage:
    python lab4_capstone_compliance_agent.py

Requirements:
    - OpenAI API key in .env
    - langchain, langgraph, langchain-openai packages
"""

import os
import sys
from typing import TypedDict, Literal, Annotated
from datetime import datetime

# Add utils to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Load environment
load_dotenv()


# =============================================================================
# State Definition
# =============================================================================

class ComplianceState(TypedDict):
    """State for the compliance review workflow."""
    
    # Input
    document_text: str
    document_id: str
    
    # Classification
    document_type: str  # "policy", "contract", "disclosure", "marketing", "other"
    
    # Extracted entities
    entities: dict  # Parties, dates, amounts, regulations referenced
    
    # Risk analysis
    risk_flags: list[dict]  # List of {category, description, severity}
    risk_score: int  # 0-100
    risk_level: str  # "low", "medium", "high", "critical"
    
    # Routing
    requires_human_review: bool
    human_review_reason: str
    
    # Output
    analysis_summary: str
    recommendations: list[str]
    
    # Metadata
    timestamp: str
    processing_status: str


# =============================================================================
# Node Functions
# =============================================================================

def classify_document(state: ComplianceState) -> dict:
    """Classify the document type."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = f"""Classify this document into exactly one of these categories:
- policy: Internal company policies, procedures, guidelines
- contract: Legal agreements, terms of service, SLAs
- disclosure: Financial disclosures, risk disclosures, regulatory filings
- marketing: Marketing materials, advertisements, promotional content
- other: Documents that don't fit the above categories

Document text:
{state['document_text'][:3000]}

Respond with ONLY the category name (lowercase), nothing else."""

    response = llm.invoke([HumanMessage(content=prompt)])
    doc_type = response.content.strip().lower()
    
    # Validate response
    valid_types = ["policy", "contract", "disclosure", "marketing", "other"]
    if doc_type not in valid_types:
        doc_type = "other"
    
    return {
        "document_type": doc_type,
        "processing_status": "classified"
    }


def extract_entities(state: ComplianceState) -> dict:
    """Extract compliance-relevant entities from the document."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = f"""Extract compliance-relevant entities from this {state['document_type']} document.

Document text:
{state['document_text'][:4000]}

Return a JSON object with these fields (use empty arrays/strings if not found):
{{
    "parties": ["list of named parties/organizations"],
    "dates": ["list of important dates mentioned"],
    "monetary_amounts": ["list of monetary values mentioned"],
    "regulations_referenced": ["list of laws/regulations mentioned (e.g., GDPR, SOX, FINRA)"],
    "key_terms": ["list of important compliance terms"],
    "contact_information": ["any email/phone/address mentioned"]
}}

Return ONLY the JSON object, no other text."""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Parse response (with fallback)
    import json
    try:
        entities = json.loads(response.content)
    except json.JSONDecodeError:
        entities = {
            "parties": [],
            "dates": [],
            "monetary_amounts": [],
            "regulations_referenced": [],
            "key_terms": [],
            "contact_information": [],
            "parse_error": "Could not parse entity extraction response"
        }
    
    return {
        "entities": entities,
        "processing_status": "entities_extracted"
    }


def analyze_risks(state: ComplianceState) -> dict:
    """Analyze the document for compliance risks."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Risk categories by document type
    risk_focus = {
        "policy": "policy gaps, unclear procedures, missing approvals",
        "contract": "unfavorable terms, liability exposure, missing clauses",
        "disclosure": "incomplete information, misleading statements, omissions",
        "marketing": "false claims, missing disclaimers, regulatory violations",
        "other": "general compliance concerns"
    }
    
    focus = risk_focus.get(state['document_type'], risk_focus['other'])
    
    prompt = f"""Analyze this {state['document_type']} document for compliance risks.
Focus particularly on: {focus}

Document text:
{state['document_text'][:4000]}

Entities found:
{state['entities']}

Return a JSON object:
{{
    "risk_flags": [
        {{
            "category": "category of risk",
            "description": "specific description of the risk",
            "severity": "low|medium|high|critical",
            "location": "where in document this appears"
        }}
    ],
    "risk_score": 0-100 (overall risk score),
    "risk_level": "low|medium|high|critical"
}}

Return ONLY the JSON object."""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    import json
    try:
        risk_analysis = json.loads(response.content)
    except json.JSONDecodeError:
        risk_analysis = {
            "risk_flags": [{"category": "parse_error", "description": "Could not analyze", "severity": "medium"}],
            "risk_score": 50,
            "risk_level": "medium"
        }
    
    return {
        "risk_flags": risk_analysis.get("risk_flags", []),
        "risk_score": risk_analysis.get("risk_score", 50),
        "risk_level": risk_analysis.get("risk_level", "medium"),
        "processing_status": "risks_analyzed"
    }


def determine_routing(state: ComplianceState) -> dict:
    """Determine if human review is required based on risk analysis."""
    
    requires_review = False
    review_reason = ""
    
    # High risk score triggers review
    if state.get("risk_score", 0) >= 70:
        requires_review = True
        review_reason = f"High risk score: {state['risk_score']}"
    
    # Critical or high severity flags trigger review
    critical_flags = [f for f in state.get("risk_flags", []) 
                     if f.get("severity") in ["critical", "high"]]
    if critical_flags:
        requires_review = True
        if review_reason:
            review_reason += "; "
        review_reason += f"{len(critical_flags)} high/critical risk flags"
    
    # Certain document types always need review
    if state.get("document_type") in ["disclosure", "contract"]:
        if state.get("risk_score", 0) >= 50:
            requires_review = True
            if review_reason:
                review_reason += "; "
            review_reason += f"{state['document_type']} with elevated risk"
    
    return {
        "requires_human_review": requires_review,
        "human_review_reason": review_reason if review_reason else "No review required",
        "processing_status": "routing_determined"
    }


def generate_summary(state: ComplianceState) -> dict:
    """Generate final analysis summary and recommendations."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = f"""Generate a compliance analysis summary for this document.

Document Type: {state['document_type']}
Risk Level: {state['risk_level']} (score: {state['risk_score']})
Risk Flags: {len(state.get('risk_flags', []))} issues identified
Requires Human Review: {state['requires_human_review']}

Entities Found:
{state.get('entities', {})}

Risk Flags:
{state.get('risk_flags', [])}

Provide:
1. A 2-3 sentence executive summary
2. 3-5 specific recommendations

Return as JSON:
{{
    "summary": "executive summary text",
    "recommendations": ["rec1", "rec2", "rec3"]
}}

Return ONLY the JSON object."""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    import json
    try:
        output = json.loads(response.content)
    except json.JSONDecodeError:
        output = {
            "summary": f"Analysis complete for {state['document_type']} document. Risk level: {state['risk_level']}.",
            "recommendations": ["Review document manually", "Consult compliance team"]
        }
    
    return {
        "analysis_summary": output.get("summary", ""),
        "recommendations": output.get("recommendations", []),
        "processing_status": "complete",
        "timestamp": datetime.now().isoformat()
    }


def human_review_checkpoint(state: ComplianceState) -> dict:
    """Checkpoint for human review - execution pauses here."""
    # This node exists as a pause point for human-in-the-loop
    # In production, this would integrate with a review queue
    return {
        "processing_status": "awaiting_human_review"
    }


# =============================================================================
# Routing Functions
# =============================================================================

def route_after_risk_analysis(state: ComplianceState) -> Literal["determine_routing", "generate_summary"]:
    """Route based on whether we need to check for human review."""
    # Always go through routing to determine if human review needed
    return "determine_routing"


def route_after_routing(state: ComplianceState) -> Literal["human_review", "generate_summary"]:
    """Route to human review or directly to summary."""
    if state.get("requires_human_review", False):
        return "human_review"
    return "generate_summary"


# =============================================================================
# Build the Graph
# =============================================================================

def build_compliance_graph():
    """Build and compile the compliance review graph."""
    
    # Create graph with state schema
    graph = StateGraph(ComplianceState)
    
    # Add nodes
    graph.add_node("classify", classify_document)
    graph.add_node("extract_entities", extract_entities)
    graph.add_node("analyze_risks", analyze_risks)
    graph.add_node("determine_routing", determine_routing)
    graph.add_node("human_review", human_review_checkpoint)
    graph.add_node("generate_summary", generate_summary)
    
    # Add edges
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "extract_entities")
    graph.add_edge("extract_entities", "analyze_risks")
    graph.add_edge("analyze_risks", "determine_routing")
    
    # Conditional routing after determining if human review needed
    graph.add_conditional_edges(
        "determine_routing",
        route_after_routing,
        {
            "human_review": "human_review",
            "generate_summary": "generate_summary"
        }
    )
    
    # After human review, proceed to summary
    graph.add_edge("human_review", "generate_summary")
    
    # End after summary
    graph.add_edge("generate_summary", END)
    
    # Compile with checkpointer for human-in-the-loop
    checkpointer = MemorySaver()
    
    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_review"]  # Pause before human review
    )


# =============================================================================
# Main Execution
# =============================================================================

def analyze_document(document_text: str, document_id: str = "doc_001") -> dict:
    """
    Analyze a document for compliance issues.
    
    Args:
        document_text: The document content to analyze
        document_id: Unique identifier for the document
        
    Returns:
        Final state with analysis results
    """
    
    # Build the graph
    app = build_compliance_graph()
    
    # Initial state
    initial_state = {
        "document_text": document_text,
        "document_id": document_id,
        "document_type": "",
        "entities": {},
        "risk_flags": [],
        "risk_score": 0,
        "risk_level": "",
        "requires_human_review": False,
        "human_review_reason": "",
        "analysis_summary": "",
        "recommendations": [],
        "timestamp": "",
        "processing_status": "started"
    }
    
    # Thread config for checkpointing
    config = {"configurable": {"thread_id": document_id}}
    
    # Run the graph
    print(f"\n{'='*60}")
    print(f"Analyzing document: {document_id}")
    print(f"{'='*60}\n")
    
    # Stream through nodes
    for event in app.stream(initial_state, config):
        for node_name, node_output in event.items():
            status = node_output.get("processing_status", "processing")
            print(f"✓ {node_name}: {status}")
            
            # If paused for human review, handle it
            if status == "awaiting_human_review":
                print("\n" + "!"*60)
                print("PAUSED: Document requires human review")
                print(f"Reason: {app.get_state(config).values.get('human_review_reason', 'Unknown')}")
                print("!"*60 + "\n")
                
                # In a real system, this would wait for approval
                # For demo, we auto-approve
                print("(Auto-approving for demo purposes...)\n")
                
                # Resume execution
                for resume_event in app.stream(None, config):
                    for name, output in resume_event.items():
                        print(f"✓ {name}: {output.get('processing_status', 'processing')}")
    
    # Get final state
    final_state = app.get_state(config).values
    
    return final_state


def print_results(state: dict):
    """Pretty print the analysis results."""
    
    print(f"\n{'='*60}")
    print("COMPLIANCE ANALYSIS RESULTS")
    print(f"{'='*60}\n")
    
    print(f"Document ID: {state.get('document_id', 'N/A')}")
    print(f"Document Type: {state.get('document_type', 'N/A').upper()}")
    print(f"Timestamp: {state.get('timestamp', 'N/A')}")
    
    print(f"\n--- Risk Assessment ---")
    print(f"Risk Level: {state.get('risk_level', 'N/A').upper()}")
    print(f"Risk Score: {state.get('risk_score', 'N/A')}/100")
    print(f"Human Review Required: {'YES' if state.get('requires_human_review') else 'NO'}")
    if state.get('requires_human_review'):
        print(f"Review Reason: {state.get('human_review_reason', 'N/A')}")
    
    print(f"\n--- Entities Extracted ---")
    entities = state.get('entities', {})
    for key, values in entities.items():
        if values and key != "parse_error":
            print(f"  {key}: {', '.join(values) if isinstance(values, list) else values}")
    
    print(f"\n--- Risk Flags ({len(state.get('risk_flags', []))}) ---")
    for i, flag in enumerate(state.get('risk_flags', []), 1):
        severity = flag.get('severity', 'unknown').upper()
        print(f"  {i}. [{severity}] {flag.get('category', 'N/A')}: {flag.get('description', 'N/A')}")
    
    print(f"\n--- Summary ---")
    print(state.get('analysis_summary', 'No summary available'))
    
    print(f"\n--- Recommendations ---")
    for i, rec in enumerate(state.get('recommendations', []), 1):
        print(f"  {i}. {rec}")
    
    print(f"\n{'='*60}\n")


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    # Sample document for testing
    sample_document = """
    INVESTMENT ADVISORY AGREEMENT
    
    This Investment Advisory Agreement ("Agreement") is entered into as of 
    January 15, 2024, between Alpha Wealth Management LLC ("Advisor") and 
    the undersigned client ("Client").
    
    1. SERVICES
    The Advisor agrees to provide investment advisory services including 
    portfolio management and financial planning. The Advisor guarantees 
    annual returns of at least 15% on invested assets.
    
    2. FEES
    Client agrees to pay an annual fee of 1.5% of assets under management,
    calculated quarterly. Additional performance fees of 20% apply to any
    returns exceeding 10% annually.
    
    3. RISKS
    Past performance is not indicative of future results. Investments may
    lose value. Client acknowledges understanding these risks.
    
    4. CONFIDENTIALITY  
    All client information will be kept strictly confidential and will not
    be shared with third parties except as required by law under regulations
    including but not limited to SEC Rule 206(4)-7, FINRA Rule 2111, and
    the Investment Advisers Act of 1940.
    
    5. TERMINATION
    This agreement may be terminated by either party with 30 days written
    notice. Fees will be prorated to the termination date.
    
    Client Signature: _________________ Date: _________
    Advisor Signature: ________________ Date: _________
    
    Alpha Wealth Management LLC
    123 Financial District, Suite 500
    New York, NY 10005
    contact@alphawealth.example.com
    (555) 123-4567
    """
    
    # Run analysis
    result = analyze_document(sample_document, "DEMO_001")
    
    # Print results
    print_results(result)

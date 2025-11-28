"""
Lab 2 Solution: CrewAI Research Team

A multi-agent research team using CrewAI's role-based approach.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment
load_dotenv()


def build_research_crew(topic: str):
    """Build and return a CrewAI research crew."""

    # Research Analyst Agent
    researcher = Agent(
        role="Research Analyst",
        goal="Conduct thorough research and provide accurate, well-sourced information",
        backstory="""You are an experienced research analyst with expertise in
        gathering and analyzing information. You pride yourself on accuracy and
        depth of research. You always break down complex topics into key questions
        and provide comprehensive findings.""",
        verbose=True,
        allow_delegation=False
    )

    # Writer Agent
    writer = Agent(
        role="Content Writer",
        goal="Transform research into clear, engaging, and well-structured content",
        backstory="""You are a skilled content writer with a talent for making
        complex topics accessible. You create engaging narratives while maintaining
        accuracy. You always structure your content with a clear introduction,
        body, and conclusion.""",
        verbose=True,
        allow_delegation=False
    )

    # Critic Agent
    critic = Agent(
        role="Content Reviewer",
        goal="Ensure content quality through constructive feedback and final polish",
        backstory="""You are a meticulous editor with years of experience reviewing
        content. You have a keen eye for inconsistencies, unclear passages, and
        areas that need improvement. You provide specific, actionable feedback
        and ensure the final product is polished and professional.""",
        verbose=True,
        allow_delegation=False
    )

    # Define Tasks
    research_task = Task(
        description=f"""Research the topic: {topic}

        Your research should include:
        1. 3 key benefits with supporting evidence
        2. 3 main challenges with context
        3. Any relevant statistics or current trends
        4. Expert opinions or insights

        Provide structured, factual findings.""",
        expected_output="A structured research summary with categorized findings",
        agent=researcher
    )

    writing_task = Task(
        description=f"""Using the research findings, write a compelling article about: {topic}

        Requirements:
        - Under 300 words
        - Clear structure: introduction, body (benefits and challenges), conclusion
        - Engaging but professional tone
        - Accessible to a general audience""",
        expected_output="A polished article under 300 words",
        agent=writer,
        context=[research_task]
    )

    review_task = Task(
        description="""Review and finalize the article:

        Check for:
        1. Factual accuracy (cross-reference with research)
        2. Clarity and readability
        3. Proper structure and flow
        4. Grammar and style
        5. Word count (must be under 300 words)

        Provide the final, publication-ready version.""",
        expected_output="The final, reviewed article ready for publication",
        agent=critic,
        context=[writing_task]
    )

    # Create Crew
    crew = Crew(
        agents=[researcher, writer, critic],
        tasks=[research_task, writing_task, review_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


def run_research_task(topic: str):
    """Run a research task with the crew."""
    print("=" * 60)
    print(f"Research Topic: {topic}")
    print("=" * 60)

    crew = build_research_crew(topic)
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("FINAL OUTPUT:")
    print("=" * 60)
    print(result)

    return result


def main():
    """Demo the CrewAI research team."""
    topic = "The benefits and challenges of remote work for software developers"
    run_research_task(topic)


if __name__ == "__main__":
    main()

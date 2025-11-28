"""
Lab 2 Solution: AutoGen Research Team

A multi-agent research team using AutoGen's conversational approach.
"""

import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Load environment
load_dotenv()


def build_research_team():
    """Build and return the AutoGen research team."""

    llm_config = {
        "config_list": [{
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY")
        }],
        "temperature": 0.7
    }

    # Research Analyst Agent
    researcher = AssistantAgent(
        name="Researcher",
        system_message="""You are a research analyst. Your job is to:
        1. Break down research topics into key questions
        2. Identify important facts and data points
        3. Provide well-sourced information

        Focus on accuracy and depth. Cite your reasoning.
        Be thorough but concise.""",
        llm_config=llm_config
    )

    # Writer Agent
    writer = AssistantAgent(
        name="Writer",
        system_message="""You are a professional writer. Your job is to:
        1. Take research findings and turn them into clear, engaging content
        2. Structure information logically with introduction, body, conclusion
        3. Use accessible language for a general audience

        Wait for the Researcher to provide information before writing.
        Keep content focused and avoid unnecessary padding.""",
        llm_config=llm_config
    )

    # Critic Agent
    critic = AssistantAgent(
        name="Critic",
        system_message="""You are a constructive critic and editor. Your job is to:
        1. Review content for accuracy and clarity
        2. Identify gaps, errors, or unclear passages
        3. Suggest specific improvements

        Be constructive and specific in your feedback.
        When the content is satisfactory and polished, say 'APPROVED' and 'TERMINATE'.
        Only approve when the content meets quality standards.""",
        llm_config=llm_config
    )

    # User Proxy (initiates conversation)
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", "")
    )

    # Create group chat
    group_chat = GroupChat(
        agents=[user_proxy, researcher, writer, critic],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    # Create manager
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config
    )

    return user_proxy, manager


def run_research_task(topic: str):
    """Run a research task with the team."""
    user_proxy, manager = build_research_team()

    print("=" * 60)
    print(f"Research Topic: {topic}")
    print("=" * 60)

    user_proxy.initiate_chat(
        manager,
        message=f"""Research and write a brief article about:

{topic}

Requirements:
- Under 300 words
- Clear structure
- Well-researched
- Engaging but professional tone"""
    )


def main():
    """Demo the AutoGen research team."""
    topic = "The benefits and challenges of remote work for software developers"
    run_research_task(topic)


if __name__ == "__main__":
    main()

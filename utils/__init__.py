"""Utilities package for the Crafting Custom Agents Workshop.

This module provides a unified interface for LLM configuration, environment
management, and framework-specific helpers for LangChain, AutoGen, and CrewAI.

Quick Start:
    >>> from utils import load_environment, get_langchain_llm
    >>> load_environment()
    >>> llm = get_langchain_llm("gpt-4o-mini")
"""
from .settings import load_environment, load_dotenv, display, Markdown, IPyImage, PlantUML
from .models import RECOMMENDED_MODELS, recommended_models_table
from .llm import (
    setup_llm_client, async_setup_llm_client,
    get_completion, get_completion_compat,
    async_get_completion, async_get_completion_compat,
    get_vision_completion, get_vision_completion_compat,
    async_get_vision_completion, async_get_vision_completion_compat,
    clean_llm_output,
    prompt_enhancer, prompt_enhancer_compat,
    # Workshop helper functions
    get_langchain_llm, get_autogen_config, get_crewai_llm,
)
from .image_gen import (
    get_image_generation_completion, get_image_generation_completion_compat,
    async_get_image_generation_completion, async_get_image_generation_completion_compat,
    get_image_edit_completion, get_image_edit_completion_compat,
    async_get_image_edit_completion, async_get_image_edit_completion_compat,
)
from .audio import (
    transcribe_audio,
    transcribe_audio_compat,
    async_transcribe_audio,
    async_transcribe_audio_compat,
)
from .artifacts import *  # noqa: F401,F403 re-export for backwards compatibility
from .errors import *  # noqa: F401,F403
from .logging import *  # noqa: F401,F403
from .plantuml import render_plantuml_diagram

__all__ = [
    # Environment and display
    'load_environment', 'load_dotenv', 'display', 'Markdown', 'IPyImage', 'PlantUML',
    # Model registry
    'RECOMMENDED_MODELS', 'recommended_models_table',
    # Workshop helpers (use these in labs!)
    'get_langchain_llm', 'get_autogen_config', 'get_crewai_llm',
    # Low-level client setup
    'setup_llm_client', 'async_setup_llm_client',
    # Completion functions
    'get_completion', 'get_completion_compat',
    'async_get_completion', 'async_get_completion_compat',
    'get_vision_completion', 'get_vision_completion_compat',
    'async_get_vision_completion', 'async_get_vision_completion_compat',
    # Image generation
    'get_image_generation_completion', 'get_image_generation_completion_compat',
    'async_get_image_generation_completion', 'async_get_image_generation_completion_compat',
    'get_image_edit_completion', 'get_image_edit_completion_compat',
    'async_get_image_edit_completion', 'async_get_image_edit_completion_compat',
    # Audio
    'transcribe_audio', 'transcribe_audio_compat',
    'async_transcribe_audio', 'async_transcribe_audio_compat',
    # Utilities
    'clean_llm_output', 'prompt_enhancer', 'prompt_enhancer_compat',
    'render_plantuml_diagram',
]

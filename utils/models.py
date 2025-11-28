"""
Model metadata and helper utilities for the Crafting Custom Agents Workshop.

This module provides a registry of recommended LLM models with their capabilities
and metadata, plus helper functions to display and filter models.
"""
from __future__ import annotations

from typing import Any, Dict

from .settings import display, Markdown

# --- Model & Provider Configuration ---
# These are production-ready models tested with the workshop labs
RECOMMENDED_MODELS: Dict[str, Dict[str, Any]] = {
    # OpenAI Models - Primary models for workshop
    "gpt-4o": {
        "provider": "openai",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 128_000,
        "output_tokens": 16_384,
        "description": "Most capable GPT-4 model with vision support",
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 128_000,
        "output_tokens": 16_384,
        "description": "Fast, cost-effective model - recommended for workshop labs",
    },
    "gpt-4-turbo": {
        "provider": "openai",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 128_000,
        "output_tokens": 4_096,
        "description": "GPT-4 Turbo with vision capabilities",
    },
    "gpt-3.5-turbo": {
        "provider": "openai",
        "vision": False,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 16_385,
        "output_tokens": 4_096,
        "description": "Fast, economical model for simpler tasks",
    },
    "o1": {
        "provider": "openai",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 200_000,
        "output_tokens": 100_000,
        "description": "Advanced reasoning model",
    },
    "o1-mini": {
        "provider": "openai",
        "vision": False,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 128_000,
        "output_tokens": 65_536,
        "description": "Fast reasoning model for coding and math",
    },
    "o3-mini": {
        "provider": "openai",
        "vision": False,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 200_000,
        "output_tokens": 100_000,
        "description": "Latest reasoning model",
    },
    "dall-e-3": {
        "provider": "openai",
        "vision": False,
        "text_generation": False,
        "image_generation": True,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": None,
        "output_tokens": None,
        "description": "Image generation model",
    },
    "whisper-1": {
        "provider": "openai",
        "vision": False,
        "text_generation": False,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": True,
        "context_window_tokens": None,
        "output_tokens": None,
        "description": "Audio transcription model",
    },
    # Anthropic Models
    "claude-3-5-sonnet-20241022": {
        "provider": "anthropic",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 200_000,
        "output_tokens": 8_192,
        "description": "Claude 3.5 Sonnet - balanced performance and speed",
    },
    "claude-3-5-haiku-20241022": {
        "provider": "anthropic",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 200_000,
        "output_tokens": 8_192,
        "description": "Claude 3.5 Haiku - fast and efficient",
    },
    "claude-3-opus-20240229": {
        "provider": "anthropic",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 200_000,
        "output_tokens": 4_096,
        "description": "Claude 3 Opus - most capable Claude model",
    },
    "claude-3-haiku-20240307": {
        "provider": "anthropic",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 200_000,
        "output_tokens": 4_096,
        "description": "Claude 3 Haiku - fast and economical",
    },
    # Google Models
    "gemini-1.5-pro": {
        "provider": "google",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 2_000_000,
        "output_tokens": 8_192,
        "description": "Gemini 1.5 Pro - large context window",
    },
    "gemini-1.5-flash": {
        "provider": "google",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 1_000_000,
        "output_tokens": 8_192,
        "description": "Gemini 1.5 Flash - fast and efficient",
    },
    "gemini-2.0-flash-exp": {
        "provider": "google",
        "vision": True,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 1_048_576,
        "output_tokens": 8_192,
        "description": "Gemini 2.0 Flash experimental",
    },
    # Hugging Face Models
    "meta-llama/Llama-3.3-70B-Instruct": {
        "provider": "huggingface",
        "vision": False,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 128_000,
        "output_tokens": 4_096,
        "description": "Llama 3.3 70B - open source LLM",
    },
    "mistralai/Mistral-7B-Instruct-v0.3": {
        "provider": "huggingface",
        "vision": False,
        "text_generation": True,
        "image_generation": False,
        "image_modification": False,
        "audio_transcription": False,
        "context_window_tokens": 32_768,
        "output_tokens": 8_192,
        "description": "Mistral 7B - efficient open source model",
    },
}


def recommended_models_table(task: str | None = None,
                             provider: str | None = None,
                             text_generation: bool | None = None,
                             vision: bool | None = None,
                             image_generation: bool | None = None,
                             audio_transcription: bool | None = None,
                             min_context: int | None = None,
                             min_output_tokens: int | None = None,
                             image_modification: bool | None = None) -> str:
    """Return a markdown table of recommended models filtered by capabilities."""
    if task:
        t = task.lower()
        if t in {"vision", "multimodal", "vl"} and vision is None:
            vision = True
        elif t in {"image", "image_generation", "image-generation"} and image_generation is None:
            image_generation = True
        elif t in {"image_modification", "image-edit", "image_edit", "image-editing", "editing"} and image_modification is None:
            image_modification = True
        elif t in {"audio", "speech", "audio_transcription", "stt"} and audio_transcription is None:
            audio_transcription = True
        elif t == "text" and text_generation is None:
            text_generation = True
            vision = False if vision is None else vision
            image_generation = False if image_generation is None else image_generation
            image_modification = False if image_modification is None else image_modification
            audio_transcription = False if audio_transcription is None else audio_transcription

    rows = []
    for model_name in sorted(RECOMMENDED_MODELS.keys()):
        cfg = RECOMMENDED_MODELS[model_name]
        model_provider = (cfg.get("provider") or "").lower()
        model_text = cfg.get("text_generation", False)
        model_vision = cfg.get("vision", False)
        model_image = cfg.get("image_generation", False)
        model_image_mod = cfg.get("image_modification", False)
        model_audio = cfg.get("audio_transcription", False)

        context = cfg.get("context_window_tokens")
        if context is None:
            context = cfg.get("context_window")

        max_tokens = cfg.get("output_tokens")
        if max_tokens is None:
            max_tokens = cfg.get("max_output_tokens")

        if provider and model_provider != provider.lower():
            continue
        if text_generation is not None and bool(model_text) != bool(text_generation):
            continue
        if vision is not None and bool(model_vision) != bool(vision):
            continue
        if image_generation is not None and bool(model_image) != bool(image_generation):
            continue
        if image_modification is not None and bool(model_image_mod) != bool(image_modification):
            continue
        if audio_transcription is not None and bool(model_audio) != bool(audio_transcription):
            continue
        if min_context and (context is None or (isinstance(context, int) and context < min_context)):
            continue
        if min_output_tokens and (max_tokens is None or (isinstance(max_tokens, int) and max_tokens < min_output_tokens)):
            continue

        def _fmt_num(x: Any) -> str:
            if x is None:
                return "-"
            try:
                return f"{int(x):,}"
            except Exception:
                return str(x)

        rows.append(
            f"| {model_name} | {model_provider or '-'} | {'✅' if model_text else '❌'} | "
            f"{'✅' if model_vision else '❌'} | {'✅' if model_image else '❌'} | "
            f"{'✅' if model_image_mod else '❌'} | {'✅' if model_audio else '❌'} | "
            f"{_fmt_num(context)} | {_fmt_num(max_tokens)} |"
        )

    if not rows:
        return "No models match the specified criteria."

    header = (
        "| Model | Provider | Text | Vision | Image Gen | Image Edit | Audio Transcription | Context Window | Max Output Tokens |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
    )
    table = header + "\n".join(rows)
    display(Markdown(table))
    return table

__all__ = ['RECOMMENDED_MODELS', 'recommended_models_table']

#!/usr/bin/env python3
"""
Multi-LLM Provider Demonstration

Tests availability and configuration of all supported LLM providers:
OpenAI (GPT), GLM (ChatGLM/Qwen), and DeepSeek.

Shows current configuration, validates API keys, and runs a quick
smoke test on each configured provider.
"""

import os
import sys
from loguru import logger

from isaac_agent.config import settings
from isaac_agent.llm_factory import init_llm


def check_provider(name: str, env_key: str) -> dict:
    """Check if a provider is configured and test initialization.

    Returns a dict with status info.
    """
    result = {
        "provider": name,
        "api_key_set": bool(os.getenv(env_key)),
        "initialized": False,
        "error": None,
    }

    try:
        llm = init_llm(provider=name)
        if llm is not None:
            result["initialized"] = True
            result["model"] = getattr(llm, "model_name", str(llm))
        else:
            result["error"] = "init_llm returned None (missing API key or config)"
    except Exception as e:
        result["error"] = str(e)

    return result


def show_config() -> None:
    """Display current LLM configuration from settings."""
    print("\n" + "=" * 60)
    print("  LLM Configuration (from .env / environment)")
    print("=" * 60)
    print(f"  LLM_PROVIDER:        {settings.llm_provider or '(not set)'}")
    print(f"  OPENAI_API_KEY:      {'***' if settings.openai_api_key else '(not set)'}")
    print(f"  OPENAI_MODEL:        {settings.openai_model}")
    print(f"  GLM_API_KEY:         {'***' if settings.glm_api_key else '(not set)'}")
    print(f"  GLM_MODEL:           {settings.glm_model}")
    print(f"  DEEPSEEK_API_KEY:    {'***' if settings.deepseek_api_key else '(not set)'}")
    print(f"  DEEPSEEK_MODEL:       {settings.deepseek_model}")
    print(f"  TEMPERATURE:         {settings.temperature}")
    print(f"  MAX_TOKENS:          {settings.max_tokens}")
    print("=" * 60)


def test_providers() -> None:
    """Test all providers and report status."""
    print("\n" + "=" * 60)
    print("  LLM Provider Status")
    print("=" * 60)

    providers = [
        ("openai", "OPENAI_API_KEY"),
        ("glm", "GLM_API_KEY"),
        ("deepseek", "DEEPSEEK_API_KEY"),
    ]

    results = []
    for name, env_key in providers:
        result = check_provider(name, env_key)
        results.append(result)

        status = "READY" if result["initialized"] else "UNAVAILABLE"
        print(f"\n  [{status}] {name}")
        print(f"    API Key:    {'configured' if result['api_key_set'] else 'missing'}")
        if result["initialized"]:
            print(f"    Model:      {result.get('model', '?')}")
        if result["error"]:
            print(f"    Error:      {result['error']}")

    print("\n" + "=" * 60)
    ready = [r for r in results if r["initialized"]]
    print(f"  Providers ready: {len(ready)}/{len(results)}")
    if ready:
        print(f"  Available: {', '.join(r['provider'] for r in ready)}")
    else:
        print("  No LLM providers configured. Set API keys in .env to enable.")
        print("  The agent will use fallback keyword-based parsing instead.")
    print("=" * 60 + "\n")


def run_smoke_test() -> None:
    """Run a quick smoke test on the default provider."""
    provider = settings.llm_provider
    if not provider:
        print("No default LLM provider configured — skipping smoke test.")
        return

    print(f"\n  Running smoke test on default provider: {provider}")
    try:
        llm = init_llm()
        if llm is None:
            print("  Failed to initialize LLM.")
            return

        # Simple invocation test
        from langchain_core.messages import HumanMessage
        import asyncio

        async def _test():
            response = await llm.ainvoke([HumanMessage(content="Say 'hello' in one word.")])
            content = response.content if hasattr(response, "content") else str(response)
            print(f"  Response: {content[:100]}")

        asyncio.run(_test())
    except Exception as e:
        print(f"  Smoke test failed: {e}")


def main() -> None:
    """Entry point for demo_llm_providers.py"""
    show_config()
    test_providers()
    if "--smoke" in sys.argv:
        run_smoke_test()


if __name__ == "__main__":
    main()

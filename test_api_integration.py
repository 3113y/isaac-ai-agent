#!/usr/bin/env python3
"""
API Integration Test

End-to-end test exercising the full Isaac AI Agent workflow through the API:
1. Health check
2. Template listing
3. API search
4. Mod generation (multiple scenarios)
5. Output folder structure verification via ModBuilder
"""

import json
import sys
from pathlib import Path

import httpx
from loguru import logger

BASE_URL = "http://localhost:8000"
BUILD_DIR = Path("build")


def check_server() -> bool:
    """Verify the API server is reachable."""
    try:
        resp = httpx.get(f"{BASE_URL}/health", timeout=5)
        return resp.status_code == 200
    except httpx.ConnectError:
        return False


def test_health() -> dict:
    """Test health endpoint."""
    resp = httpx.get(f"{BASE_URL}/health")
    assert resp.status_code == 200, f"Health failed: {resp.text}"
    return resp.json()


def test_info() -> dict:
    """Test agent info endpoint."""
    resp = httpx.get(f"{BASE_URL}/info")
    assert resp.status_code == 200, f"Info failed: {resp.text}"
    return resp.json()


def test_templates() -> dict:
    """Test template listing."""
    resp = httpx.get(f"{BASE_URL}/templates")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["templates"]) >= 6, f"Expected >=6 templates, got {len(data['templates'])}"
    return data


def test_api_search(query: str = "GetPlayer") -> dict:
    """Test API search."""
    resp = httpx.get(f"{BASE_URL}/api/search", params={"query": query})
    assert resp.status_code == 200
    return resp.json()


def test_generate(user_input: str) -> dict:
    """Test mod generation and return response."""
    resp = httpx.post(
        f"{BASE_URL}/generate",
        json={"user_input": user_input},
        timeout=60,
    )
    assert resp.status_code == 200, f"Generate failed: {resp.text}"
    data = resp.json()
    assert "session_id" in data
    assert len(data["generated_code"]) > 0, "Expected at least one code artifact"
    return data


def build_mod_from_response(response: dict, mod_name: str) -> Path:
    """Build a mod folder from an API response using ModBuilder."""
    from isaac_agent.core.state import GeneratedCode
    from isaac_agent.build import ModBuilder

    artifacts = [
        GeneratedCode(
            scaffold_type=a["scaffold_type"],
            lua_code=a["lua_code"],
            imports=a.get("imports", []),
            dependencies=a.get("dependencies", []),
        )
        for a in response["generated_code"]
    ]

    builder = ModBuilder()
    return builder.build(
        artifacts=artifacts,
        mod_name=mod_name,
        mod_description=response.get("user_input", ""),
        session_id=response["session_id"],
    )


def print_tree(path: Path, prefix: str = "") -> None:
    """Print directory tree."""
    items = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "  └── " if is_last else "  ├── "
        if item.is_dir():
            print(f"{prefix}{connector}{item.name}/")
            print_tree(item, prefix + ("     " if is_last else "  │   "))
        else:
            size = item.stat().st_size
            if size < 1024:
                size_str = f" ({size}B)"
            elif size < 1024 * 1024:
                size_str = f" ({size // 1024}KB)"
            else:
                size_str = f" ({size // 1024 // 1024}MB)"
            print(f"{prefix}{connector}{item.name}{size_str}")


def main() -> None:
    """Run all integration tests against the API server."""
    print("\n" + "=" * 70)
    print("  Isaac AI Agent — API Integration Test")
    print("=" * 70)

    if not check_server():
        print("\n  ERROR: API server is not running!")
        print(f"  Start it with: uvicorn isaac_agent.api:app --reload --host 0.0.0.0 --port 8000")
        print(f"  Or: make serve")
        sys.exit(1)

    print("  Server is running.\n")

    # Phase 1: Read-only endpoints
    print("─" * 70)
    print("  Phase 1: Read-only endpoints")
    print("─" * 70)

    health = test_health()
    print(f"  GET /health       -> status={health['status']}, agent_ready={health['agent_ready']}")

    info = test_info()
    print(f"  GET /info         -> stages={len(info['stages'])}, has_llm={info['has_llm']}")

    templates = test_templates()
    print(f"  GET /templates    -> {len(templates['templates'])} templates: {', '.join(templates['templates'])}")

    search_result = test_api_search("player health")
    print(f"  GET /api/search   -> {len(search_result['results'])} results for 'player health'")

    # Phase 2: Mod generation
    print(f"\n{'─' * 70}")
    print("  Phase 2: Mod generation (no LLM — fallback parser)")
    print("─" * 70)

    test_scenarios = [
        ("health_on_clear", "Give the player one full heart when they clear a room"),
        ("explosive_item", "Create a custom active item called Megablast that spawns explosions"),
        ("speed_demon", "Create a custom enemy called Speed Demon that moves fast and explodes on death"),
        ("starter_bonus", "Give the player coins, bombs, and keys at the start of a new game"),
    ]

    for mod_slug, prompt in test_scenarios:
        print(f"\n  Test prompt: \"{prompt}\"")
        response = test_generate(prompt)
        print(f"    Session: {response['session_id']}")
        print(f"    Status: {response['status']}")
        print(f"    Stage: {response['stage']}")
        print(f"    Artifacts: {len(response['generated_code'])}")
        for a in response["generated_code"]:
            code_len = len(a["lua_code"])
            print(f"      - {a['scaffold_type']}: {code_len} chars")

        # Build mod folder
        mod_path = build_mod_from_response(response, mod_slug)
        print(f"\n    Output folder structure ({mod_path}):")
        print_tree(mod_path)

    # Summary
    print(f"\n{'═' * 70}")
    print(f"  Integration test complete.")
    print(f"  All builds in: {BUILD_DIR.resolve()}")
    built = sorted(BUILD_DIR.iterdir()) if BUILD_DIR.exists() else []
    for b in built:
        if b.is_dir():
            print(f"    {b.name}/")
    print(f"{'═' * 70}\n")


if __name__ == "__main__":
    main()

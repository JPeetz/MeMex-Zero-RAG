"""Shared pytest fixtures for the MeMex Zero-RAG backend test suite.

The ``mcp/`` directory shadows the pip-installed ``mcp`` package, so we
cannot simply ``from mcp.server import MemexServer`` in tests without
risking collisions with third-party imports elsewhere in the process.
Instead, we load ``mcp/server.py`` directly via ``importlib.util`` under
a distinct module name (``memex_server``) and expose it as a fixture.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVER_PATH = REPO_ROOT / "mcp" / "server.py"


def _load_memex_server_module():
    """Load mcp/server.py as a standalone module named 'memex_server'."""
    if "memex_server" in sys.modules:
        return sys.modules["memex_server"]

    # Ensure the repo root is on sys.path so intra-repo imports resolve.
    repo_root_str = str(REPO_ROOT)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)

    spec = importlib.util.spec_from_file_location(
        "memex_server", str(SERVER_PATH)
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load spec for {SERVER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["memex_server"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def memex_server_module():
    """Return the loaded ``mcp/server.py`` module (as ``memex_server``)."""
    return _load_memex_server_module()

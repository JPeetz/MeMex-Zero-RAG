"""Shared pytest fixtures for the MeMex Zero-RAG backend test suite.

The repo's local package is ``memex_mcp`` (renamed from ``mcp/``) so it can
never shadow the pip-installed ``mcp`` SDK package. ``server.py`` includes a
runtime path bootstrap so it imports cleanly regardless of how it is run. We
still load ``memex_mcp/server.py`` via ``importlib.util`` under a distinct
module name (``memex_server``) for clean fixture isolation.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVER_PATH = REPO_ROOT / "memex_mcp" / "server.py"


def _load_memex_server_module():
    """Load memex_mcp/server.py as a standalone module named 'memex_server'."""
    if "memex_server" in sys.modules:
        return sys.modules["memex_server"]
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
    """Return the loaded ``memex_mcp/server.py`` module (as ``memex_server``)."""
    return _load_memex_server_module()

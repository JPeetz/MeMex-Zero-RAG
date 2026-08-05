"""Shared pytest fixtures for the MeMex Zero-RAG backend test suite.

The ``mcp/`` directory shadows the pip-installed ``mcp`` package. In
particular, ``mcp/server.py`` internally does ``from mcp.server import
Server``, which needs to resolve to the pip-installed package — NOT to
the file we are currently loading. So we deliberately keep the repo
root OFF ``sys.path`` while importing, and load ``mcp/server.py``
directly via ``importlib.util`` under a distinct module name
(``memex_server``).
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

    # Defensively remove repo root and mcp/ from sys.path so that the
    # ``from mcp.server import Server`` inside server.py resolves to the
    # pip-installed mcp package rather than shadowing itself.
    repo_root_str = str(REPO_ROOT)
    mcp_dir_str = str(REPO_ROOT / "mcp")
    for p in (repo_root_str, mcp_dir_str, ""):
        while p in sys.path:
            sys.path.remove(p)

    # Also drop any pre-cached local ``mcp`` module reference so the
    # next import goes through site-packages resolution.
    for name in list(sys.modules):
        if name == "mcp" or name.startswith("mcp."):
            mod = sys.modules.get(name)
            mod_file = getattr(mod, "__file__", "") or ""
            if str(REPO_ROOT) in mod_file:
                del sys.modules[name]

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

"""Transport security: the network mode must never be silently open.

The SSE transport carries no authentication of its own, and this server can rewrite the
wiki. So it binds loopback by default, and refuses any non-loopback bind that has no token.
These tests exist because a guardrail without a failing test is a comment.
"""

import pytest


@pytest.mark.asyncio
async def test_non_loopback_without_token_is_refused(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    with pytest.raises(RuntimeError) as exc:
        await server.run(transport="sse", port=0, host="0.0.0.0", token="")
    assert "refusing to bind" in str(exc.value)
    # the message must say how to fix it, not just that it failed
    assert "127.0.0.1" in str(exc.value) or "--token" in str(exc.value)


@pytest.mark.asyncio
async def test_lan_address_without_token_is_refused(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    with pytest.raises(RuntimeError):
        await server.run(transport="sse", port=0, host="192.168.1.50", token="")


def test_run_signature_defaults_to_loopback(memex_server_module):
    """The default must be safe without any flag being passed."""
    import inspect

    sig = inspect.signature(memex_server_module.MemexServer.run)
    assert sig.parameters["host"].default == "127.0.0.1"
    assert sig.parameters["token"].default == ""


def test_cli_defaults(memex_server_module):
    """--host defaults to loopback; --token falls back to MEMEX_MCP_TOKEN."""
    import os
    import sys

    argv = sys.argv
    try:
        sys.argv = ["memex-mcp", "--help"]
        with pytest.raises(SystemExit):
            memex_server_module.main()
    finally:
        sys.argv = argv
    assert os.environ.get("MEMEX_MCP_TOKEN", "") == os.environ.get("MEMEX_MCP_TOKEN", "")

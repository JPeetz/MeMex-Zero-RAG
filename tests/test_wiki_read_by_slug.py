"""Tests for the wiki_read_by_slug MCP tool.

wiki_read_by_slug finds a page by bare slug (no type prefix) by scanning
all four type dirs (entities/concepts/sources/synthesis). It must:
  - return found=false (not raise) when no page matches
  - raise a clear "ambiguous" error listing all candidate paths when the
    slug matches in more than one type dir
  - otherwise delegate to _read() and return its content
"""
import pytest


@pytest.mark.asyncio
async def test_read_by_slug_finds_unique_match(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="zero-rag",
        title="Zero RAG",
        content="body [Source: raw/test.md]",
        agent="test",
    )

    result = await server._read_by_slug("zero-rag")

    assert result["found"] is True
    assert result["path"] == "concepts/zero-rag"
    assert "Zero RAG" in result["content"]


@pytest.mark.asyncio
async def test_read_by_slug_missing_returns_found_false(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()

    result = await server._read_by_slug("does-not-exist")

    assert result["found"] is False
    assert "path" not in result or result.get("path") is None


@pytest.mark.asyncio
async def test_read_by_slug_ambiguous_raises_with_candidates(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    (tmp_path / "entities").mkdir()
    await server._write(
        page_type="concepts",
        slug="marvin",
        title="Marvin (concept)",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._write(
        page_type="entities",
        slug="marvin",
        title="Marvin (entity)",
        content="body [Source: raw/test.md]",
        agent="test",
    )

    with pytest.raises(memex_server_module.AmbiguousSlugError) as exc_info:
        await server._read_by_slug("marvin")

    candidates = exc_info.value.candidates
    assert set(candidates) == {"concepts/marvin", "entities/marvin"}


@pytest.mark.asyncio
async def test_read_by_slug_normalizes_slug_input(tmp_path, memex_server_module):
    """Bare slug should tolerate a leading slash and a trailing .md."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "sources").mkdir()
    await server._write(
        page_type="sources",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )

    result = await server._read_by_slug("/foo.md")

    assert result["found"] is True
    assert result["path"] == "sources/foo"


@pytest.mark.asyncio
async def test_read_by_slug_rejects_slug_with_type_prefix(tmp_path, memex_server_module):
    """This tool takes a *bare* slug — a path containing a '/' is invalid input."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )

    with pytest.raises(ValueError):
        await server._read_by_slug("concepts/foo")


@pytest.mark.asyncio
async def test_read_by_slug_delegates_to_read(tmp_path, memex_server_module):
    """The content returned for a unique match must match plain _read()'s output."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )

    direct = await server._read("concepts/foo")
    via_slug = await server._read_by_slug("foo")

    assert via_slug["content"] == direct


@pytest.mark.asyncio
async def test_wiki_read_by_slug_tool_is_registered(memex_server_module):
    """The tool schema must exist so MCP clients can discover wiki_read_by_slug."""
    server = memex_server_module.MemexServer(wiki_path="wiki")
    import sys

    ListToolsRequest = sys.modules["mcp.types"].ListToolsRequest
    list_handler = server.server.request_handlers[ListToolsRequest]

    res = await list_handler(ListToolsRequest(method="tools/list"))
    names = [t.name for t in res.root.tools]
    assert "wiki_read_by_slug" in names


@pytest.mark.asyncio
async def test_wiki_read_by_slug_via_dispatcher(tmp_path, memex_server_module):
    """Exercise wiki_read_by_slug through the real MCP call_tool dispatcher."""
    import sys

    CallToolRequest = sys.modules["mcp.types"].CallToolRequest
    CallToolRequestParams = sys.modules["mcp.types"].CallToolRequestParams

    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )

    call_handler = server.server.request_handlers[CallToolRequest]
    req = CallToolRequest(
        method="tools/call",
        params=CallToolRequestParams(name="wiki_read_by_slug", arguments={"slug": "foo"}),
    )
    result = await call_handler(req)
    text = result.root.content[0].text
    assert "title: Foo" in text
    assert "body [Source: raw/test.md]" in text


@pytest.mark.asyncio
async def test_wiki_read_by_slug_via_dispatcher_missing_returns_json_not_found(
    tmp_path, memex_server_module
):
    """A missing slug must surface as found=false, not as a thrown error."""
    import json
    import sys

    CallToolRequest = sys.modules["mcp.types"].CallToolRequest
    CallToolRequestParams = sys.modules["mcp.types"].CallToolRequestParams

    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()

    call_handler = server.server.request_handlers[CallToolRequest]
    req = CallToolRequest(
        method="tools/call",
        params=CallToolRequestParams(name="wiki_read_by_slug", arguments={"slug": "nope"}),
    )
    result = await call_handler(req)
    text = result.root.content[0].text
    assert json.loads(text) == {"found": False}


@pytest.mark.asyncio
async def test_wiki_read_by_slug_via_dispatcher_ambiguous_surfaces_candidates(
    tmp_path, memex_server_module
):
    """An ambiguous slug must surface a structured JSON payload naming
    candidates, not the generic str(exception) error-string fallback."""
    import json
    import sys

    CallToolRequest = sys.modules["mcp.types"].CallToolRequest
    CallToolRequestParams = sys.modules["mcp.types"].CallToolRequestParams

    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    (tmp_path / "entities").mkdir()
    await server._write(
        page_type="concepts", slug="marvin", title="Marvin (concept)",
        content="body [Source: raw/test.md]", agent="test",
    )
    await server._write(
        page_type="entities", slug="marvin", title="Marvin (entity)",
        content="body [Source: raw/test.md]", agent="test",
    )

    call_handler = server.server.request_handlers[CallToolRequest]
    req = CallToolRequest(
        method="tools/call",
        params=CallToolRequestParams(name="wiki_read_by_slug", arguments={"slug": "marvin"}),
    )
    result = await call_handler(req)
    text = result.root.content[0].text

    # Must NOT fall through to the generic "Error: <str(exception)>" handler.
    assert not text.startswith("Error:")

    payload = json.loads(text)
    assert payload["found"] is False
    assert payload["ambiguous"] is True
    assert set(payload["candidates"]) == {"concepts/marvin", "entities/marvin"}

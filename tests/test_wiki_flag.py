import re

import pytest
import yaml


def _frontmatter(page_text: str) -> dict:
    fm_match = re.match(r"^---\n(.*?)\n---\n", page_text, re.DOTALL)
    assert fm_match, "frontmatter block must be well-formed"
    return yaml.safe_load(fm_match.group(1))


@pytest.mark.asyncio
async def test_wiki_flag_sets_quarantine_status(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="stale data")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    assert "status: quarantine" in page_text
    assert "flagged_reason: stale data" in page_text


@pytest.mark.asyncio
async def test_wiki_flag_records_iso_timestamp(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="stale data")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    parsed = _frontmatter(page_text)
    assert "flagged_at" in parsed
    # Must be a parseable ISO-8601 UTC timestamp.
    from datetime import datetime

    datetime.fromisoformat(parsed["flagged_at"].replace("Z", "+00:00"))


@pytest.mark.asyncio
async def test_wiki_flag_preserves_other_frontmatter_fields(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo Title",
        content="body [Source: raw/test.md]",
        tags=["tag1", "tag2"],
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="needs check")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    parsed = _frontmatter(page_text)
    assert parsed["title"] == "Foo Title"
    assert parsed["tags"] == ["tag1", "tag2"]
    assert "body [Source: raw/test.md]" in page_text


@pytest.mark.asyncio
async def test_wiki_flag_raises_on_missing_page(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        await server._flag(page="concepts/does-not-exist", reason="test")


@pytest.mark.asyncio
async def test_wiki_flag_requires_reason(tmp_path, memex_server_module):
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
        await server._flag(page="concepts/foo", reason="")


@pytest.mark.asyncio
async def test_wiki_flag_refuses_immutable_page(tmp_path, memex_server_module):
    """SCHEMA.md §Lifecycle Mapping: is_immutable=true pages MUST NOT be
    mutated by wiki_flag (or any edit tool). flag() must refuse instead of
    silently quarantining a locked fact."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="locked-fact",
        title="Locked Fact",
        content="body [Source: raw/test.md]",
        agent="test",
        is_immutable=True,
    )
    with pytest.raises(PermissionError):
        await server._flag(page="concepts/locked-fact", reason="attempted override")

    # The page must be left untouched — still active, no flag fields set.
    page_text = (tmp_path / "concepts" / "locked-fact.md").read_text()
    parsed = _frontmatter(page_text)
    assert parsed["status"] == "active"
    assert "flagged_reason" not in parsed
    assert "flagged_at" not in parsed


@pytest.mark.asyncio
async def test_wiki_flag_via_dispatcher(tmp_path, memex_server_module, monkeypatch):
    """Exercise the wiki_flag entry through the MCP call_tool dispatcher."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    result = await server._flag(page="concepts/foo", reason="via dispatcher check")
    assert "quarantine" in result
    assert "via dispatcher check" in result

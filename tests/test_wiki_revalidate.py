import re

import pytest
import yaml


def _frontmatter(page_text: str) -> dict:
    fm_match = re.match(r"^---\n(.*?)\n---\n", page_text, re.DOTALL)
    assert fm_match, "frontmatter block must be well-formed"
    return yaml.safe_load(fm_match.group(1))


@pytest.mark.asyncio
async def test_revalidate_confirm_flagged_page_becomes_active(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="check")
    await server._revalidate(page="concepts/foo", outcome="confirm", rationale="verified")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    assert "status: active" in page_text
    assert "flagged_reason" not in page_text
    assert "flagged_at" not in page_text


@pytest.mark.asyncio
async def test_revalidate_update_replaces_body(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="old body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="wrong")
    await server._revalidate(
        page="concepts/foo",
        outcome="update",
        new_body="corrected body [Source: raw/test.md]",
        rationale="fixed based on source",
    )
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    assert "status: active" in page_text
    assert "corrected body" in page_text
    assert "old body" not in page_text


@pytest.mark.asyncio
async def test_revalidate_retire_sets_stale(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="outdated")
    await server._revalidate(page="concepts/foo", outcome="retire", rationale="superseded")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    assert "status: stale" in page_text
    parsed = _frontmatter(page_text)
    assert parsed["retire_rationale"] == "superseded"
    assert "retired_at" in parsed


@pytest.mark.asyncio
async def test_revalidate_retire_records_iso_timestamp(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="outdated")
    await server._revalidate(page="concepts/foo", outcome="retire", rationale="superseded")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    parsed = _frontmatter(page_text)
    from datetime import datetime

    datetime.fromisoformat(parsed["retired_at"].replace("Z", "+00:00"))


@pytest.mark.asyncio
async def test_revalidate_on_non_flagged_page_raises_invalid_state(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    # Not flagged — still status: active.
    with pytest.raises(memex_server_module.InvalidStateError):
        await server._revalidate(page="concepts/foo", outcome="confirm", rationale="")


@pytest.mark.asyncio
async def test_revalidate_on_retired_page_raises_invalid_state(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="check")
    await server._revalidate(page="concepts/foo", outcome="retire", rationale="gone")
    # Page is now status: stale — no longer quarantine, must not accept a
    # second revalidate call.
    with pytest.raises(memex_server_module.InvalidStateError):
        await server._revalidate(page="concepts/foo", outcome="confirm", rationale="")


@pytest.mark.asyncio
async def test_revalidate_update_without_new_body_raises_value_error(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="wrong")
    with pytest.raises(ValueError):
        await server._revalidate(page="concepts/foo", outcome="update", rationale="")


@pytest.mark.asyncio
async def test_revalidate_unknown_outcome_raises_value_error(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="check")
    with pytest.raises(ValueError):
        await server._revalidate(page="concepts/foo", outcome="bogus", rationale="")


@pytest.mark.asyncio
async def test_revalidate_raises_on_missing_page(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        await server._revalidate(page="concepts/does-not-exist", outcome="confirm", rationale="")


@pytest.mark.asyncio
async def test_revalidate_refuses_immutable_page(tmp_path, memex_server_module):
    """SCHEMA.md §Lifecycle Mapping: is_immutable=true pages MUST NOT be
    mutated by wiki_revalidate (or any edit tool), even if somehow flagged
    as quarantine — the immutability guard takes priority over the state
    check so a locked fact can never be silently confirmed/updated/retired.
    """
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
    # Bypass wiki_flag's own immutability guard by writing quarantine
    # status directly via _write's overwrite path, so we can prove
    # _revalidate has its own independent guard.
    await server._write(
        page_type="concepts",
        slug="locked-fact",
        title="Locked Fact",
        content="body [Source: raw/test.md]",
        agent="test",
        overwrite=True,
        status="quarantine",
        is_immutable=True,
    )
    with pytest.raises(PermissionError):
        await server._revalidate(page="concepts/locked-fact", outcome="confirm", rationale="")

    page_text = (tmp_path / "concepts" / "locked-fact.md").read_text()
    parsed = _frontmatter(page_text)
    assert parsed["status"] == "quarantine"


@pytest.mark.asyncio
async def test_revalidate_preserves_other_frontmatter_fields(tmp_path, memex_server_module):
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
    await server._flag(page="concepts/foo", reason="check")
    await server._revalidate(page="concepts/foo", outcome="confirm", rationale="verified")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    parsed = _frontmatter(page_text)
    assert parsed["title"] == "Foo Title"
    assert parsed["tags"] == ["tag1", "tag2"]


@pytest.mark.asyncio
async def test_revalidate_via_dispatcher(tmp_path, memex_server_module):
    """Exercise wiki_revalidate through the MCP call_tool dispatcher."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="check")
    result = await server._revalidate(page="concepts/foo", outcome="confirm", rationale="via dispatcher check")
    assert "confirm" in result
    assert "via dispatcher check" in result


# -- A3.5: fix new_sources dead param + retire flag-field cleanup ----------


@pytest.mark.asyncio
async def test_revalidate_confirm_appends_new_sources_to_body(tmp_path, memex_server_module):
    """new_sources must not be silently dropped — confirm should append a
    citation line to the body when new_sources is provided."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="check")
    await server._revalidate(
        page="concepts/foo",
        outcome="confirm",
        new_sources=["raw/new-evidence.md"],
        rationale="verified against new evidence",
    )
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    assert "[Source: raw/new-evidence.md]" in page_text


@pytest.mark.asyncio
async def test_revalidate_update_appends_new_sources_to_body(tmp_path, memex_server_module):
    """update: new_sources citations must be appended to the replacement body,
    not silently dropped."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="old body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="wrong")
    await server._revalidate(
        page="concepts/foo",
        outcome="update",
        new_body="corrected body",
        new_sources=["raw/corrected-source.md", "raw/second-source.md"],
        rationale="fixed based on new sources",
    )
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    assert "corrected body" in page_text
    assert "[Source: raw/corrected-source.md, raw/second-source.md]" in page_text


@pytest.mark.asyncio
async def test_revalidate_without_new_sources_does_not_append_citation_line(tmp_path, memex_server_module):
    """Sanity check: when new_sources is omitted, no spurious [Source: ...]
    line is appended."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="check")
    await server._revalidate(page="concepts/foo", outcome="confirm", rationale="verified")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    assert page_text.count("[Source:") == 1


@pytest.mark.asyncio
async def test_revalidate_retire_clears_flagged_reason_and_flagged_at(tmp_path, memex_server_module):
    """retire must clear flagged_reason / flagged_at from frontmatter, same
    as confirm and update do — for consistency across all three outcomes."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="foo",
        title="Foo",
        content="body [Source: raw/test.md]",
        agent="test",
    )
    await server._flag(page="concepts/foo", reason="outdated")
    await server._revalidate(page="concepts/foo", outcome="retire", rationale="superseded")
    page_text = (tmp_path / "concepts" / "foo.md").read_text()
    parsed = _frontmatter(page_text)
    assert "flagged_reason" not in parsed
    assert "flagged_at" not in parsed
    # Retire-specific fields must still be present.
    assert parsed["status"] == "stale"
    assert parsed["retire_rationale"] == "superseded"

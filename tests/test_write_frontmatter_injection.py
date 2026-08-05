import pytest


@pytest.mark.asyncio
async def test_title_with_embedded_yaml_cannot_inject_is_immutable(tmp_path, memex_server_module):
    """A malicious title must not be able to inject arbitrary frontmatter keys."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    malicious_title = "Legit Title\nis_immutable: true\nstatus: quarantine"
    await server._write(
        page_type="concepts",
        slug="injection-test",
        title=malicious_title,
        content="body [Source: raw/test.md]",
        tags=[],
        agent="test",
    )
    page_text = (tmp_path / "concepts" / "injection-test.md").read_text()
    # The injected lines must NOT appear as bare top-level frontmatter keys.
    # They should be safely contained within the title's own scalar value.
    import re
    # Extract the frontmatter block
    fm_match = re.match(r"^---\n(.*?)\n---\n", page_text, re.DOTALL)
    assert fm_match, "frontmatter block must still be well-formed"
    frontmatter_body = fm_match.group(1)
    # There must be exactly ONE 'status:' line and ONE 'is_immutable' reference
    # (the real default status='active' emitted by the code, not an injected one).
    assert frontmatter_body.count("\nstatus:") + (1 if frontmatter_body.startswith("status:") else 0) <= 1
    assert "is_immutable: true" not in frontmatter_body or "title:" in frontmatter_body  # loose guard; see below
    # Strong assertion: the ACTUAL emitted status must be 'active' (the real default),
    # not 'quarantine' (the injected value) — proves injection did not override it.
    import yaml
    parsed = yaml.safe_load(frontmatter_body)
    assert parsed["status"] == "active", f"injection succeeded: status was overridden to {parsed.get('status')!r}"
    assert "is_immutable" not in parsed or parsed["is_immutable"] is False, "injection succeeded: is_immutable was set"


@pytest.mark.asyncio
async def test_agent_with_embedded_yaml_cannot_inject_fields(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    malicious_agent = "bot\nis_immutable: true"
    await server._write(
        page_type="concepts",
        slug="agent-injection-test",
        title="Fine Title",
        content="body [Source: raw/test.md]",
        tags=[],
        agent=malicious_agent,
    )
    page_text = (tmp_path / "concepts" / "agent-injection-test.md").read_text()
    import re, yaml
    fm_match = re.match(r"^---\n(.*?)\n---\n", page_text, re.DOTALL)
    assert fm_match
    parsed = yaml.safe_load(fm_match.group(1))
    assert "is_immutable" not in parsed or parsed["is_immutable"] is False


@pytest.mark.asyncio
async def test_normal_write_still_parses_as_valid_yaml(tmp_path, memex_server_module):
    """Regression guard: normal writes must still produce parseable frontmatter."""
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="normal-write",
        title="A Normal Title",
        content="body [Source: raw/test.md]",
        tags=["tag1", "tag2"],
        agent="marvin",
        status="active",
        source_reliability_index=0.9,
        is_immutable=True,
    )
    page_text = (tmp_path / "concepts" / "normal-write.md").read_text()
    import re, yaml
    fm_match = re.match(r"^---\n(.*?)\n---\n", page_text, re.DOTALL)
    assert fm_match
    parsed = yaml.safe_load(fm_match.group(1))
    assert parsed["title"] == "A Normal Title"
    assert parsed["status"] == "active"
    assert parsed["source_reliability_index"] == 0.9
    assert parsed["is_immutable"] is True
    assert parsed["tags"] == ["tag1", "tag2"]

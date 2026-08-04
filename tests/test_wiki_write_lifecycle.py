import json
import pytest
from pathlib import Path


@pytest.mark.asyncio
async def test_wiki_write_accepts_status_and_sri(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    # Create required subdirs
    (tmp_path / "concepts").mkdir()
    result = await server._write(
        page_type="concepts",
        slug="test-lifecycle",
        title="Test Lifecycle",
        content="body content [Source: raw/test.md]",
        tags=[],
        agent="test",
        status="quarantine",
        source_reliability_index=0.75,
        is_immutable=True,
    )
    page = (tmp_path / "concepts" / "test-lifecycle.md").read_text()
    assert "status: quarantine" in page
    assert "source_reliability_index: 0.75" in page
    assert "is_immutable: true" in page


@pytest.mark.asyncio
async def test_wiki_write_defaults_status_to_active(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="default-status",
        title="Default",
        content="body [Source: raw/test.md]",
        tags=[],
        agent="test",
    )
    page = (tmp_path / "concepts" / "default-status.md").read_text()
    assert "status: active" in page


@pytest.mark.asyncio
async def test_wiki_write_omits_sri_and_immutable_when_not_passed(tmp_path, memex_server_module):
    server = memex_server_module.MemexServer(wiki_path=str(tmp_path))
    (tmp_path / "concepts").mkdir()
    await server._write(
        page_type="concepts",
        slug="minimal",
        title="Minimal",
        content="body [Source: raw/test.md]",
        tags=[],
        agent="test",
    )
    page = (tmp_path / "concepts" / "minimal.md").read_text()
    assert "source_reliability_index" not in page
    assert "is_immutable" not in page

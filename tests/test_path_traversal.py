"""Path containment for client-supplied page names and types.

A wiki is a directory of files, and every path component that reaches it comes from an MCP
client. Traversal here means reading a private key or writing an authorised_keys file, so
these are the tests that matter most in the suite.
"""

import pytest

TRAVERSALS = [
    "../outside",
    "../../outside",
    "a/../../outside",
    "./../outside",
]

# Not traversals: b"..%2f" is URL encoding, which the filesystem never decodes, and "...."
# is a legal directory name. These must resolve *inside* the root, which is the safe outcome —
# asserting rejection would have been a test that lies about what the guard does.
IN_ROOT = ["..%2foutside", "....//outside"]


@pytest.mark.parametrize("name", TRAVERSALS)
def test_contained_rejects_traversal(memex_server_module, tmp_path, name):
    root = tmp_path / "wiki"
    root.mkdir()
    with pytest.raises(ValueError, match="escapes the wiki root"):
        memex_server_module._contained(root, f"{name}.md")


@pytest.mark.parametrize("name", IN_ROOT)
def test_contained_keeps_encoded_and_dotted_names_inside(memex_server_module, tmp_path, name):
    root = tmp_path / "wiki"
    root.mkdir()
    got = memex_server_module._contained(root, f"{name}.md")
    assert root.resolve() in got.parents


def test_contained_allows_normal_pages(memex_server_module, tmp_path):
    root = tmp_path / "wiki"
    root.mkdir()
    got = memex_server_module._contained(root, "concepts", "zero-rag.md")
    assert got == (root / "concepts" / "zero-rag.md").resolve()


def test_contained_rejects_absolute_path(memex_server_module, tmp_path):
    root = tmp_path / "wiki"
    root.mkdir()
    with pytest.raises(ValueError):
        memex_server_module._contained(root, "/etc/passwd.md")


def test_contained_rejects_symlink_escape(memex_server_module, tmp_path):
    """Resolution happens before the check, so a symlink pointing out cannot pass."""
    root = tmp_path / "wiki"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "link").symlink_to(outside)
    with pytest.raises(ValueError, match="escapes the wiki root"):
        memex_server_module._contained(root, "link", "page.md")


@pytest.mark.parametrize("page_type", ["../concepts", "/abs", "", ".", "a/b", "Concepts", "x" * 40])
def test_safe_type_rejects_bad_types(memex_server_module, page_type):
    with pytest.raises(ValueError):
        memex_server_module._safe_type(page_type)


@pytest.mark.parametrize("page_type", ["concepts", "entities", "sources", "synthesis", "a-b_c"])
def test_safe_type_accepts_real_types(memex_server_module, page_type):
    assert memex_server_module._safe_type(page_type) == page_type


@pytest.mark.asyncio
async def test_write_rejects_traversing_type_end_to_end(memex_server_module, tmp_path):
    """The handler must refuse, not raise — an MCP client gets an error string."""
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    server = memex_server_module.MemexServer(wiki_path=str(wiki))
    result = await server._write(page_type="../escaped", slug="pwn", title="pwn", content="x")
    assert result.startswith("Error:")
    assert not (tmp_path / "escaped").exists()


@pytest.mark.asyncio
async def test_read_rejects_traversal_end_to_end(memex_server_module, tmp_path):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    secret = tmp_path / "secret.md"
    secret.write_text("PRIVATE", encoding="utf-8")
    server = memex_server_module.MemexServer(wiki_path=str(wiki))
    result = await server._read("../secret")
    assert "PRIVATE" not in result
    assert result.startswith("Error:")

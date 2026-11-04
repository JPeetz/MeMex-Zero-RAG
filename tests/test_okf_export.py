"""Tests for the OKF exporter — verifies OKF v0.2 conformance AND the
independence/exclusion rule (private trees never leak into the bundle)."""
from __future__ import annotations

from pathlib import Path
import yaml

from memex_mcp import okf_export as E


SAMPLE_WIKI = Path(__file__).parent / "_okf_fixture"


def _make_fixture():
    """Tiny MeMex-shaped wiki with one public concept + one private page."""
    if SAMPLE_WIKI.exists():
        import shutil
        shutil.rmtree(SAMPLE_WIKI)
    (SAMPLE_WIKI / "concepts").mkdir(parents=True)
    (SAMPLE_WIKI / "agentforge" / "polymarket").mkdir(parents=True)
    (SAMPLE_WIKI / "concepts" / "zero-rag.md").write_text(
        "---\ntitle: Zero-RAG\ntype: concept\nstatus: active\ntags: [knowledge, rag]\n---\n"
        "Zero-RAG compiles knowledge once. [Source: wiki/sources/karpathy-gist.md]\n",
        encoding="utf-8")
    (SAMPLE_WIKI / "agentforge" / "polymarket" / "secret.md").write_text(
        "---\ntitle: private\ntype: entity\n---\nprivate operational content\n",
        encoding="utf-8")


def test_conformance_basics():
    _make_fixture()
    out = SAMPLE_WIKI.parent / "_okf_bundle"
    import datetime
    now = datetime.datetime(2026, 6, 30, tzinfo=datetime.timezone.utc)
    stats = E.export(SAMPLE_WIKI, out, now=now)

    # independence: private tree excluded
    assert not list(out.rglob("agentforge/**/*.md"))
    # every concept has frontmatter + non-empty type
    for md in out.rglob("*.md"):
        if md.name in ("index.md", "log.md"):
            continue
        fm, _ = E._parse_frontmatter(md.read_text(encoding="utf-8"))
        assert fm and str(fm.get("type", "")).strip(), f"no type in {md.name}"
    # source citation mapped to OKF sources
    concept = (out / "concepts" / "zero-rag.md").read_text(encoding="utf-8")
    fm_dict, _ = E._parse_frontmatter(concept)
    assert fm_dict is not None
    assert fm_dict["sources"][0]["resource"].endswith("karpathy-gist.md")
    # root index declares version
    assert "okf_version" in (out / "index.md").read_text(encoding="utf-8")


def test_no_parse_crash_on_invalid_frontmatter():
    md = SAMPLE_WIKI / "concepts" / "bad.md"
    md.write_text("no frontmatter here\nplain body\n", encoding="utf-8")
    out = SAMPLE_WIKI.parent / "_okf_bundle2"
    import datetime
    stats = E.export(SAMPLE_WIKI, out, now=datetime.datetime(2026, 6, 30, tzinfo=datetime.timezone.utc))
    # gracefully defaults type to Reference rather than crashing
    bad_out = out / "concepts" / "bad.md"
    assert bad_out.exists()
    fm, _ = E._parse_frontmatter(bad_out.read_text(encoding="utf-8"))
    assert fm is not None and str(fm.get("type", "")).strip() == "Reference"
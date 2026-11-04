#!/usr/bin/env python3
"""
OKF exporter — emit an Open Knowledge Format v0.2 conformant bundle from a MeMex wiki.

Why not migrate? MeMex's canonical store stays markdown+git (its independence +
your zero-draft-coupling principle). This tool produces an OKF bundle ON DEMAND,
so any OKF-aware agent/tool can read your knowledge — interoperability without
core churn. It is a one-way export: OKF bundle -> discarded/regenerated anytime.

Mapping (MeMex frontmatter/body -> OKF frontmatter, per OKF v0.2 SPEC §4-§5,§8-§9):
  type                    -> type                                   (OKF REQUIRED)
  title                   -> title
  tags                    -> tags
  status: active          -> verified: { by: process:memex-export, at: <now> }  (§5.2)
  source_count / updated  -> (soft provenance signal)
  body [Source: X]        -> sources: [{ resource: X, title: X }]                (§5.1)
  index.md                -> §8 progressive-disclosure index (grouped by dir)
  log.md                  -> §9 date-grouped log

Conformance (§11): every .md carries YAML frontmatter + non-empty type; index/log
follow §8/§9. Bundle root index.md may declare okf_version: "0.2".

Private content (L1/, wiki/agentforge/, etc.) is EXCLUDED by default — the
exported bundle is clean + shareable. Override with --include-private.

Run:
    python memex_mcp/okf_export.py --wiki wiki --out /tmp/okf-bundle
"""
from __future__ import annotations

import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path
from typing import Optional

import yaml

OKF_VERSION = "0.2"

# MeMex private/operational trees never exported by default (independence rule).
# Matched against BOTH the repo-root-relative path (wiki/agentforge/...) and the
# wiki-relative path (agentforge/...), so it works regardless of how --wiki is rooted.
DEFAULT_EXCLUDES = [
    "L1/",                    # identity/credentials/private context
    "agentforge/",            # live operational knowledge (BetterLife, polymarket, etc.)
    "x-growth-monitor-accounts.md",
    "raw/",                   # raw sources (OKF bundle carries concepts, not raw)
    "outputs/",
    "graph/",
]

SRC_RE = re.compile(r"\[Source:\s*([^\]]+)\]")


def _is_excluded(rel: str, rel_from_wiki: str, excludes: list[str]) -> bool:
    return any(rel == ex or rel.startswith(ex)
               or rel_from_wiki == ex.rstrip("/") or rel_from_wiki.startswith(ex)
               for ex in excludes)


def _parse_frontmatter(text: str) -> tuple[Optional[dict], str]:
    """Return (frontmatter_dict, body). Tolerant: no/invalid frontmatter -> {} + full text."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
        if not isinstance(fm, dict):
            fm = {}
    except yaml.YAMLError:
        fm = {}
    return fm, parts[2]


def _to_okf_fm(fm: Optional[dict], body: str, now: datetime.datetime) -> dict:
    """Transform MeMex frontmatter + body into OKF frontmatter."""
    fm = fm or {}
    okf: dict = {}
    # REQUIRED
    okf["type"] = str(fm.get("type") or "Reference").strip() or "Reference"
    # recommended
    if fm.get("title"):
        okf["title"] = fm["title"]
    if fm.get("tags"):
        okf["tags"] = [t.strip() for t in fm["tags"]] if isinstance(fm["tags"], list) else fm["tags"]
    if fm.get("description"):
        okf["description"] = fm["description"]
    # trust/lifecycle (§5): map MeMex status to OKF verified/status
    status = str(fm.get("status") or "").lower()
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    if status == "active":
        okf["status"] = "stable"
        okf["verified"] = {"by": "process:memex-export", "at": ts}
    else:
        okf["status"] = status  # quarantine/stale/draft passthrough
    # provenance (§5.1): body [Source: X] -> sources list
    srcs = []
    for m in SRC_RE.finditer(body):
        ref = m.group(1).strip()
        srcs.append({"resource": ref, "title": ref.rsplit("/", 1)[-1]})
    if srcs:
        okf["sources"] = srcs
    # keep useful MeMex metadata as extension keys (OKF tolerates unknown keys)
    for k in ("created", "updated", "source_count"):
        if k in fm:
            okf[f"memex_{k}"] = fm[k]
    return okf


def _okf_index(by_dir: dict) -> str:
    """§8 index.md: grouped by heading, entries as links + description."""
    lines = ["# Memex Wiki — OKF bundle", ""]
    for group in sorted(by_dir):
        lines.append(f"## {group.title() if group else 'Root'}")
        for path, meta in sorted(by_dir[group], key=lambda x: x[0].lower()):
            desc = meta.get("description") or ""
            lines.append(f"* [{meta.get('title', path)}]({path}) — {desc}".rstrip())
        lines.append("")
    return "\n".join(lines)


def _okf_log(entries: list[dict[str, str]]) -> str:
    """§9 log.md: date-grouped, newest first."""
    by_day: dict[str, list[str]] = {}
    for e in entries:
        day = e.get("date", "")[:10]
        by_day.setdefault(day, []).append(f"* **{e['op']}**: {e['what']}")
    out = ["# Directory Update Log"]
    for day in sorted(by_day, reverse=True):
        out.append(f"## {day}")
        out.extend(by_day[day])
        out.append("")
    return "\n".join(out) or "# Directory Update Log\n"


def export(wiki_dir: Path, out_dir: Path, excludes: Optional[list[str]] = None,
           now: Optional[datetime.datetime] = None) -> dict:
    """Convert a MeMex wiki into an OKF v0.2 bundle. Returns bundle stats."""
    excludes = [e.rstrip("/") + ("/" if not e.endswith(".md") else "")
                for e in (excludes or DEFAULT_EXCLUDES)]
    now = now or datetime.datetime.now(datetime.timezone.utc)
    stats = {"files": 0, "excluded": 0, "sources": 0}

    if out_dir.exists():
        shutil.rmtree(out_dir)
    bundles_by_dir: dict[str, list[tuple[str, dict]]] = {}

    for md in sorted(wiki_dir.rglob("*.md")):
        rel = str(md.relative_to(wiki_dir.parent))       # e.g. 'wiki/entities/x.md'
        rel_from_wiki = str(md.relative_to(wiki_dir))    # e.g. 'entities/x.md'
        if _is_excluded(rel, rel_from_wiki, excludes):
            stats["excluded"] += 1
            continue
        if md.name in ("index.md", "log.md"):
            continue  # regenerated below

        fm, body = _parse_frontmatter(md.read_text(encoding="utf-8"))
        okf_fm = _to_okf_fm(fm, body, now)
        stats["sources"] += len(okf_fm.get("sources", []))

        # output path mirrors repo path but under out_dir, strips wiki/
        rel_from_wiki = str(md.relative_to(wiki_dir))
        dest_rel = rel_from_wiki
        dest = out_dir / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        blob = "---\n" + yaml.safe_dump(okf_fm, sort_keys=False, allow_unicode=True) + "---\n" + body
        dest.write_text(blob, encoding="utf-8")
        stats["files"] += 1

        group = str(dest.parent.relative_to(out_dir)) if dest.parent != out_dir else ""
        bundles_by_dir.setdefault(group, []).append(
            (dest_rel, {"title": okf_fm.get("title", dest_rel),
                        "description": okf_fm.get("description", "")}))

    # §8 index (bundle root + per-group)
    idx = _okf_index(bundles_by_dir)
    (out_dir / "index.md").write_text(
        f"---\nokf_version: \"{OKF_VERSION}\"\n---\n{idx}", encoding="utf-8")
    # §9 log
    log_lines = [{"date": now.strftime("%Y-%m-%d"), "op": "Creation",
                  "what": f"Exported Memex wiki as OKF v{OKF_VERSION} bundle."}]
    (out_dir / "log.md").write_text(_okf_log(log_lines), encoding="utf-8")
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Export a MeMex wiki as an OKF v0.2 bundle")
    ap.add_argument("--wiki", type=str, default="wiki", help="Path to the wiki dir")
    ap.add_argument("--out", type=str, default="/tmp/okf-bundle", help="Output bundle dir")
    ap.add_argument("--exclude", action="append", default=[], help="Extra path prefix to exclude")
    args = ap.parse_args()

    wiki_dir = Path(args.wiki).resolve()
    if not wiki_dir.exists():
        print(f"❌ wiki dir not found: {wiki_dir}")
        return 1
    out_dir = Path(args.out).resolve()
    stats = export(wiki_dir, out_dir, excludes=(DEFAULT_EXCLUDES + args.exclude))
    print(f"✅ Exported OKF v{OKF_VERSION} bundle -> {out_dir}")
    print(f"   concepts: {stats['files']}  excluded: {stats['excluded']}  sources tagged: {stats['sources']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
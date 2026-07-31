#!/usr/bin/env python3
"""Knowledge graph builder for MeMex Zero RAG.

Scans wiki/*.md for [[wikilinks]] and builds graph/data.json
for visualization via graph/graph.html.

Usage:
    python3 mcp/graph_builder.py [--wiki WIKI_DIR] [--output OUTPUT_DIR]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)")  # Match [[page]] or [[page|alias]]


def build_graph(wiki_dir: str = "wiki", output_dir: str = "graph") -> Dict:
    """Build knowledge graph from wiki pages.

    Returns:
        Dict with 'nodes', 'edges', and stats.
    """
    wiki_path = Path(wiki_dir)
    output_path = Path(output_dir)

    if not wiki_path.is_dir():
        raise FileNotFoundError(f"Wiki directory not found: {wiki_dir}")

    nodes: List[Dict] = []
    edges: List[Dict] = []
    seen_nodes = set()
    seen_edges = set()

    for md_file in sorted(wiki_path.rglob("*.md")):
        if md_file.name.startswith("."):
            continue

        rel_path = md_file.relative_to(wiki_path)
        dir_name = str(rel_path.parent) if str(rel_path.parent) != "." else ""
        slug = md_file.stem

        if slug in seen_nodes:
            continue
        seen_nodes.add(slug)

        # Determine node type from directory
        if "synthesis" in dir_name:
            node_type = "synthesis"
        elif "concepts" in dir_name:
            node_type = "concept"
        elif "entities" in dir_name:
            node_type = "entity"
        elif "sources" in dir_name:
            node_type = "source"
        elif "departments" in dir_name:
            node_type = "department"
        elif "infrastructure" in dir_name:
            node_type = "infrastructure"
        elif "projects" in dir_name:
            node_type = "project"
        elif "conventions" in dir_name:
            node_type = "convention"
        else:
            node_type = "other"

        label = slug.replace("-", " ").replace("_", " ")

        nodes.append({
            "id": slug,
            "label": label,
            "type": node_type,
            "group": dir_name.replace("/", " ") if dir_name else "root"
        })

        # Extract wikilinks
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        for match in WIKILINK_PATTERN.finditer(content):
            target = match.group(1).strip()
            if not target or target.startswith("#"):
                continue
            edge_key = f"{slug}->{target}"
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append({"from": slug, "to": target})

    output_path.mkdir(parents=True, exist_ok=True)
    data = {
        "nodes": nodes,
        "edges": edges
    }

    with open(output_path / "data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "data_path": str(output_path / "data.json"),
        "graph_html": str(output_path / "graph.html")
    }


def main():
    parser = argparse.ArgumentParser(description="Build MeMex knowledge graph")
    parser.add_argument("--wiki", default="wiki", help="Wiki directory (default: wiki)")
    parser.add_argument("--output", default="graph", help="Output directory (default: graph)")
    args = parser.parse_args()

    try:
        stats = build_graph(wiki_dir=args.wiki, output_dir=args.output)
        print(f"✅ Knowledge graph built: {stats['nodes']} nodes, {stats['edges']} edges")
        print(f"   Data: {stats['data_path']}")
        print(f"   Open: {stats['graph_html']}")
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
